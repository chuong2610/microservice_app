from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.user_route import router as user_router

# Create FastAPI app
app = FastAPI(
    title="User Service",
    description="A microservice for user management (CRUD operations only)",
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

# Include routes
app.include_router(user_router, prefix="/api/v1", tags=["users"])

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "user-service"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

