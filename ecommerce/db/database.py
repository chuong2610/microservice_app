from settings import settings
from azure.cosmos import CosmosClient

client = CosmosClient(settings.COSMOS_ENDPOINT, settings.COSMOS_KEY)
database = client.create_database_if_not_exists(id=settings.COSMOS_DB_NAME)
cart_container = database.create_container_if_not_exists(
    id=settings.COSMOS_CONTAINER_CARTS,
    partition_key="/id",
    offer_throughput=400
)
order_container = database.create_container_if_not_exists(
    id=settings.COSMOS_CONTAINER_ORDERS,
    partition_key="/id",
    offer_throughput=400
)
review_container = database.create_container_if_not_exists(
    id=settings.COSMOS_CONTAINER_REVIEWS,
    partition_key="/id",
    offer_throughput=400
)