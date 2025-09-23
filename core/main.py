"""
FastAPI application exposing search endpoints for testing the backend search service.
"""

import os
from typing import Optional

from dotenv import load_dotenv
from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse

from core.search.clients import items_client, authors_client
from core.services.search_service import SearchService


load_dotenv()

app = FastAPI(title="Search Core API", version="0.1.0")


def _get_service() -> SearchService:
    items = items_client()
    authors = authors_client()
    return SearchService(items_sc=items, authors_sc=authors)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/search")
def search(
    q: str = Query(..., min_length=1, description="Search query"),
    k: int = Query(10, ge=1, le=100),
    page_index: Optional[int] = Query(None, ge=0),
    page_size: Optional[int] = Query(None, ge=1, le=100),
    app_id: Optional[str] = Query(None)
):
    try:
        svc = _get_service()
        result = svc.search(q, k=k, page_index=page_index, page_size=page_size, app_id=app_id)
        return JSONResponse(result)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.get("/search/items")
def search_items(
    q: str = Query(..., min_length=1),
    k: int = Query(10, ge=1, le=100),
    page_index: Optional[int] = Query(None, ge=0),
    page_size: Optional[int] = Query(None, ge=1, le=100),
    app_id: Optional[str] = Query(None)
):
    try:
        svc = _get_service()
        result = svc.search_items(q, k=k, page_index=page_index, page_size=page_size, app_id=app_id)
        return JSONResponse(result)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.get("/search/authors")
def search_authors(
    q: str = Query(..., min_length=1),
    k: int = Query(10, ge=1, le=100),
    page_index: Optional[int] = Query(None, ge=0),
    page_size: Optional[int] = Query(None, ge=1, le=100),
    app_id: Optional[str] = Query(None)
):
    try:
        svc = _get_service()
        result = svc.search_authors(q, k=k, page_index=page_index, page_size=page_size, app_id=app_id)
        return JSONResponse(result)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
