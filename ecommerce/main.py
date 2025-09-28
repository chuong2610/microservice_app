from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Create FastAPI app
app = FastAPI(
    title="E-commerce Service",
    description="A microservice for managing e-commerce operations (cart, orders, reviews)",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# TODO: Add routes when implemented
# app.include_router(cart_router, prefix="/api/v1", tags=["cart"])
# app.include_router(order_router, prefix="/api/v1", tags=["orders"]) 
# app.include_router(review_router, prefix="/api/v1", tags=["reviews"])

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "ecommerce-service"}

# Placeholder endpoints for testing
@app.get("/api/v1/cart")
async def get_cart():
    return {"message": "Cart service - Not implemented yet"}

@app.get("/api/v1/orders")
async def get_orders():
    return {"message": "Order service - Not implemented yet"}

@app.get("/api/v1/reviews")
async def get_reviews():
    return {"message": "Review service - Not implemented yet"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8004)
