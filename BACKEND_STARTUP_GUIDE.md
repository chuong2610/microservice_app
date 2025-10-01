# Backend Services Startup Guide

## 🚨 Current Issue
The frontend is getting a Cosmos DB error when trying to fetch items. This guide will help you fix the database issues and start all services properly.

## 🔧 Fixes Applied

### 1. **Fixed Cosmos DB Query Syntax**
- ✅ Corrected `OFFSET` and `LIMIT` clause positioning in SQL queries
- ✅ Added null handling for `app_id` parameter
- ✅ Improved error handling and logging

### 2. **Database Configuration**
- ✅ Created `core/env_example` with proper Cosmos DB settings
- ✅ Added database setup script with sample data
- ✅ Enhanced connection error handling

## 🚀 Step-by-Step Startup

### Step 1: Setup Cosmos DB (Local Emulator)

1. **Install Cosmos DB Emulator** (if not already installed):
   - Download from: https://docs.microsoft.com/en-us/azure/cosmos-db/local-emulator
   - Or use Docker: `docker run -p 8081:8081 mcr.microsoft.com/cosmosdb/linux/azure-cosmos-emulator`

2. **Start Cosmos DB Emulator**:
   - Windows: Start from Start Menu
   - Docker: `docker run -p 8081:8081 -e AZURE_COSMOS_EMULATOR_PARTITION_COUNT=10 mcr.microsoft.com/cosmosdb/linux/azure-cosmos-emulator`

3. **Verify Emulator is Running**:
   - Open: https://localhost:8081/_explorer/index.html
   - Accept the SSL certificate if prompted

### Step 2: Configure Environment Files

For each service, create `.env` file from `env_example`:

```bash
# Core Service
cd core
copy env_example .env

# Authentication Service  
cd ../authentication
copy env_exemple .env  # Note: fix the typo in filename if needed

# User Service
cd ../user
copy env_example .env  # Create if doesn't exist

# Search Service
cd ../search  
copy env_example .env  # Create if doesn't exist
```

### Step 3: Setup Database with Sample Data

```bash
cd core
python setup_database.py
```

Expected output:
```
🔧 Setting up Cosmos DB...
✅ Database 'microservicedb' ready
✅ Container 'items' ready
✅ Added sample item: Welcome to Our Blog Platform
✅ Added sample item: Premium Wireless Headphones
🎉 Database setup completed successfully!
✅ Connection successful! Found 2 items
```

### Step 4: Start Kong API Gateway

```bash
cd api_gateway
docker-compose up -d
```

Verify Kong is running:
```bash
curl http://localhost:8001/services
```

### Step 5: Start Backend Services

Open 4 separate terminals and run:

**Terminal 1 - Authentication Service:**
```bash
cd authentication
# Activate virtual environment if needed
# myenv\Scripts\activate  # Windows
# source myenv/bin/activate  # Linux/Mac
uvicorn main:app --host 0.0.0.0 --port 8080 --reload
```

**Terminal 2 - Core Service:**
```bash
cd core  
uvicorn main:app --host 0.0.0.0 --port 8081 --reload
```

**Terminal 3 - Search Service:**
```bash
cd search
uvicorn main:app --host 0.0.0.0 --port 8082 --reload
```

**Terminal 4 - User Service:**
```bash
cd user
uvicorn main:app --host 0.0.0.0 --port 8083 --reload
```

### Step 6: Verify Services

Check each service health:
```bash
curl http://localhost:8000/auth/health
curl http://localhost:8000/items/health  
curl http://localhost:8000/users/health
```

### Step 7: Test Frontend

```bash
cd frontend
npm run start:blog
```

Visit: http://localhost:3000
Click "Test API" button to verify all connections.

## 🐛 Troubleshooting

### Issue: "BadRequest - One of the input values is invalid"
**Solution**: 
1. Ensure Cosmos DB Emulator is running
2. Run the database setup script: `python core/setup_database.py`
3. Check that `.env` files exist with correct Cosmos DB settings

### Issue: Services not starting
**Solution**:
1. Check if ports are available (8080, 8081, 8082, 8083)
2. Activate Python virtual environment
3. Install dependencies: `pip install -r requirements.txt`

### Issue: Kong Gateway not working
**Solution**:
1. Ensure Docker is running
2. Check Kong configuration: `cd api_gateway && docker-compose ps`
3. Restart Kong: `docker-compose down && docker-compose up -d`

### Issue: CORS errors
**Solution**: 
Kong configuration has been updated to include `app_id` header. Restart Kong:
```bash
cd api_gateway
docker-compose down
docker-compose up -d
```

## 📋 Service Ports

| Service | Port | Health Check |
|---------|------|-------------|
| Kong Gateway | 8000 | http://localhost:8001/status |
| Authentication | 8080 | http://localhost:8000/auth/health |
| Core (Items) | 8081 | http://localhost:8000/items/health |
| Search | 8082 | http://localhost:8000/search/health |
| User | 8083 | http://localhost:8000/users/health |
| Frontend | 3000 | http://localhost:3000 |

## ✅ Expected Results

After following this guide:
- ✅ Cosmos DB running with sample data
- ✅ All 4 backend services running
- ✅ Kong Gateway routing requests
- ✅ Frontend can fetch items successfully
- ✅ No more "BadRequest" errors

## 🔄 Quick Restart Command

Create a batch file `start_all.bat` (Windows) or `start_all.sh` (Linux/Mac):

```bash
# start_all.bat
start cmd /k "cd authentication && uvicorn main:app --host 0.0.0.0 --port 8080 --reload"
start cmd /k "cd core && uvicorn main:app --host 0.0.0.0 --port 8081 --reload"  
start cmd /k "cd search && uvicorn main:app --host 0.0.0.0 --port 8082 --reload"
start cmd /k "cd user && uvicorn main:app --host 0.0.0.0 --port 8083 --reload"
```

This will start all services in separate windows.


