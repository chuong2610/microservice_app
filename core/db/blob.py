from azure.storage.blob import BlobServiceClient 

from settings import settings


account_name = settings.AZURE_STORAGE_ACCOUNT_NAME
account_key = settings.AZURE_STORAGE_ACCOUNT_KEY
container_name = settings.AZURE_STORAGE_CONTAINER_NAME

connect_str = f"DefaultEndpointsProtocol=https;AccountName={account_name};AccountKey={account_key};EndpointSuffix=core.windows.net"
blob_service_client = BlobServiceClient.from_connection_string(connect_str)
container_client = blob_service_client.get_container_client(container_name)
