# Frontend Integration Template

This template shows how to properly integrate your React frontend with the FastAPI backend.

## 🔄 Updated getQuotation Function

Replace the placeholder function in `src/pages/chat.jsx`:

```javascript
// Updated getQuotation function with proper API integration
const getQuotation = async () => {
  console.log("Generating quotation with data:", formData);
  
  try {
    // Show loading state
    setIsLoading(true);
    
    // Prepare API request
    const apiUrl = process.env.REACT_APP_API_URL || 'http://localhost:8000';
    const response = await fetch(`${apiUrl}/api/quote`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        age: parseInt(formData.age),
        medical_history: formData.medicalHistory,
        lifestyle: formData.lifestyle,
        coverage_need: formData.coverageNeed
      })
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const quoteData = await response.json();
    console.log("Received quote:", quoteData);
    
    // Update UI with real quote data
    setQuoteData(quoteData);
    setIsLoading(false);
    
    return quoteData;
    
  } catch (error) {
    console.error("Error generating quote:", error);
    setIsLoading(false);
    
    // Show error message to user
    sendBotMessage(
      "I'm sorry, I encountered an error while generating your quote. Please try again or contact support if the issue persists.",
      ["Try again", "Contact support"]
    );
    
    // Return fallback quote
    return getFallbackQuote();
  }
};

// Add fallback quote function
const getFallbackQuote = () => {
  return {
    quote_id: "fallback_" + Date.now(),
    plan: {
      name: "Standard Health Plan",
      monthly_premium: 285,
      annual_deductible: 1500,
      out_of_pocket_max: 5000,
      coverage_type: "standard",
      network_type: "PPO"
    },
    benefits: [
      "Primary care visits: $25 copay",
      "Preventive care: Covered 100%", 
      "Emergency room: $250 copay"
    ],
    recommendations: [
      "This is a fallback quote - please try again for personalized results"
    ],
    confidence_score: 0.5,
    generated_at: new Date().toISOString()
  };
};
```

## 🔧 Environment Configuration

Create `.env` file in your React project root:

```env
# Backend API Configuration
REACT_APP_API_URL=http://localhost:8000
REACT_APP_API_TIMEOUT=30000

# Feature flags
REACT_APP_ENABLE_REAL_TIME_CHAT=false
REACT_APP_ENABLE_OFFLINE_MODE=false
```

## 📱 Enhanced Chat Component

Here's an enhanced version of the chat component with better API integration:

