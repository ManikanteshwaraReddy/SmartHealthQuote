# LLM Integration Guide for FastAPI

This guide shows you how to integrate Language Models with your FastAPI backend for generating intelligent insurance quotes.

## 🤖 Supported LLM Options

1. **OpenAI GPT** - Powerful, API-based, easy integration
2. **Anthropic Claude** - Strong reasoning, safety-focused
3. **Local Models** - Mistral 7B, Llama 2, privacy-focused
4. **Hugging Face** - Open source models, customizable

## 🚀 Quick Start with OpenAI

### 1. Install Dependencies
```bash
pip install openai==1.3.9
```

### 2. Set API Key
Add to your `.env` file:
```env
OPENAI_API_KEY=sk-your-openai-key-here
```

### 3. Create LLM Service

Create `app/services/llm_service.py`:

```python
import openai
from typing import Dict, List, Optional, Any
from app.core.config import settings
from app.api.models import ChatResponse, UserInput
import json
import logging

logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self):
        self.client = openai.OpenAI(api_key=settings.openai_api_key)
        self.model = "gpt-3.5-turbo"  # or "gpt-4" for better quality
        
    async def process_chat_message(self, message: str, context: Optional[Dict] = None) -> ChatResponse:
        """Process chat message and return response"""
        try:
            system_prompt = self._get_system_prompt()
            user_prompt = self._format_user_message(message, context)
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            response_text = response.choices[0].message.content
            suggestions = self._extract_suggestions(response_text)
            
            return ChatResponse(
                response=response_text,
                suggestions=suggestions,
                next_step=self._determine_next_step(message, context)
            )
            
        except Exception as e:
            logger.error(f"LLM processing error: {e}")
            return ChatResponse(
                response="I'm sorry, I'm having trouble processing your request right now. Please try again.",
                suggestions=["Try rephrasing your question", "Contact support if the issue persists"]
            )
    
    async def generate_insurance_quote(self, user_input: UserInput, retrieved_policies: List[Dict]) -> Dict[str, Any]:
        """Generate personalized insurance quote using LLM"""
        try:
            system_prompt = self._get_quote_system_prompt()
            user_prompt = self._format_quote_prompt(user_input, retrieved_policies)
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3,  # Lower temperature for more consistent quotes
                max_tokens=1000,
                response_format={"type": "json_object"}  # Ensure JSON response
            )
            
            quote_data = json.loads(response.choices[0].message.content)
            return quote_data
            
        except Exception as e:
            logger.error(f"Quote generation error: {e}")
            # Return a fallback quote
            return self._get_fallback_quote(user_input)
    
    def _get_system_prompt(self) -> str:
        """Get system prompt for chat interactions"""
        return """You are a helpful and knowledgeable health insurance assistant. 
        Your role is to help users understand their insurance options and guide them 
        through the quote process.
        
        Guidelines:
        - Be friendly and professional
        - Ask clarifying questions when needed
        - Explain insurance terms in simple language
        - Focus on helping users find the best coverage for their needs
        - Always prioritize user privacy and data security
        
        Keep responses concise but informative."""
    
    def _get_quote_system_prompt(self) -> str:
        """Get system prompt for quote generation"""
        return """You are an expert insurance quote generator. Based on user health 
        information and available insurance policies, generate personalized insurance 
        quotes.
        
        Your response must be a valid JSON object with this structure:
        {
            "recommended_plan": {
                "name": "Plan name",
                "monthly_premium": 285.00,
                "annual_deductible": 1500,
                "out_of_pocket_max": 5000,
                "coverage_type": "comprehensive",
                "network_type": "PPO"
            },
            "rationale": "Explanation of why this plan fits the user",
            "benefits": ["Benefit 1", "Benefit 2", "Benefit 3"],
            "considerations": ["Important consideration 1", "Important consideration 2"],
            "confidence_score": 0.85
        }
        
        Consider:
        - User's age and health status
        - Lifestyle factors
        - Coverage preferences
        - Budget implications
        - Available policy options"""
    
    def _format_user_message(self, message: str, context: Optional[Dict]) -> str:
        """Format user message with context"""
        if context:
            return f"Context: {json.dumps(context)}\n\nUser message: {message}"
        return message
    
    def _format_quote_prompt(self, user_input: UserInput, policies: List[Dict]) -> str:
        """Format prompt for quote generation"""
        prompt = f"""
        User Profile:
        - Age: {user_input.age}
        - Medical History: {user_input.medical_history}
        - Lifestyle: {user_input.lifestyle}
        - Coverage Need: {user_input.coverage_need}
        
        Available Insurance Policies:
        {json.dumps(policies, indent=2)}
        
        Please recommend the best insurance plan for this user and provide a detailed quote.
        """
        return prompt
    
    def _extract_suggestions(self, response: str) -> List[str]:
        """Extract actionable suggestions from response"""
        # Simple implementation - could be enhanced with NLP
        suggestions = []
        if "consider" in response.lower():
            suggestions.append("Review the considerations mentioned")
        if "question" in response.lower():
            suggestions.append("Ask follow-up questions if needed")
        if "compare" in response.lower():
            suggestions.append("Compare different plan options")
        return suggestions
    
    def _determine_next_step(self, message: str, context: Optional[Dict]) -> Optional[str]:
        """Determine the next step in the conversation"""
        if not context:
            return "collect_basic_info"
        
        if "age" not in str(context):
            return "collect_age"
        elif "medical" not in message.lower():
            return "collect_medical_history"
        elif "lifestyle" not in message.lower():
            return "collect_lifestyle"
        elif "coverage" not in message.lower():
            return "collect_coverage_needs"
        else:
            return "generate_quote"
    
    def _get_fallback_quote(self, user_input: UserInput) -> Dict[str, Any]:
        """Return a basic fallback quote if LLM fails"""
        base_premium = 200
        age_factor = max(1.0, user_input.age / 30)
        
        return {
            "recommended_plan": {
                "name": "Standard Health Plan",
                "monthly_premium": round(base_premium * age_factor, 2),
                "annual_deductible": 1500,
                "out_of_pocket_max": 5000,
                "coverage_type": "standard",
                "network_type": "PPO"
            },
            "rationale": "Basic plan recommendation based on your profile",
            "benefits": [
                "Primary care visits: $25 copay",
                "Preventive care: Covered 100%",
                "Emergency room: $250 copay"
            ],
            "considerations": [
                "This is a basic quote - personalized quote failed to generate",
                "Contact support for detailed analysis"
            ],
            "confidence_score": 0.5
        }
```

