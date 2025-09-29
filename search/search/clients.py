"""
Factory functions for Azure Search clients.
Provides consistent client creation pattern for different index types.
"""

import os
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from dotenv import load_dotenv
load_dotenv()

def items_client() -> SearchClient:
    """
    Create a SearchClient for the items-index only (simplified implementation).
    """
    print("🔧 Creating items search client...")
    try:
        index_name = os.getenv('SEARCH_ITEM_INDEX_NAME')
        client = SearchClient(os.getenv('AZURE_SEARCH_ENDPOINT'), index_name, AzureKeyCredential(os.getenv('AZURE_SEARCH_KEY')))
        print(f"✅ Items client created: {index_name}")
        return client
    except Exception as e:
        print(f"❌ Failed to create items client: {e}")
        raise

def authors_client() -> SearchClient:
    """
    Create a SearchClient for the authors-index.
    """
    print("🔧 Creating authors search client...")
    try:
        index_name = os.getenv('SEARCH_AUTHOR_INDEX_NAME')
        client = SearchClient(os.getenv('AZURE_SEARCH_ENDPOINT'), index_name, AzureKeyCredential(os.getenv('AZURE_SEARCH_KEY')))
        print(f"✅ Authors client created: {os.getenv('AZURE_SEARCH_ENDPOINT')}/{index_name}")
        return client
    except Exception as e:
        print(f"❌ Failed to create authors client: {e}")
        raise


