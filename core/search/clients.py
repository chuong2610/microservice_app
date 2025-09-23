"""
Factory functions for Azure Search clients.
Provides consistent client creation pattern for different index types.
"""

import os
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from dotenv import load_dotenv
load_dotenv()

def articles_client() -> SearchClient:
    """
    Create a SearchClient for the articles-index only (simplified implementation).
    """
    print("🔧 Creating articles search client...")
    try:
        client = SearchClient(os.getenv('AZURE_SEARCH_ENDPOINT'), "articles-index", AzureKeyCredential(os.getenv('AZURE_SEARCH_KEY')))
        print(f"✅ Articles client created: articles-index")
        return client
    except Exception as e:
        print(f"❌ Failed to create articles client: {e}")
        raise

def authors_client() -> SearchClient:
    """
    Create a SearchClient for the authors-index.
    """
    print("🔧 Creating authors search client...")
    try:
        client = SearchClient(os.getenv('AZURE_SEARCH_ENDPOINT'), "authors-index", AzureKeyCredential(os.getenv('AZURE_SEARCH_KEY')))
        print(f"✅ Authors client created: {os.getenv('AZURE_SEARCH_ENDPOINT')}/authors-index")
        return client
    except Exception as e:
        print(f"❌ Failed to create authors client: {e}")
        raise


