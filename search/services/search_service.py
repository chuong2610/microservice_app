"""
Search Service for Azure AI Search Integration

This module implements a high-level search service that combines multiple scoring methods 
for both items and authors:

Items search combines:
 - Semantic search (natural language understanding)
 - BM25 (keyword matching)
 - Vector search (embedding similarity)
 - Business logic (freshness boost)

Authors search combines:
 - Semantic search (natural language understanding)
 - BM25 (keyword matching)
 - Optional vector/business components if weights > 0

The service handles pagination, error recovery, and score fusion with configurable weights.
"""

import json
import asyncio
import unicodedata
import re
import math
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, Any, List, Optional, Tuple
from difflib import SequenceMatcher
from azure.search.documents import SearchClient
from azure.search.documents.models import VectorizedQuery
from azure.core.exceptions import HttpResponseError

from services.llm_service import build_default_service
from search.scoring import fuse_items, fuse_authors, business_freshness
from search.fuzzy_matching import fuzzy_match_authors
from services.prompts import prompts

SCORE_THRESHOLD = 0.1

class SearchService:
    def __init__(self, items_sc: SearchClient, authors_sc: SearchClient):
        print("🔧 Initializing SearchService...")

        # Azure Search clients are required
        if not items_sc or not authors_sc:
            raise ValueError("Both items_sc and authors_sc SearchClient instances are required")

        # Simplified: single items client (no chunks)
        self.items = items_sc
        self.authors = authors_sc
        self.azure_search_available = True
        print("✅ Azure Search clients initialized")
        
        # Initialize LLM service for query enhancement and answer generation
        try:
            self.llm_service = build_default_service()
            print("✅ LLM service initialized")
        except Exception as e:
            print(f"⚠️ LLM service not available: {e}")
            self.llm_service = None
        
        # Check semantic search capability
        self.semantic_enabled = self._test_semantic_search()
        
        if self.semantic_enabled:
            print("✅ Semantic search is available")
        else:
            print("⚠️ Semantic search is not available")

        print("✅ SearchService initialized successfully")

        # Thread pool for parallel operations (allow some concurrency for overlapping IO)
        self.executor = ThreadPoolExecutor(max_workers=4)
   
    def search(self, query: str, k: int = 10, page_index: Optional[int] = None, page_size: Optional[int] = None, app_id: str = None) -> Dict[str, Any]:
        """General search function that normalizes query and searches both items and authors."""
        print(f"🔍 General search initiated: '{query}'")
        
        # Step 1: Normalize the query using LLM (if query is 5+ words)
        plan = None
        normalized_query = query
        if self.llm_service and len(query.split()) >= 5:
            try:
                system_prompt = prompts.SYSTEM_PROMPT_PLANNING_SIMPLE
                user_prompt = prompts.USER_PROMPT_PLANNING_SIMPLE.format(user_query=query)
                plan = self.llm_service.chat(system_prompt, user_prompt)
                plan = json.loads(plan)

                normalized_query = plan.get("normalized_query", query)
                print(f"✅ Query normalized: '{query}' -> '{normalized_query}'")
            except Exception as e:
                print(f"⚠️ LLM normalization failed: {e}, using original query")
                normalized_query = query
        else:
            if not self.llm_service:
                print("⚠️ LLM service not available, using original query")
            else:
                print(f"📝 Query too short ({len(query.split())} words), keeping original")

            plan = {
                "normalized_query": query,
                "search_parameters": {}
            }
        
        # Step 2: Search both items and authors
        print("🔍 Searching both items and authors...")
        print(f"Plan: {plan}")
        
        # Search items
        try:
            items_result = self._search_items_planned(query, plan, k, page_index, page_size, app_id)
        except Exception as e:
            print(f"❌ Items search failed: {e}")
            items_result = {"results": [], "normalized_query": normalized_query, "pagination": None, "search_type": "items"}
        
        # Search authors
        try:
            authors_result = self._search_authors_planned(query, plan, k, page_index, page_size, app_id)
        except Exception as e:
            print(f"❌ Authors search failed: {e}")
            authors_result = {"results": [], "normalized_query": normalized_query, "pagination": None, "search_type": "authors"}
        
        # Step 3: Return combined results
        print(f"✅ General search completed: {len(items_result.get('results', []))} items, {len(authors_result.get('results', []))} authors")
        
        return {
            "item": items_result,
            "author": authors_result
        }
        
    def search_items(self, query: str, k: int = 10, page_index: Optional[int] = None, page_size: Optional[int] = None, app_id: str = None) -> Dict[str, Any]:
        """
        Search for items using LLM planning for query enhancement.
        """
        print(f"📖 Items search: '{query}'")
        
        normalized_query = query
        plan = None  # Initialize plan variable
        
        if self.llm_service and len(query.split()) >= 5:
            try:
                system_prompt = prompts.SYSTEM_PROMPT_PLANNING_SIMPLE
                user_prompt = prompts.USER_PROMPT_PLANNING_SIMPLE.format(user_query=query)
                plan_response = self.llm_service.chat(system_prompt, user_prompt)
                plan = json.loads(plan_response)
                
                normalized_query = plan.get("normalized_query", query)
                print(f"✅ Query normalized: '{query}' -> '{normalized_query}'")
            except Exception as e:
                print(f"⚠️ LLM normalization failed: {e}, using original query")
                plan = None
        else:
            if not self.llm_service:
                print("⚠️ LLM service not available, using original query")
            else:
                print(f"📝 Query too short ({len(query.split())} words), keeping original")

        # Use the planned search function
        return self._search_items_planned(query, plan, k, page_index, page_size, app_id)

    def search_authors(self, query: str, k: int = 10, page_index: Optional[int] = None, page_size: Optional[int] = None, app_id: str = None) -> Dict[str, Any]:
        """
        Search for authors using LLM planning for query enhancement.
        """
        print(f"👤 Authors search: '{query}'")
        
        normalized_query = query
        plan = None  # Initialize plan variable
        
        if self.llm_service and len(query.split()) >= 5:
            try:
                system_prompt = prompts.SYSTEM_PROMPT_PLANNING_SIMPLE
                user_prompt = prompts.USER_PROMPT_PLANNING_SIMPLE.format(user_query=query)
                plan_response = self.llm_service.chat(system_prompt, user_prompt)
                plan = json.loads(plan_response)
                
                normalized_query = plan.get("normalized_query", query)
                print(f"✅ Query normalized: '{query}' -> '{normalized_query}'")
            except Exception as e:
                print(f"⚠️ LLM normalization failed: {e}, using original query")
                plan = None
        else:
            if not self.llm_service:
                print("⚠️ LLM service not available, using original query")
            else:
                print(f"📝 Query too short ({len(query.split())} words), keeping original")

        # Use the planned search function
        return self._search_authors_planned(query, plan, k, page_index, page_size, app_id)
    
    def _test_semantic_search(self) -> bool:
        """Test if semantic search is available on this service."""
        try:
            # Try a simple semantic search to test capability
            test_result = self.items.search(
                search_text="test",
                query_type="semantic",
                semantic_configuration_name="items-semantic",
                top=1
            )
            # The SDK returns a pageable object without performing the request until iterated.
            # Force iteration (or a single next()) so any HttpResponseError is raised here.
            try:
                next(iter(test_result))
                # If iteration succeeded (even with zero results), semantic queries are supported
                return True
            except StopIteration:
                # No results in the index but the semantic query executed successfully
                return True
        except HttpResponseError as e:
            if "SemanticQueriesNotAvailable" in str(e) or "FeatureNotSupportedInService" in str(e):
                return False
            # Re-raise other errors as they're unexpected
            raise
        except Exception:
            # For any other errors, assume semantic search is not available
            return False
    
    def _apply_score_threshold(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Apply score threshold filtering to search results.
        """
        original_count = len(results)
        filtered_results = [r for r in results if r.get("_final", 0.0) >= SCORE_THRESHOLD]
        filtered_count = len(filtered_results)
        
        if filtered_count < original_count:
            print(f"🎯 Score threshold filtering: {original_count} → {filtered_count} results (threshold: {SCORE_THRESHOLD})")
        
        return filtered_results
    
    def _batch_get_documents(self, client: SearchClient, document_ids: List[str], app_id: str = None) -> Dict[str, Dict[str, Any]]:
        """
        Batch retrieve documents by IDs to avoid N+1 query problem.
        """
        if not document_ids:
            return {}
        
        print(f"📦 Batch retrieving {len(document_ids)} documents")
        
        try:
            # Use search with ID filter to batch retrieve documents
            id_filter = " or ".join([f"id eq '{doc_id}'" for doc_id in document_ids])
            
            # Apply app_id filter
            app_filter = f"app_id eq '{app_id}'"    
            final_filter = f"{id_filter} and {app_filter}"
            
            results = client.search(
                search_text="*",
                filter=final_filter,
                top=len(document_ids),
                select=["*"]  # Get all fields
            )
            
            # Convert to dict for fast lookup
            doc_dict = {doc["id"]: doc for doc in results}
            print(f"✅ Successfully retrieved {len(doc_dict)} documents")
            return doc_dict
            
        except Exception as e:
            print(f"⚠️ Batch document retrieval failed: {e}")
            # Fallback to individual retrieval
            doc_dict = {}
            for doc_id in document_ids:
                try:
                    doc_dict[doc_id] = client.get_document(doc_id)
                except Exception as individual_error:
                    print(f"⚠️ Failed to retrieve document {doc_id}: {individual_error}")
            return doc_dict

    def _search_authors_planned(self, original_query: str, plan: Optional[Dict[str, Any]], k: int = 10, page_index: Optional[int] = None, page_size: Optional[int] = None, app_id: str = None) -> Dict[str, Any]:
        """
        Internal authors search function that uses pre-planned query data.
        """
        # Handle case where plan is None (LLM not available or query too short)
        if plan is None:
            normalized_query = original_query
        else:
            normalized_query = plan["normalized_query"]
        
        # Handle pagination parameters
        if page_index is not None and page_size is not None:
            # For pagination consistency, always fetch the same amount of results
            # then apply pagination in-memory to ensure consistent total counts
            offset = page_index * page_size
            total_needed = offset + page_size
            # Use consistent search_k to ensure we get all relevant results
            search_k = max(k * 4, 100)  # Fetch enough for consistent pagination
            print(f"👤 Starting planned authors search: query='{normalized_query}', page_index={page_index}, page_size={page_size}, search_k={search_k}")
        else:
            search_k = k
            offset = 0
            print(f"👤 Starting planned authors search: query='{normalized_query}', k={k}")
        
        try:
            # Get all authors and perform fuzzy matching (as per established approach)
            print("🔍 Getting all authors from index for fuzzy matching...")
            all_authors = self._get_all_authors(app_id)
            print(f"📋 Retrieved {len(all_authors)} authors from index")
            
            # Perform fuzzy matching using advanced algorithm
            print(f"🔍 Performing advanced fuzzy matching for query: '{normalized_query}'")
            fuzzy_matches = fuzzy_match_authors(normalized_query, all_authors, search_k)
            
            # Convert fuzzy matches to the expected format for fuse_authors
            rows: List[Dict[str, Any]] = []
            for i, (author_doc, score) in enumerate(fuzzy_matches):
                rows.append({
                    "id": author_doc["id"], 
                    "doc": author_doc,
                    "_bm25": score,  # Use fuzzy match score as BM25 score
                    "_semantic": 0.0, 
                    "_vector": 0.0, 
                    "_business": 0.0
                })
            
            print(f"✅ Fuzzy matching returned {len(rows)} results")
            
            # Fuse results
            print("⚖️ Fusing author scores...")
            all_fused_results = fuse_authors(rows)
            
            # Apply score threshold filtering
            all_fused_results = self._apply_score_threshold(all_fused_results)
            total_results = len(all_fused_results)
            
            # Apply pagination if requested
            if page_index is not None and page_size is not None:
                start_idx = offset
                end_idx = start_idx + page_size
                paginated_results = all_fused_results[start_idx:end_idx]
                
                print(f"✅ Authors search completed: {len(paginated_results)} results (page {page_index + 1}, total: {total_results})")
                
                return {
                    "results": paginated_results,
                    "normalized_query": normalized_query,
                    "pagination": {
                        "page_index": page_index,
                        "page_size": page_size,
                        "total_results": total_results,
                        "total_pages": (total_results + page_size - 1) // page_size,
                        "has_next": end_idx < total_results,
                        "has_previous": page_index > 0
                    },
                    "search_type": "authors"
                }
            else:
                final_results = all_fused_results[:k]
                print(f"✅ Authors search completed: {len(final_results)} final results")
                
                return {
                    "results": final_results,
                    "normalized_query": normalized_query,
                    "pagination": None,
                    "search_type": "authors"
                }
                
        except Exception as e:
            print(f"❌ Authors search failed: {e}")
            raise
    
    def _search_items_planned(self, original_query: str, plan: Optional[Dict[str, Any]], k: int = 10, page_index: Optional[int] = None, page_size: Optional[int] = None, app_id: str = None) -> Dict[str, Any]:
        """
        Internal items search function that uses pre-planned query data.
        """
        # Handle case where plan is None (LLM not available or query too short)
        if plan is None:
            normalized_query = original_query
            search_params = {
                "semantic_weight": 0.3,
                "bm25_weight": 0.4,
                "vector_weight": 0.2,
                "business_weight": 0.1
            }
        else:
            normalized_query = plan["normalized_query"]
            search_params = plan["search_parameters"]
        
        # Handle pagination parameters
        if page_index is not None and page_size is not None:
            # For pagination consistency, always fetch the same large amount of results
            # then apply pagination in-memory to ensure consistent total counts
            offset = page_index * page_size
            total_needed = offset + page_size
            # Use a consistent large search_k to ensure we get all relevant results
            # This prevents inconsistent total counts across pages
            search_k = max(k * 4, 200)  # Fetch enough for consistent pagination
            print(f"📖 Starting planned items search: query='{normalized_query}', page_index={page_index}, page_size={page_size}, search_k={search_k}")
        else:
            search_k = k
            offset = 0
            print(f"📖 Starting planned items search: query='{normalized_query}', k={k}")
        
        # Continue with existing search logic but without normalization step
        try:
            # Run text (BM25/semantic) and vector (chunk) searches concurrently using the thread pool
            # A) Text search with semantic reranker if available
            def run_text_search():
                search_kwargs = {
                    "search_text": normalized_query,
                    "query_type": "semantic",
                    "top": int(search_k*1.1),
                    "select": ["id","title","abstract","updated_at"]
                }
                if self.semantic_enabled:
                    print("🔍 Executing semantic+BM25 search for items...")
                    try:
                        search_kwargs_temp = search_kwargs.copy()
                        # Apply app_id filter
                        search_kwargs_temp["semantic_configuration_name"] = "items-semantic"
                        search_kwargs_temp["filter"] = f"app_id eq '{app_id}'" if app_id else None
                        search_kwargs_temp["highlight_fields"] = search_params.get("highlight_fields", "abstract")

                        print(f"Search params: {search_kwargs_temp}")

                        text_res_local = self.items.search(**search_kwargs_temp)
                    except HttpResponseError as he:
                        # Service doesn't actually support semantic at runtime - fallback
                        if "SemanticQueriesNotAvailable" in str(he) or "FeatureNotSupportedInService" in str(he):
                            print("⚠️ Semantic search rejected by service at runtime - falling back to BM25")
                            self.semantic_enabled = False
                            
                            search_kwargs_temp = search_kwargs.copy()
                            search_kwargs_temp["query_type"] = "simple"
                            search_kwargs_temp["highlight_fields"] = "abstract"
                            search_kwargs_temp["filter"] = f"app_id eq '{app_id}'" if app_id else None

                            print(f"Search params: {search_kwargs_temp}")

                            text_res_local = self.items.search(**search_kwargs_temp)

                        else:
                            raise
                else:
                    print("🔍 Executing BM25-only search for items (semantic not available)...")
                    # Apply enhanced search parameters
                    search_kwargs_temp = search_kwargs.copy()
                    search_kwargs_temp["query_type"] = "simple"
                    search_kwargs_temp["highlight_fields"] = "abstract"
                    search_kwargs_temp["filter"] = f"app_id eq '{app_id}'" if app_id else None

                    print(f"Search params: {search_kwargs_temp}")

                    text_res_local = self.items.search(**search_kwargs_temp)
                
                rows_local: List[Dict[str, Any]] = []
                text_count_local = 0
                
                for d in text_res_local:
                    text_count_local += 1
                    rows_local.append({
                        "id": d["id"],
                        "doc": d,
                        "_bm25": d["@search.score"],
                        "_semantic": d.get("@search.rerankerScore", 0.0),
                        "_vector": 0.0,
                        "_business": business_freshness(d.get("updated_at")),
                    })
                print(f"✅ Text search returned {text_count_local} results")
                return rows_local, text_count_local

            # B) Vector Search for Abstract 
            def run_vector_search():
                print("🧮 Generating query embedding for abstract vector search...")
                qvec = self.llm_service.embed([ normalized_query ])[0]
                print(f"✅ Generated embedding vector (dim={len(qvec)})")
                print("🔍 Executing vector search for items using abstract_vector...")

                vector_search_kwargs = {
                    "search_text": None,
                    "vector_queries": [VectorizedQuery(vector=qvec, fields="abstract_vector")],
                    "top": int(search_k * 1.2),
                    "select": ["id", "title", "abstract", "updated_at"]
                }

                # Apply app_id filter
                vector_search_kwargs["filter"] = f"app_id eq '{app_id}'" if app_id else None

                print(f"Vector search params: {vector_search_kwargs}")

                return list(self.items.search(**vector_search_kwargs))

            # Submit both tasks to the executor to allow overlap of network I/O
            text_future = self.executor.submit(run_text_search)
            vector_future = self.executor.submit(run_vector_search)

            # Wait for both to complete
            rows, text_count = text_future.result()
            vec_res = vector_future.result()
            
            id_to_row = {r["id"]: r for r in rows}
            vec_count = len(vec_res)    
            
            # vec_res are item documents directly from abstract vector search
            for d in vec_res:
                try:
                    item_id = d.get("id")
                    if not item_id:
                        continue
                    score = d.get("@search.score", 0.0)

                    if item_id in id_to_row:
                        # Merge vector score with existing text search result
                        id_to_row[item_id]["_vector"] = score
                    else:
                        # New result from vector search only
                        id_to_row[item_id] = {
                            "id": item_id,
                            "doc": d,
                            "_bm25": 0.0,
                            "_semantic": 0.0,
                            "_vector": score,
                            "_business": 0.0,
                        }
                except Exception:
                    continue

            print(f"✅ Vector search returned {vec_count} item results")

            # Batch retrieve item docs for any ids missing the doc payload
            missing_item_ids = [aid for aid, row in id_to_row.items() if row.get("doc") is None]
            if missing_item_ids:
                print(f"📦 Fetching {len(missing_item_ids)} item documents")
                batch_items = self._batch_get_documents(self.items, missing_item_ids, app_id)
                for aid in missing_item_ids:
                    if aid in batch_items:
                        item_doc = batch_items[aid]
                        id_to_row[aid]["doc"] = item_doc
                        id_to_row[aid]["_business"] = business_freshness(item_doc.get("updated_at"))

            print("⚖️ Fusing item scores...")
            all_fused_results = fuse_items(list(id_to_row.values()))
            
            # Apply score threshold filtering
            all_fused_results = self._apply_score_threshold(all_fused_results)
            
            # Apply pagination if requested
            if page_index is not None and page_size is not None:
                total_results = len(all_fused_results)
                start_idx = offset
                end_idx = start_idx + page_size
                paginated_results = all_fused_results[start_idx:end_idx]
                
                print(f"✅ Items search completed: {len(paginated_results)} results (page {page_index + 1}, total: {total_results})")
                
                return {
                    "results": paginated_results,
                    "normalized_query": normalized_query,
                    "pagination": {
                        "page_index": page_index,
                        "page_size": page_size,
                        "total_results": total_results,
                        "total_pages": (total_results + page_size - 1) // page_size,
                        "has_next": end_idx < total_results,
                        "has_previous": page_index > 0
                    },
                    "search_type": "items"
                }
            else:
                final_results = all_fused_results[:k]
                print(f"✅ Items search completed: {len(final_results)} final results")
                
                return {
                    "results": final_results,
                    "normalized_query": normalized_query,
                    "pagination": None,
                    "search_type": "items"
                }
                
        except Exception as e:
            print(f"❌ Items search failed: {e}")
            raise

    def _get_all_authors(self, app_id: str = None) -> List[Dict[str, Any]]:
        """
        Get all authors from the index for fuzzy matching.
        """
        try:
            # Use wildcard search to get all authors
            search_kwargs = {
                "search_text": "*",
                "query_type": "simple",
                # top=10000,  # Large number to get all authors
                "select": ["id", "full_name"]
            }
            
            # Apply app_id filter
            search_kwargs["filter"] = f"app_id eq '{app_id}'" if app_id else None
            
            all_results = self.authors.search(**search_kwargs)
            
            authors = []
            for doc in all_results:
                authors.append(doc)
            
            return authors
            
        except Exception as e:
            print(f"❌ Failed to retrieve all authors: {e}")
            return []
    


