from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(redirect_slashes=False)

# Enable CORS so Opal can talk to your API from their domain
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root path to prevent 404s on the base URL
@app.get("/")
async def root():
    return {"status": "Elysian Truth Engine Online", "version": "1.0.1"}

# THE DISCOVERY ENDPOINT (What Opal reads first)
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
                "http_method": "GET"
            }
        ]
    }

# THE EXECUTION ENDPOINT (Where the logic happens)
@app.get("/tools/get-product-data")
async def get_product_data(product_id: str = Query(..., description="The SKU of the product")):
    # Mock Database - This is your 'Source of Truth'
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
    
    # Return the specific SKU data or an error if not found
    product = inventory.get(product_id.upper())
    
    if product:
        return {"success": True, "product": product}
    else:
        return {"success": False, "error": f"SKU {product_id} not found in Elysian inventory."}

# Required for some local testing environments, Vercel ignores this part
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
