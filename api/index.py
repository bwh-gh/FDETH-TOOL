from fastapi import FastAPI, Request
from pydantic import BaseModel

app = FastAPI()

# Opal prefers a clean, flat parameter structure
class ProductRequest(BaseModel):
    product_id: str

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
async def get_product_data(req: ProductRequest):
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
    
    sku = req.product_id.upper()
    data = inventory.get(sku)
    
    if data:
        # Return a flat object—easier for AI to parse
        return {
            "name": data["name"],
            "price": data["price"],
            "stock_count": data["stock"],
            "mandatory_footer": data["message"],
            "can_sell_now": data["stock"] > 0
        }
    
    return {"error": "SKU not found in Truth Engine"}
