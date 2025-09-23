"""
Create Azure AI Search indexes:
 - items-index: text fields + semantic config + vector field + freshness profile
 - authors-index : text fields + semantic config + vector field
"""

import os
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchIndex, SimpleField, SearchableField, SearchField, SearchFieldDataType,
    VectorSearch, HnswParameters, HnswAlgorithmConfiguration, VectorSearchProfile,
    SemanticSearch, SemanticConfiguration, SemanticField, SemanticPrioritizedFields,
    ScoringProfile, FreshnessScoringFunction, FreshnessScoringParameters
)
import traceback
from azure.core.exceptions import HttpResponseError
from dotenv import load_dotenv
load_dotenv()


def describe_field(f):
    """Collect common attributes safely for debugging"""
    info = {
        "py_type": type(f).__name__,
        "repr": repr(f),
    }
    for attr in ("name", "type", "key", "searchable", "filterable", "facetable", "sortable",
                    "analyzer_name", "vector_search_dimensions", "vector_search_profile_name"):
        try:
            info[attr] = getattr(f, attr)
        except Exception:
            info[attr] = None
    # try to dump __dict__ if available
    try:
        info["__dict__"] = dict(getattr(f, "__dict__", {}))
    except Exception:
        info["__dict__"] = None
    return info


def dump_index_debug(idx):
    print("\n--- Debug: Index to create ---")
    print(f"index.name: {getattr(idx, 'name', None)}")
    print(f"fields (count): {len(getattr(idx, 'fields', []) or [])}")
    for fi, f in enumerate(getattr(idx, 'fields', []) or []):
        info = describe_field(f)
        print(f" field[{fi}]: name={info.get('name')} type={info.get('py_type')} searchable={info.get('searchable')} vector_dims={info.get('vector_search_dimensions')} vector_profile={info.get('vector_search_profile_name')}")
    vs = getattr(idx, 'vector_search', None)
    print(f"vector_search: {vs}")
    try:
        # try to introspect common attrs on VectorSearch
        if vs is not None:
            for a in ("profiles", "algorithm_configurations", "profiles_list", "algorithms"):
                try:
                    val = getattr(vs, a)
                    print(f" vector_search.{a}: {val}")
                except Exception:
                    pass
    except Exception:
        print("could not introspect vector_search")
    print(f"semantic_search: {getattr(idx, 'semantic_search', None)}")
    print("--- end debug ---\n")


def _log_detailed_error(hre):
    """Helper function to log detailed error information from HttpResponseError"""
    try:
        # Some HttpResponseError objects include .response or .error
        if hasattr(hre, 'response') and hre.response is not None:
            try:
                body = hre.response.text()
                print(f"Response body: {body}")
            except Exception:
                print("Unable to read hre.response.text()")
        if hasattr(hre, 'error') and hre.error is not None:
            print(f"Error model: {hre.error}")
        traceback.print_exc()
    except Exception:
        traceback.print_exc()


