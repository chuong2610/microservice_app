from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.search_route import search

# Create FastAPI app
app = FastAPI(
    title="Search Service",
    description="A microservice for semantic search of items and authors",
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
app.include_router(search,  tags=["search"])

# Health check endpoint
@app.get("/search/health")
async def health_check():
    return {"status": "healthy", "service": "search-service"}

# Debug endpoint to check environment variables
@app.get("/debug/env")
async def debug_env():
    from settings import settings
    return {
        "azure_search_endpoint": settings.AZURE_SEARCH_ENDPOINT,
        "search_item_index": settings.SEARCH_ITEM_INDEX_NAME,
        "search_author_index": settings.SEARCH_AUTHOR_INDEX_NAME,
        "llm_provider": settings.LLM_PROVIDER,
        "azure_openai_endpoint": settings.AZURE_OPENAI_ENDPOINT,
        "embed_model_dimension": settings.EMBED_MODEL_DIMENSION,
        "weight_semantic": settings.WEIGHT_SEMANTIC,
        "weight_bm25": settings.WEIGHT_BM25,
        "weight_vector": settings.WEIGHT_VECTOR,
        "cosmos_endpoint": settings.COSMOS_ENDPOINT,
        "redis_host": settings.REDIS_HOST,
        "redis_port": settings.REDIS_PORT
    }

# Debug endpoint to test raw Azure Search without app_id filter
@app.get("/debug/raw-search")
async def debug_raw_search(q: str = "test", top: int = 5):
    from search.clients import items_client
    try:
        client = items_client()
        # Search without any filters
        results = client.search(search_text=q, top=top, select=["id", "title", "abstract"])
        items = [dict(item) for item in results]
        return {
            "query": q,
            "total_found": len(items),
            "items": items[:3]  # Show first 3 for debugging
        }
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)



