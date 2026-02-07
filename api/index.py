from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# We make the field optional in the Pydantic model so it doesn't 
# crash before it reaches our custom logic
class ProductRequest(BaseModel):
    product_id: Optional[str] = None

@app.get("/discovery")
async def discovery():
    return {
        "functions": [
            {
                "name": "get_product_data",
                "description": "Returns authoritative price, stock, and legal footer for Elysian SKUs.",
                "parameters": [
                    {
                        "name": "product_id",
                        "type": "string",
                        "description": "The SKU (e.g., SILVER-LEATHER-02)",
                        "required": True
                    }
                ],
                "endpoint": "/tools/get-product-data",
                "http_method": "POST"
            }
        ]
    }

@app.post("/tools/get-product-data")
async def get_product_data(request: Request):
    # Manually parse the JSON to handle Opal's nesting
    body = await request.json()
    
    # Try to find product_id in the 'parameters' nest first (Opal style), 
    # then fall back to the top level (standard style)
    target_id = body.get("parameters", {}).get("product_id") or body.get("product_id")

    if not target_id:
        return {"error": "Missing product_id in request body"}

    inventory = {
        "SILVER-LEATHER-02": {
            "name": "Argento Slimline",
            "price": "£450",
            "stock": 0,
            "message": "© Elysian Ltd. All items subject to waitlist. No immediate delivery promised."
        },
        "GOLD-WATCH-01": {
            "name": "Elysian Gold Chronograph",
            "price": "£1,250",
            "stock": 3,
            "message": "© Elysian Ltd. Luxury shipping included. Available immediately."
        }
    }
    
    data = inventory.get(target_id.upper())
    
    if data:
        return {
            "name": data["name"],
            "price": data["price"],
            "stock_count": data["stock"],
            "mandatory_footer": data["message"],
            "can_sell_now": data["stock"] > 0
        }
    
    return {"error": f"SKU {target_id} not found in Truth Engine"}
