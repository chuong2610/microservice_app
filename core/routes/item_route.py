from fastapi import APIRouter

from factories.item_factory import ItemServiceFactory
from schemas.base_response import BaseResponse



router = APIRouter()
item_service = ItemServiceFactory.create()

@router.get("/items/{item_id}")
def get_item_by_id(item_id: str):
    try:
        item = item_service.get_item_by_id(item_id)
        if item:
            return BaseResponse(status_code=200, message="Item retrieved successfully", data=item.model_dump(mode='json'))
        else:
            return BaseResponse(status_code=404, message="Item not found", data=None)
    except Exception as e:
        return BaseResponse(status_code=500, message=str(e), data=None)    

@router.get("/items")
def get_items(page_number: int = 1, page_size: int = 10):
    try:
        items = item_service.get_items(page_number, page_size)
        return BaseResponse(status_code=200, message="Items retrieved successfully", data=items)
    except Exception as e:
        return BaseResponse(status_code=500, message=str(e), data=None)

@router.get("/items/author/{author_id}")
def get_items_by_author(author_id: str, page_number: int = 1, page_size: int = 10):
    try:
        items = item_service.get_items_by_author(author_id, page_number, page_size)
        return BaseResponse(status_code=200, message="Items retrieved successfully", data=items)
    except Exception as e:
        return BaseResponse(status_code=500, message=str(e), data=None)
        
@router.get("/items/category/{category}")
def get_items_by_category(category: str, page_number: int = 1, page_size: int = 10):
    try:
        items = item_service.get_items_by_category(category, page_number, page_size)
        return BaseResponse(status_code=200, message="Items retrieved successfully", data=items)
    except Exception as e:
        return BaseResponse(status_code=500, message=str(e), data=None)        
    
@router.post("/items")
def create_item(item_data: dict):
    try:
        new_item = item_service.create_item(item_data)
        return BaseResponse(status_code=201, message="Item created successfully", data=new_item.model_dump(mode='json'))
    except Exception as e:
        return BaseResponse(status_code=500, message=str(e), data=None)    

@router.put("/items/{item_id}")
def update_item(item_id: str, update_data: dict):
    try:
        updated_item = item_service.update_item(item_id, update_data)
        if updated_item:
            return BaseResponse(status_code=200, message="Item updated successfully", data=updated_item.model_dump(mode='json'))
        else:
            return BaseResponse(status_code=404, message="Item not found", data=None)
    except Exception as e:
        return BaseResponse(status_code=500, message=str(e), data=None)
    
@router.delete("/items/{item_id}")
def delete_item(item_id: str):
    try:
        success = item_service.delete_item(item_id)
        if success:
            return BaseResponse(status_code=200, message="Item deleted successfully", data=None)
        else:
            return BaseResponse(status_code=404, message="Item not found", data=None)
    except Exception as e:
        return BaseResponse(status_code=500, message=str(e), data=None)

