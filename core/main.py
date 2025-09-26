"""
FastAPI application exposing search endpoints for testing the backend search service.
"""


from fastapi import FastAPI
from fastapi.responses import JSONResponse

from routes.search_route import search
from routes.item_route import router



app = FastAPI()
app.include_router(search,prefix="/search",tags=["search"])
app.include_router(router,prefix="/items",tags=["items"])



@app.get("/health")
def health() -> dict:
    return {"status": "ok"}



