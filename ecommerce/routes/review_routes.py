from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi.responses import JSONResponse
from schemas.review_schema import (
    CreateReviewRequest,
    UpdateReviewRequest,
    ReviewResponse,
    ReviewsWithSummaryResponse,
    RatingSummary
) 

from services.review_service import ReviewService
from repositories.review_repository import ReviewRepository
from typing import List

router = APIRouter(prefix="/reviews", tags=["Reviews"])

# Dependency injection
def get_review_service():
    review_repository = ReviewRepository()
    return ReviewService(review_repository)


@router.post("/", response_model=ReviewResponse)
async def create_review(
    user_id: str,
    request: CreateReviewRequest,
    review_service: ReviewService = Depends(get_review_service)
):
    """Create a new review for a product"""
    try:
        result = await review_service.create_review(
            user_id=user_id,
            product_id=request.product_id,
            rating=request.rating,
            comment=request.comment,
            user_name=request.user_name
        )
        
        if isinstance(result, dict) and "error" in result:
            if "already reviewed" in result["error"]:
                raise HTTPException(status_code=409, detail=result["error"])
            raise HTTPException(status_code=400, detail=result["error"])
        
        return ReviewResponse(**result)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/{review_id}", response_model=ReviewResponse)
async def get_review(
    review_id: str,
    review_service: ReviewService = Depends(get_review_service)
):
    """Get a specific review by ID"""
    try:
        review = await review_service.get_review_by_id(review_id)
        if not review:
            raise HTTPException(status_code=404, detail="Review not found")
        
        return ReviewResponse(**review)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/product/{product_id}", response_model=ReviewsWithSummaryResponse)
async def get_product_reviews(
    product_id: str,
    limit: int = Query(default=50, ge=1, le=100, description="Number of reviews per page"),
    offset: int = Query(default=0, ge=0, description="Number of reviews to skip"),
    review_service: ReviewService = Depends(get_review_service)
):
    """Get all reviews for a specific product with rating summary and pagination"""
    try:
        result = await review_service.get_reviews_with_rating_summary(
            product_id=product_id,
            limit=limit,
            offset=offset
        )
        
        reviews = [ReviewResponse(**review) for review in result["reviews"]]
        
        return ReviewsWithSummaryResponse(
            reviews=reviews,
            rating_summary=result["rating_summary"],
            pagination=result["pagination"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/user/{user_id}", response_model=List[ReviewResponse])
async def get_user_reviews(
    user_id: str,
    limit: int = Query(default=50, ge=1, le=100, description="Number of reviews per page"),
    offset: int = Query(default=0, ge=0, description="Number of reviews to skip"),
    review_service: ReviewService = Depends(get_review_service)
):
    """Get all reviews by a specific user with pagination"""
    try:
        reviews = await review_service.get_user_reviews(user_id, limit, offset)
        return [ReviewResponse(**review) for review in reviews]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/product/{product_id}/summary", response_model=RatingSummary)
async def get_product_rating_summary(
    product_id: str,
    review_service: ReviewService = Depends(get_review_service)
):
    """Get rating summary for a product"""
    try:
        summary = await review_service.get_product_rating_summary(product_id)
        return RatingSummary(**summary)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.put("/{review_id}", response_model=ReviewResponse)
async def update_review(
    review_id: str,
    user_id: str,
    request: UpdateReviewRequest,
    review_service: ReviewService = Depends(get_review_service)
):
    """Update an existing review (only by the review owner)"""
    try:
        result = await review_service.update_review(
            review_id=review_id,
            user_id=user_id,
            rating=request.rating,
            comment=request.comment
        )
        
        if isinstance(result, dict) and "error" in result:
            if "not found" in result["error"]:
                raise HTTPException(status_code=404, detail=result["error"])
            elif "Unauthorized" in result["error"]:
                raise HTTPException(status_code=403, detail=result["error"])
            raise HTTPException(status_code=400, detail=result["error"])
        
        return ReviewResponse(**result)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.delete("/{review_id}")
async def delete_review(
    review_id: str,
    user_id: str,
    review_service: ReviewService = Depends(get_review_service)
):
    """Delete a review (only by the review owner)"""
    try:
        result = await review_service.delete_review(review_id, user_id)
        
        if isinstance(result, dict) and "error" in result:
            if "not found" in result["error"]:
                raise HTTPException(status_code=404, detail=result["error"])
            elif "Unauthorized" in result["error"]:
                raise HTTPException(status_code=403, detail=result["error"])
            raise HTTPException(status_code=400, detail=result["error"])
        
        if result["success"]:
            return JSONResponse(
                status_code=200,
                content={"message": "Review deleted successfully"}
            )
        else:
            raise HTTPException(status_code=500, detail="Failed to delete review")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/product/{product_id}/stats")
async def get_product_review_stats(
    product_id: str,
    review_service: ReviewService = Depends(get_review_service)
):
    """Get detailed review statistics for a product"""
    try:
        summary = await review_service.get_product_rating_summary(product_id)
        recent_reviews = await review_service.get_product_reviews(product_id, limit=5, offset=0)
        
        return JSONResponse(
            status_code=200,
            content={
                "product_id": product_id,
                "rating_summary": summary,
                "recent_reviews": [
                    review_service.map_to_review_dto(review) 
                    for review in recent_reviews
                ]
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")