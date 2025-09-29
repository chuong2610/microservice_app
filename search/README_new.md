# Search Service

A microservice for semantic search of items and authors in the microservice architecture.

## Features

- **Semantic Search**: AI-powered semantic search capabilities
- **Multi-target Search**: Search across items and authors
- **Hybrid Search**: Combines semantic, BM25, and vector search
- **Configurable Scoring**: Weighted scoring system
- **Pagination Support**: Configurable result pagination
- **Azure Search Integration**: Powered by Azure Cognitive Search
- **LLM Integration**: Support for multiple LLM providers (OpenAI, Azure OpenAI, Ollama)

## API Endpoints

### Search
- `GET /api/v1/search` - Search across all content (items + authors)
- `GET /api/v1/search/items` - Search items only
- `GET /api/v1/search/authors` - Search authors only
- `GET /health` - Service health check

### Query Parameters
- `q` (required): Search query string
- `k` (optional): Number of results to return (default: 10, max: 100)
- `page_index` (optional): Page index for pagination
- `page_size` (optional): Page size for pagination
- `app_id` (optional): Application identifier

## Search Features

### Supported Search Types
- **Semantic Search**: Understanding context and meaning
- **BM25 Search**: Traditional keyword-based search
- **Vector Search**: Embedding-based similarity search
- **Business Logic**: Custom scoring based on freshness and relevance

### Scoring Weights
Configurable weights for different search components:
- Semantic search weight
- BM25 search weight  
- Vector search weight
- Business logic weight

## Environment Variables

Required environment variables:

```
# Azure Search Configuration
AZURE_SEARCH_ENDPOINT=your_search_endpoint
AZURE_SEARCH_KEY=your_search_key
SEARCH_ITEM_INDEX_NAME=items-index
SEARCH_AUTHOR_INDEX_NAME=authors-index

# LLM Provider Configuration
LLM_PROVIDER=openai  # or azure_openai, ollama

# OpenAI Configuration (if using OpenAI)
OPENAI_API_KEY=your_openai_key
OPENAI_CHAT_MODEL=gpt-3.5-turbo
OPENAI_EMBED_MODEL=text-embedding-ada-002

# Azure OpenAI Configuration (if using Azure OpenAI)
AZURE_OPENAI_API_KEY=your_azure_openai_key
AZURE_OPENAI_ENDPOINT=your_azure_openai_endpoint
AZURE_OPENAI_API_VERSION=2023-05-15
AZURE_OPENAI_CHAT_MODEL=gpt-35-turbo
AZURE_OPENAI_EMBED_MODEL=text-embedding-ada-002

# Ollama Configuration (if using Ollama)
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_CHAT_MODEL=llama2
OLLAMA_EMBED_MODEL=llama2

# Search Weights
WEIGHT_SEMANTIC=0.3
WEIGHT_BM25=0.3
WEIGHT_VECTOR=0.2
WEIGHT_BUSINESS=0.2

AUTHORS_WEIGHT_SEMANTIC=0.4
AUTHORS_WEIGHT_BM25=0.3
AUTHORS_WEIGHT_VECTOR=0.2
AUTHORS_WEIGHT_BUSINESS=0.1

# Freshness Configuration
FRESHNESS_HALFLIFE_DAYS=30
FRESHNESS_WINDOW_DAYS=90
```

## Running the Service

### Local Development
```bash
pip install -r requirements.txt
uvicorn main:app --reload --port 8003
```

## Architecture

- **FastAPI**: Web framework
- **Azure Cognitive Search**: Search backend
- **LLM Integration**: Multiple AI provider support
- **Hybrid Search**: Multiple search algorithms
- **Configurable Scoring**: Flexible relevance tuning

## Port

This service runs on port **8003** by default.

## Testing

Use the CLI tool for testing search functionality:
```bash
python cli.py --query "your search term"
```
