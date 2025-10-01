from db.database import review_container
from datetime import datetime
import uuid


class ReviewRepository:
    async def create_review(self, review_data: dict):
        """Create a new review"""
        try:
            review_id = str(uuid.uuid4())
            review_data.update({
                "id": review_id,
                "created_at": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat()
            })
            return review_container.create_item(body=review_data)
        except Exception as e:
            print(f"Error creating review: {e}")
            return None

    async def get_review_by_id(self, review_id: str):
        """Get review by ID"""
        try:
            review = review_container.read_item(item=review_id, partition_key=review_id)
            return review
        except Exception as e:
            print(f"Error retrieving review: {e}")
            return None

    async def get_reviews_by_product(self, product_id: str, limit: int = 50, offset: int = 0):
        """Get all reviews for a specific product with pagination"""
        try:
            query = f"SELECT * FROM r WHERE r.product_id = '{product_id}' ORDER BY r.created_at DESC OFFSET {offset} LIMIT {limit}"
            return list(review_container.query_items(query=query, enable_cross_partition_query=True))
        except Exception as e:
            print(f"Error retrieving reviews by product: {e}")
            return []

    async def get_reviews_by_user(self, user_id: str, limit: int = 50, offset: int = 0):
        """Get all reviews by a specific user with pagination"""
        try:
            query = f"SELECT * FROM r WHERE r.user_id = '{user_id}' ORDER BY r.created_at DESC OFFSET {offset} LIMIT {limit}"
            return list(review_container.query_items(query=query, enable_cross_partition_query=True))
        except Exception as e:
            print(f"Error retrieving reviews by user: {e}")
            return []

    async def update_review(self, review_id: str, updated_data: dict):
        """Update an existing review"""
        try:
            review = await self.get_review_by_id(review_id)
            if review:
                updated_data["updated_at"] = datetime.utcnow().isoformat()
                for key, value in updated_data.items():
                    review[key] = value
                review_container.replace_item(item=review, body=review)
                return review
            return None
        except Exception as e:
            print(f"Error updating review: {e}")
            return None

    async def delete_review(self, review_id: str):
        """Delete a review"""
        try:
            review_container.delete_item(item=review_id, partition_key=review_id)
            return True
        except Exception as e:
            print(f"Error deleting review: {e}")
            return False

    async def get_product_rating_stats(self, product_id: str):
        """Get rating statistics for a product"""
        try:
            query = f"""
            SELECT 
                COUNT(1) as total_reviews,
                AVG(r.rating) as average_rating,
                SUM(CASE WHEN r.rating = 5 THEN 1 ELSE 0 END) as five_stars,
                SUM(CASE WHEN r.rating = 4 THEN 1 ELSE 0 END) as four_stars,
                SUM(CASE WHEN r.rating = 3 THEN 1 ELSE 0 END) as three_stars,
                SUM(CASE WHEN r.rating = 2 THEN 1 ELSE 0 END) as two_stars,
                SUM(CASE WHEN r.rating = 1 THEN 1 ELSE 0 END) as one_star
            FROM r 
            WHERE r.product_id = '{product_id}'
            """
            result = list(review_container.query_items(query=query, enable_cross_partition_query=True))
            return result[0] if result else None
        except Exception as e:
            print(f"Error getting rating stats: {e}")
            return None

    async def check_user_review_exists(self, user_id: str, product_id: str):
        """Check if user has already reviewed this product"""
        try:
            query = f"SELECT * FROM r WHERE r.user_id = '{user_id}' AND r.product_id = '{product_id}'"
            reviews = list(review_container.query_items(query=query, enable_cross_partition_query=True))
            return reviews[0] if reviews else None
        except Exception as e:
            print(f"Error checking user review: {e}")
            return None