```javascript
import React, { useState, useRef, useEffect } from "react";
import { useForm } from "react-hook-form";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Progress } from "@/components/ui/progress";
import { Send, Download, Bot, User, AlertCircle, CheckCircle } from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { NavLink } from "react-router";

// API configuration
const API_CONFIG = {
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000',
  timeout: parseInt(process.env.REACT_APP_API_TIMEOUT) || 30000,
  retries: 3
};

const ChatPage = () => {
  const { register, handleSubmit, reset } = useForm();
  const chatContainerRef = useRef(null);
  
  // State management
  const [messages, setMessages] = useState([
    {
      id: "welcome",
      content: "Hi there! I'm your insurance assistant. I'll help you find the perfect insurance plan based on your health history and needs. Ready to get started?",
      sender: "bot",
      options: ["Yes, let's begin", "Tell me more first"],
    },
  ]);
  
  const [showQuote, setShowQuote] = useState(false);
  const [currentStage, setCurrentStage] = useState(0);
  const [introCompleted, setIntroCompleted] = useState(false);
  const [currentQuestionKey, setCurrentQuestionKey] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [quoteData, setQuoteData] = useState(null);
  const [error, setError] = useState(null);
  const [apiStatus, setApiStatus] = useState('unknown'); // 'unknown', 'online', 'offline'
  
  const [stages, setStages] = useState([
    { name: "Basic Info", completed: false },
    { name: "Health History", completed: false },
    { name: "Lifestyle", completed: false },
    { name: "Coverage Needs", completed: false },
    { name: "Quote Generation", completed: false },
  ]);
  
  const [formData, setFormData] = useState({
    age: "",
    medicalHistory: "",
    lifestyle: "",
    coverageNeed: "",
  });

  // Check API status on component mount
  useEffect(() => {
    checkApiStatus();
  }, []);

  const checkApiStatus = async () => {
    try {
      const response = await fetch(`${API_CONFIG.baseURL}/health`, {
        method: 'GET',
        timeout: 5000
      });
      
      if (response.ok) {
        setApiStatus('online');
        setError(null);
      } else {
        setApiStatus('offline');
        setError('Backend service is not responding properly');
      }
    } catch (error) {
      console.error('API health check failed:', error);
      setApiStatus('offline');
      setError('Cannot connect to backend service');
    }
  };

  // Enhanced API call with retry logic
  const makeApiCall = async (url, options, retries = API_CONFIG.retries) => {
    for (let i = 0; i < retries; i++) {
      try {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), API_CONFIG.timeout);
        
        const response = await fetch(url, {
          ...options,
          signal: controller.signal
        });
        
        clearTimeout(timeoutId);
        
        if (!response.ok) {
          throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        
        return await response.json();
        
      } catch (error) {
        console.error(`API call attempt ${i + 1} failed:`, error);
        
        if (i === retries - 1) {
          throw error;
        }
        
        // Wait before retry (exponential backoff)
        await new Promise(resolve => setTimeout(resolve, Math.pow(2, i) * 1000));
      }
    }
  };

  const getQuotation = async () => {
    console.log("Generating quotation with data:", formData);
    
    try {
      setIsLoading(true);
      setError(null);
      
      // Validate form data
      if (!formData.age || !formData.medicalHistory || !formData.lifestyle || !formData.coverageNeed) {
        throw new Error("Missing required information for quote generation");
      }
      
      const quoteRequest = {
        age: parseInt(formData.age),
        medical_history: formData.medicalHistory,
        lifestyle: formData.lifestyle,
        coverage_need: formData.coverageNeed
      };
      
      console.log("Sending quote request:", quoteRequest);
      
      const quoteData = await makeApiCall(`${API_CONFIG.baseURL}/api/quote`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(quoteRequest)
      });
      
      console.log("Received quote:", quoteData);
      setQuoteData(quoteData);
      setApiStatus('online');
      
      return quoteData;
      
    } catch (error) {
      console.error("Error generating quote:", error);
      setError(error.message);
      setApiStatus('offline');
      
      // Show error message to user
      sendBotMessage(
        "I'm sorry, I encountered an error while generating your quote. Please try again or contact support if the issue persists.",
        ["Try again", "Contact support"]
      );
      
      // Return fallback quote if API is unavailable
      return getFallbackQuote();
      
    } finally {
      setIsLoading(false);
    }
  };

  const getFallbackQuote = () => {
    // Calculate basic quote based on age
    const baseQuote = {
      quote_id: `fallback_${Date.now()}`,
      plan: {
        plan_id: "fallback_plan",
        name: "Standard Health Plan",
        provider: "HealthCorp",
        monthly_premium: Math.max(200, parseInt(formData.age) * 5),
        annual_deductible: 1500,
        out_of_pocket_max: 5000,
        coverage_type: "standard",
        network_type: "PPO"
      },
      benefits: [
        "Primary care visits: $25 copay",
        "Preventive care: Covered 100%",
        "Emergency room: $250 copay",
        "Prescription drugs: Generic $10, Brand $40"
      ],
      recommendations: [
        "This is an estimated quote based on basic calculations",
        "Connect to our backend service for personalized recommendations",
        "Contact an insurance broker for detailed analysis"
      ],
      confidence_score: 0.6,
      generated_at: new Date().toISOString()
    };
    
    setQuoteData(baseQuote);
    return baseQuote;
  };

  // Rest of your existing component logic...
  // (processUserResponse, handleUserMessage, etc.)

  const processUserResponse = (userContent) => {
    setTimeout(async () => {
      if (!introCompleted) {
        if (userContent === "Yes, let's begin") {
          setIntroCompleted(true);
          sendBotMessage("Great! Let's start with some basic information. What's your age?");
          setCurrentQuestionKey("age");
          setCurrentStage(1);
          updateStageCompletion(0);
        } else if (userContent === "Tell me more first") {
          sendBotMessage(
            "I'm here to guide you through a few simple questions about your health and lifestyle. Based on your answers, I'll recommend the best insurance plans for you!",
            ["Okay, let's begin"]
          );
        } else if (userContent === "Okay, let's begin") {
          setIntroCompleted(true);
          sendBotMessage("Awesome! Let's start with your basic information. What's your age?");
          setCurrentQuestionKey("age");
          setCurrentStage(1);
          updateStageCompletion(0);
        }
      } else {
        if (currentStage === 1) {
          sendBotMessage("Thanks! Do you have any pre-existing medical conditions?", []);
          setCurrentQuestionKey("medicalHistory");
          setCurrentStage(2);
          updateStageCompletion(1);
        } else if (currentStage === 2) {
          sendBotMessage("How would you describe your lifestyle?", [
            "Sedentary",
            "Moderately active", 
            "Very active",
          ]);
          setCurrentQuestionKey("lifestyle");
          setCurrentStage(3);
          updateStageCompletion(2);
        } else if (currentStage === 3) {
          sendBotMessage("What type of coverage are you looking for?", [
            "Basic health insurance",
            "Comprehensive coverage",
            "Specialized coverage",
          ]);
          setCurrentQuestionKey("coverageNeed");
          setCurrentStage(4);
          updateStageCompletion(3);
        } else if (currentStage === 4) {
          sendBotMessage("Thank you! I'm generating your personalized insurance quote...");
          updateStageCompletion(4);
          
          setTimeout(async () => {
            try {
              await getQuotation();
              setShowQuote(true);
            } catch (error) {
              console.error("Quote generation failed:", error);
              // Error handling is done in getQuotation
            }
          }, 2000);
        }
      }
    }, 800);
  };

  // API Status indicator component
  const ApiStatusIndicator = () => (
    <div className="mb-4">
      {apiStatus === 'offline' && (
        <Alert variant="destructive">
          <AlertCircle className="h-4 w-4" />
          <AlertDescription>
            Backend service unavailable. Quotes will be estimated. 
            <Button variant="link" onClick={checkApiStatus} className="p-0 ml-2">
              Retry connection
            </Button>
          </AlertDescription>
        </Alert>
      )}
      {apiStatus === 'online' && error === null && (
        <Alert>
          <CheckCircle className="h-4 w-4" />
          <AlertDescription>
            Connected to backend service. Personalized quotes available.
          </AlertDescription>
        </Alert>
      )}
    </div>
  );

  // Enhanced quote display with API data
  const QuoteDisplay = () => {
    if (!quoteData) return null;

    const { plan, benefits, recommendations, confidence_score } = quoteData;

    return (
      <Card className="p-6 border-2 border-blue-200 dark:border-blue-900">
        <div className="text-center mb-6">
          <h2 className="text-2xl font-bold text-blue-900 mb-2 dark:text-blue-400">
            Your Personalized Insurance Quote
          </h2>
          <p className="text-gray-600 dark:text-gray-400">
            Based on your health profile and needs
          </p>
          {confidence_score && (
            <div className="mt-2">
              <span className="text-sm text-gray-500">
                Confidence Score: {Math.round(confidence_score * 100)}%
              </span>
            </div>
          )}
        </div>

        <div className="bg-blue-50 p-4 rounded-lg mb-6 dark:bg-blue-950">
          <h3 className="text-xl font-semibold text-blue-900 mb-3 dark:text-blue-400">
            Recommended Plan: {plan.name}
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <p><strong>Monthly Premium:</strong> ${plan.monthly_premium}</p>
              <p><strong>Annual Deductible:</strong> ${plan.annual_deductible}</p>
              <p><strong>Out-of-pocket Maximum:</strong> ${plan.out_of_pocket_max}</p>
            </div>
            <div>
              <p><strong>Coverage Type:</strong> {plan.coverage_type}</p>
              <p><strong>Network Type:</strong> {plan.network_type}</p>
              <p><strong>Provider:</strong> {plan.provider}</p>
            </div>
          </div>
        </div>

        {benefits && benefits.length > 0 && (
          <div className="mb-6">
            <h3 className="text-lg font-semibold text-blue-900 mb-3 dark:text-blue-400">
              Plan Benefits
            </h3>
            <ul className="list-disc pl-5 space-y-1 text-gray-700 dark:text-gray-300">
              {benefits.map((benefit, index) => (
                <li key={index}>{benefit}</li>
              ))}
            </ul>
          </div>
        )}

        {recommendations && recommendations.length > 0 && (
          <div className="mb-6">
            <h3 className="text-lg font-semibold text-blue-900 mb-3 dark:text-blue-400">
              Recommendations
            </h3>
            <ul className="list-disc pl-5 space-y-1 text-gray-700 dark:text-gray-300">
              {recommendations.map((rec, index) => (
                <li key={index}>{rec}</li>
              ))}
            </ul>
          </div>
        )}

        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <NavLink to="/print">
            <Button className="bg-blue-600 hover:bg-blue-700">
              <Download className="mr-2 h-4 w-4" /> Download Quote
            </Button>
          </NavLink>
        </div>

        <div className="mt-8 pt-6 border-t border-gray-200 text-center dark:border-gray-800">
          <p className="text-gray-600 mb-4 dark:text-gray-400">
            This quote can be used for negotiations with insurance brokers.
          </p>
          <NavLink to="/providers">
            <Button variant="link" className="text-blue-700 dark:text-blue-400">
              View Insurance Providers →
            </Button>
          </NavLink>
        </div>
      </Card>
    );
  };

  // Rest of your existing functions (updateStageCompletion, calculateProgress, etc.)
  
  return (
    <div className="container mx-auto max-w-4xl px-4 py-8">
      <h1 className="text-3xl font-bold text-center text-blue-900 mb-8 dark:text-blue-400">
        Insurance Quote Chat
      </h1>

      <ApiStatusIndicator />

      <div className="mb-8">
        <div className="flex justify-between mb-2">
          {stages.map((stage, index) => (
            <div key={index} className="text-xs text-center flex-1">
              <div
                className={`font-medium ${
                  stage.completed
                    ? "text-green-600 dark:text-green-400"
                    : "text-gray-500"
                }`}
              >
                {stage.name}
              </div>
            </div>
          ))}
        </div>
        <Progress value={calculateProgress()} className="h-2" />
      </div>

      {!showQuote ? (
        <>
          {/* Chat interface */}
          <div 
            ref={chatContainerRef}
            className="bg-gray-50 rounded-lg p-4 mb-4 h-[500px] overflow-y-auto border border-gray-200 dark:bg-gray-900 dark:border-gray-800"
          >
            {/* Your existing chat messages rendering */}
          </div>

          <form onSubmit={handleSubmit(onSubmit)} className="flex gap-2">
            <Input
              {...register("message")}
              placeholder="Type your message..."
              className="flex-grow"
              disabled={isLoading}
            />
            <Button 
              type="submit" 
              className="bg-blue-600 hover:bg-blue-700"
              disabled={isLoading}
            >
              {isLoading ? "..." : <Send className="h-4 w-4" />}
            </Button>
          </form>
        </>
      ) : (
        <QuoteDisplay />
      )}
    </div>
  );
};

export default ChatPage;
```

