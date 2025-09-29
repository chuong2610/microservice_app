from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.item_route import router

# Create FastAPI app
app = FastAPI(
    title="Core Service",
    description="A microservice for managing core items/content",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(router, prefix="/items" , tags=["items"])


# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "core-service"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
