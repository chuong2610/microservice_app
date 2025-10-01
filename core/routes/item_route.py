from typing import Optional
from fastapi import APIRouter, Depends, Header, UploadFile
from enums.role_enum import RoleEnum
from factories.item_factory import ItemServiceFactory
from schemas.base_response import BaseResponse
from services.file_service import upload_image
from utils import verify_token



router = APIRouter()
item_service = ItemServiceFactory.create()

@router.get("")
def get_items(page_number: int = 1, page_size: int = 10, app_id: str = Header(None, convert_underscores=False)):
    try:
        print(f"[DEBUG] get_items called with app_id: {app_id}, page: {page_number}, size: {page_size}")
        items = item_service.get_items(page_number, page_size, app_id=app_id)
        print(f"[DEBUG] app_id: {app_id} returned {len(items.get('items', []))} items, total: {items.get('total_items', 0)}")
        return BaseResponse(status_code=200, message="Items retrieved successfully", data=items)
    except Exception as e:
        return BaseResponse(status_code=500, message=str(e), data=None)

@router.get("/health")
def health_check():
    return BaseResponse(status_code=200, data={"status": "healthy"}, message="Service is healthy")

@router.get("/{item_id}")
def get_item_by_id(item_id: str):
    try:
        item = item_service.get_item_by_id(item_id)
        if item:
            return BaseResponse(status_code=200, message="Item retrieved successfully", data=item.model_dump(mode='json'))
        else:
            return BaseResponse(status_code=404, message="Item not found", data=None)
    except Exception as e:
        return BaseResponse(status_code=500, message=str(e), data=None)    


@router.get("/author/{author_id}")
def get_items_by_author(author_id: str, page_number: int = 1, page_size: int = 10, app_id: str = Header(None, convert_underscores=False)):
    try:
        print(f"[DEBUG] get_items_by_author called with author_id: {author_id}, app_id: {app_id}, page: {page_number}")
        items = item_service.get_items_by_author(author_id, page_number, page_size, app_id=app_id)
        print(f"[DEBUG] Found {len(items.get('items', []))} items for author {author_id}")
        return BaseResponse(status_code=200, message="Items retrieved successfully", data=items)
    except Exception as e:
        print(f"[DEBUG] Error in get_items_by_author: {str(e)}")
        return BaseResponse(status_code=500, message=str(e), data=None)
        
@router.get("/category/{category}")
def get_items_by_category(category: str, page_number: int = 1, page_size: int = 10, app_id: str = Header(None, convert_underscores=False)):
    try:
        items = item_service.get_items_by_category(category, page_number, page_size, app_id=app_id)
        return BaseResponse(status_code=200, message="Items retrieved successfully", data=items)
    except Exception as e:
        return BaseResponse(status_code=500, message=str(e), data=None)        
    
@router.post("")
def create_item(title: str,
        abstract: str,
        content: str,
        author_id: str,
        images: list[UploadFile] = [],
        tags: list[str] = [],
        category: list[str] = [],
        meta_field: Optional[dict] = None,
        user = Depends(verify_token)):
    try:
        if(user.get("role") not in [RoleEnum.ADMIN, RoleEnum.WRITER]):
            return BaseResponse(status_code=403, message="Forbidden: You don't have permission to create items", data=None)
        if images:
            image_urls = []
            for image in images:
                image_url = upload_image(image)
                image_urls.append(image_url)
            images = image_urls
        item_data = {
            "title": title,
            "abstract": abstract,
            "content": content,
            "images": images,
            "tags": tags,
            "category": category,
            "meta_field": meta_field,
            "author_id": author_id
        }
        new_item = item_service.create_item(item_data)
        return BaseResponse(status_code=201, message="Item created successfully", data=new_item.model_dump(mode='json'))
    except Exception as e:
        return BaseResponse(status_code=500, message=str(e), data=None)    

@router.put("/{item_id}")
def update_item(item_id: str, 
                title: str ,
                abstract: str,
                content: str,
                author_id: str,
                images: list[UploadFile] = [],
                tags: list[str] = [],
                category: list[str] = [],
                meta_field: Optional[dict] = None,
                user = Depends(verify_token)):
    try:
        if(user.get("role") not in [RoleEnum.ADMIN, RoleEnum.WRITER]):
            return BaseResponse(status_code=403, message="Forbidden: You don't have permission to update items", data=None)
        if images:
            image_urls = []
            for image in images:
                image_url = upload_image(image)
                image_urls.append(image_url)
            images = image_urls
        update_data = {
            "title": title,
            "abstract": abstract,
            "content": content,
            "images": images,
            "tags": tags,
            "category": category,
            "meta_field": meta_field,
            "author_id": author_id
        }
        updated_item = item_service.update_item(item_id, update_data)
        if updated_item:
            return BaseResponse(status_code=200, message="Item updated successfully", data=updated_item.model_dump(mode='json'))
        else:
            return BaseResponse(status_code=404, message="Item not found", data=None)
    except Exception as e:
        return BaseResponse(status_code=500, message=str(e), data=None)
    
@router.delete("/{item_id}")
def delete_item(item_id: str, user = Depends(verify_token)):
    try:
        if(user.get("role") not in [RoleEnum.ADMIN, RoleEnum.WRITER]):
            return BaseResponse(status_code=403, message="Forbidden: You don't have permission to delete items", data=None)
        success = item_service.delete_item(item_id)
        if success:
            return BaseResponse(status_code=200, message="Item deleted successfully", data=None)
        else:
            return BaseResponse(status_code=404, message="Item not found", data=None)
    except Exception as e:
        return BaseResponse(status_code=500, message=str(e), data=None)
    
@router.put("/files")
def upload_file(file: UploadFile, user = Depends(verify_token)):
    try:
        if(user.get("role") not in [RoleEnum.ADMIN, RoleEnum.WRITER]):
            return BaseResponse(status_code=403, message="Forbidden: You don't have permission to upload files", data=None)
        file_url = upload_image(file)
        return BaseResponse(status_code=200, message="File uploaded successfully", data={"file_url": file_url})
    except Exception as e:    
        return BaseResponse(status_code=500, message=str(e), data=None)

@router.post("/{item_id}/view")
def increment_item_views(item_id: str):
    """Increment item view count"""
    try:
        success = item_service.increment_views(item_id)
        if success:
            return BaseResponse(status_code=200, message="View count incremented", data=None)
        else:
            return BaseResponse(status_code=404, message="Item not found", data=None)
    except Exception as e:
        return BaseResponse(status_code=500, message=str(e), data=None)