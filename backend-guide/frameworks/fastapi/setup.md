# FastAPI Setup Guide

This guide walks you through setting up a FastAPI backend for SmartHealthQuote.

## 📋 Prerequisites

- Python 3.8+ installed
- Node.js (for frontend integration testing)
- Git (for version control)
- Basic understanding of Python and REST APIs

## 🚀 Step 1: Project Setup

### Create Project Directory
```bash
mkdir smarthealth-backend
cd smarthealth-backend
```

### Create Virtual Environment
```bash
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### Create Requirements File
Create `requirements.txt`:

```txt
# Core FastAPI
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
pydantic-settings==2.1.0

# Database
sqlalchemy==2.0.23
sqlite3  # Built into Python
psycopg2-binary==2.9.9  # For PostgreSQL in production

# LLM and AI
openai==1.3.9
anthropic==0.7.8
transformers==4.36.2
torch==2.1.2
sentence-transformers==2.2.2

# Vector Database
faiss-cpu==1.7.4
# pinecone-client==2.2.4  # Uncomment if using Pinecone

# Utilities
python-multipart==0.0.6
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-dotenv==1.0.0
httpx==0.25.2

# Development
pytest==7.4.3
pytest-asyncio==0.21.1
black==23.11.0
flake8==6.1.0
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

## 🏗️ Step 2: Project Structure

Create the directory structure:

```bash
mkdir -p app/{api,core,services,models,data}
mkdir tests

# Create __init__.py files
touch app/__init__.py
touch app/api/__init__.py
touch app/core/__init__.py
touch app/services/__init__.py
touch app/models/__init__.py
```

## ⚙️ Step 3: Configuration

### Create Environment Configuration

Create `app/core/config.py`:

```python
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # App settings
    app_name: str = "SmartHealthQuote API"
    debug: bool = False
    version: str = "1.0.0"
    
    # API settings
    api_prefix: str = "/api"
    cors_origins: list = ["http://localhost:3000"]  # React dev server
    
    # Database
    database_url: str = "sqlite:///./smarthealth.db"
    
    # LLM settings
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    
    # Vector DB settings
    vector_db_type: str = "faiss"  # faiss, pinecone, weaviate
    pinecone_api_key: Optional[str] = None
    pinecone_environment: Optional[str] = None
    
    # Security
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    class Config:
        env_file = ".env"

settings = Settings()
```

### Create Environment File

Create `.env` file:

```env
# Development settings
DEBUG=true
CORS_ORIGINS=["http://localhost:3000"]

# LLM API Keys (add your keys here)
OPENAI_API_KEY=sk-your-openai-key-here
ANTHROPIC_API_KEY=your-anthropic-key-here

# Vector Database
VECTOR_DB_TYPE=faiss
# PINECONE_API_KEY=your-pinecone-key
# PINECONE_ENVIRONMENT=your-pinecone-env

# Security (generate a secure key for production)
SECRET_KEY=your-super-secret-key-change-in-production
```

## 🗄️ Step 4: Basic FastAPI App

### Create Main Application

Create `main.py`:

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.routes import router

# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    description="AI-powered health insurance quote system",
    version=settings.version,
    debug=settings.debug
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router, prefix=settings.api_prefix)

