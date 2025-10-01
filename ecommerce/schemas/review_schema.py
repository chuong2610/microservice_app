from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime


class CreateReviewRequest(BaseModel):
    product_id: str = Field(..., description="Product ID to review")
    rating: int = Field(..., ge=1, le=5, description="Rating from 1 to 5 stars")
    comment: str = Field(..., min_length=1, max_length=1000, description="Review comment")
    user_name: Optional[str] = Field(None, max_length=100, description="User display name")


class UpdateReviewRequest(BaseModel):
    rating: Optional[int] = Field(None, ge=1, le=5, description="Updated rating from 1 to 5 stars")
    comment: Optional[str] = Field(None, min_length=1, max_length=1000, description="Updated review comment")


class ReviewResponse(BaseModel):
    id: str
    product_id: str
    user_id: str
    user_name: Optional[str] = "Anonymous"
    rating: int
    comment: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class RatingDistribution(BaseModel):
    five_stars: int = Field(alias="5", default=0)
    four_stars: int = Field(alias="4", default=0)
    three_stars: int = Field(alias="3", default=0)
    two_stars: int = Field(alias="2", default=0)
    one_star: int = Field(alias="1", default=0)

    class Config:
        allow_population_by_field_name = True


class RatingSummary(BaseModel):
    total_reviews: int = 0
    average_rating: float = 0.0
    rating_distribution: Dict[str, int] = {
        "5": 0, "4": 0, "3": 0, "2": 0, "1": 0
    }


class ReviewsWithSummaryResponse(BaseModel):
    reviews: List[ReviewResponse]
    rating_summary: RatingSummary
    pagination: Dict[str, any]


class PaginationQuery(BaseModel):
    limit: int = Field(default=50, ge=1, le=100, description="Number of reviews per page")
    offset: int = Field(default=0, ge=0, description="Number of reviews to skip")


class DeleteReviewResponse(BaseModel):
    success: bool
    message: str