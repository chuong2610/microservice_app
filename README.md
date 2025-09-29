# Microservice Application

A modern, scalable microservice architecture built with FastAPI, featuring comprehensive user management, content management, e-commerce capabilities, and intelligent search functionality.

## 🏗️ Architecture Overview

This project demonstrates a production-ready microservice architecture with clean separation of concerns, implementing modern software engineering practices and cloud-native technologies.

### Core Principles

- **Microservice Architecture**: Independent, loosely-coupled services
- **API-First Design**: RESTful APIs with comprehensive documentation
- **Cloud-Native**: Built for scalability and cloud deployment
- **Security-First**: JWT-based authentication with proper token management
- **Performance Optimized**: Redis caching and efficient data access patterns
- **Developer Experience**: Comprehensive documentation and easy local development

## 🚀 Services Overview

### 🌐 API Gateway (Port 8000)
**Kong-based API Gateway** - Central entry point for all microservices
- Request routing and load balancing
- Rate limiting and authentication
- Service discovery and health monitoring
- CORS and security policy enforcement

### 🔐 Authentication Service (Port 8002)
**JWT-based Authentication System**
- User registration and login
- Access and refresh token management
- Password security with BCrypt hashing
- Redis-based session management
- Token validation for other services

### 👥 User Service (Port 8000)
**User Profile Management**
- Complete user CRUD operations
- Profile management and updates
- Role-based access control
- Soft delete capabilities
- Email-based user lookup

### 📦 Core Service (Port 8001)
**Content and Item Management**
- Item lifecycle management (CRUD)
- Category and author-based filtering
- Pagination and search capabilities
- Redis caching for performance
- Comprehensive content validation

### 🛒 E-commerce Service (Port 8004)
**E-commerce Operations** *(Development Ready)*
- Shopping cart management
- Order processing and tracking
- Review and rating system
- Payment gateway integration ready
- Inventory management capabilities

### 🔍 Search Service (Port 8003)
**Intelligent Search System**
- Semantic search with AI integration
- Multi-target search (items, authors, content)
- Hybrid search algorithms (BM25, Vector, Semantic)
- Configurable relevance scoring
- Multiple LLM provider support (OpenAI, Azure OpenAI, Ollama)

## 🏃‍♂️ Quick Start

### Prerequisites
- Python 3.12+
- Docker & Docker Compose
- Redis server
- Azure Cosmos DB account (or local emulator)

### Local Development

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd microservice-app
   ```

2. **Set up environment variables**
   ```bash
   # Copy environment templates for each service
   cp authentication/env_exemple authentication/.env
   cp core/.env.example core/.env
   # Configure your database and API keys
   ```

3. **Start the API Gateway**
   ```bash
   cd api_gateway
   docker-compose up -d
   ```

4. **Run individual services**
   ```bash
   # Authentication Service
   cd authentication
   pip install -r requirements.txt
   uvicorn main:app --reload --port 8002

   # Core Service
   cd core
   pip install -r requirements.txt
   uvicorn main:app --reload --port 8001

   # Add other services as needed...
   ```
---