## 🔧 API Client Setup

Create a dedicated API client:

```javascript
// src/services/apiClient.js
class ApiClient {
  constructor(baseURL = process.env.REACT_APP_API_URL || 'http://localhost:8000') {
    this.baseURL = baseURL;
    this.timeout = parseInt(process.env.REACT_APP_API_TIMEOUT) || 30000;
  }

  async makeRequest(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    const controller = new AbortController();
    
    const timeoutId = setTimeout(() => controller.abort(), this.timeout);
    
    try {
      const response = await fetch(url, {
        headers: {
          'Content-Type': 'application/json',
          ...options.headers
        },
        signal: controller.signal,
        ...options
      });
      
      clearTimeout(timeoutId);
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }
      
      return await response.json();
    } catch (error) {
      clearTimeout(timeoutId);
      throw error;
    }
  }

  async generateQuote(userInput) {
    return this.makeRequest('/api/quote', {
      method: 'POST',
      body: JSON.stringify(userInput)
    });
  }

  async getProviders() {
    return this.makeRequest('/api/providers');
  }

  async chatMessage(message, context = null) {
    return this.makeRequest('/api/chat', {
      method: 'POST',
      body: JSON.stringify({ message, context })
    });
  }

  async healthCheck() {
    return this.makeRequest('/health');
  }
}

export default new ApiClient();
```

