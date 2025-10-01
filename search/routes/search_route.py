
from typing import Optional
from fastapi import APIRouter, Query, Header
from fastapi.responses import JSONResponse

from search.clients import items_client, authors_client
from services.search_service import SearchService


search = APIRouter()

def _get_service() -> SearchService:
    items = items_client()
    authors = authors_client()
    return SearchService(items_sc=items, authors_sc=authors)

@search.get("/search")
def search_all(
    q: str = Query(..., min_length=1, description="Search query"),
    k: int = Query(10, ge=1, le=100),
    page_index: Optional[int] = Query(None, ge=0),
    page_size: Optional[int] = Query(None, ge=1, le=100),
    app_id: Optional[str] = Header(None, convert_underscores=False)
):
    try:
        svc = _get_service()
        result = svc.search(q, k=k, page_index=page_index, page_size=page_size, app_id=app_id)
        return JSONResponse(result)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@search.get("/search/items")
def search_items(
    q: str = Query(..., min_length=1),
    k: int = Query(10, ge=1, le=100),
    page_index: Optional[int] = Query(None, ge=0),
    page_size: Optional[int] = Query(None, ge=1, le=100),
    app_id: Optional[str] = Header(None, convert_underscores=False)
):
    try:
        print(f"[DEBUG] search_items called with q='{q}', k={k}, page_index={page_index}, page_size={page_size}, app_id={app_id}")
        svc = _get_service()
        print(f"[DEBUG] SearchService created successfully")
        result = svc.search_items(q, k=k, page_index=page_index, page_size=page_size, app_id=app_id)
        print(f"[DEBUG] search_items completed successfully, result type: {type(result)}")
        return JSONResponse(result)
    except Exception as e:
        print(f"[ERROR] search_items failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"error": str(e)})


@search.get("/search/authors")
def search_authors(
    q: str = Query(..., min_length=1),
    k: int = Query(10, ge=1, le=100),
    page_index: Optional[int] = Query(None, ge=0),
    page_size: Optional[int] = Query(None, ge=1, le=100),
    app_id: Optional[str] = Header(None, convert_underscores=False)
):
    try:
        svc = _get_service()
        result = svc.search_authors(q, k=k, page_index=page_index, page_size=page_size, app_id=app_id)
        return JSONResponse(result)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

        