# FastAPI Backend for SmartHealthQuote

This guide helps you build a FastAPI backend with LLM integration and RAG pipeline for the health insurance quote system.

## 🚀 Quick Start

1. **Setup Project**:
   ```bash
   mkdir smarthealth-backend && cd smarthealth-backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Run Development Server**:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

3. **API Documentation**: Visit `http://localhost:8000/docs`

## 📁 Project Structure

```
smarthealth-backend/
├── main.py                 # FastAPI app entry point
├── requirements.txt        # Dependencies
├── app/
│   ├── __init__.py
│   ├── api/               # API routes
│   │   ├── __init__.py
│   │   ├── routes.py      # Main API endpoints
│   │   └── models.py      # Pydantic models
│   ├── core/              # Core functionality
│   │   ├── __init__.py
│   │   ├── config.py      # Configuration
│   │   ├── security.py    # Authentication
│   │   └── database.py    # Database connection
│   ├── services/          # Business logic
│   │   ├── __init__.py
│   │   ├── llm_service.py # LLM integration
│   │   ├── rag_service.py # RAG pipeline
│   │   └── quote_service.py # Quote generation
│   ├── models/            # Database models
│   │   ├── __init__.py
│   │   └── insurance.py   # Insurance data models
│   └── data/              # Sample data
│       ├── policies.json
│       └── providers.json
├── tests/                 # Test files
├── docker-compose.yml     # Local development
└── Dockerfile            # Container definition
```

## ⚡ Key Features

- **🚀 High Performance**: Async/await for concurrent requests
- **📚 Auto Documentation**: Interactive API docs with Swagger UI
- **🔒 Type Safety**: Pydantic models for request/response validation
- **🤖 LLM Integration**: Support for multiple LLM providers
- **🔍 Vector Search**: FAISS/Pinecone integration for RAG
- **🛡️ Security**: JWT authentication, CORS, rate limiting
- **📊 Monitoring**: Request logging and health checks

## 🔧 Configuration

FastAPI offers excellent flexibility for different deployment scenarios:

### Development
- SQLite database
- Local FAISS vector store  
- Debug logging
- Hot reload

### Production
- PostgreSQL database
- Managed vector DB (Pinecone)
- Structured logging
- Performance monitoring

## 📖 Implementation Guide

1. [Setup & Installation](setup.md)
2. [API Design](api-design.md) 
3. [LLM Integration](llm-integration.md)
4. [RAG Pipeline](rag-pipeline.md)
5. [Database Setup](database.md)
6. [Authentication](authentication.md)
7. [Testing](testing.md)
8. [Deployment](deployment.md)

## 🌟 Why FastAPI?

- **Perfect for ML/AI**: Excellent support for data science libraries
- **Production Ready**: Used by companies like Uber, Netflix
- **Great Documentation**: Automatic OpenAPI schema generation
- **Modern Python**: Built on Python 3.6+ with type hints
- **High Performance**: Comparable to Node.js and Go

## 🤝 Integration with React Frontend

Your React app will connect to these endpoints:

```javascript
// In your React app (src/pages/chat.jsx)
const getQuotation = async () => {
  const response = await fetch('http://localhost:8000/api/quote', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(formData)
  });
  return response.json();
};
```

## 🏃‍♂️ Next Steps

1. **Follow the setup guide**: [setup.md](setup.md)
2. **Run the demo**: See working examples in action
3. **Customize**: Adapt the code to your specific needs
4. **Deploy**: Use the deployment guide for production

Ready to build? Start with the [setup guide](setup.md)!