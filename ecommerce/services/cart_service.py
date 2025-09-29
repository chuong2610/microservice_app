from repositories.cart_repository import CartRepository


class CartService:
    def __init__(self, cart_repository: CartRepository):
        self.cart_repository = cart_repository

    async def get_cart(self, user_id: str):
        return await self.map_to_cart_detail_dto(self.cart_repository.get_cart(user_id))

    async def add_to_cart(self, user_id: str, product: dict, quantity: int):
        cart = await self.get_cart(user_id)
        if not cart:
            return None

        found = False
        for item in cart["items"]:
            if item["product_id"] == product["product_id"]:
                item["quantity"] += quantity
                found = True
                break

        if not found:
            cart["items"].append({
                "product_id": product["product_id"],
                "name": product["name"],
                "price": product["price"],
                "quantity": quantity
            })

        cart["total_price"] = sum(item["price"] * item["quantity"] for item in cart["items"])

        return await self.map_to_cart_detail_dto(self.cart_repository.update_cart(user_id, cart))

    async def update_quantity(self, user_id: str, product_id: str, quantity: int):
        cart = await self.get_cart(user_id)
        if not cart:
            return None

        for item in cart["items"]:
            if item["product_id"] == product_id:
                if quantity <= 0:
                    cart["items"] = [i for i in cart["items"] if i["product_id"] != product_id]
                else:
                    item["quantity"] = quantity
                break

        cart["total_price"] = sum(item["price"] * item["quantity"] for item in cart["items"])

        return await self.map_to_cart_detail_dto(self.cart_repository.update_cart(user_id, cart))

    async def remove_from_cart(self, user_id: str, product_id: str):
        cart = await self.get_cart(user_id)
        if not cart:
            return None

        cart["items"] = [item for item in cart["items"] if item["product_id"] != product_id]

        cart["total_price"] = sum(item["price"] * item["quantity"] for item in cart["items"])

        return await self.map_to_cart_detail_dto(self.cart_repository.update_cart(user_id, cart))

    async def clear_cart(self, user_id: str):
        cart = await self.get_cart(user_id)
        if not cart:
            return None

        cart["items"] = []
        cart["total_price"] = 0.0

        return await self.map_to_cart_detail_dto(self.cart_repository.update_cart(user_id, cart))
    
    def map_to_cart_detail_dto(self, cart) -> dict:
        if cart:
            return {
                "id": cart.get("id"),
                "user_id": cart.get("user_id"),
                "items": cart.get("items", []),
                "total_price": cart.get("total_price", 0.0),

            }
        return None