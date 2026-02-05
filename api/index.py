from fastapi import FastAPI, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

app = FastAPI(redirect_slashes=False)

# Enable CORS for Opal's cloud infrastructure
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic model for POST requests
class ProductQuery(BaseModel):
    product_id: str

@app.get("/")
async def root():
    return {"status": "Elysian Truth Engine Online", "version": "1.0.2"}

# 1. DISCOVERY ENDPOINT
@app.get("/discovery")
async def discovery():
    return {
        "functions": [
            {
                "name": "get_product_data",
                "description": "Fetch real-time stock and pricing for Elysian watches by SKU.",
                "parameters": [
                    {
                        "name": "product_id",
                        "type": "string",
                        "description": "The watch SKU (e.g., SILVER-LEATHER-02)",
                        "required": True
                    }
                ],
                "endpoint": "/tools/get-product-data",
                "http_method": "POST"  # Changed to POST as it's more standard for Opal tools
            }
        ]
    }

# 2. EXECUTION ENDPOINT (Handles both GET and POST)
@app.api_route("/tools/get-product-data", methods=["GET", "POST"])
async def get_product_data(request: Request, product_id: Optional[str] = None):
    # Determine the product_id from either Query Params (GET) or JSON Body (POST)
    target_id = product_id
    
    if request.method == "POST":
        try:
            body = await request.json()
            # Opal often sends parameters inside a 'parameters' key
            target_id = body.get("product_id") or body.get("parameters", {}).get("product_id")
        except:
            pass

    if not target_id:
        return {"success": False, "error": "No product_id provided."}

    # Inventory 'Source of Truth'
    inventory = {
        "SILVER-LEATHER-02": {
            "name": "Argento Slimline",
            "price": "£450",
            "stock": 0,
            "status": "Out of Stock",
            "message": "Waitlist Only. Do not promise immediate delivery."
        },
        "GOLD-WATCH-01": {
            "name": "Elysian Gold Chronograph",
            "price": "£1,250",
            "stock": 3,
            "status": "In Stock",
            "message": "Available for overnight shipping."
        }
    }
    
    product = inventory.get(target_id.upper())
    if product:
        return {"success": True, "product": product}
    
    return {"success": False, "error": f"SKU {target_id} not found."}