## 🔀 Alternative: Anthropic Claude Integration

Create `app/services/claude_service.py`:

```python
import anthropic
from app.core.config import settings
from typing import Dict, List, Optional, Any
import json
import logging

logger = logging.getLogger(__name__)

class ClaudeService:
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
        self.model = "claude-3-sonnet-20240229"
    
    async def generate_quote(self, user_input, retrieved_policies) -> Dict[str, Any]:
        """Generate quote using Claude"""
        try:
            prompt = f"""
            <user_profile>
            Age: {user_input.age}
            Medical History: {user_input.medical_history}
            Lifestyle: {user_input.lifestyle}
            Coverage Need: {user_input.coverage_need}
            </user_profile>
            
            <available_policies>
            {json.dumps(retrieved_policies, indent=2)}
            </available_policies>
            
            Please analyze this user's profile and recommend the best insurance plan.
            Respond with a JSON object containing the quote details.
            """
            
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1000,
                messages=[{"role": "user", "content": prompt}]
            )
            
            # Parse response and return quote
            quote_data = json.loads(response.content[0].text)
            return quote_data
            
        except Exception as e:
            logger.error(f"Claude quote generation error: {e}")
            return self._get_fallback_quote(user_input)
    
    def _get_fallback_quote(self, user_input):
        """Fallback quote implementation"""
        # Similar to OpenAI fallback
        pass
```

## 🏠 Local LLM Integration (Mistral 7B)

For privacy-focused deployments, run models locally:

```python
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from typing import Dict, Any
import json

class LocalLLMService:
    def __init__(self):
        self.model_name = "mistralai/Mistral-7B-Instruct-v0.1"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            torch_dtype=torch.float16,
            device_map="auto"
        )
        
    async def generate_quote(self, user_input, retrieved_policies) -> Dict[str, Any]:
        """Generate quote using local Mistral model"""
        try:
            prompt = self._build_prompt(user_input, retrieved_policies)
            
            inputs = self.tokenizer(prompt, return_tensors="pt")
            
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=500,
                    temperature=0.3,
                    do_sample=True,
                    pad_token_id=self.tokenizer.eos_token_id
                )
            
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Extract JSON from response
            quote_data = self._extract_json(response)
            return quote_data
            
        except Exception as e:
            logger.error(f"Local LLM error: {e}")
            return self._get_fallback_quote(user_input)
    
    def _build_prompt(self, user_input, policies):
        """Build prompt for Mistral model"""
        return f"""[INST] You are an insurance expert. Generate a personalized insurance quote.

User Profile:
- Age: {user_input.age}
- Medical History: {user_input.medical_history}
- Lifestyle: {user_input.lifestyle}
- Coverage Need: {user_input.coverage_need}

Available Policies:
{json.dumps(policies, indent=2)}

Respond with a JSON object containing the recommended plan and rationale. [/INST]"""

    def _extract_json(self, response: str) -> Dict[str, Any]:
        """Extract JSON from model response"""
        try:
            # Find JSON object in response
            start = response.find('{')
            end = response.rfind('}') + 1
            json_str = response[start:end]
            return json.loads(json_str)
        except:
            return self._get_basic_quote()
```

## 🔧 Configuration and Model Selection

