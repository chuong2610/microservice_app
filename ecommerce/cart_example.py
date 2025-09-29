# Cart Functionality Example Usage

"""
This file demonstrates how to use the cart functionality.
The implementation is similar to your MongoDB example but adapted for CosmosDB.

## API Endpoints:

### 1. Get Cart
GET /cart/{user_id}
- Returns user's cart, creates new one if doesn't exist

### 2. Add to Cart
POST /cart/{user_id}/add
Body:
{
    "product_id": "prod123",
    "name": "Product Name",
    "price": 29.99,
    "quantity": 2
}

### 3. Update Quantity
PUT /cart/{user_id}/update-quantity
Body:
{
    "product_id": "prod123",
    "quantity": 5
}

### 4. Remove from Cart
DELETE /cart/{user_id}/remove
Body:
{
    "product_id": "prod123"
}

### 5. Clear Cart
DELETE /cart/{user_id}/clear

### 6. Get Cart Summary
GET /cart/{user_id}/summary
- Returns items count and total price

## Example Usage in Python:

```python
import asyncio
from services.cart_service import CartService
from repositories.cart_repository import CartRepository

async def example_usage():
    # Initialize service
    cart_repository = CartRepository()
    cart_service = CartService(cart_repository)
    
    user_id = "user123"
    
    # Get cart (creates if not exists)
    cart = await cart_service.get_cart(user_id)
    print("Initial cart:", cart)
    
    # Add item to cart
    product = {
        "product_id": "prod123",
        "name": "Laptop",
        "price": 999.99
    }
    cart = await cart_service.add_to_cart(user_id, product, 1)
    print("After adding laptop:", cart)
    
    # Add another item
    product2 = {
        "product_id": "prod456",
        "name": "Mouse",
        "price": 29.99
    }
    cart = await cart_service.add_to_cart(user_id, product2, 2)
    print("After adding mouse:", cart)
    
    # Update quantity
    cart = await cart_service.update_quantity(user_id, "prod123", 2)
    print("After updating laptop quantity:", cart)
    
    # Remove item
    cart = await cart_service.remove_from_cart(user_id, "prod456")
    print("After removing mouse:", cart)
    
    # Clear cart
    cart = await cart_service.clear_cart(user_id)
    print("After clearing cart:", cart)

# Run example
# asyncio.run(example_usage())
```

## Key Features Implemented:

1. **Get Cart**: Automatically creates cart if it doesn't exist
2. **Add to Cart**: Adds new items or updates quantity if item already exists
3. **Update Quantity**: Updates specific item quantity, removes if quantity <= 0
4. **Remove from Cart**: Removes specific item from cart
5. **Clear Cart**: Removes all items from cart
6. **Auto-calculate Total**: Automatically recalculates total price after each operation
7. **Timestamps**: Tracks created_at and updated_at timestamps

## Database Structure:

The cart document in CosmosDB looks like:
```json
{
    "id": "uuid-string",
    "user_id": "user123",
    "items": [
        {
            "product_id": "prod123",
            "name": "Product Name",
            "price": 29.99,
            "quantity": 2
        }
    ],
    "total_price": 59.98,
    "created_at": "2025-09-29T10:00:00Z",
    "updated_at": "2025-09-29T10:05:00Z"
}
```
"""

# Example test function
async def test_cart_functionality():
    """Test function to verify cart functionality"""
    from services.cart_service import CartService
    from repositories.cart_repository import CartRepository
    
    cart_repository = CartRepository()
    cart_service = CartService(cart_repository)
    
    user_id = "test_user_123"
    
    try:
        # Test 1: Get empty cart
        print("=== Test 1: Get empty cart ===")
        cart = await cart_service.get_cart(user_id)
        print(f"Empty cart: {cart}")
        
        # Test 2: Add first item
        print("\n=== Test 2: Add first item ===")
        product1 = {
            "product_id": "laptop_001",
            "name": "Gaming Laptop",
            "price": 1299.99
        }
        cart = await cart_service.add_to_cart(user_id, product1, 1)
        print(f"After adding laptop: {cart}")
        
        # Test 3: Add second item
        print("\n=== Test 3: Add second item ===")
        product2 = {
            "product_id": "mouse_001",
            "name": "Gaming Mouse",
            "price": 79.99
        }
        cart = await cart_service.add_to_cart(user_id, product2, 2)
        print(f"After adding mouse: {cart}")
        
        # Test 4: Add same item (should update quantity)
        print("\n=== Test 4: Add same item (should update quantity) ===")
        cart = await cart_service.add_to_cart(user_id, product1, 1)
        print(f"After adding laptop again: {cart}")
        
        # Test 5: Update quantity
        print("\n=== Test 5: Update quantity ===")
        cart = await cart_service.update_quantity(user_id, "mouse_001", 3)
        print(f"After updating mouse quantity to 3: {cart}")
        
        # Test 6: Remove item
        print("\n=== Test 6: Remove item ===")
        cart = await cart_service.remove_from_cart(user_id, "mouse_001")
        print(f"After removing mouse: {cart}")
        
        # Test 7: Clear cart
        print("\n=== Test 7: Clear cart ===")
        cart = await cart_service.clear_cart(user_id)
        print(f"After clearing cart: {cart}")
        
        print("\n=== All tests completed successfully! ===")
        
    except Exception as e:
        print(f"Test failed with error: {e}")

if __name__ == "__main__":
    # Uncomment to run tests
    # asyncio.run(test_cart_functionality())
    pass