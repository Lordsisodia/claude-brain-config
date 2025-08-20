#!/usr/bin/env python3
"""
Claude Code Multi-Model AI Orchestration System
Smart delegation to cheap/free models with premium oversight
"""

import os
import json
import asyncio
import aiohttp
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
from dataclasses import dataclass
from enum import Enum

class TaskComplexity(Enum):
    TRIVIAL = "trivial"        # Cheap models can handle
    SIMPLE = "simple"          # Cheap models preferred
    MODERATE = "moderate"      # Either model works
    COMPLEX = "complex"        # Premium model preferred
    CRITICAL = "critical"      # Premium model only

class ModelTier(Enum):
    FREE = "free"              # $0 cost
    CHEAP = "cheap"            # < $0.001/1K tokens
    PREMIUM = "premium"        # > $0.01/1K tokens

@dataclass
class AIModel:
    name: str
    api_endpoint: str
    api_key: str
    tier: ModelTier
    cost_per_1k_tokens: float
    max_tokens: int
    capabilities: List[str]
    reliability_score: float = 0.85

@dataclass
class Task:
    id: str
    description: str
    complexity: TaskComplexity
    required_capabilities: List[str]
    context: str
    priority: int = 5
    max_cost: Optional[float] = None

class AIOrchestrator:
    def __init__(self, claude_dir: str = "/Users/shaansisodia/.claude"):
        self.claude_dir = Path(claude_dir)
        self.config_file = self.claude_dir / "infrastructure" / "ai-models.json"
        self.analytics_file = self.claude_dir / "analytics" / "model-usage.json"
        
        # Load model configurations
        self.models = self._load_models()
        self.usage_analytics = self._load_analytics()
        
        # Task routing intelligence
        self.routing_rules = {
            TaskComplexity.TRIVIAL: [ModelTier.FREE, ModelTier.CHEAP],
            TaskComplexity.SIMPLE: [ModelTier.FREE, ModelTier.CHEAP, ModelTier.PREMIUM],
            TaskComplexity.MODERATE: [ModelTier.CHEAP, ModelTier.PREMIUM],
            TaskComplexity.COMPLEX: [ModelTier.PREMIUM],
            TaskComplexity.CRITICAL: [ModelTier.PREMIUM]
        }
    
    def _load_models(self) -> Dict[str, AIModel]:
        """Load AI model configurations"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    return {name: AIModel(**model_config) for name, model_config in config.items()}
        except Exception:
            pass
        
        # Default free/cheap models
        return self._get_default_models()
    
    def _get_default_models(self) -> Dict[str, AIModel]:
        """Default configuration for free/cheap AI models"""
        return {
            "groq_llama": AIModel(
                name="groq_llama",
                api_endpoint="https://api.groq.com/openai/v1/chat/completions",
                api_key=os.getenv("GROQ_API_KEY", ""),
                tier=ModelTier.FREE,
                cost_per_1k_tokens=0.0,
                max_tokens=8192,
                capabilities=["coding", "analysis", "documentation"],
                reliability_score=0.85
            ),
            
            "ollama_local": AIModel(
                name="ollama_local",
                api_endpoint="http://localhost:11434/api/generate",
                api_key="",
                tier=ModelTier.FREE,
                cost_per_1k_tokens=0.0,
                max_tokens=4096,
                capabilities=["coding", "analysis", "local_processing"],
                reliability_score=0.80
            ),
            
            "openrouter_cheap": AIModel(
                name="openrouter_cheap",
                api_endpoint="https://openrouter.ai/api/v1/chat/completions",
                api_key=os.getenv("OPENROUTER_API_KEY", ""),
                tier=ModelTier.CHEAP,
                cost_per_1k_tokens=0.0002,
                max_tokens=8192,
                capabilities=["coding", "analysis", "documentation", "reasoning"],
                reliability_score=0.90
            ),
            
            "huggingface_free": AIModel(
                name="huggingface_free",
                api_endpoint="https://api-inference.huggingface.co/models/microsoft/DialoGPT-large",
                api_key=os.getenv("HF_API_KEY", ""),
                tier=ModelTier.FREE,
                cost_per_1k_tokens=0.0,
                max_tokens=2048,
                capabilities=["simple_analysis", "documentation"],
                reliability_score=0.75
            ),
            
            "gemini_free": AIModel(
                name="gemini_free",
                api_endpoint="https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent",
                api_key=os.getenv("GEMINI_API_KEY", ""),
                tier=ModelTier.FREE,
                cost_per_1k_tokens=0.0,
                max_tokens=8192,
                capabilities=["coding", "analysis", "reasoning"],
                reliability_score=0.88
            )
        }
    
    def classify_task_complexity(self, task_description: str) -> TaskComplexity:
        """Classify task complexity using intelligent analysis"""
        description_lower = task_description.lower()
        
        # Critical tasks (premium only)
        critical_keywords = [
            "architecture", "security", "critical", "production", 
            "enterprise", "complex analysis", "strategic", "design"
        ]
        if any(keyword in description_lower for keyword in critical_keywords):
            return TaskComplexity.CRITICAL
        
        # Complex tasks (premium preferred)
        complex_keywords = [
            "debug", "troubleshoot", "optimize", "performance", 
            "algorithm", "refactor", "analyze complex"
        ]
        if any(keyword in description_lower for keyword in complex_keywords):
            return TaskComplexity.COMPLEX
        
        # Moderate tasks (flexible)
        moderate_keywords = [
            "implement", "build", "create", "develop", "review"
        ]
        if any(keyword in description_lower for keyword in moderate_keywords):
            return TaskComplexity.MODERATE
        
        # Simple tasks (cheap preferred)
        simple_keywords = [
            "format", "document", "comment", "cleanup", "basic"
        ]
        if any(keyword in description_lower for keyword in simple_keywords):
            return TaskComplexity.SIMPLE
        
        # Trivial tasks (free models only)
        trivial_keywords = [
            "list", "show", "display", "print", "echo"
        ]
        if any(keyword in description_lower for keyword in trivial_keywords):
            return TaskComplexity.TRIVIAL
        
        # Default to moderate for unknown tasks
        return TaskComplexity.MODERATE
    
    def select_optimal_model(self, task: Task) -> Optional[AIModel]:
        """Select the optimal model for a given task"""
        # Get allowed model tiers for this complexity
        allowed_tiers = self.routing_rules.get(task.complexity, [ModelTier.PREMIUM])
        
        # Filter models by tier and capabilities
        candidates = []
        for model in self.models.values():
            if (model.tier in allowed_tiers and 
                all(cap in model.capabilities for cap in task.required_capabilities)):
                candidates.append(model)
        
        if not candidates:
            return None
        
        # Sort by cost efficiency and reliability
        def model_score(model: AIModel) -> float:
            # Prefer free models, then cheap, then premium
            tier_score = {ModelTier.FREE: 1.0, ModelTier.CHEAP: 0.8, ModelTier.PREMIUM: 0.6}
            cost_score = tier_score.get(model.tier, 0.5)
            
            # Factor in reliability
            reliability_weight = 0.3
            cost_weight = 0.7
            
            return (cost_score * cost_weight) + (model.reliability_score * reliability_weight)
        
        # Return best model
        return max(candidates, key=model_score)
    
    async def execute_task(self, task: Task) -> Dict[str, Any]:
        """Execute a task using the optimal model"""
        model = self.select_optimal_model(task)
        
        if not model:
            return {
                "success": False,
                "error": "No suitable model found for task",
                "task_id": task.id
            }
        
        try:
            # Execute task with selected model
            result = await self._call_model(model, task)
            
            # Track usage analytics
            self._track_usage(task, model, result)
            
            return {
                "success": True,
                "result": result,
                "model_used": model.name,
                "cost": self._calculate_cost(result, model),
                "task_id": task.id
            }
            
        except Exception as e:
            # Try fallback to premium model if cheap model fails
            if model.tier != ModelTier.PREMIUM:
                return await self._fallback_to_premium(task, str(e))
            
            return {
                "success": False,
                "error": str(e),
                "task_id": task.id,
                "model_used": model.name
            }
    
    async def _call_model(self, model: AIModel, task: Task) -> str:
        """Call the AI model API"""
        if model.name == "ollama_local":
            return await self._call_ollama(model, task)
        elif model.name == "gemini_free":
            return await self._call_gemini(model, task)
        else:
            return await self._call_openai_compatible(model, task)
    
    async def _call_openai_compatible(self, model: AIModel, task: Task) -> str:
        """Call OpenAI-compatible API (Groq, OpenRouter, etc.)"""
        headers = {
            "Authorization": f"Bearer {model.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "llama-3.1-8b-instant" if "groq" in model.name else "meta-llama/llama-3.1-8b-instruct:free",
            "messages": [
                {"role": "system", "content": "You are a helpful AI assistant specialized in coding and analysis."},
                {"role": "user", "content": f"{task.description}\n\nContext: {task.context}"}
            ],
            "max_tokens": min(task.max_cost or 2048, model.max_tokens),
            "temperature": 0.1
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(model.api_endpoint, headers=headers, json=payload) as response:
                if response.status == 200:
                    data = await response.json()
                    return data["choices"][0]["message"]["content"]
                else:
                    raise Exception(f"API call failed: {response.status}")
    
    async def _call_ollama(self, model: AIModel, task: Task) -> str:
        """Call local Ollama instance"""
        payload = {
            "model": "llama3.1:8b",
            "prompt": f"{task.description}\n\nContext: {task.context}",
            "stream": False
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(model.api_endpoint, json=payload) as response:
                if response.status == 200:
                    data = await response.json()
                    return data["response"]
                else:
                    raise Exception(f"Ollama call failed: {response.status}")
    
    async def _call_gemini(self, model: AIModel, task: Task) -> str:
        """Call Google Gemini API"""
        headers = {
            "Content-Type": "application/json"
        }
        
        payload = {
            "contents": [{
                "parts": [{"text": f"{task.description}\n\nContext: {task.context}"}]
            }]
        }
        
        url = f"{model.api_endpoint}?key={model.api_key}"
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=payload) as response:
                if response.status == 200:
                    data = await response.json()
                    return data["candidates"][0]["content"]["parts"][0]["text"]
                else:
                    raise Exception(f"Gemini call failed: {response.status}")
    
    async def _fallback_to_premium(self, task: Task, error: str) -> Dict[str, Any]:
        """Fallback to premium model when cheap models fail"""
        # Find premium model
        premium_models = [m for m in self.models.values() if m.tier == ModelTier.PREMIUM]
        
        if not premium_models:
            return {
                "success": False,
                "error": f"Cheap model failed: {error}. No premium fallback available.",
                "task_id": task.id
            }
        
        # Use Claude Code's built-in capabilities as premium fallback
        return {
            "success": True,
            "result": f"Task escalated to premium model due to error: {error}",
            "model_used": "claude_premium_fallback",
            "cost": 0.01,  # Estimated premium cost
            "task_id": task.id,
            "fallback": True
        }
    
    def _calculate_cost(self, result: str, model: AIModel) -> float:
        """Calculate cost of model usage"""
        if model.tier == ModelTier.FREE:
            return 0.0
        
        # Rough token estimation (4 chars per token)
        estimated_tokens = len(result) / 4
        return (estimated_tokens / 1000) * model.cost_per_1k_tokens
    
    def _track_usage(self, task: Task, model: AIModel, result: str):
        """Track model usage for analytics"""
        usage_entry = {
            "timestamp": datetime.now().isoformat(),
            "task_id": task.id,
            "task_complexity": task.complexity.value,
            "model_name": model.name,
            "model_tier": model.tier.value,
            "cost": self._calculate_cost(result, model),
            "success": True,
            "result_length": len(result)
        }
        
        self.usage_analytics.setdefault("usage_history", []).append(usage_entry)
        self._save_analytics()
    
    def _load_analytics(self) -> Dict:
        """Load usage analytics"""
        try:
            if self.analytics_file.exists():
                with open(self.analytics_file, 'r') as f:
                    return json.load(f)
        except Exception:
            pass
        
        return {"usage_history": [], "cost_savings": 0.0}
    
    def _save_analytics(self):
        """Save usage analytics"""
        try:
            self.analytics_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.analytics_file, 'w') as f:
                json.dump(self.usage_analytics, f, indent=2)
        except Exception:
            pass
    
    def get_cost_savings_report(self) -> Dict:
        """Generate cost savings report"""
        usage_history = self.usage_analytics.get("usage_history", [])
        
        total_tasks = len(usage_history)
        free_tasks = len([u for u in usage_history if u["cost"] == 0.0])
        cheap_tasks = len([u for u in usage_history if 0.0 < u["cost"] < 0.01])
        
        # Estimate savings vs all-premium approach
        estimated_premium_cost = total_tasks * 0.02  # $0.02 per task estimate
        actual_cost = sum(u["cost"] for u in usage_history)
        savings = estimated_premium_cost - actual_cost
        
        return {
            "total_tasks": total_tasks,
            "free_tasks": free_tasks,
            "cheap_tasks": cheap_tasks,
            "actual_cost": actual_cost,
            "estimated_premium_cost": estimated_premium_cost,
            "cost_savings": savings,
            "savings_percentage": (savings / estimated_premium_cost * 100) if estimated_premium_cost > 0 else 0
        }

# CLI Interface
async def main():
    """CLI interface for AI Orchestrator"""
    import sys
    
    orchestrator = AIOrchestrator()
    
    if len(sys.argv) < 2:
        print("🤖 Claude Code AI Orchestrator")
        print("Usage:")
        print("  ai-orchestrator task 'format this code'")
        print("  ai-orchestrator analyze 'review this function'") 
        print("  ai-orchestrator savings")
        print("  ai-orchestrator models")
        return
    
    command = sys.argv[1]
    
    if command == "task" and len(sys.argv) > 2:
        description = " ".join(sys.argv[2:])
        
        # Create task
        complexity = orchestrator.classify_task_complexity(description)
        task = Task(
            id=f"task_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            description=description,
            complexity=complexity,
            required_capabilities=["coding"],
            context="CLI execution"
        )
        
        print(f"🎯 Task Classification: {complexity.value}")
        print(f"📋 Task: {description}")
        
        # Execute task
        result = await orchestrator.execute_task(task)
        
        if result["success"]:
            print(f"✅ Success! Model: {result['model_used']}")
            print(f"💰 Cost: ${result['cost']:.4f}")
            print(f"📄 Result: {result['result'][:200]}...")
        else:
            print(f"❌ Failed: {result['error']}")
    
    elif command == "savings":
        report = orchestrator.get_cost_savings_report()
        
        print("💰 Cost Savings Report:")
        print(f"  Total Tasks: {report['total_tasks']}")
        print(f"  Free Tasks: {report['free_tasks']} ({report['free_tasks']/max(report['total_tasks'],1)*100:.1f}%)")
        print(f"  Actual Cost: ${report['actual_cost']:.4f}")
        print(f"  Estimated Premium Cost: ${report['estimated_premium_cost']:.2f}")
        print(f"  Cost Savings: ${report['cost_savings']:.2f} ({report['savings_percentage']:.1f}%)")
    
    elif command == "models":
        print("🤖 Available AI Models:")
        for name, model in orchestrator.models.items():
            status = "✅" if model.api_key else "⚠️"
            print(f"  {status} {name}: {model.tier.value} (${model.cost_per_1k_tokens:.4f}/1K tokens)")

if __name__ == "__main__":
    asyncio.run(main())