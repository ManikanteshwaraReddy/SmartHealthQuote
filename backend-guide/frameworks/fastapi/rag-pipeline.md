# RAG Pipeline Implementation Guide

This guide shows you how to implement a Retrieval-Augmented Generation (RAG) pipeline for intelligent insurance policy matching.

## 🎯 What is RAG?

RAG combines:
- **Retrieval**: Finding relevant insurance policies from a knowledge base
- **Generation**: Using LLM to create personalized quotes based on retrieved data

This ensures your quotes are based on actual policy data, not just LLM hallucinations.

## 🏗️ RAG Architecture

```
User Query → Embeddings → Vector Search → Policy Retrieval → LLM Context → Personalized Quote
```

## 🚀 Implementation Options

### Option 1: FAISS (Local, Fast)
- Best for: Development, small datasets, privacy-focused
- Pros: Fast, local, no API costs
- Cons: Limited scalability, manual management

### Option 2: Pinecone (Managed)
- Best for: Production, large datasets, scaling
- Pros: Managed, scalable, features
- Cons: Cost, external dependency

### Option 3: Weaviate (Open Source)
- Best for: Hybrid search, GraphQL APIs
- Pros: Open source, flexible, hybrid search
- Cons: More complex setup

## 📊 Setup with FAISS (Recommended for Start)

### 1. Install Dependencies
```bash
pip install faiss-cpu sentence-transformers pandas numpy
```

### 2. Create RAG Service

Create `app/services/rag_service.py`:

