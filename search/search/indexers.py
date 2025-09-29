"""
Azure AI Search Native Indexers for Cosmos DB Integration.
"""

import os
from typing import Optional

from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import ResourceNotFoundError, ResourceExistsError, HttpResponseError

from azure.search.documents.indexes import SearchIndexerClient
from dotenv import load_dotenv
load_dotenv()

# ==========================================
# CURRENT IMPORTS (Simplified Implementation)
# ==========================================
from azure.search.documents.indexes.models import (
    SearchIndexerDataContainer,
    SearchIndexerDataSourceConnection,
    SearchIndexer,
    IndexingSchedule,
    IndexingParameters,
    FieldMapping,
    OutputFieldMappingEntry,
    SearchIndexerSkillset,
    InputFieldMappingEntry,
    SoftDeleteColumnDeletionDetectionPolicy,
    HighWaterMarkChangeDetectionPolicy,
)
from azure.search.documents.indexes.models import AzureOpenAIEmbeddingSkill


class AzureIndexerManager:
    """
    Manages Azure AI Search indexers for automatic Cosmos DB synchronization.
    """
    
    def __init__(self):
        """Initialize the indexer client."""
        self.client = SearchIndexerClient(os.getenv('AZURE_SEARCH_ENDPOINT'), AzureKeyCredential(os.getenv('AZURE_SEARCH_KEY')))
        
        self.item_index_name = os.getenv('SEARCH_ITEM_INDEX_NAME')
        self.author_index_name = os.getenv('SEARCH_AUTHOR_INDEX_NAME')
        
        self.item_indexer_name = self.item_index_name + "-indexer"
        self.author_indexer_name = self.author_index_name + "-indexer"
        
        self.item_data_source_name = self.item_index_name + "-datasource"
        self.author_data_source_name = self.author_index_name + "-datasource"
        
        self.item_skillset_name = self.item_index_name + "-skillset"
        self.author_skillset_name = self.author_index_name + "-skillset"

    # ==========================================
    # DATA SOURCES & INDEXERS
    # ==========================================
    def create_cosmos_data_source(
        self, 
        name: str, 
        container_name: str, 
        query: Optional[str] = None,
        enable_soft_delete: bool = True,  # Re-enabled for proper deletion tracking
        soft_delete_column: str = "is_active",
        soft_delete_marker: str = "false"
    ) -> SearchIndexerDataSourceConnection:
        """
        Create a Cosmos DB data source for Azure AI Search indexer with proper deletion tracking.
        """
        # Construct Cosmos DB connection string
        cosmos_connection_string = (
            f"AccountEndpoint={os.getenv('COSMOS_ENDPOINT')};"
            f"AccountKey={os.getenv('COSMOS_KEY')};"
            f"Database={os.getenv('COSMOS_DB_NAME')}"
        )
        
        # Create data container configuration
        container = SearchIndexerDataContainer(
            name=container_name,
            query=query
        )
        
        # Configure change detection policy for incremental indexing using _ts timestamp
        change_detection_policy = HighWaterMarkChangeDetectionPolicy(
            high_water_mark_column_name="_ts"
        )
        
        # Configure deletion detection policy if enabled
        deletion_policy = None
        if enable_soft_delete:
            deletion_policy = SoftDeleteColumnDeletionDetectionPolicy(
                soft_delete_column_name=soft_delete_column,
                soft_delete_marker_value=soft_delete_marker
            )
        
        # Create data source with both change detection and deletion detection policies
        data_source = SearchIndexerDataSourceConnection(
            name=name,
            type="cosmosdb",
            connection_string=cosmos_connection_string,
            container=container,
            data_change_detection_policy=change_detection_policy,
            data_deletion_detection_policy=deletion_policy,
            description=f"Cosmos DB data source for {container_name} container with change and deletion tracking"
        )
        
        return data_source
    
    def create_items_indexer(self) -> SearchIndexer:
        """
        Create an indexer for items with field mappings and automatic scheduling.
        """
        # Field mappings from Cosmos DB to search index
        field_mappings = [
            FieldMapping(source_field_name="id", target_field_name="id"),
            FieldMapping(source_field_name="title", target_field_name="title"),
            FieldMapping(source_field_name="abstract", target_field_name="abstract"),
            FieldMapping(source_field_name="updated_at", target_field_name="updated_at"),
            FieldMapping(source_field_name="app_id", target_field_name="app_id"),
        ]
        
        # Output field mappings for computed fields (using raw dict due to SDK/API mismatch)
        output_field_mappings = []
        
        # Use raw dict to match REST API schema
        output_field_mappings.append({
            "sourceFieldName": "/document/abstract_vector",
            "targetFieldName": "abstract_vector"
        })
        
        # Indexing parameters for high-water mark change detection
        # Note: No configuration needed for Cosmos DB (dataToExtract/parsingMode not supported)
        # Reduced batch size to avoid Azure OpenAI rate limiting
        parameters = IndexingParameters(
            batch_size=50,                  # Reduced from 100 to avoid rate limits
            max_failed_items=10,
            max_failed_items_per_batch=3    # Reduced to fail faster
        )
        
        # Schedule for automatic runs (every 5 minutes)
        schedule = IndexingSchedule(interval="PT5M")  # ISO 8601 duration format
        
        # Create indexer with skillset 
        indexer = SearchIndexer(
            name=self.item_indexer_name,
            data_source_name=self.item_data_source_name,
            target_index_name=self.item_index_name,
            skillset_name=self.item_skillset_name,
            field_mappings=field_mappings,
            output_field_mappings=output_field_mappings,
            parameters=parameters,
            schedule=schedule,
            description="Indexer for items with abstract embeddings only"
        )
        
        return indexer
    
    def create_authors_indexer(self) -> SearchIndexer:
        """
        Create an indexer for authors with field mappings and automatic scheduling.
        """
        # Field mappings from Cosmos DB to search index
        field_mappings = [
            FieldMapping(source_field_name="id", target_field_name="id"),
            FieldMapping(source_field_name="full_name", target_field_name="full_name"),
            FieldMapping(source_field_name="app_id", target_field_name="app_id"),
        ]
        
        # Output field mappings for computed fields
        output_field_mappings = [
            # # Set searchable_text to full_name
            # {
            #     "sourceFieldName": "/document/full_name",
            #     "targetFieldName": "searchable_text"
            # }
        ]
        
        # Indexing parameters
        # Note: No configuration needed for Cosmos DB (dataToExtract/parsingMode not supported)
        # Reduced batch size to avoid Azure OpenAI rate limiting
        parameters = IndexingParameters(
            batch_size=50,                  # Reduced from 100 to avoid rate limits
            max_failed_items=10,
            max_failed_items_per_batch=3    # Reduced to fail faster
        )
        
        # Schedule for automatic runs (every 5 minutes)
        schedule = IndexingSchedule(interval="PT5M")
        
        # Create indexer with skillset 
        indexer = SearchIndexer(
            name=self.author_indexer_name,
            data_source_name=self.author_data_source_name,
            target_index_name=self.author_index_name,
            # skillset_name="authors-skillset",
            field_mappings=field_mappings,
            output_field_mappings=output_field_mappings,
            parameters=parameters,
            schedule=schedule,
            description="Automatic indexer for authors from Cosmos DB with deletion tracking"
        )
        
        return indexer
    
    # ==========================================
    # SKILLSETS
    # ==========================================
    def create_items_skillset(self) -> SearchIndexerSkillset:
        """
        Simplified items skillset:
          - Embed abstract field directly (max 8000 tokens, no splitting)
          - Single index for items (no chunk projections)
        """
        skills = []
        
        # Embed abstract directly (no splitting needed for abstracts which are typically short)
        embedding_skill = AzureOpenAIEmbeddingSkill(
            name="embed-abstract",
            description="Embed item abstract via Azure OpenAI",
            context="/document",
            resource_url=os.getenv('AZURE_OPENAI_ENDPOINT'),
            api_key=os.getenv('AZURE_OPENAI_API_KEY'),
            deployment_name=os.getenv('AZURE_OPENAI_EMBED_MODEL'),
            model_name=os.getenv('AZURE_OPENAI_EMBED_MODEL'),
            inputs=[InputFieldMappingEntry(name="text", source="/document/abstract")],
            outputs=[OutputFieldMappingEntry(name="embedding", target_name="abstract_vector")],
        )
            
        skills.append(embedding_skill)
        
        skillset = SearchIndexerSkillset(
            name=self.item_skillset_name,
            description="Simple embedding of item abstract",
            skills=skills,
        )
        
        return skillset
    
    def setup_indexers(
        self, 
        reset: bool = False, 
        verbose: bool = False
    ) -> None:
        """
        Set up all indexers, data sources, and skillsets for automatic sync.
        
        Args:
            reset: Whether to delete existing resources before creating new ones
            verbose: Enable verbose logging
        """
            
        if verbose:
            print("🔧 Setting up Azure AI Search indexers for automatic Cosmos DB sync...")
        
        try:
            # Delete existing resources if reset is requested
            if reset:
                self._cleanup_indexers(verbose)
            
            # 1. Create or update data sources
            if verbose:
                print("📊 Creating/updating Cosmos DB data sources...")
            
            # Now handles:
            # - added docs (via _ts high water mark change detection)
            # - updated docs (via _ts high water mark change detection) 
            # - deleted docs (via is_active soft delete detection policy)
            # Note: Soft delete re-enabled as per Microsoft documentation - this is the only supported way
            # Filter out records with empty content to avoid skillset warnings
            items_ds = self.create_cosmos_data_source(
                self.item_data_source_name, 
                os.getenv('COSMOS_CONTAINER_ITEMS'),
                "SELECT * FROM c WHERE c._ts >= @HighWaterMark ORDER BY c._ts",
                enable_soft_delete=True,
                soft_delete_column="is_active",
                soft_delete_marker="false"
            )
            
            authors_ds = self.create_cosmos_data_source(
                self.author_data_source_name, 
                os.getenv('COSMOS_CONTAINER_AUTHORS'),
                "SELECT * FROM c WHERE c._ts >= @HighWaterMark ORDER BY c._ts",
                enable_soft_delete=True,
                soft_delete_column="is_active", 
                soft_delete_marker="false"
            )
            
            self._create_or_update_data_source(items_ds, verbose)
            self._create_or_update_data_source(authors_ds, verbose)
            
            if verbose:
                print("✅ Data sources configured successfully")
            
            # 2. Create or update skillsets if embeddings are enabled
            if verbose:
                print("🧠 Creating/updating skillsets for content processing...")
            
            items_skillset = self.create_items_skillset()
            
            self._create_or_update_skillset(items_skillset, verbose)
            
            if verbose:
                print("✅ Skillsets configured successfully")

            # 3. Create or update indexers
            if verbose:
                print("⚙️ Creating/updating indexers...")
            
            items_indexer = self.create_items_indexer()
            authors_indexer = self.create_authors_indexer()
            
            self._create_or_update_indexer(items_indexer, verbose)
            self._create_or_update_indexer(authors_indexer, verbose)
            
            if verbose:
                print("✅ Indexers configured successfully")
            
            # 4. Run indexers once to populate data
            if verbose:
                print("🚀 Running initial indexing...")
            
            # Run the indexers by their configured names (respecting any env overrides)
            self.client.run_indexer(self.item_indexer_name)
            self.client.run_indexer(self.author_indexer_name)

            if verbose:
                print("✅ Initial indexing started")
                print("🔄 Indexers are now configured to run automatically every 5 minutes")
                print("📈 Data will be automatically synchronized from Cosmos DB to Azure AI Search")
            
        except Exception as e:
            print(f"❌ Failed to setup indexers: {e}")
            raise
    
    # ==========================================
    # HELPERS
    # ==========================================
    def _cleanup_indexers(self, verbose: bool = False) -> None:
        """Clean up existing indexers, skillsets, and data sources."""
        if verbose:
            print("🧹 Cleaning up existing indexer resources...")
        
        resources_to_delete = [
            ("indexer", [self.item_indexer_name, self.author_indexer_name]),
            ("skillset", [self.item_skillset_name, self.author_skillset_name]),
            ("data_source_connection", [self.item_data_source_name, self.author_data_source_name])
        ]
        
        for resource_type, names in resources_to_delete:
            for name in names:
                try:
                    if resource_type == "indexer":
                        self.client.delete_indexer(name)
                    elif resource_type == "skillset":
                        self.client.delete_skillset(name)
                    elif resource_type == "data_source_connection":
                        self.client.delete_data_source_connection(name)
                    
                    if verbose:
                        print(f"🗑️ Deleted {resource_type}: {name}")
                        
                except ResourceNotFoundError:
                    if verbose:
                        print(f"ℹ️ {resource_type} {name} not found (already deleted)")
                except Exception as e:
                    if verbose:
                        print(f"⚠️ Failed to delete {resource_type} {name}: {e}")
    
    def _create_or_update_data_source(self, data_source: SearchIndexerDataSourceConnection, verbose: bool = False) -> None:
        """
        Create or update a data source connection.
        
        Args:
            data_source: The data source to create or update
            verbose: Enable verbose logging
        """
        try:
            self.client.create_data_source_connection(data_source)
            if verbose:
                print(f"   ✅ Created data source: {data_source.name}")
        except ResourceExistsError as e:
            # Resource already exists, update it instead
            if verbose:
                print(f"   🔍 Data source {data_source.name} already exists, updating...")
            try:
                self.client.create_or_update_data_source_connection(data_source)
                if verbose:
                    print(f"   🔄 Updated existing data source: {data_source.name}")
            except Exception as update_error:
                print(f"   ❌ Failed to update data source {data_source.name}: {update_error}")
                print(f"   🔍 Update error type: {type(update_error).__name__}")
                raise
        except HttpResponseError as e:
            # Check if it's a resource exists error in HTTP response
            if e.status_code == 409 or "already exists" in str(e).lower():
                if verbose:
                    print(f"   🔍 HTTP 409 or 'already exists' detected for {data_source.name}, updating...")
                try:
                    self.client.create_or_update_data_source_connection(data_source)
                    if verbose:
                        print(f"   🔄 Updated existing data source: {data_source.name}")
                except Exception as update_error:
                    print(f"   ❌ Failed to update data source {data_source.name}: {update_error}")
                    print(f"   🔍 Update error type: {type(update_error).__name__}")
                    raise
            else:
                print(f"   ❌ HTTP error creating data source {data_source.name}: {e}")
                print(f"   🔍 HTTP error details: status={e.status_code}, message={e.message}")
                raise
        except Exception as e:
            print(f"   ❌ Failed to create data source {data_source.name}: {e}")
            print(f"   🔍 Exception type: {type(e).__name__}")
            print(f"   🔍 Exception details: {str(e)}")
            raise
    
    def _create_or_update_skillset(self, skillset: SearchIndexerSkillset, verbose: bool = False) -> None:
        """
        Create or update a skillset.
        
        Args:
            skillset: The skillset to create or update
            verbose: Enable verbose logging
        """
        try:
            self.client.create_skillset(skillset)
            if verbose:
                print(f"   ✅ Created skillset: {skillset.name}")
        except ResourceExistsError as e:
            # Resource already exists, update it instead
            if verbose:
                print(f"   🔍 Skillset {skillset.name} already exists, updating...")
            try:
                self.client.create_or_update_skillset(skillset)
                if verbose:
                    print(f"   🔄 Updated existing skillset: {skillset.name}")
            except Exception as update_error:
                print(f"   ❌ Failed to update skillset {skillset.name}: {update_error}")
                print(f"   🔍 Update error type: {type(update_error).__name__}")
                raise
        except HttpResponseError as e:
            # Check if it's a resource exists error in HTTP response
            if e.status_code == 409 or "already exists" in str(e).lower():
                if verbose:
                    print(f"   🔍 HTTP 409 or 'already exists' detected for {skillset.name}, updating...")
                try:
                    self.client.create_or_update_skillset(skillset)
                    if verbose:
                        print(f"   🔄 Updated existing skillset: {skillset.name}")
                except Exception as update_error:
                    print(f"   ❌ Failed to update skillset {skillset.name}: {update_error}")
                    print(f"   🔍 Update error type: {type(update_error).__name__}")
                    raise
            else:
                print(f"   ❌ HTTP error creating skillset {skillset.name}: {e}")
                print(f"   🔍 HTTP error details: status={e.status_code}, message={e.message}")
                raise
        except Exception as e:
            print(f"   ❌ Failed to create skillset {skillset.name}: {e}")
            print(f"   🔍 Exception type: {type(e).__name__}")
            print(f"   🔍 Exception details: {str(e)}")
            raise
    
    def _create_or_update_indexer(self, indexer: SearchIndexer, verbose: bool = False) -> None:
        """
        Create or update an indexer.
        
        Args:
            indexer: The indexer to create or update
            verbose: Enable verbose logging
        """
        try:
            if verbose:
                print(f"   🔍 Creating indexer: {indexer.name}")
                print(f"   📋 Indexer details:")
                print(f"      - Data source: {indexer.data_source_name}")
                print(f"      - Target index: {indexer.target_index_name}")
                print(f"      - Skillset: {indexer.skillset_name}")
                print(f"      - Field mappings count: {len(indexer.field_mappings or [])}")
                print(f"      - Output field mappings count: {len(indexer.output_field_mappings or [])}")
                
                # Debug field mappings
                if indexer.field_mappings:
                    print(f"   🗂️ Field mappings:")
                    for i, fm in enumerate(indexer.field_mappings):
                        print(f"      [{i}] {fm.source_field_name} -> {fm.target_field_name}")
                
                # Debug output field mappings  
                if indexer.output_field_mappings:
                    print(f"   📤 Output field mappings:")
                    for i, ofm in enumerate(indexer.output_field_mappings):
                        if isinstance(ofm, dict):
                            # Handle raw dict format
                            source = ofm.get('sourceFieldName', 'NO_SOURCE')
                            target = ofm.get('targetFieldName', 'NO_TARGET')
                            print(f"      [{i}] {source} -> {target}")
                            print(f"      [{i}] Type: dict (raw API format)")
                        else:
                            # Handle SDK object format
                            print(f"      [{i}] {getattr(ofm, 'name', 'NO_NAME')} -> {getattr(ofm, 'target_name', 'NO_TARGET')}")
                            print(f"      [{i}] Type: {type(ofm).__name__}")
                            print(f"      [{i}] All attributes: {[attr for attr in dir(ofm) if not attr.startswith('_')]}")
            
            self.client.create_indexer(indexer)
            if verbose:
                print(f"   ✅ Created indexer: {indexer.name}")
        except ResourceExistsError as e:
            # Resource already exists, update it instead
            if verbose:
                print(f"   🔍 Indexer {indexer.name} already exists, updating...")
            try:
                self.client.create_or_update_indexer(indexer)
                if verbose:
                    print(f"   🔄 Updated existing indexer: {indexer.name}")
            except Exception as update_error:
                print(f"   ❌ Failed to update indexer {indexer.name}: {update_error}")
                print(f"   🔍 Update error type: {type(update_error).__name__}")
                raise
        except HttpResponseError as e:
            # Check if it's a resource exists error in HTTP response
            if e.status_code == 409 or "already exists" in str(e).lower():
                if verbose:
                    print(f"   🔍 HTTP 409 or 'already exists' detected for {indexer.name}, updating...")
                try:
                    self.client.create_or_update_indexer(indexer)
                    if verbose:
                        print(f"   🔄 Updated existing indexer: {indexer.name}")
                except Exception as update_error:
                    print(f"   ❌ Failed to update indexer {indexer.name}: {update_error}")
                    print(f"   🔍 Update error type: {type(update_error).__name__}")
                    raise
            else:
                print(f"   ❌ HTTP error creating indexer {indexer.name}: {e}")
                print(f"   🔍 HTTP error details: status={e.status_code}, message={e.message}")
                raise
        except Exception as e:
            print(f"   ❌ Failed to create indexer {indexer.name}: {e}")
            print(f"   🔍 Exception type: {type(e).__name__}")
            print(f"   🔍 Exception details: {str(e)}")
            raise
    

def setup_azure_indexers(
    reset: bool = False, 
    verbose: bool = False
) -> None:
    """
    Main function to set up Azure AI Search indexers for automatic Cosmos DB sync.
    
    Args:
        reset: Whether to reset existing indexers
        verbose: Enable verbose logging
    """
    manager = AzureIndexerManager()
    manager.setup_indexers(reset=reset, verbose=verbose)