Update `app/core/config.py`:

```python
class Settings(BaseSettings):
    # ... existing settings ...
    
    # LLM Configuration
    llm_provider: str = "openai"  # openai, anthropic, local, huggingface
    openai_model: str = "gpt-3.5-turbo"
    anthropic_model: str = "claude-3-sonnet-20240229"
    local_model_name: str = "mistralai/Mistral-7B-Instruct-v0.1"
    
    # LLM Parameters
    llm_temperature: float = 0.7
    llm_max_tokens: int = 1000
    llm_timeout: int = 30
```

## 🎯 Integration with Quote Service

Update `app/services/quote_service.py`:

```python
from app.services.llm_service import LLMService
from app.services.rag_service import RAGService
from app.api.models import UserInput, QuoteResponse, InsurancePlan
import uuid
from datetime import datetime

class QuoteService:
    def __init__(self):
        self.llm_service = LLMService()
        self.rag_service = RAGService()
    
    async def generate_quote(self, user_input: UserInput) -> QuoteResponse:
        """Generate insurance quote using LLM and RAG"""
        try:
            # 1. Retrieve relevant policies using RAG
            retrieved_policies = await self.rag_service.search_policies(user_input)
            
            # 2. Generate quote using LLM
            quote_data = await self.llm_service.generate_insurance_quote(
                user_input, retrieved_policies
            )
            
            # 3. Format response
            plan_data = quote_data["recommended_plan"]
            plan = InsurancePlan(
                plan_id=f"plan_{uuid.uuid4().hex[:8]}",
                name=plan_data["name"],
                provider="HealthCorp",  # Could be determined by RAG
                monthly_premium=plan_data["monthly_premium"],
                annual_deductible=plan_data["annual_deductible"],
                out_of_pocket_max=plan_data["out_of_pocket_max"],
                coverage_type=plan_data["coverage_type"],
                network_type=plan_data.get("network_type", "PPO")
            )
            
            return QuoteResponse(
                quote_id=f"quote_{uuid.uuid4().hex}",
                plan=plan,
                benefits=quote_data.get("benefits", []),
                recommendations=quote_data.get("considerations", []),
                confidence_score=quote_data.get("confidence_score", 0.8),
                generated_at=datetime.now()
            )
            
        except Exception as e:
            # Return fallback quote
            return self._generate_fallback_quote(user_input)
```

## 🧪 Testing LLM Integration

Create `tests/test_llm_service.py`:

```python
import pytest
from app.services.llm_service import LLMService
from app.api.models import UserInput

@pytest.fixture
def llm_service():
    return LLMService()

@pytest.fixture
def sample_user_input():
    return UserInput(
        age=35,
        medical_history="No pre-existing conditions",
        lifestyle="Moderately active",
        coverage_need="Comprehensive coverage"
    )

@pytest.mark.asyncio
async def test_chat_message_processing(llm_service):
    """Test chat message processing"""
    response = await llm_service.process_chat_message(
        "I need help choosing health insurance"
    )
    
    assert response.response is not None
    assert len(response.response) > 0
    assert isinstance(response.suggestions, list)

@pytest.mark.asyncio
async def test_quote_generation(llm_service, sample_user_input):
    """Test quote generation"""
    sample_policies = [
        {
            "name": "Basic Health Plan",
            "premium": 200,
            "deductible": 1500,
            "coverage": "basic"
        }
    ]
    
    quote = await llm_service.generate_insurance_quote(
        sample_user_input, sample_policies
    )
    
    assert "recommended_plan" in quote
    assert "confidence_score" in quote
    assert quote["confidence_score"] >= 0.0
    assert quote["confidence_score"] <= 1.0
```

## 🚀 Running Tests

```bash
# Install test dependencies
pip install pytest pytest-asyncio

# Run LLM tests
pytest tests/test_llm_service.py -v

# Run with coverage
pip install pytest-cov
pytest tests/ --cov=app/services --cov-report=html
```

## 📊 Monitoring and Logging

Add logging to track LLM performance:

```python
import logging
import time
from functools import wraps

def log_llm_calls(func):
    """Decorator to log LLM API calls"""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = await func(*args, **kwargs)
            duration = time.time() - start_time
            logging.info(f"LLM call successful: {func.__name__} took {duration:.2f}s")
            return result
        except Exception as e:
            duration = time.time() - start_time
            logging.error(f"LLM call failed: {func.__name__} after {duration:.2f}s: {e}")
            raise
    return wrapper
```

## 🎯 Next Steps

1. **Implement RAG Service**: Create the retrieval component
2. **Add Error Handling**: Robust fallbacks and retry logic
3. **Optimize Performance**: Caching and async processing
4. **Add Model Switching**: Support multiple LLM providers
5. **Monitor Usage**: Track API costs and performance

Your LLM integration is now ready! Next, implement the RAG pipeline to provide context for better quotes.