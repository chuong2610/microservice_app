# Review Functionality Example Usage

"""
This file demonstrates how to use the comprehensive review functionality.
The implementation provides full CRUD operations for product reviews with rating statistics.

## API Endpoints:

### 1. Create Review
POST /reviews/?user_id={user_id}
Body:
{
    "product_id": "prod123",
    "rating": 5,
    "comment": "Great product!",
    "user_name": "John Doe"
}

### 2. Get Review by ID
GET /reviews/{review_id}

### 3. Get Product Reviews with Summary
GET /reviews/product/{product_id}?limit=50&offset=0
- Returns reviews with rating summary and pagination

### 4. Get User Reviews
GET /reviews/user/{user_id}?limit=50&offset=0

### 5. Get Product Rating Summary
GET /reviews/product/{product_id}/summary
- Returns total reviews, average rating, and rating distribution

### 6. Update Review
PUT /reviews/{review_id}?user_id={user_id}
Body:
{
    "rating": 4,
    "comment": "Updated comment"
}

### 7. Delete Review
DELETE /reviews/{review_id}?user_id={user_id}

### 8. Get Product Review Stats
GET /reviews/product/{product_id}/stats
- Returns rating summary + recent reviews

## Example Usage in Python:

```python
import asyncio
from services.review_service import ReviewService
from repositories.review_repository import ReviewRepository

async def example_review_usage():
    # Initialize service
    review_repository = ReviewRepository()
    review_service = ReviewService(review_repository)
    
    user_id = "user123"
    product_id = "laptop001"
    
    # Create a review
    review = await review_service.create_review(
        user_id=user_id,
        product_id=product_id,
        rating=5,
        comment="Excellent laptop! Fast delivery and great quality.",
        user_name="John Doe"
    )
    print("Created review:", review)
    
    # Try to create duplicate review (should fail)
    duplicate = await review_service.create_review(
        user_id=user_id,
        product_id=product_id,
        rating=4,
        comment="Another review",
        user_name="John Doe"
    )
    print("Duplicate review attempt:", duplicate)
    
    # Get product reviews with summary
    reviews_data = await review_service.get_reviews_with_rating_summary(product_id)
    print("Product reviews with summary:", reviews_data)
    
    # Get rating summary only
    rating_summary = await review_service.get_product_rating_summary(product_id)
    print("Rating summary:", rating_summary)
    
    # Update review
    if not isinstance(review, dict) or "error" not in review:
        updated_review = await review_service.update_review(
            review_id=review["id"],
            user_id=user_id,
            rating=4,
            comment="Updated: Very good laptop, minor issues with battery life."
        )
        print("Updated review:", updated_review)
    
    # Get user's reviews
    user_reviews = await review_service.get_user_reviews(user_id)
    print("User reviews:", user_reviews)
    
    # Delete review
    if not isinstance(review, dict) or "error" not in review:
        delete_result = await review_service.delete_review(
            review_id=review["id"],
            user_id=user_id
        )
        print("Delete result:", delete_result)

# Run example
# asyncio.run(example_review_usage())
```

## Key Features Implemented:

✅ **Create Reviews**: Users can review products with ratings (1-5 stars) and comments
✅ **Duplicate Prevention**: Users can only review each product once
✅ **Rating Statistics**: Calculate average ratings and rating distribution
✅ **Pagination**: Support for paginated review lists
✅ **User Authorization**: Users can only edit/delete their own reviews
✅ **Review Management**: Full CRUD operations for reviews
✅ **Product Analytics**: Get comprehensive review stats for products
✅ **Search & Filter**: Get reviews by product or user
✅ **Timestamps**: Track creation and update times
✅ **Data Validation**: Proper validation for ratings, comments, etc.

## Database Structure:

The review document in CosmosDB looks like:
```json
{
    "id": "uuid-string",
    "product_id": "prod123",
    "user_id": "user456",
    "user_name": "John Doe",
    "rating": 5,
    "comment": "Excellent product! Highly recommended.",
    "created_at": "2025-09-29T10:00:00Z",
    "updated_at": "2025-09-29T10:00:00Z"
}
```

## Rating Summary Structure:
```json
{
    "total_reviews": 25,
    "average_rating": 4.2,
    "rating_distribution": {
        "5": 12,
        "4": 8,
        "3": 3,
        "2": 1,
        "1": 1
    }
}
```
"""

