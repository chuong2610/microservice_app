from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from schemas.cart_schema import (
    AddToCartRequest, 
    UpdateQuantityRequest, 
    RemoveFromCartRequest,
    CartResponse,
    CartSummaryResponse
)
from services.cart_service import CartService
from repositories.cart_repository import CartRepository

router = APIRouter(prefix="/cart", tags=["Cart"])

# Dependency injection
def get_cart_service():
    cart_repository = CartRepository()
    return CartService(cart_repository)


@router.get("/{user_id}", response_model=CartResponse)
async def get_cart(user_id: str, cart_service: CartService = Depends(get_cart_service)):
    try:
        cart = await cart_service.get_cart(user_id)
        if not cart:
            raise HTTPException(status_code=404, detail="Cart not found")
        
        return CartResponse(**cart)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.post("/{user_id}/add")
async def add_to_cart(
    user_id: str, 
    request: AddToCartRequest,
    cart_service: CartService = Depends(get_cart_service)
):
    try:
        product = {
            "product_id": request.product_id,
            "name": request.name,
            "price": request.price
        }
        
        cart = await cart_service.add_to_cart(user_id, product, request.quantity)
        if not cart:
            raise HTTPException(status_code=500, detail="Failed to add item to cart")
        
        return JSONResponse(
            status_code=200,
            content={
                "message": "Item added to cart successfully",
                "cart": cart_service.map_to_cart_detail_dto(cart)
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.put("/{user_id}/update-quantity")
async def update_quantity(
    user_id: str,
    request: UpdateQuantityRequest,
    cart_service: CartService = Depends(get_cart_service)
):
    try:
        cart = await cart_service.update_quantity(user_id, request.product_id, request.quantity)
        if not cart:
            raise HTTPException(status_code=404, detail="Cart not found")
        
        action = "removed from" if request.quantity == 0 else "updated in"
        return JSONResponse(
            status_code=200,
            content={
                "message": f"Item {action} cart successfully",
                "cart": cart_service.map_to_cart_detail_dto(cart)
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.delete("/{user_id}/remove")
async def remove_from_cart(
    user_id: str,
    request: RemoveFromCartRequest,
    cart_service: CartService = Depends(get_cart_service)
):
    try:
        cart = await cart_service.remove_from_cart(user_id, request.product_id)
        if not cart:
            raise HTTPException(status_code=404, detail="Cart not found")
        
        return JSONResponse(
            status_code=200,
            content={
                "message": "Item removed from cart successfully",
                "cart": cart_service.map_to_cart_detail_dto(cart)
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.delete("/{user_id}/clear")
async def clear_cart(
    user_id: str,
    cart_service: CartService = Depends(get_cart_service)
):
    try:
        cart = await cart_service.clear_cart(user_id)
        if not cart:
            raise HTTPException(status_code=404, detail="Cart not found")
        
        return JSONResponse(
            status_code=200,
            content={
                "message": "Cart cleared successfully",
                "cart": cart_service.map_to_cart_detail_dto(cart)
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/{user_id}/summary", response_model=CartSummaryResponse)
async def get_cart_summary(
    user_id: str,
    cart_service: CartService = Depends(get_cart_service)
):
    try:
        cart = await cart_service.get_cart(user_id)
        if not cart:
            raise HTTPException(status_code=404, detail="Cart not found")
        
        return CartSummaryResponse(
            items_count=len(cart["items"]),
            total_price=cart["total_price"],
            items=cart["items"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")