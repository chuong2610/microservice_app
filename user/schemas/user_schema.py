from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class UserDTO(BaseModel):
    """User Data Transfer Object - excludes sensitive information like password"""
    id: str
    full_name: str = Field(..., max_length=100)
    email: EmailStr
    avatar_url: Optional[str] = None
    role: Optional[str] = "user"
    is_active: Optional[bool] = True


class UserDetailDTO(UserDTO):
    """Detailed User DTO - same as UserDTO for now, but can be extended"""
    pass


class UserCreateRequest(BaseModel):
    """Request schema for creating a new user"""
    full_name: str = Field(..., max_length=100, min_length=1)
    email: EmailStr
    password: str = Field(..., min_length=8)
    avatar_url: Optional[str] = None
    role: Optional[str] = "user"
    is_active: Optional[bool] = True


class UserUpdateRequest(BaseModel):
    """Request schema for updating user information"""
    full_name: Optional[str] = Field(None, max_length=100, min_length=1)
    email: Optional[EmailStr] = None
    avatar_url: Optional[str] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None