```python
import faiss
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any, Optional
import json
import os
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class RAGService:
    def __init__(self, index_path: str = "data/faiss_index"):
        self.model_name = "all-MiniLM-L6-v2"  # Good balance of speed/quality
        self.encoder = SentenceTransformer(self.model_name)
        self.index_path = Path(index_path)
        self.index = None
        self.policies_df = None
        self.dimension = 384  # Dimension for all-MiniLM-L6-v2
        
        # Initialize index
        self._initialize_index()
    
    def _initialize_index(self):
        """Initialize FAISS index and load policies"""
        try:
            if self.index_path.exists():
                self._load_existing_index()
            else:
                self._create_new_index()
        except Exception as e:
            logger.error(f"Error initializing RAG index: {e}")
            self._create_empty_index()
    
    def _load_existing_index(self):
        """Load existing FAISS index and metadata"""
        try:
            # Load FAISS index
            self.index = faiss.read_index(str(self.index_path / "index.faiss"))
            
            # Load policy metadata
            policies_path = self.index_path / "policies.json"
            if policies_path.exists():
                with open(policies_path, 'r') as f:
                    policies_data = json.load(f)
                self.policies_df = pd.DataFrame(policies_data)
                logger.info(f"Loaded {len(self.policies_df)} policies from index")
            else:
                logger.warning("Index exists but no policy metadata found")
                self._create_empty_index()
                
        except Exception as e:
            logger.error(f"Error loading existing index: {e}")
            self._create_new_index()
    
    def _create_new_index(self):
        """Create new FAISS index from policy data"""
        try:
            # Load sample policy data
            policies_data = self._load_sample_policies()
            
            if not policies_data:
                logger.warning("No policy data found, creating empty index")
                self._create_empty_index()
                return
            
            # Create DataFrame
            self.policies_df = pd.DataFrame(policies_data)
            
            # Generate embeddings for policies
            policy_texts = self._prepare_policy_texts(self.policies_df)
            embeddings = self.encoder.encode(policy_texts, show_progress_bar=True)
            
            # Create FAISS index
            self.index = faiss.IndexFlatL2(self.dimension)
            self.index.add(embeddings.astype('float32'))
            
            # Save index and metadata
            self._save_index()
            
            logger.info(f"Created new index with {len(policies_data)} policies")
            
        except Exception as e:
            logger.error(f"Error creating new index: {e}")
            self._create_empty_index()
    
    def _create_empty_index(self):
        """Create empty FAISS index"""
        self.index = faiss.IndexFlatL2(self.dimension)
        self.policies_df = pd.DataFrame()
        logger.info("Created empty FAISS index")
    
    def _load_sample_policies(self) -> List[Dict]:
        """Load sample insurance policies"""
        # Try to load from data directory
        data_path = Path("app/data/policies.json")
        if data_path.exists():
            with open(data_path, 'r') as f:
                return json.load(f)
        
        # Return sample data if no file exists
        return self._get_sample_policies()
    
    def _get_sample_policies(self) -> List[Dict]:
        """Generate sample insurance policies for demo"""
        return [
            {
                "policy_id": "basic_001",
                "name": "Basic Health Plan",
                "provider": "HealthCorp",
                "coverage_type": "basic",
                "monthly_premium_base": 200,
                "annual_deductible": 2500,
                "out_of_pocket_max": 7000,
                "network_type": "HMO",
                "description": "Affordable basic health coverage with essential benefits",
                "benefits": [
                    "Primary care visits: $30 copay",
                    "Preventive care: Covered 100%",
                    "Emergency room: $500 copay",
                    "Prescription drugs: Generic $10, Brand $40"
                ],
                "age_range": "18-65",
                "suitable_for": ["young adults", "healthy individuals", "budget-conscious"]
            },
            {
                "policy_id": "comprehensive_001",
                "name": "Comprehensive Health Plus",
                "provider": "HealthCorp",
                "coverage_type": "comprehensive",
                "monthly_premium_base": 350,
                "annual_deductible": 1500,
                "out_of_pocket_max": 5000,
                "network_type": "PPO",
                "description": "Comprehensive health coverage with wide provider network",
                "benefits": [
                    "Primary care visits: $25 copay",
                    "Specialist visits: $50 copay",
                    "Emergency room: $250 copay",
                    "Hospital stay: 20% coinsurance after deductible",
                    "Mental health services: $25 copay",
                    "Prescription drugs: Tier 1-3 coverage"
                ],
                "age_range": "18-65",
                "suitable_for": ["families", "chronic conditions", "comprehensive coverage seekers"]
            },
            {
                "policy_id": "premium_001",
                "name": "Premium Elite Plan",
                "provider": "EliteHealth",
                "coverage_type": "premium",
                "monthly_premium_base": 500,
                "annual_deductible": 500,
                "out_of_pocket_max": 3000,
                "network_type": "PPO",
                "description": "Premium health coverage with minimal out-of-pocket costs",
                "benefits": [
                    "Primary care visits: $15 copay",
                    "Specialist visits: $30 copay",
                    "Emergency room: $150 copay",
                    "Hospital stay: 10% coinsurance after deductible",
                    "Mental health services: $15 copay",
                    "Prescription drugs: $5 generic, $25 brand",
                    "Dental and vision included"
                ],
                "age_range": "25-65",
                "suitable_for": ["high-income", "frequent healthcare users", "premium coverage"]
            },
            {
                "policy_id": "senior_001",
                "name": "Senior Care Plan",
                "provider": "SeniorHealth",
                "coverage_type": "senior",
                "monthly_premium_base": 400,
                "annual_deductible": 1200,
                "out_of_pocket_max": 4500,
                "network_type": "PPO",
                "description": "Specialized health coverage designed for seniors",
                "benefits": [
                    "Primary care visits: $20 copay",
                    "Specialist visits: $40 copay",
                    "Emergency room: $200 copay",
                    "Hospital stay: 15% coinsurance",
                    "Prescription drugs: Enhanced coverage",
                    "Wellness programs included",
                    "Home healthcare coverage"
                ],
                "age_range": "55+",
                "suitable_for": ["seniors", "retirement planning", "age-related conditions"]
            },
            {
                "policy_id": "family_001",
                "name": "Family Care Plan",
                "provider": "FamilyFirst",
                "coverage_type": "family",
                "monthly_premium_base": 450,
                "annual_deductible": 2000,
                "out_of_pocket_max": 6000,
                "network_type": "PPO",
                "description": "Comprehensive family health coverage with pediatric care",
                "benefits": [
                    "Primary care visits: $25 copay",
                    "Pediatric visits: $20 copay",
                    "Specialist visits: $45 copay",
                    "Emergency room: $300 copay",
                    "Maternity care: Covered 100% after deductible",
                    "Child wellness visits: Covered 100%",
                    "Family planning services"
                ],
                "age_range": "All ages",
                "suitable_for": ["families with children", "maternity planning", "pediatric care"]
            }
        ]
    
    def _prepare_policy_texts(self, policies_df: pd.DataFrame) -> List[str]:
        """Prepare policy texts for embedding"""
        texts = []
        for _, policy in policies_df.iterrows():
            # Combine relevant fields into searchable text
            text_parts = [
                f"Policy: {policy['name']}",
                f"Provider: {policy['provider']}",
                f"Coverage: {policy['coverage_type']}",
                f"Network: {policy['network_type']}",
                f"Description: {policy['description']}",
                f"Suitable for: {', '.join(policy.get('suitable_for', []))}",
                f"Benefits: {'; '.join(policy.get('benefits', []))}"
            ]
            texts.append(" | ".join(text_parts))
        return texts
    
    def _save_index(self):
        """Save FAISS index and metadata"""
        try:
            # Create directory if it doesn't exist
            self.index_path.mkdir(parents=True, exist_ok=True)
            
            # Save FAISS index
            faiss.write_index(self.index, str(self.index_path / "index.faiss"))
            
            # Save policy metadata
            policies_data = self.policies_df.to_dict('records')
            with open(self.index_path / "policies.json", 'w') as f:
                json.dump(policies_data, f, indent=2)
            
            logger.info("Index and metadata saved successfully")
            
        except Exception as e:
            logger.error(f"Error saving index: {e}")
    
    async def search_policies(self, user_input, k: int = 3) -> List[Dict]:
        """Search for relevant policies based on user input"""
        try:
            if self.index is None or len(self.policies_df) == 0:
                logger.warning("Index not available, returning sample policies")
                return self._get_sample_policies()[:k]
            
            # Create search query from user input
            query_text = self._create_search_query(user_input)
            
            # Generate query embedding
            query_embedding = self.encoder.encode([query_text])
            
            # Search FAISS index
            distances, indices = self.index.search(
                query_embedding.astype('float32'), k
            )
            
            # Get matching policies
            matching_policies = []
            for i, idx in enumerate(indices[0]):
                if idx < len(self.policies_df):
                    policy = self.policies_df.iloc[idx].to_dict()
                    policy['similarity_score'] = float(1 / (1 + distances[0][i]))  # Convert distance to similarity
                    matching_policies.append(policy)
            
            logger.info(f"Found {len(matching_policies)} matching policies")
            return matching_policies
            
        except Exception as e:
            logger.error(f"Error searching policies: {e}")
            return self._get_sample_policies()[:k]
    
    def _create_search_query(self, user_input) -> str:
        """Create search query from user input"""
        query_parts = [
            f"Age: {user_input.age}",
            f"Medical history: {user_input.medical_history}",
            f"Lifestyle: {user_input.lifestyle}",
            f"Coverage need: {user_input.coverage_need}"
        ]
        
        # Add age-based preferences
        if user_input.age < 30:
            query_parts.append("young adult affordable basic")
        elif user_input.age > 55:
            query_parts.append("senior care specialized")
        else:
            query_parts.append("comprehensive family")
        
        # Add lifestyle-based preferences
        if "active" in user_input.lifestyle.lower():
            query_parts.append("wellness programs active lifestyle")
        
        # Add coverage-based preferences
        if "comprehensive" in user_input.coverage_need.lower():
            query_parts.append("comprehensive premium coverage")
        elif "basic" in user_input.coverage_need.lower():
            query_parts.append("basic affordable essential")
        
        return " ".join(query_parts)
    
    def add_policy(self, policy_data: Dict) -> bool:
        """Add new policy to the index"""
        try:
            # Prepare policy text
            policy_text = self._prepare_policy_texts(pd.DataFrame([policy_data]))[0]
            
            # Generate embedding
            embedding = self.encoder.encode([policy_text])
            
            # Add to index
            self.index.add(embedding.astype('float32'))
            
            # Add to DataFrame
            self.policies_df = pd.concat([
                self.policies_df, 
                pd.DataFrame([policy_data])
            ], ignore_index=True)
            
            # Save updated index
            self._save_index()
            
            logger.info(f"Added new policy: {policy_data.get('name', 'Unknown')}")
            return True
            
        except Exception as e:
            logger.error(f"Error adding policy: {e}")
            return False
    
    def get_policy_stats(self) -> Dict[str, Any]:
        """Get statistics about the policy database"""
        if self.policies_df is None or len(self.policies_df) == 0:
            return {"total_policies": 0}
        
        stats = {
            "total_policies": len(self.policies_df),
            "providers": self.policies_df['provider'].unique().tolist(),
            "coverage_types": self.policies_df['coverage_type'].unique().tolist(),
            "avg_premium": self.policies_df['monthly_premium_base'].mean(),
            "premium_range": {
                "min": self.policies_df['monthly_premium_base'].min(),
                "max": self.policies_df['monthly_premium_base'].max()
            }
        }
        return stats
```

