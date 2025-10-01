from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.cart_routes import router as cart_router
from routes.review_routes import router as review_router

app = FastAPI(
    title="E-commerce API",
    description="A simple e-commerce API with cart and review functionality",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(cart_router)
app.include_router(review_router)

@app.get("/")
async def root():
    return {"message": "Welcome to E-commerce API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)