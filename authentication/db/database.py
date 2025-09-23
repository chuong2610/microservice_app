from azure.cosmos import CosmosClient
from settings import settings

client = CosmosClient(settings.COSMOS_ENDPOINT, settings.COSMOS_KEY)
database = client.create_database_if_not_exists(id=settings.COSMOS_DB_NAME)
container = database.create_container_if_not_exists(
    id=settings.COSMOS_CONTAINER_NAME,
    partition_key="/id",
    offer_throughput=400
)
