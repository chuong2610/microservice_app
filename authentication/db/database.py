from azure.cosmos import CosmosClient
from settings import Settings

client = CosmosClient(Settings.COSMOS_ENDPOINT, Settings.COSMOS_KEY)
database = client.create_database_if_not_exists(id=Settings.COSMOS_DB_NAME)
container = database.create_container_if_not_exists(
    id=Settings.COSMOS_CONTAINER_NAME,
    partition_key="/id",
    offer_throughput=400
)
