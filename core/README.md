# Core: Azure AI Search – Indexes and Indexers

This module lets you create/update Azure AI Search indexes and indexers, and run/check them via a small CLI.

## Prerequisites
- Python 3.12 (already bundled in `myenv`)
- Azure resources and keys available in a `.env` file at the project root:
  - `AZURE_SEARCH_ENDPOINT`
  - `AZURE_SEARCH_KEY`
  - `COSMOS_ENDPOINT`, `COSMOS_KEY`, `COSMOS_DB_NAME`, `COSMOS_CONTAINER_ITEMS`, `COSMOS_CONTAINER_USERS`
  - `AZURE_OPENAI_ENDPOINT`, `AZURE_OPENAI_API_KEY`, `AZURE_OPENAI_EMBED_MODEL`
  - `EMBED_MODEL_DIMENSION` (e.g., `1536`)
  - `FRESHNESS_WINDOW_DAYS` (e.g., `30`)

## Activate virtual environment
```powershell
cd <correct-path>\microservice-app
.\myenv\Scripts\Activate.ps1
```

## Commands
All commands assume you are in the project root with the venv activated.

### Create or update indexes
- Reset (delete first, then create):
```powershell
python -m core.main indexes --reset --verbose
```
- Update/create without deleting:
```powershell
python -m core.main indexes --verbose
```

### Create or update indexers (data sources + skillsets + indexers) and kick off initial runs
- Reset flow:
```powershell
python -m core.main indexers --reset --verbose
```
- No reset:
```powershell
python -m core.main indexers --verbose
```

### Manually run indexers on demand
```powershell
python -m core.main run --verbose
```

### Check indexer status
```powershell
python -m core.main status --verbose
```