### 3. Create Sample Data

Create `app/data/policies.json`:

```json
[
  {
    "policy_id": "basic_001",
    "name": "Basic Health Plan",
    "provider": "HealthCorp",
    "coverage_type": "basic",
    "monthly_premium_base": 200,
    "annual_deductible": 2500,
    "out_of_pocket_max": 7000,
    "network_type": "HMO",
    "description": "Affordable basic health coverage with essential benefits",
    "benefits": [
      "Primary care visits: $30 copay",
      "Preventive care: Covered 100%",
      "Emergency room: $500 copay",
      "Prescription drugs: Generic $10, Brand $40"
    ],
    "age_range": "18-65",
    "suitable_for": ["young adults", "healthy individuals", "budget-conscious"]
  },
  {
    "policy_id": "comprehensive_001", 
    "name": "Comprehensive Health Plus",
    "provider": "HealthCorp",
    "coverage_type": "comprehensive",
    "monthly_premium_base": 350,
    "annual_deductible": 1500,
    "out_of_pocket_max": 5000,
    "network_type": "PPO",
    "description": "Comprehensive health coverage with wide provider network",
    "benefits": [
      "Primary care visits: $25 copay",
      "Specialist visits: $50 copay", 
      "Emergency room: $250 copay",
      "Hospital stay: 20% coinsurance after deductible",
      "Mental health services: $25 copay",
      "Prescription drugs: Tier 1-3 coverage"
    ],
    "age_range": "18-65",
    "suitable_for": ["families", "chronic conditions", "comprehensive coverage seekers"]
  }
]
```

