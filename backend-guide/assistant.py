#!/usr/bin/env python3
"""
SmartHealthQuote Backend Development Assistant

An interactive CLI tool that guides developers through building and integrating
a Language Model-based health insurance quote system backend.
"""

import json
import os
import sys
from typing import Dict, List, Optional


class BackendAssistant:
    def __init__(self):
        self.session_data = {
            "frontend_tech_stack": None,
            "backend_framework": None,
            "llm_requirements": None,
            "data_format": None,
            "api_design": None,
            "auth_requirements": None,
            "deployment_target": None,
            "communication_method": None,
            "current_step": 1
        }
        self.conversation_history = []
        
    def display_welcome(self):
        """Display welcome message and overview."""
        print("\n" + "="*70)
        print("🏥 SmartHealthQuote Backend Development Assistant")
        print("="*70)
        print("\nWelcome! I'm here to guide you through building a robust backend")
        print("for your health insurance quote system. Let's build something amazing!")
        print("\nI'll ask you questions one at a time to understand your needs")
        print("and provide tailored guidance, code snippets, and best practices.")
        print("\n" + "-"*70)
        
    def ask_question(self, question: str, options: Optional[List[str]] = None, 
                    allow_custom: bool = True) -> str:
        """Ask a question and get user response."""
        print(f"\n📋 {question}")
        
        if options:
            print("\nAvailable options:")
            for i, option in enumerate(options, 1):
                print(f"  {i}. {option}")
            
            if allow_custom:
                print(f"  {len(options) + 1}. Other (specify)")
        
        while True:
            if options:
                response = input("\nEnter your choice (number): ").strip()
                try:
                    choice = int(response)
                    if 1 <= choice <= len(options):
                        selected = options[choice - 1]
                        print(f"✅ Selected: {selected}")
                        return selected
                    elif allow_custom and choice == len(options) + 1:
                        custom = input("Please specify: ").strip()
                        if custom:
                            print(f"✅ Custom choice: {custom}")
                            return custom
                    else:
                        print("❌ Invalid choice. Please try again.")
                except ValueError:
                    print("❌ Please enter a valid number.")
            else:
                response = input("\nYour answer: ").strip()
                if response:
                    return response
                print("❌ Please provide an answer.")
    
    def step_1_frontend_analysis(self):
        """Step 1: Understand frontend tech stack and data flow."""
        print("\n🔍 STEP 1: Frontend Analysis")
        print("Let's understand your current frontend setup.")
        
        # Analyze the existing React frontend
        print("\n💡 I can see you have a React frontend with:")
        print("  • React + Vite setup")
        print("  • Tailwind CSS for styling")
        print("  • Chat interface for user interaction")
        print("  • Form handling with react-hook-form")
        print("  • Routing with react-router")
        
        # Ask about data flow
        question = "How familiar are you with the current frontend data flow?"
        options = [
            "Very familiar - I built it",
            "Somewhat familiar - I've reviewed the code",
            "Not familiar - I'm new to this project"
        ]
        
        familiarity = self.ask_question(question, options)
        self.session_data["frontend_tech_stack"] = {
            "framework": "React + Vite",
            "styling": "Tailwind CSS",
            "familiarity": familiarity
        }
        
        # Explain current frontend integration points
        print("\n📊 Current Frontend Integration Points:")
        print("  • Chat interface collects: age, medical history, lifestyle, coverage needs")
        print("  • Expected API call in chat.jsx: getQuotation() function")
        print("  • Quote display component ready for API response")
        print("  • Form data structure: {age, medicalHistory, lifestyle, coverageNeed}")
        
        return True
    
    def step_2_backend_framework(self):
        """Step 2: Determine preferred backend framework."""
        print("\n🔧 STEP 2: Backend Framework Selection")
        print("Let's choose the best backend framework for your needs.")
        
        question = "Which backend framework would you prefer?"
        options = [
            "FastAPI (Python) - High performance, automatic API docs",
            "Flask (Python) - Lightweight, flexible, great for MVPs", 
            "Node.js (Express) - JavaScript full-stack, familiar syntax",
            "Django (Python) - Full-featured, built-in admin, ORM"
        ]
        
        framework_choice = self.ask_question(question, options)
        self.session_data["backend_framework"] = framework_choice
        
        # Provide framework-specific benefits
        self.explain_framework_benefits(framework_choice)
        
        # Ask about experience level
        exp_question = "What's your experience level with this framework?"
        exp_options = [
            "Expert - I've built production applications",
            "Intermediate - I've built some projects",
            "Beginner - I'm learning or new to it"
        ]
        
        experience = self.ask_question(exp_question, exp_options)
        self.session_data["backend_framework_experience"] = experience
        
        return True
    
    def step_3_llm_integration(self):
        """Step 3: Plan LLM integration with RAG pipeline."""
        print("\n🤖 STEP 3: LLM and RAG Pipeline Planning")
        print("Let's design your Language Model integration.")
        
        # Explain RAG concept
        print("\n💡 RAG (Retrieval-Augmented Generation) combines:")
        print("  • Vector database for insurance policy data")
        print("  • Semantic search for relevant policies")
        print("  • LLM for generating personalized quotes")
        
        llm_question = "Which LLM approach interests you most?"
        llm_options = [
            "Mistral 7B (Local) - Privacy-focused, no API costs",
            "OpenAI GPT (API) - Powerful, easy to integrate",
            "Anthropic Claude (API) - Strong reasoning, safety-focused",
            "Hugging Face Models - Open source, customizable"
        ]
        
        llm_choice = self.ask_question(llm_question, llm_options)
        
        # Ask about vector database preference
        vector_question = "Which vector database would you prefer?"
        vector_options = [
            "Faiss (Facebook) - Fast, local, good for prototypes",
            "Pinecone - Managed, scalable, easy to use",
            "Weaviate - Open source, GraphQL API",
            "Chroma - Simple, local-first, Python-friendly"
        ]
        
        vector_choice = self.ask_question(vector_question, vector_options)
        
        self.session_data["llm_requirements"] = {
            "llm_choice": llm_choice,
            "vector_db": vector_choice
        }
        
        # Explain implementation approach
        self.explain_rag_implementation()
        
        return True
    
    def step_4_data_structure(self):
        """Step 4: Identify insurance data format and structure."""
        print("\n📊 STEP 4: Insurance Data Structure")
        print("Let's design your insurance data model.")
        
        print("\n💡 Your system needs to handle:")
        print("  • Insurance policies and plans")
        print("  • Coverage options and limits")  
        print("  • Premium calculations")
        print("  • Provider information")
        print("  • User health profiles")
        
        data_question = "What's your primary data source for insurance information?"
        data_options = [
            "Insurance company APIs - Real-time policy data",
            "Static datasets - CSV/JSON files with policy info",
            "Manual curation - Build your own policy database", 
            "Third-party services - Insurance aggregator APIs"
        ]
        
        data_source = self.ask_question(data_question, data_options)
        
        # Ask about data complexity
        complexity_question = "How complex should your initial data model be?"
        complexity_options = [
            "Simple - Basic plans with premium ranges",
            "Moderate - Multiple coverage types and tiers",
            "Complex - Detailed underwriting and calculations"
        ]
        
        complexity = self.ask_question(complexity_question, complexity_options)
        
        self.session_data["data_format"] = {
            "source": data_source,
            "complexity": complexity
        }
        
        # Show example data structure
        self.show_data_structure_example(complexity)
        
        return True
    
    def step_5_api_design(self):
        """Step 5: Design APIs for health insurance parameters and quotes."""
        print("\n🔌 STEP 5: API Design")
        print("Let's design your API endpoints.")
        
        print("\n💡 Based on your frontend, we need these APIs:")
        print("  • POST /api/quote - Generate insurance quote")
        print("  • GET /api/providers - List insurance providers")
        print("  • GET /api/plans - Get available plans")
        print("  • POST /api/chat - Handle chat interactions")
        
        api_question = "What API style do you prefer?"
        api_options = [
            "REST - Simple, widely supported",
            "GraphQL - Flexible queries, single endpoint",
            "FastAPI/OpenAPI - Auto-generated docs, type safety"
        ]
        
        api_style = self.ask_question(api_question, api_options)
        
        # Ask about real-time features
        realtime_question = "Do you need real-time features?"
        realtime_options = [
            "Yes - WebSocket for live chat",
            "Yes - Server-sent events for updates",
            "No - Standard HTTP requests are fine"
        ]
        
        realtime = self.ask_question(realtime_question, realtime_options)
        
        self.session_data["api_design"] = {
            "style": api_style,
            "realtime": realtime
        }
        
        # Show API specification example
        self.show_api_examples()
        
        return True
    
    def step_6_authentication_security(self):
        """Step 6: Discuss authentication and security."""
        print("\n🔐 STEP 6: Authentication & Security")
        print("Let's secure your application.")
        
        auth_question = "What authentication approach do you need?"
        auth_options = [
            "None - Anonymous quotes (simplest start)",
            "Basic - Email/password registration",
            "OAuth - Google/Facebook login",
            "Enterprise - SAML/LDAP integration"
        ]
        
        auth_choice = self.ask_question(auth_question, auth_options)
        
        # Ask about data privacy
        privacy_question = "How sensitive is the health data you'll handle?"
        privacy_options = [
            "Low - General health questions only",
            "Medium - Some medical history",
            "High - Detailed medical records (HIPAA compliance needed)"
        ]
        
        privacy_level = self.ask_question(privacy_question, privacy_options)
        
        self.session_data["auth_requirements"] = {
            "auth_type": auth_choice,
            "privacy_level": privacy_level
        }
        
        # Provide security recommendations
        self.provide_security_recommendations(privacy_level)
        
        return True
    
    def step_7_deployment_scalability(self):
        """Step 7: Plan deployment and scalability."""
        print("\n🚀 STEP 7: Deployment & Scalability")
        print("Let's plan your deployment strategy.")
        
        deploy_question = "Where would you like to deploy?"
        deploy_options = [
            "Local development - Docker Compose",
            "Cloud platform - AWS/GCP/Azure",
            "PaaS solution - Heroku/Railway/Render",
            "Serverless - AWS Lambda/Vercel Functions"
        ]
        
        deployment = self.ask_question(deploy_question, deploy_options)
        
        # Ask about expected scale
        scale_question = "What's your expected initial scale?"
        scale_options = [
            "Small - <100 users/day",
            "Medium - 100-1000 users/day", 
            "Large - 1000+ users/day"
        ]
        
        scale = self.ask_question(scale_question, scale_options)
        
        self.session_data["deployment_target"] = {
            "platform": deployment,
            "scale": scale
        }
        
        # Provide deployment guidance
        self.provide_deployment_guidance(deployment, scale)
        
        return True
    
    def step_8_communication_method(self):
        """Step 8: Ensure smooth frontend-backend communication."""
        print("\n🔄 STEP 8: Frontend-Backend Communication")
        print("Let's ensure smooth integration with your React frontend.")
        
        print("\n💡 Your frontend currently expects:")
        print("  • getQuotation() function in chat.jsx")
        print("  • JSON response with quote data")
        print("  • Error handling for failed requests")
        
        comm_question = "How should we handle API communication?"
        comm_options = [
            "Axios (already used) - HTTP client library",
            "Fetch API - Native browser API",
            "TanStack Query - Advanced caching and sync",
            "Custom wrapper - Tailored to your needs"
        ]
        
        communication = self.ask_question(comm_question, comm_options)
        
        # Ask about error handling
        error_question = "How comprehensive should error handling be?"
        error_options = [
            "Basic - Simple try/catch blocks",
            "Intermediate - User-friendly error messages",
            "Advanced - Retry logic, fallbacks, monitoring"
        ]
        
        error_handling = self.ask_question(error_question, error_options)
        
        self.session_data["communication_method"] = {
            "client": communication,
            "error_handling": error_handling
        }
        
        return True
    
    def generate_implementation_plan(self):
        """Generate a comprehensive implementation plan."""
        print("\n📋 IMPLEMENTATION PLAN")
        print("="*50)
        
        print("\n🎯 Your Customized Backend Implementation Plan:")
        
        # Framework setup
        framework = self.session_data.get("backend_framework", "Not specified")
        print(f"\n1. **Backend Framework**: {framework}")
        
        # LLM integration
        llm_info = self.session_data.get("llm_requirements", {})
        print(f"\n2. **LLM Integration**: {llm_info.get('llm_choice', 'Not specified')}")
        print(f"   **Vector DB**: {llm_info.get('vector_db', 'Not specified')}")
        
        # Data structure
        data_info = self.session_data.get("data_format", {})
        print(f"\n3. **Data Source**: {data_info.get('source', 'Not specified')}")
        print(f"   **Complexity**: {data_info.get('complexity', 'Not specified')}")
        
        # API design
        api_info = self.session_data.get("api_design", {})
        print(f"\n4. **API Style**: {api_info.get('style', 'Not specified')}")
        print(f"   **Real-time**: {api_info.get('realtime', 'Not specified')}")
        
        # Security
        auth_info = self.session_data.get("auth_requirements", {})
        print(f"\n5. **Authentication**: {auth_info.get('auth_type', 'Not specified')}")
        print(f"   **Privacy Level**: {auth_info.get('privacy_level', 'Not specified')}")
        
        # Deployment
        deploy_info = self.session_data.get("deployment_target", {})
        print(f"\n6. **Deployment**: {deploy_info.get('platform', 'Not specified')}")
        print(f"   **Scale**: {deploy_info.get('scale', 'Not specified')}")
        
        print("\n" + "="*50)
        print("✅ Plan generated! Check the framework-specific guides for detailed implementation.")
        
        # Generate next steps
        self.generate_next_steps()
    
    def generate_next_steps(self):
        """Generate specific next steps based on choices."""
        print("\n🚀 NEXT STEPS:")
        
        framework = self.session_data.get("backend_framework", "")
        
        if "FastAPI" in framework:
            print("\n1. Set up FastAPI project:")
            print("   pip install fastapi uvicorn")
            print("   Check: backend-guide/frameworks/fastapi/")
            
        elif "Flask" in framework:
            print("\n1. Set up Flask project:")
            print("   pip install flask flask-cors")
            print("   Check: backend-guide/frameworks/flask/")
            
        elif "Node.js" in framework:
            print("\n1. Set up Node.js project:")
            print("   npm init && npm install express cors")
            print("   Check: backend-guide/frameworks/nodejs/")
        
        print("\n2. Update frontend integration:")
        print("   • Replace getQuotation() placeholder in src/pages/chat.jsx")
        print("   • Add proper API endpoints")
        print("   • Implement error handling")
        
        print("\n3. Explore detailed guides:")
        print("   • Architecture diagrams: backend-guide/architecture/")
        print("   • Code templates: backend-guide/templates/")
        print("   • Deployment guides: backend-guide/deployment/")
        
        print("\n4. Run the assistant again anytime:")
        print("   python backend-guide/assistant.py")
    
    def explain_framework_benefits(self, framework: str):
        """Explain benefits of chosen framework."""
        benefits = {
            "FastAPI": [
                "🚀 High performance (async/await)",
                "📚 Automatic API documentation",
                "🔒 Built-in data validation",
                "🐍 Great for ML/LLM integration"
            ],
            "Flask": [
                "⚡ Lightweight and flexible",
                "📖 Extensive documentation",
                "🔧 Easy to customize",
                "👨‍💻 Great for rapid prototyping"
            ],
            "Node.js": [
                "🌐 JavaScript full-stack",
                "⚡ Fast I/O operations",
                "📦 Huge npm ecosystem",
                "🔄 Easy frontend integration"
            ],
            "Django": [
                "🏗️ Full-featured framework",
                "👑 Built-in admin interface",
                "🗄️ Powerful ORM",
                "🔐 Strong security features"
            ]
        }
        
        framework_key = framework.split(" ")[0]
        if framework_key in benefits:
            print(f"\n✅ Great choice! {framework_key} benefits:")
            for benefit in benefits[framework_key]:
                print(f"   {benefit}")
    
    def explain_rag_implementation(self):
        """Explain RAG implementation approach."""
        print("\n🔧 RAG Implementation Overview:")
        print("1. **Data Preparation**:")
        print("   • Collect insurance policy documents")
        print("   • Chunk text into semantic segments") 
        print("   • Generate embeddings for each chunk")
        print("   • Store in vector database")
        
        print("\n2. **Query Processing**:")
        print("   • Convert user input to embeddings")
        print("   • Search vector DB for relevant policies")
        print("   • Rank results by similarity")
        
        print("\n3. **Response Generation**:")
        print("   • Combine user query + retrieved context")
        print("   • Send to LLM for quote generation")
        print("   • Format response for frontend")
    
    def show_data_structure_example(self, complexity: str):
        """Show example data structure based on complexity."""
        print(f"\n📊 Example Data Structure ({complexity}):")
        
        if "Simple" in complexity:
            print("""
{
  "plan_id": "basic_health_001",
  "name": "Basic Health Plan",
  "premium_range": {
    "min": 200,
    "max": 400
  },
  "coverage_type": "basic",
  "deductible": 1500
}""")
        
        elif "Moderate" in complexity:
            print("""
{
  "plan_id": "comprehensive_001",
  "name": "Comprehensive Health Plus",
  "tiers": ["bronze", "silver", "gold"],
  "coverage": {
    "medical": true,
    "dental": true,
    "vision": false
  },
  "pricing": {
    "age_groups": {
      "18-30": 285,
      "31-50": 385,
      "51+": 485
    }
  }
}""")
        
        else:  # Complex
            print("""
{
  "plan_id": "premium_underwritten_001",
  "underwriting_factors": {
    "age": {"weight": 0.3, "bands": [...]},
    "medical_history": {"weight": 0.4, "conditions": [...]},
    "lifestyle": {"weight": 0.2, "factors": [...]}
  },
  "calculation_engine": {
    "base_premium": 300,
    "risk_multipliers": {...},
    "discounts": {...}
  }
}""")
    
    def show_api_examples(self):
        """Show API endpoint examples."""
        print("\n🔌 API Endpoint Examples:")
        print("""
POST /api/quote
{
  "age": 35,
  "medical_history": "No pre-existing conditions",
  "lifestyle": "Moderately active",
  "coverage_need": "Comprehensive coverage"
}

Response:
{
  "quote_id": "q123456",
  "plan": {
    "name": "Comprehensive Health Plus",
    "monthly_premium": 285,
    "deductible": 1500,
    "out_of_pocket_max": 5000
  },
  "benefits": [...],
  "provider": "HealthCorp"
}""")
    
    def provide_security_recommendations(self, privacy_level: str):
        """Provide security recommendations based on privacy level."""
        print(f"\n🔐 Security Recommendations ({privacy_level} privacy):")
        
        if "High" in privacy_level:
            print("   • HIPAA compliance required")
            print("   • End-to-end encryption")
            print("   • Audit logging")
            print("   • Data retention policies")
            print("   • Regular security assessments")
        
        elif "Medium" in privacy_level:
            print("   • HTTPS everywhere")
            print("   • Data encryption at rest")
            print("   • Input validation")
            print("   • Rate limiting")
            print("   • Basic audit logging")
        
        else:  # Low
            print("   • HTTPS for API calls")
            print("   • Basic input validation")
            print("   • CORS configuration")
            print("   • API rate limiting")
    
    def provide_deployment_guidance(self, deployment: str, scale: str):
        """Provide deployment guidance."""
        print(f"\n🚀 Deployment Guidance ({deployment}, {scale} scale):")
        
        if "Local" in deployment:
            print("   • Use Docker Compose for multi-service setup")
            print("   • Include database, API, and vector DB services")
            print("   • Hot reload for development")
        
        elif "Cloud" in deployment:
            print("   • Consider containerization (Docker)")
            print("   • Use managed databases")
            print("   • Implement auto-scaling")
            print("   • Set up monitoring and logging")
        
        elif "PaaS" in deployment:
            print("   • Simple git-based deployment")
            print("   • Environment variable configuration")
            print("   • Built-in scaling options")
        
        elif "Serverless" in deployment:
            print("   • Function-based architecture")
            print("   • Cold start considerations for LLM")
            print("   • Use managed vector databases")
    
    def save_session(self):
        """Save session data for later reference."""
        try:
            with open("backend_assistant_session.json", "w") as f:
                json.dump(self.session_data, f, indent=2)
            print("\n💾 Session saved to backend_assistant_session.json")
        except Exception as e:
            print(f"⚠️ Could not save session: {e}")
    
    def run(self):
        """Run the interactive assistant."""
        try:
            self.display_welcome()
            
            steps = [
                self.step_1_frontend_analysis,
                self.step_2_backend_framework,
                self.step_3_llm_integration,
                self.step_4_data_structure,
                self.step_5_api_design,
                self.step_6_authentication_security,
                self.step_7_deployment_scalability,
                self.step_8_communication_method
            ]
            
            for i, step in enumerate(steps, 1):
                try:
                    step()
                    self.session_data["current_step"] = i + 1
                    
                    # Ask if user wants to continue
                    if i < len(steps):
                        continue_question = "Ready to continue to the next step?"
                        continue_options = ["Yes, continue", "No, let me review this step"]
                        
                        if "No" in self.ask_question(continue_question, continue_options):
                            print("\n⏸️ Feel free to review the information above.")
                            print("Run the assistant again when you're ready to continue!")
                            self.save_session()
                            return
                
                except KeyboardInterrupt:
                    print("\n\n⏸️ Assistant paused. Your progress has been saved.")
                    self.save_session()
                    return
                except Exception as e:
                    print(f"\n❌ Error in step {i}: {e}")
                    print("Don't worry, you can restart the assistant anytime!")
                    return
            
            # Generate final implementation plan
            self.generate_implementation_plan()
            self.save_session()
            
            print("\n🎉 Congratulations! You have a complete backend development plan.")
            print("Check the framework-specific guides in backend-guide/frameworks/ to start coding!")
            
        except KeyboardInterrupt:
            print("\n\n👋 Thanks for using the Backend Development Assistant!")
            print("Run it again anytime: python backend-guide/assistant.py")


def main():
    """Main entry point."""
    assistant = BackendAssistant()
    assistant.run()


if __name__ == "__main__":
    main()