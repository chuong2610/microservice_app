from azure.cosmos import CosmosClient, exceptions
from settings import settings

try:
    print(f"Connecting to Cosmos DB at: {settings.COSMOS_ENDPOINT}")
    client = CosmosClient(settings.COSMOS_ENDPOINT, settings.COSMOS_KEY)
    database = client.create_database_if_not_exists(id=settings.COSMOS_DB_NAME)
    container = database.create_container_if_not_exists(
        id=settings.COSMOS_CONTAINER_ITEMS,
        partition_key="/id",
        offer_throughput=400
    )
    print(f"Successfully connected to Cosmos DB: {settings.COSMOS_DB_NAME}/{settings.COSMOS_CONTAINER_ITEMS}")
except exceptions.CosmosHttpResponseError as e:
    print(f"Cosmos DB connection failed: {e}")
    raise
except Exception as e:
    print(f"Unexpected error connecting to Cosmos DB: {e}")
    raise