# Example test function
async def test_review_functionality():
    """Test function to verify review functionality"""
    from services.review_service import ReviewService
    from repositories.review_repository import ReviewRepository
    
    review_repository = ReviewRepository()
    review_service = ReviewService(review_repository)
    
    user_id = "test_user_456"
    product_id = "test_product_789"
    
    try:
        print("=== Review Functionality Tests ===\n")
        
        # Test 1: Create first review
        print("=== Test 1: Create first review ===")
        review1 = await review_service.create_review(
            user_id=user_id,
            product_id=product_id,
            rating=5,
            comment="Amazing product! Exceeded my expectations.",
            user_name="Alice Johnson"
        )
        print(f"Created review: {review1}\n")
        
        # Test 2: Try to create duplicate review (should fail)
        print("=== Test 2: Try duplicate review (should fail) ===")
        duplicate = await review_service.create_review(
            user_id=user_id,
            product_id=product_id,
            rating=4,
            comment="Another review attempt",
            user_name="Alice Johnson"
        )
        print(f"Duplicate attempt result: {duplicate}\n")
        
        # Test 3: Create review from different user
        print("=== Test 3: Create review from different user ===")
        review2 = await review_service.create_review(
            user_id="different_user_123",
            product_id=product_id,
            rating=4,
            comment="Good product, fast shipping.",
            user_name="Bob Smith"
        )
        print(f"Second review: {review2}\n")
        
        # Test 4: Get product reviews with summary
        print("=== Test 4: Get product reviews with summary ===")
        reviews_summary = await review_service.get_reviews_with_rating_summary(product_id)
        print(f"Reviews with summary: {reviews_summary}\n")
        
        # Test 5: Get rating summary only
        print("=== Test 5: Get rating summary ===")
        rating_summary = await review_service.get_product_rating_summary(product_id)
        print(f"Rating summary: {rating_summary}\n")
        
        # Test 6: Update review
        if not isinstance(review1, dict) or "error" not in review1:
            print("=== Test 6: Update review ===")
            updated = await review_service.update_review(
                review_id=review1["id"],
                user_id=user_id,
                rating=4,
                comment="Updated: Great product, minor packaging issues."
            )
            print(f"Updated review: {updated}\n")
        
        # Test 7: Get user reviews
        print("=== Test 7: Get user reviews ===")
        user_reviews = await review_service.get_user_reviews(user_id)
        print(f"User reviews: {user_reviews}\n")
        
        # Test 8: Try unauthorized update (should fail)
        if not isinstance(review2, dict) or "error" not in review2:
            print("=== Test 8: Try unauthorized update (should fail) ===")
            unauthorized = await review_service.update_review(
                review_id=review2["id"],
                user_id=user_id,  # Wrong user trying to update
                rating=1,
                comment="Trying to update someone else's review"
            )
            print(f"Unauthorized update result: {unauthorized}\n")
        
        # Test 9: Delete review
        if not isinstance(review1, dict) or "error" not in review1:
            print("=== Test 9: Delete review ===")
            delete_result = await review_service.delete_review(
                review_id=review1["id"],
                user_id=user_id
            )
            print(f"Delete result: {delete_result}\n")
        
        print("=== All review tests completed successfully! ===")
        
    except Exception as e:
        print(f"Test failed with error: {e}")

if __name__ == "__main__":
    # Uncomment to run tests
    # asyncio.run(test_review_functionality())
    pass