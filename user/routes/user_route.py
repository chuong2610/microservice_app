from fastapi import APIRouter, HTTPException, Query, Depends, Header
from typing import Optional

from factories.user_factory import UserServiceFactory
from schemas.base_response import BaseResponse
from schemas.user_schema import (
    UserCreateRequest, 
    UserUpdateRequest
)
from utils import get_current_user


router = APIRouter()
user_service = UserServiceFactory.create()


@router.get("/{user_id}")
def get_user_by_id(user_id: str, app_id: str = Header(None, convert_underscores=False)):
    """Get a user by ID"""
    try:
        print(f"[DEBUG] get_user_by_id called with user_id: {user_id}, app_id: {app_id}")
        user = user_service.get_user_by_id(user_id, app_id=app_id)
        if user:
            print(f"[DEBUG] User found: {user.full_name if hasattr(user, 'full_name') else 'Unknown'}")
            return BaseResponse(
                status_code=200, 
                message="User retrieved successfully", 
                data=user.model_dump()
            )
        else:
            print(f"[DEBUG] User not found for user_id: {user_id}, app_id: {app_id}")
            return BaseResponse(
                status_code=404, 
                message="User not found", 
                data=None
            )
    except Exception as e:
        return BaseResponse(
            status_code=500, 
            message=str(e), 
            data=None
        )


@router.get("")
def get_users(
    page_number: int = Query(1, ge=1, description="Page number"), 
    page_size: int = Query(10, ge=1, le=100, description="Page size"),
    app_id: str = Header(None, convert_underscores=False)
):
    """Get paginated list of users"""
    try:
        users = user_service.get_users(page_number, page_size, app_id=app_id)
        return BaseResponse(
            status_code=200, 
            message="Users retrieved successfully", 
            data=users
        )
    except Exception as e:
        return BaseResponse(
            status_code=500, 
            message=str(e), 
            data=None
        )


@router.post("")
def create_user(user_request: UserCreateRequest):
    """Create a new user"""
    try:
        new_user = user_service.create_user(user_request)
        return BaseResponse(
            status_code=201, 
            message="User created successfully", 
            data=new_user.model_dump()
        )
    except ValueError as e:
        return BaseResponse(
            status_code=400, 
            message=str(e), 
            data=None
        )
    except Exception as e:
        return BaseResponse(
            status_code=500, 
            message=str(e), 
            data=None
        )


@router.put("/{user_id}")
def update_user(user_id: str, update_request: UserUpdateRequest):
    """Update user information"""
    try:
        # Convert to dict and remove None values
        update_data = {k: v for k, v in update_request.model_dump().items() if v is not None}
        
        if not update_data:
            return BaseResponse(
                status_code=400, 
                message="No valid update data provided", 
                data=None
            )
        
        updated_user = user_service.update_user(user_id, update_data)
        if updated_user:
            return BaseResponse(
                status_code=200, 
                message="User updated successfully", 
                data=updated_user.model_dump()
            )
        else:
            return BaseResponse(
                status_code=404, 
                message="User not found", 
                data=None
            )
    except Exception as e:
        return BaseResponse(
            status_code=500, 
            message=str(e), 
            data=None
        )


@router.put("/{user_id}/deactivate")
def deactivate_user(user_id: str):
    """Deactivate a user (soft delete)"""
    try:
        success = user_service.deactivate_user(user_id)
        if success:
            return BaseResponse(
                status_code=200, 
                message="User deactivated successfully", 
                data=None
            )
        else:
            return BaseResponse(
                status_code=404, 
                message="User not found", 
                data=None
            )
    except Exception as e:
        return BaseResponse(
            status_code=500, 
            message=str(e), 
            data=None
        )


@router.put("/{user_id}/activate")
def activate_user(user_id: str):
    """Activate a user"""
    try:
        success = user_service.activate_user(user_id)
        if success:
            return BaseResponse(
                status_code=200, 
                message="User activated successfully", 
                data=None
            )
        else:
            return BaseResponse(
                status_code=404, 
                message="User not found", 
                data=None
            )
    except Exception as e:
        return BaseResponse(
            status_code=500, 
            message=str(e), 
            data=None
        )


@router.delete("/{user_id}")
def delete_user(user_id: str):
    """Hard delete a user"""
    try:
        success = user_service.delete_user(user_id)
        if success:
            return BaseResponse(
                status_code=200, 
                message="User deleted successfully", 
                data=None
            )
        else:
            return BaseResponse(
                status_code=404, 
                message="User not found", 
                data=None
            )
    except Exception as e:
        return BaseResponse(
            status_code=500, 
            message=str(e), 
            data=None
        )