## 🔗 Alternative: Pinecone Integration

For production scale, consider Pinecone:

```python
import pinecone
from app.core.config import settings

class PineconeRAGService:
    def __init__(self):
        pinecone.init(
            api_key=settings.pinecone_api_key,
            environment=settings.pinecone_environment
        )
        
        self.index_name = "insurance-policies"
        self.encoder = SentenceTransformer("all-MiniLM-L6-v2")
        
        # Create index if it doesn't exist
        if self.index_name not in pinecone.list_indexes():
            pinecone.create_index(
                self.index_name,
                dimension=384,
                metric="cosine"
            )
        
        self.index = pinecone.Index(self.index_name)
    
    async def search_policies(self, user_input, k: int = 3) -> List[Dict]:
        """Search policies using Pinecone"""
        try:
            # Create query embedding
            query_text = self._create_search_query(user_input)
            query_embedding = self.encoder.encode([query_text]).tolist()[0]
            
            # Search Pinecone
            results = self.index.query(
                vector=query_embedding,
                top_k=k,
                include_metadata=True
            )
            
            # Extract policies from results
            policies = []
            for match in results['matches']:
                policy = match['metadata']
                policy['similarity_score'] = match['score']
                policies.append(policy)
            
            return policies
            
        except Exception as e:
            logger.error(f"Pinecone search error: {e}")
            return self._get_fallback_policies()
    
    def upsert_policy(self, policy_data: Dict):
        """Add/update policy in Pinecone"""
        try:
            # Generate embedding
            policy_text = self._prepare_policy_text(policy_data)
            embedding = self.encoder.encode([policy_text]).tolist()[0]
            
            # Upsert to Pinecone
            self.index.upsert([
                (policy_data['policy_id'], embedding, policy_data)
            ])
            
            logger.info(f"Upserted policy: {policy_data['policy_id']}")
            
        except Exception as e:
            logger.error(f"Error upserting policy: {e}")
```

## 🧪 Testing RAG Service

Create `tests/test_rag_service.py`:

```python
import pytest
from app.services.rag_service import RAGService
from app.api.models import UserInput

@pytest.fixture
def rag_service():
    return RAGService()

@pytest.fixture
def sample_user_input():
    return UserInput(
        age=35,
        medical_history="No pre-existing conditions",
        lifestyle="Moderately active", 
        coverage_need="Comprehensive coverage"
    )

@pytest.mark.asyncio
async def test_search_policies(rag_service, sample_user_input):
    """Test policy search"""
    policies = await rag_service.search_policies(sample_user_input, k=3)
    
    assert len(policies) <= 3
    assert len(policies) > 0
    
    # Check policy structure
    policy = policies[0]
    assert 'policy_id' in policy
    assert 'name' in policy
    assert 'monthly_premium_base' in policy

def test_policy_stats(rag_service):
    """Test policy statistics"""
    stats = rag_service.get_policy_stats()
    
    assert 'total_policies' in stats
    assert stats['total_policies'] >= 0

@pytest.mark.asyncio 
async def test_add_policy(rag_service):
    """Test adding new policy"""
    new_policy = {
        "policy_id": "test_001",
        "name": "Test Plan",
        "provider": "TestCorp",
        "coverage_type": "test",
        "monthly_premium_base": 300,
        "description": "Test policy for unit testing"
    }
    
    initial_count = rag_service.get_policy_stats()['total_policies']
    
    success = rag_service.add_policy(new_policy)
    assert success
    
    final_count = rag_service.get_policy_stats()['total_policies']
    assert final_count == initial_count + 1
```

