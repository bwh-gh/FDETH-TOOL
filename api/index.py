from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import Optional

app = FastAPI(redirect_slashes=False)

# Pydantic model - we keep product_id optional to handle custom unwrapping
class ProductRequest(BaseModel):
    product_id: Optional[str] = None

@app.get("/")
async def root():
    return {"status": "Elysian Truth Engine Online", "version": "2.0.0"}

# 1. DISCOVERY ENDPOINT (Opal's Map)
@app.get("/discovery")
async def discovery():
    return {
        "functions": [
            {
                "name": "get_product_data",
                "description": "Fetch authoritative stock, price, and style context for Elysian watches.",
                "parameters": [
                    {
                        "name": "product_id",
                        "type": "string",
                        "description": "The SKU (e.g., SILVER-LEATHER-02 or GOLD-WATCH-01)",
                        "required": True
                    }
                ],
                "endpoint": "/tools/get-product-data",
                "http_method": "POST"
            }
        ]
    }

# 2. EXECUTION ENDPOINT (The Source of Truth)
@app.post("/tools/get-product-data")
async def get_product_data(request: Request):
    # Handle Opal's nested 'parameters' wrapper or flat JSON
    body = await request.json()
    target_id = body.get("parameters", {}).get("product_id") or body.get("product_id")

    if not target_id:
        return {"success": False, "error": "No product_id provided."}

    # Our "Single Source of Truth" Database
    inventory = {
        "SILVER-LEATHER-02": {
            "name": "Argento Slimline",
            "price": "£450",
            "stock": 0,
            "style_notes": "Minimalist Italian leather, sunburst silver dial, ultra-thin 7mm profile. Heritage-focused.",
            "message": "© Elysian Ltd. All items subject to waitlist. No immediate delivery promised."
        },
        "GOLD-WATCH-01": {
            "name": "Elysian Gold Chronograph",
            "price": "£1,250",
            "stock": 3,
            "style_notes": "18k gold plating, sapphire crystal, tachymeter bezel, automatic movement. Bold and presence-driven.",
            "message": "© Elysian Ltd. Luxury shipping included. Available immediately."
        }
    }
    
    # Normalize input to uppercase to match our keys
    data = inventory.get(target_id.upper())
    
    if data:
        return {
            "success": True,
            "product_name": data["name"],
            "price": data["price"],
            "stock_count": data["stock"],
            "style_context": data["style_notes"],
            "mandatory_footer": data["message"],
            "can_sell_now": data["stock"] > 0
        }
    
    return {"success": False, "error": f"SKU {target_id} not found."}