## 🧪 Testing Integration

Create integration tests:

```javascript
// src/services/__tests__/apiClient.test.js
import ApiClient from '../apiClient';

// Mock fetch
global.fetch = jest.fn();

describe('ApiClient', () => {
  beforeEach(() => {
    fetch.mockClear();
  });

  test('generates quote successfully', async () => {
    const mockQuote = {
      quote_id: 'test123',
      plan: { name: 'Test Plan', monthly_premium: 300 }
    };
    
    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => mockQuote
    });

    const userInput = {
      age: 30,
      medical_history: 'None',
      lifestyle: 'Active',
      coverage_need: 'Basic'
    };

    const result = await ApiClient.generateQuote(userInput);
    
    expect(fetch).toHaveBeenCalledWith(
      'http://localhost:8000/api/quote',
      expect.objectContaining({
        method: 'POST',
        body: JSON.stringify(userInput)
      })
    );
    
    expect(result).toEqual(mockQuote);
  });

  test('handles API errors gracefully', async () => {
    fetch.mockRejectedValueOnce(new Error('Network error'));

    await expect(
      ApiClient.generateQuote({})
    ).rejects.toThrow('Network error');
  });
});
```

## 🎯 Next Steps

1. **Replace the placeholder function** in your React app
2. **Test the integration** with your FastAPI backend
3. **Add error handling** for different scenarios
4. **Implement loading states** for better UX
5. **Add retry logic** for failed requests

This template provides a robust foundation for frontend-backend integration!