def create_indexes(reset: bool = True, verbose: bool = False) -> None:
    dim = int(os.getenv('EMBED_MODEL_DIMENSION', '1536')) 

    vector_search_definition = VectorSearch(
        algorithms=[
            HnswAlgorithmConfiguration(
                name="hnsw-cosine",
                parameters=HnswParameters(metric="cosine", m=16, ef_construction=400, ef_search=100),
            )
        ],
        profiles=[VectorSearchProfile(name="vs-default", algorithm_configuration_name="hnsw-cosine")]
    )
    
    client = SearchIndexClient(os.getenv('AZURE_SEARCH_ENDPOINT'), AzureKeyCredential(os.getenv('AZURE_SEARCH_KEY')))

    # -------- ITEMS --------
    # Optimized schema based on actual data structure and search requirements
    items_fields = [
        # Primary key
        SimpleField(name="id", type=SearchFieldDataType.String, key=True, filterable=True),
        
        # Core searchable content fields
        SearchableField(name="title", type=SearchFieldDataType.String, analyzer_name="en.lucene", sortable=True),
        SearchableField(name="abstract", type=SearchFieldDataType.String, analyzer_name="en.lucene"),
        
        # Temporal fields for sorting and freshness scoring
        SimpleField(name="updated_at", type=SearchFieldDataType.DateTimeOffset, filterable=True, sortable=True),
        
        # Application filtering
        SimpleField(name="app_id", type=SearchFieldDataType.String, filterable=True),
        
        # Vector field for hybrid search (abstract-based)
        SearchField(
            name="abstract_vector",
            type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
            searchable=True,
            vector_search_dimensions=dim,
            vector_search_profile_name="vs-default",
        ),
    ]

    items_semantic = SemanticConfiguration(
        name="items-semantic",
        prioritized_fields=SemanticPrioritizedFields(
            title_field=SemanticField(field_name="title"),
            content_fields=[
                SemanticField(field_name="abstract")
            ]
        ),
    )

    scoring_profiles = [
        ScoringProfile(
            name="freshness_profile",
            functions=[FreshnessScoringFunction(
                field_name="updated_at",
                boost=2.0,
                parameters=FreshnessScoringParameters(boosting_duration=f"P{os.getenv('FRESHNESS_WINDOW_DAYS')}D")
            )]
        )
    ]

    items_index = SearchIndex(
        name=os.getenv('SEARCH_ITEM_INDEX_NAME'),
        fields=items_fields,
        vector_search=vector_search_definition,
        semantic_search=SemanticSearch(
            configurations=[items_semantic],
            default_configuration_name="items-semantic"
        ),
        scoring_profiles=scoring_profiles,
    )

    # -------- AUTHORS --------
    # Optimized schema for author/user search based on actual data structure
    author_fields = [
        # Primary key
        SimpleField(name="id", type=SearchFieldDataType.String, key=True, filterable=True),
        
        # Core searchable fields
        SearchableField(name="full_name", type=SearchFieldDataType.String, analyzer_name="en.lucene", sortable=True),
        
        # Application filtering
        SimpleField(name="app_id", type=SearchFieldDataType.String, filterable=True),
    ]

    authors_semantic = SemanticConfiguration(
        name="authors-semantic",
        prioritized_fields=SemanticPrioritizedFields(
            title_field=SemanticField(field_name="full_name")
        ),
    )

    authors_index = SearchIndex(
        name=os.getenv('SEARCH_AUTHOR_INDEX_NAME'),
        fields=author_fields,
        vector_search=vector_search_definition,
        semantic_search=SemanticSearch(
            configurations=[authors_semantic],
            default_configuration_name="authors-semantic"
        ),
    )

    # Create or update all indexes we need (simplified - no chunk index)
    for idx in (items_index, authors_index):
        if reset:
            try:
                client.delete_index(idx.name)
                if verbose:
                    print(f"Deleted existing index: {idx.name}")
            except Exception:
                # Index doesn't exist, which is fine
                pass
        
        # Dump debug info before attempting to create (if verbose)
        if verbose:
            dump_index_debug(idx)
        
        try:
            client.create_index(idx)
            print(f"Successfully created index: {idx.name}")
        except HttpResponseError as hre:
            # Handle resource already exists error (409) or similar messages
            if hre.status_code == 409 or "already exists" in str(hre).lower():
                print(f"Index {idx.name} already exists, updating...")
                client.create_or_update_index(idx)
                print(f"Successfully updated index: {idx.name}")
            else:
                # Log detailed error information for other HTTP errors
                print(f"HttpResponseError creating index {idx.name}: {hre}")
                if verbose:
                    _log_detailed_error(hre)
                raise
        except Exception as e:
            print(f"Unexpected error creating index {idx.name}: {e}")
            if verbose:
                traceback.print_exc()
            raise

    print(f"Created indexes with vector dim={dim}: items-index, authors-index")


