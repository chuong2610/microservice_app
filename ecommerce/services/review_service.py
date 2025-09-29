from repositories.review_repository import ReviewRepository
from typing import Optional, List, Dict


class ReviewService:
    def __init__(self, review_repository: ReviewRepository):
        self.review_repository = review_repository

    async def create_review(self, user_id: str, product_id: str, rating: int, comment: str, user_name: Optional[str] = None):
        """Create a new review"""
        # Check if user has already reviewed this product
        existing_review = await self.review_repository.check_user_review_exists(user_id, product_id)
        if existing_review:
            return {"error": "User has already reviewed this product", "existing_review": existing_review}

        review_data = {
            "user_id": user_id,
            "product_id": product_id,
            "rating": rating,
            "comment": comment.strip(),
            "user_name": user_name
        }

        return await self.review_repository.create_review(review_data)

    async def get_review_by_id(self, review_id: str):
        """Get review by ID"""
        return await self.review_repository.get_review_by_id(review_id)

    async def get_product_reviews(self, product_id: str, limit: int = 50, offset: int = 0):
        """Get all reviews for a product with pagination"""
        reviews = await self.review_repository.get_reviews_by_product(product_id, limit, offset)
        return reviews

    async def get_user_reviews(self, user_id: str, limit: int = 50, offset: int = 0):
        """Get all reviews by a user with pagination"""
        reviews = await self.review_repository.get_reviews_by_user(user_id, limit, offset)
        return reviews

    async def update_review(self, review_id: str, user_id: str, rating: Optional[int] = None, comment: Optional[str] = None):
        """Update an existing review (only by the review owner)"""
        # Check if review exists and belongs to user
        review = await self.review_repository.get_review_by_id(review_id)
        if not review:
            return {"error": "Review not found"}
        
        if review["user_id"] != user_id:
            return {"error": "Unauthorized: You can only update your own reviews"}

        update_data = {}
        if rating is not None:
            update_data["rating"] = rating
        if comment is not None:
            update_data["comment"] = comment.strip()

        if not update_data:
            return {"error": "No data to update"}

        return await self.review_repository.update_review(review_id, update_data)

    async def delete_review(self, review_id: str, user_id: str):
        """Delete a review (only by the review owner)"""
        # Check if review exists and belongs to user
        review = await self.review_repository.get_review_by_id(review_id)
        if not review:
            return {"error": "Review not found"}
        
        if review["user_id"] != user_id:
            return {"error": "Unauthorized: You can only delete your own reviews"}

        success = await self.review_repository.delete_review(review_id)
        return {"success": success}

    async def get_product_rating_summary(self, product_id: str):
        """Get rating statistics for a product"""
        stats = await self.review_repository.get_product_rating_stats(product_id)
        if not stats:
            return {
                "total_reviews": 0,
                "average_rating": 0.0,
                "rating_distribution": {
                    "5": 0, "4": 0, "3": 0, "2": 0, "1": 0
                }
            }

        return {
            "total_reviews": stats.get("total_reviews", 0),
            "average_rating": round(stats.get("average_rating", 0.0), 2),
            "rating_distribution": {
                "5": stats.get("five_stars", 0),
                "4": stats.get("four_stars", 0),
                "3": stats.get("three_stars", 0),
                "2": stats.get("two_stars", 0),
                "1": stats.get("one_star", 0)
            }
        }

    async def get_reviews_with_rating_summary(self, product_id: str, limit: int = 50, offset: int = 0):
        """Get product reviews along with rating summary"""
        reviews = await self.get_product_reviews(product_id, limit, offset)
        rating_summary = await self.get_product_rating_summary(product_id)
        
        return {
            "reviews": reviews,
            "rating_summary": rating_summary,
            "pagination": {
                "limit": limit,
                "offset": offset,
                "has_more": len(reviews) == limit
            }
        }

    def map_to_review_dto(self, review) -> dict:
        """Map review to DTO format"""
        if review:
            return {
                "id": review.get("id"),
                "product_id": review.get("product_id"),
                "user_id": review.get("user_id"),
                "user_name": review.get("user_name", "Anonymous"),
                "rating": review.get("rating"),
                "comment": review.get("comment"),
                "created_at": review.get("created_at"),
                "updated_at": review.get("updated_at")
            }
        return None