@app.get("/")
async def root():
    return {
        "message": "SmartHealthQuote API is running!",
        "version": settings.version,
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "smarthealth-api"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### Create API Models

Create `app/api/models.py`:

```python
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

class UserInput(BaseModel):
    """User input for insurance quote"""
    age: int = Field(..., ge=18, le=100, description="User's age")
    medical_history: str = Field(..., description="Medical history description")
    lifestyle: str = Field(..., description="Lifestyle description")
    coverage_need: str = Field(..., description="Desired coverage type")

class InsurancePlan(BaseModel):
    """Insurance plan details"""
    plan_id: str
    name: str
    provider: str
    monthly_premium: float
    annual_deductible: float
    out_of_pocket_max: float
    coverage_type: str
    network_type: str = "PPO"
    prescription_coverage: str = "Tier 1-3"

class QuoteResponse(BaseModel):
    """Quote response model"""
    quote_id: str
    plan: InsurancePlan
    benefits: List[str]
    recommendations: List[str]
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    generated_at: datetime

class Provider(BaseModel):
    """Insurance provider information"""
    provider_id: str
    name: str
    description: str
    logo_url: Optional[str] = None
    rating: float = Field(..., ge=0.0, le=5.0)
    website: Optional[str] = None

class ChatMessage(BaseModel):
    """Chat message model"""
    message: str
    context: Optional[Dict[str, Any]] = None

class ChatResponse(BaseModel):
    """Chat response model"""
    response: str
    suggestions: List[str] = []
    next_step: Optional[str] = None
```

### Create API Routes

Create `app/api/routes.py`:

```python
from fastapi import APIRouter, HTTPException, Depends
from typing import List
import uuid
from datetime import datetime

from .models import (
    UserInput, QuoteResponse, Provider, 
    ChatMessage, ChatResponse, InsurancePlan
)
from app.services.quote_service import QuoteService
from app.services.llm_service import LLMService

router = APIRouter()

# Initialize services
quote_service = QuoteService()
llm_service = LLMService()

@router.post("/quote", response_model=QuoteResponse)
async def generate_quote(user_input: UserInput):
    """Generate insurance quote based on user input"""
    try:
        # Generate quote using the quote service
        quote = await quote_service.generate_quote(user_input)
        return quote
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating quote: {str(e)}")

@router.get("/providers", response_model=List[Provider])
async def get_providers():
    """Get list of insurance providers"""
    try:
        providers = await quote_service.get_providers()
        return providers
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching providers: {str(e)}")

@router.post("/chat", response_model=ChatResponse)
async def chat_interaction(message: ChatMessage):
    """Handle chat interactions"""
    try:
        response = await llm_service.process_chat_message(message.message, message.context)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat error: {str(e)}")

@router.get("/plans", response_model=List[InsurancePlan])
async def get_available_plans(
    coverage_type: str = None,
    max_premium: float = None
):
    """Get available insurance plans with optional filters"""
    try:
        plans = await quote_service.get_plans(coverage_type, max_premium)
        return plans
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching plans: {str(e)}")
```

## 🧪 Step 5: Test Basic Setup

### Run the Server
```bash
uvicorn main:app --reload
```

### Test the API
1. Visit `http://localhost:8000` - Should show welcome message
2. Visit `http://localhost:8000/docs` - Interactive API documentation
3. Visit `http://localhost:8000/health` - Health check endpoint

### Test with curl
```bash
# Health check
curl http://localhost:8000/health

# Test quote endpoint (will fail until services are implemented)
curl -X POST "http://localhost:8000/api/quote" \
     -H "Content-Type: application/json" \
     -d '{
       "age": 35,
       "medical_history": "No pre-existing conditions", 
       "lifestyle": "Moderately active",
       "coverage_need": "Comprehensive coverage"
     }'
```

## ✅ Step 6: Verify Setup

You should now have:
- ✅ FastAPI server running on port 8000
- ✅ Interactive API docs at `/docs`
- ✅ CORS configured for React frontend
- ✅ Basic project structure
- ✅ Configuration management
- ✅ API routes defined (need implementation)

## 🎯 Next Steps

1. **Implement Services**: Follow the [LLM Integration Guide](llm-integration.md)
2. **Add Database**: Set up data models and storage
3. **Test Integration**: Connect with your React frontend
4. **Add Authentication**: Implement user management
5. **Deploy**: Prepare for production deployment

The foundation is ready! Next, implement the core services to make your API functional.

## 🆘 Troubleshooting

### Common Issues

**Import Errors**: Make sure virtual environment is activated
```bash
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

**Port Conflicts**: Change port if 8000 is in use
```bash
uvicorn main:app --reload --port 8001
```

**CORS Issues**: Verify React app URL in settings.cors_origins

**Dependencies**: Reinstall if needed
```bash
pip install -r requirements.txt --force-reinstall
```