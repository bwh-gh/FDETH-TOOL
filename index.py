from fastapi import FastAPI, Request
from typing import Dict

app = FastAPI()

# --- MOCK ENTERPRISE DATA ---
PRODUCT_INVENTORY = {
    "GOLD-WATCH-01": {
        "name": "Elysian Gold Chronograph",
        "price": "£1,250",
        "stock": 3,
        "region_restriction": "None",
        "mandatory_footer": "Finance available at 0% APR. Terms apply."
    },
    "SILVER-LEATHER-02": {
        "name": "Argento Slimline",
        "price": "£450",
        "stock": 0,
        "region_restriction": "EU Only",
        "mandatory_footer": "Includes 2-year international warranty."
    }
}

# --- THE DISCOVERY ENDPOINT ---
@app.get("/discovery")
async def discovery():
    return {
        "success": True,
        "api_specification": {
            "name": "Inventory Truth Engine",
            "description": "Real-time product SKU lookups for pricing and stock.",
            "endpoints": [
                {
                    "path": "/tools/get-product-data",
                    "method": "GET", 
                    "description": "Fetch product details by SKU",
                    "parameters": [
                        {
                            "name": "product_id",
                            "in": "query",
                            "required": True,
                            "schema": {"type": "string"}
                        }
                    ]
                }
            ]
        }
    }

# --- THE UNIVERSAL TOOL ENDPOINT ---
@app.api_route("/tools/get-product-data", methods=["GET", "POST"])
async def get_product_data(request: Request):
    sku = None
    
    # 1. SPY LOG: See exactly what Opal is sending
    # Check query params first (for GET)
    sku = request.query_params.get("product_id") or request.query_params.get("sku")

   # 2. Check JSON body (for POST)
    if not sku:
        try:
            body = await request.json()
            print(f"DEBUG: Received Body: {body}")
            
            # THE FIX: Drill into the 'parameters' key that Opal is using
            if "parameters" in body:
                sku = body["parameters"].get("product_id")
            
            # Fallback for other formats just in case
            if not sku:
                sku = body.get("product_id") or body.get("sku")
        except:
            pass

    # --- FINAL DEBUG LOG ---
    print(f"DEBUG: Method: {request.method} | Resolved SKU: {sku}")

    if not sku:
        return {
            "error": "No product_id detected in request.",
            "debug_info": "Opal is hitting the endpoint but the field mapping is off."
        }
        
    sku_upper = sku.upper().strip()
    result = PRODUCT_INVENTORY.get(sku_upper)
    
    if not result:
        return {
            "error": f"SKU '{sku_upper}' not found.",
            "available": list(PRODUCT_INVENTORY.keys())
        }
    
    return result

# DELETED FOR VERCEL
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)