## 📊 RAG Performance Optimization

### 1. Caching
```python
from functools import lru_cache
import hashlib

class OptimizedRAGService(RAGService):
    @lru_cache(maxsize=128)
    def _cached_encode(self, text: str):
        """Cache embeddings for repeated queries"""
        return self.encoder.encode([text])[0]
    
    def _get_query_hash(self, user_input) -> str:
        """Generate hash for user input caching"""
        query_str = f"{user_input.age}_{user_input.medical_history}_{user_input.lifestyle}_{user_input.coverage_need}"
        return hashlib.md5(query_str.encode()).hexdigest()
```

### 2. Async Processing
```python
import asyncio
from concurrent.futures import ThreadPoolExecutor

class AsyncRAGService(RAGService):
    def __init__(self):
        super().__init__()
        self.executor = ThreadPoolExecutor(max_workers=4)
    
    async def async_search_policies(self, user_input, k: int = 3):
        """Async policy search"""
        loop = asyncio.get_event_loop()
        
        # Run embedding generation in thread pool
        query_text = self._create_search_query(user_input)
        embedding = await loop.run_in_executor(
            self.executor, 
            self.encoder.encode, 
            [query_text]
        )
        
        # Search index
        distances, indices = self.index.search(embedding.astype('float32'), k)
        
        return self._process_results(distances, indices)
```

## 🔧 Configuration Options

Add to `app/core/config.py`:

```python
class Settings(BaseSettings):
    # ... existing settings ...
    
    # RAG Configuration
    rag_provider: str = "faiss"  # faiss, pinecone, weaviate
    embedding_model: str = "all-MiniLM-L6-v2"
    max_policies_returned: int = 5
    similarity_threshold: float = 0.7
    
    # FAISS settings
    faiss_index_path: str = "data/faiss_index"
    
    # Pinecone settings  
    pinecone_index_name: str = "insurance-policies"
```

## 🚀 Integration with Quote Service

Update your quote service to use RAG:

```python
class QuoteService:
    def __init__(self):
        self.llm_service = LLMService()
        self.rag_service = RAGService()
    
    async def generate_quote(self, user_input: UserInput) -> QuoteResponse:
        """Generate quote using RAG + LLM"""
        # 1. Retrieve relevant policies
        relevant_policies = await self.rag_service.search_policies(user_input)
        
        # 2. Generate quote with LLM
        quote_data = await self.llm_service.generate_insurance_quote(
            user_input, relevant_policies
        )
        
        # 3. Format and return response
        return self._format_quote_response(quote_data, user_input)
```

## 📈 Monitoring RAG Performance

```python
import time
from collections import defaultdict

class RAGMetrics:
    def __init__(self):
        self.search_times = []
        self.query_counts = defaultdict(int)
        self.similarity_scores = []
    
    def record_search(self, duration: float, similarity_scores: List[float]):
        """Record search metrics"""
        self.search_times.append(duration)
        self.similarity_scores.extend(similarity_scores)
    
    def get_stats(self) -> Dict:
        """Get performance statistics"""
        return {
            "avg_search_time": np.mean(self.search_times) if self.search_times else 0,
            "total_searches": len(self.search_times),
            "avg_similarity": np.mean(self.similarity_scores) if self.similarity_scores else 0,
            "min_similarity": np.min(self.similarity_scores) if self.similarity_scores else 0
        }
```

## 🎯 Next Steps

1. **Test Your RAG Pipeline**: Run the tests and verify results
2. **Add More Policies**: Expand your policy database
3. **Optimize Performance**: Implement caching and async processing
4. **Monitor Quality**: Track similarity scores and user feedback
5. **Consider Hybrid Search**: Combine semantic and keyword search

Your RAG pipeline is now ready to provide intelligent policy matching! Next, integrate it with your quote generation service.