#!/usr/bin/env python3
"""
Token Usage Optimization and Cost Management System - Phase 2 Implementation
Intelligent token economy for cost-efficient AI operations
Based on CrewAI and TaskWeaver patterns for optimal resource usage
"""

import asyncio
import json
import time
from typing import Dict, List, Any, Optional, Tuple, Union
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import hashlib
from collections import defaultdict, deque
import numpy as np
import tiktoken
import re

# Token Optimization Strategies

class OptimizationStrategy(Enum):
    """Token optimization strategies"""
    COMPRESSION = "compression"              # Compress prompts and responses
    CACHING = "caching"                     # Cache and reuse responses
    BATCHING = "batching"                   # Batch similar requests
    SUMMARIZATION = "summarization"         # Summarize long contexts
    SELECTIVE = "selective"                 # Selective context inclusion
    STREAMING = "streaming"                 # Stream processing for efficiency
    PRUNING = "pruning"                     # Prune unnecessary tokens
    QUANTIZATION = "quantization"           # Reduce precision where possible

class ModelTier(Enum):
    """Model tiers for cost optimization"""
    PREMIUM = "premium"        # GPT-4, Claude Opus
    STANDARD = "standard"      # GPT-3.5, Claude Sonnet
    EFFICIENT = "efficient"    # Claude Haiku, GPT-3.5-turbo
    LOCAL = "local"           # Local models (Ollama)
    CACHED = "cached"         # Cached responses

class TokenType(Enum):
    """Types of tokens for tracking"""
    INPUT = "input"
    OUTPUT = "output"
    SYSTEM = "system"
    CACHED = "cached"
    COMPRESSED = "compressed"

@dataclass
class TokenUsage:
    """Token usage tracking"""
    model: str
    input_tokens: int
    output_tokens: int
    total_tokens: int
    cost: float
    timestamp: datetime = field(default_factory=datetime.utcnow)
    agent_id: Optional[str] = None
    task_id: Optional[str] = None
    optimization_applied: List[OptimizationStrategy] = field(default_factory=list)
    cache_hit: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class CostBudget:
    """Cost budget configuration"""
    daily_limit: float
    monthly_limit: float
    per_agent_limit: float
    per_task_limit: float
    alert_threshold: float = 0.8  # Alert at 80% of budget
    hard_stop_threshold: float = 0.95  # Stop at 95% of budget

@dataclass
class OptimizationResult:
    """Result of optimization attempt"""
    original_tokens: int
    optimized_tokens: int
    tokens_saved: int
    cost_saved: float
    strategies_applied: List[OptimizationStrategy]
    quality_score: float  # 0-1 score of maintained quality
    execution_time: float

class TokenOptimizationSystem:
    """
    Enterprise-grade token optimization and cost management system
    Reduces AI operational costs while maintaining quality
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or self._default_config()
        self.usage_tracker = UsageTracker()
        self.cost_calculator = CostCalculator()
        self.prompt_optimizer = PromptOptimizer()
        self.response_cache = ResponseCache(
            max_size=self.config["cache_max_size"],
            ttl_hours=self.config["cache_ttl_hours"]
        )
        self.batch_processor = BatchProcessor()
        self.model_router = IntelligentModelRouter()
        self.budget_manager = BudgetManager(self.config["budget"])
        self.compression_engine = CompressionEngine()
        self.context_manager = ContextManager()
        self._initialize_tokenizers()
        
    def _default_config(self) -> Dict[str, Any]:
        """Default optimization configuration"""
        return {
            "optimization_level": "aggressive",  # conservative, moderate, aggressive
            "cache_enabled": True,
            "cache_max_size": 10000,
            "cache_ttl_hours": 24,
            "batch_enabled": True,
            "batch_size": 10,
            "batch_wait_ms": 100,
            "compression_enabled": True,
            "compression_ratio_target": 0.7,
            "smart_routing_enabled": True,
            "budget": {
                "daily_limit": 100.0,
                "monthly_limit": 2000.0,
                "per_agent_limit": 20.0,
                "per_task_limit": 5.0
            },
            "model_costs": {
                "gpt-4": {"input": 0.03, "output": 0.06},
                "gpt-3.5-turbo": {"input": 0.001, "output": 0.002},
                "claude-3-opus": {"input": 0.015, "output": 0.075},
                "claude-3-sonnet": {"input": 0.003, "output": 0.015},
                "claude-3-haiku": {"input": 0.00025, "output": 0.00125}
            }
        }
    
    def _initialize_tokenizers(self):
        """Initialize tokenizers for different models"""
        self.tokenizers = {
            "gpt": tiktoken.get_encoding("cl100k_base"),
            "claude": tiktoken.get_encoding("cl100k_base"),  # Approximation
        }
    
    async def optimize_request(self, prompt: str, model: str = None,
                              agent_id: str = None, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Optimize a request before sending to model"""
        
        start_time = time.time()
        original_tokens = self._count_tokens(prompt, model)
        
        # Check cache first
        if self.config["cache_enabled"]:
            cached_response = await self.response_cache.get(prompt, model)
            if cached_response:
                return {
                    "optimized_prompt": prompt,
                    "response": cached_response["response"],
                    "model_used": ModelTier.CACHED.value,
                    "tokens_used": 0,
                    "cost": 0.0,
                    "cache_hit": True,
                    "optimization_time": time.time() - start_time
                }
        
        # Check budget
        budget_check = await self.budget_manager.check_budget(agent_id)
        if not budget_check["allowed"]:
            return {
                "error": "Budget exceeded",
                "reason": budget_check["reason"],
                "limit": budget_check["limit"],
                "used": budget_check["used"]
            }
        
        # Route to optimal model
        if self.config["smart_routing_enabled"]:
            model = await self.model_router.select_model(prompt, context)
        
        # Apply optimization strategies
        optimization_results = []
        optimized_prompt = prompt
        
        # 1. Compression
        if self.config["compression_enabled"]:
            compressed = await self.compression_engine.compress(optimized_prompt)
            if compressed["success"]:
                optimized_prompt = compressed["compressed_text"]
                optimization_results.append(OptimizationStrategy.COMPRESSION)
        
        # 2. Context pruning
        if context:
            pruned_context = await self.context_manager.prune_context(context, optimized_prompt)
            if pruned_context["pruned"]:
                optimized_prompt = self._apply_pruned_context(optimized_prompt, pruned_context)
                optimization_results.append(OptimizationStrategy.PRUNING)
        
        # 3. Selective inclusion
        selective_result = await self.prompt_optimizer.selective_include(optimized_prompt)
        if selective_result["optimized"]:
            optimized_prompt = selective_result["prompt"]
            optimization_results.append(OptimizationStrategy.SELECTIVE)
        
        # 4. Check for batching opportunity
        if self.config["batch_enabled"]:
            batch_result = await self.batch_processor.add_to_batch(
                optimized_prompt, model, agent_id
            )
            if batch_result["batched"]:
                optimization_results.append(OptimizationStrategy.BATCHING)
                # Return batch ticket for later retrieval
                return {
                    "batch_id": batch_result["batch_id"],
                    "estimated_completion": batch_result["estimated_completion"],
                    "optimization_strategies": optimization_results
                }
        
        # Calculate optimization metrics
        optimized_tokens = self._count_tokens(optimized_prompt, model)
        tokens_saved = original_tokens - optimized_tokens
        cost_saved = self.cost_calculator.calculate_savings(
            original_tokens, optimized_tokens, model
        )
        
        execution_time = time.time() - start_time
        
        return {
            "optimized_prompt": optimized_prompt,
            "model_selected": model,
            "original_tokens": original_tokens,
            "optimized_tokens": optimized_tokens,
            "tokens_saved": tokens_saved,
            "cost_saved": cost_saved,
            "optimization_strategies": optimization_results,
            "quality_score": await self._assess_quality(prompt, optimized_prompt),
            "optimization_time": execution_time
        }
    
    async def optimize_response(self, response: str, model: str,
                               agent_id: str = None) -> Dict[str, Any]:
        """Optimize model response for storage and transmission"""
        
        original_tokens = self._count_tokens(response, model)
        
        # Summarize if too long
        if original_tokens > 1000:
            summary = await self.compression_engine.summarize(response)
            if summary["success"]:
                return {
                    "optimized_response": summary["summary"],
                    "full_response": response,
                    "tokens_saved": original_tokens - summary["tokens"],
                    "strategy": OptimizationStrategy.SUMMARIZATION
                }
        
        return {
            "optimized_response": response,
            "tokens_saved": 0,
            "strategy": None
        }
    
    async def track_usage(self, usage: TokenUsage):
        """Track token usage for analytics and budgeting"""
        
        # Record usage
        await self.usage_tracker.record(usage)
        
        # Update budget
        await self.budget_manager.update_usage(
            usage.agent_id,
            usage.cost
        )
        
        # Cache response if successful
        if usage.output_tokens > 0 and not usage.cache_hit:
            await self.response_cache.store(
                usage.metadata.get("prompt", ""),
                usage.metadata.get("response", ""),
                usage.model
            )
        
        # Check for optimization opportunities
        if await self._should_optimize_further(usage):
            asyncio.create_task(self._background_optimization(usage))
    
    async def get_usage_analytics(self, period: str = "daily",
                                 agent_id: str = None) -> Dict[str, Any]:
        """Get detailed usage analytics"""
        
        analytics = await self.usage_tracker.get_analytics(period, agent_id)
        
        # Add cost breakdown
        analytics["cost_breakdown"] = self.cost_calculator.breakdown_costs(
            analytics["usage_by_model"]
        )
        
        # Add optimization effectiveness
        analytics["optimization_effectiveness"] = await self._calculate_optimization_effectiveness()
        
        # Add recommendations
        analytics["recommendations"] = await self._generate_recommendations(analytics)
        
        return analytics
    
    async def _assess_quality(self, original: str, optimized: str) -> float:
        """Assess quality preservation after optimization"""
        
        # Simple quality assessment (would use more sophisticated methods in production)
        
        # Check information preservation
        original_keywords = set(original.lower().split())
        optimized_keywords = set(optimized.lower().split())
        
        if not original_keywords:
            return 1.0
        
        keyword_preservation = len(original_keywords.intersection(optimized_keywords)) / len(original_keywords)
        
        # Check structure preservation
        original_sentences = len(original.split('.'))
        optimized_sentences = len(optimized.split('.'))
        structure_preservation = min(optimized_sentences / max(original_sentences, 1), 1.0)
        
        # Combined score
        quality_score = (keyword_preservation * 0.7 + structure_preservation * 0.3)
        
        return quality_score
    
    async def _should_optimize_further(self, usage: TokenUsage) -> bool:
        """Determine if further optimization is needed"""
        
        # Check if cost is high
        if usage.cost > self.config["budget"]["per_task_limit"] * 0.5:
            return True
        
        # Check if token usage is high
        if usage.total_tokens > 4000:
            return True
        
        # Check if no optimization was applied
        if not usage.optimization_applied:
            return True
        
        return False
    
    async def _background_optimization(self, usage: TokenUsage):
        """Perform background optimization analysis"""
        
        # Analyze usage patterns
        patterns = await self.usage_tracker.analyze_patterns(usage.agent_id)
        
        # Generate optimization suggestions
        suggestions = []
        
        if patterns["avg_tokens"] > 2000:
            suggestions.append("Consider using shorter prompts or chunking")
        
        if patterns["cache_hit_rate"] < 0.3:
            suggestions.append("Low cache hit rate - consider prompt standardization")
        
        if patterns["model_tier"] == "premium" and patterns["avg_complexity"] < 0.5:
            suggestions.append("Consider using standard tier models for simple tasks")
        
        # Store suggestions for agent
        await self._store_optimization_suggestions(usage.agent_id, suggestions)
    
    def _count_tokens(self, text: str, model: str = None) -> int:
        """Count tokens in text"""
        
        tokenizer_type = "gpt" if model and "gpt" in model.lower() else "claude"
        tokenizer = self.tokenizers.get(tokenizer_type, self.tokenizers["gpt"])
        
        try:
            return len(tokenizer.encode(text))
        except:
            # Fallback to approximation
            return len(text) // 4
    
    def _apply_pruned_context(self, prompt: str, pruned_context: Dict[str, Any]) -> str:
        """Apply pruned context to prompt"""
        
        # Replace context references with pruned versions
        context_str = json.dumps(pruned_context["context"], indent=2)
        
        # Simple replacement (would be more sophisticated in production)
        if "context:" in prompt.lower():
            parts = prompt.split("context:", 1)
            if len(parts) == 2:
                return parts[0] + "context:\n" + context_str
        
        return prompt

class PromptOptimizer:
    """Optimize prompts for token efficiency"""
    
    def __init__(self):
        self.optimization_rules = self._load_optimization_rules()
        self.template_cache = {}
    
    def _load_optimization_rules(self) -> List[Dict[str, Any]]:
        """Load prompt optimization rules"""
        return [
            {
                "pattern": r"\b(please|kindly|could you)\b",
                "replacement": "",
                "description": "Remove politeness tokens"
            },
            {
                "pattern": r"\s+",
                "replacement": " ",
                "description": "Normalize whitespace"
            },
            {
                "pattern": r"(\w+)\s+\1\b",
                "replacement": r"\1",
                "description": "Remove duplicate words"
            },
            {
                "pattern": r"\b(very|really|quite|rather)\s+",
                "replacement": "",
                "description": "Remove intensifiers"
            }
        ]
    
    async def optimize(self, prompt: str) -> Dict[str, Any]:
        """Optimize prompt for token efficiency"""
        
        original_length = len(prompt)
        optimized = prompt
        
        # Apply optimization rules
        for rule in self.optimization_rules:
            optimized = re.sub(rule["pattern"], rule["replacement"], optimized, flags=re.IGNORECASE)
        
        # Remove redundant instructions
        optimized = self._remove_redundant_instructions(optimized)
        
        # Compress numbered lists
        optimized = self._compress_lists(optimized)
        
        return {
            "original": prompt,
            "optimized": optimized.strip(),
            "reduction": 1 - (len(optimized) / original_length),
            "tokens_saved": (original_length - len(optimized)) // 4  # Approximate
        }
    
    async def selective_include(self, prompt: str) -> Dict[str, Any]:
        """Selectively include only necessary parts"""
        
        # Identify essential vs optional sections
        essential_markers = ["REQUIRED:", "MUST:", "CRITICAL:"]
        optional_markers = ["OPTIONAL:", "NICE TO HAVE:", "IF POSSIBLE:"]
        
        lines = prompt.split('\n')
        essential_lines = []
        optional_lines = []
        current_section = "essential"
        
        for line in lines:
            upper_line = line.upper()
            
            if any(marker in upper_line for marker in essential_markers):
                current_section = "essential"
            elif any(marker in upper_line for marker in optional_markers):
                current_section = "optional"
            
            if current_section == "essential" or not line.strip():
                essential_lines.append(line)
            else:
                optional_lines.append(line)
        
        # Build optimized prompt with only essentials
        optimized_prompt = '\n'.join(essential_lines)
        
        return {
            "prompt": optimized_prompt,
            "optimized": len(optional_lines) > 0,
            "optional_excluded": len(optional_lines)
        }
    
    def _remove_redundant_instructions(self, text: str) -> str:
        """Remove redundant instructions"""
        
        # Common redundant patterns
        redundant_patterns = [
            r"(Please )?(ensure|make sure) (that|to)",
            r"It (is|would be) (important|crucial|essential) (to|that)",
            r"(Please )?(remember|note|keep in mind) (that|to)",
        ]
        
        for pattern in redundant_patterns:
            text = re.sub(pattern, "", text, flags=re.IGNORECASE)
        
        return text
    
    def _compress_lists(self, text: str) -> str:
        """Compress numbered or bulleted lists"""
        
        # Convert verbose lists to compact format
        text = re.sub(r"^\s*[-*]\s+", "• ", text, flags=re.MULTILINE)
        text = re.sub(r"^\s*\d+\.\s+", lambda m: f"{m.group().strip()} ", text, flags=re.MULTILINE)
        
        return text

class ResponseCache:
    """Cache system for response reuse"""
    
    def __init__(self, max_size: int, ttl_hours: int):
        self.max_size = max_size
        self.ttl = timedelta(hours=ttl_hours)
        self.cache = {}
        self.access_times = {}
        self.hit_count = defaultdict(int)
        self.miss_count = defaultdict(int)
    
    async def get(self, prompt: str, model: str) -> Optional[Dict[str, Any]]:
        """Get cached response"""
        
        cache_key = self._generate_key(prompt, model)
        
        if cache_key in self.cache:
            entry = self.cache[cache_key]
            
            # Check if expired
            if datetime.utcnow() - entry["timestamp"] < self.ttl:
                self.hit_count[model] += 1
                self.access_times[cache_key] = datetime.utcnow()
                return entry
            else:
                # Expired, remove
                del self.cache[cache_key]
        
        self.miss_count[model] += 1
        return None
    
    async def store(self, prompt: str, response: str, model: str) -> bool:
        """Store response in cache"""
        
        cache_key = self._generate_key(prompt, model)
        
        # Check cache size limit
        if len(self.cache) >= self.max_size:
            await self._evict_oldest()
        
        self.cache[cache_key] = {
            "response": response,
            "timestamp": datetime.utcnow(),
            "model": model
        }
        
        return True
    
    def _generate_key(self, prompt: str, model: str) -> str:
        """Generate cache key"""
        
        # Normalize prompt for better cache hits
        normalized = prompt.lower().strip()
        normalized = re.sub(r'\s+', ' ', normalized)
        
        key_str = f"{model}:{normalized}"
        return hashlib.md5(key_str.encode()).hexdigest()
    
    async def _evict_oldest(self):
        """Evict oldest cache entries"""
        
        if not self.access_times:
            # No access times, evict oldest by timestamp
            oldest_key = min(self.cache.keys(), 
                           key=lambda k: self.cache[k]["timestamp"])
        else:
            # Evict least recently accessed
            oldest_key = min(self.access_times.keys(), 
                           key=lambda k: self.access_times.get(k, datetime.min))
        
        if oldest_key in self.cache:
            del self.cache[oldest_key]
        if oldest_key in self.access_times:
            del self.access_times[oldest_key]
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        
        total_hits = sum(self.hit_count.values())
        total_misses = sum(self.miss_count.values())
        
        return {
            "size": len(self.cache),
            "max_size": self.max_size,
            "hit_rate": total_hits / max(total_hits + total_misses, 1),
            "total_hits": total_hits,
            "total_misses": total_misses,
            "hits_by_model": dict(self.hit_count),
            "misses_by_model": dict(self.miss_count)
        }

class BatchProcessor:
    """Batch similar requests for efficiency"""
    
    def __init__(self, batch_size: int = 10, wait_time_ms: int = 100):
        self.batch_size = batch_size
        self.wait_time = wait_time_ms / 1000.0
        self.batches = defaultdict(list)
        self.batch_futures = {}
    
    async def add_to_batch(self, prompt: str, model: str, 
                          agent_id: str) -> Dict[str, Any]:
        """Add request to batch"""
        
        batch_key = f"{model}:{self._get_prompt_category(prompt)}"
        
        batch_item = {
            "prompt": prompt,
            "agent_id": agent_id,
            "timestamp": time.time(),
            "future": asyncio.Future()
        }
        
        self.batches[batch_key].append(batch_item)
        
        # Check if batch is ready
        if len(self.batches[batch_key]) >= self.batch_size:
            asyncio.create_task(self._process_batch(batch_key))
        elif len(self.batches[batch_key]) == 1:
            # First item, start timer
            asyncio.create_task(self._batch_timer(batch_key))
        
        return {
            "batched": True,
            "batch_id": batch_key,
            "position": len(self.batches[batch_key]),
            "estimated_completion": time.time() + self.wait_time
        }
    
    async def _batch_timer(self, batch_key: str):
        """Timer to process batch after wait time"""
        
        await asyncio.sleep(self.wait_time)
        
        if batch_key in self.batches and self.batches[batch_key]:
            await self._process_batch(batch_key)
    
    async def _process_batch(self, batch_key: str):
        """Process a batch of requests"""
        
        if batch_key not in self.batches:
            return
        
        batch = self.batches[batch_key]
        del self.batches[batch_key]
        
        # Combine prompts intelligently
        combined_prompt = self._combine_prompts([item["prompt"] for item in batch])
        
        # Process combined request (would call actual model in production)
        result = await self._execute_batch_request(combined_prompt, batch_key.split(":")[0])
        
        # Distribute results
        responses = self._split_responses(result, len(batch))
        
        for item, response in zip(batch, responses):
            item["future"].set_result(response)
    
    def _get_prompt_category(self, prompt: str) -> str:
        """Categorize prompt for batching"""
        
        # Simple categorization (would be more sophisticated in production)
        if "code" in prompt.lower() or "implement" in prompt.lower():
            return "coding"
        elif "analyze" in prompt.lower() or "review" in prompt.lower():
            return "analysis"
        elif "test" in prompt.lower() or "verify" in prompt.lower():
            return "testing"
        else:
            return "general"
    
    def _combine_prompts(self, prompts: List[str]) -> str:
        """Combine multiple prompts into one"""
        
        combined = "Process the following requests:\n\n"
        
        for i, prompt in enumerate(prompts, 1):
            combined += f"Request {i}:\n{prompt}\n\n"
        
        combined += "Provide responses for each request separately."
        
        return combined
    
    async def _execute_batch_request(self, combined_prompt: str, model: str) -> str:
        """Execute batch request (placeholder)"""
        
        # In production, would call actual model
        return f"Response for batch with {combined_prompt.count('Request')} requests"
    
    def _split_responses(self, combined_response: str, count: int) -> List[str]:
        """Split combined response into individual responses"""
        
        # Simple split (would be more sophisticated in production)
        responses = []
        
        for i in range(count):
            responses.append(f"Response {i+1}: Processed successfully")
        
        return responses

class IntelligentModelRouter:
    """Route requests to optimal models based on complexity"""
    
    def __init__(self):
        self.complexity_analyzer = ComplexityAnalyzer()
        self.model_capabilities = self._load_model_capabilities()
    
    def _load_model_capabilities(self) -> Dict[str, Dict[str, Any]]:
        """Load model capabilities and costs"""
        return {
            "gpt-4": {
                "tier": ModelTier.PREMIUM,
                "max_complexity": 1.0,
                "cost_multiplier": 1.0,
                "capabilities": ["reasoning", "coding", "analysis", "creative"]
            },
            "gpt-3.5-turbo": {
                "tier": ModelTier.STANDARD,
                "max_complexity": 0.7,
                "cost_multiplier": 0.05,
                "capabilities": ["general", "coding", "summarization"]
            },
            "claude-3-opus": {
                "tier": ModelTier.PREMIUM,
                "max_complexity": 1.0,
                "cost_multiplier": 0.8,
                "capabilities": ["reasoning", "coding", "analysis", "long_context"]
            },
            "claude-3-sonnet": {
                "tier": ModelTier.STANDARD,
                "max_complexity": 0.8,
                "cost_multiplier": 0.2,
                "capabilities": ["general", "coding", "analysis"]
            },
            "claude-3-haiku": {
                "tier": ModelTier.EFFICIENT,
                "max_complexity": 0.5,
                "cost_multiplier": 0.01,
                "capabilities": ["general", "simple_tasks", "summarization"]
            }
        }
    
    async def select_model(self, prompt: str, context: Dict[str, Any] = None) -> str:
        """Select optimal model for request"""
        
        # Analyze prompt complexity
        complexity = await self.complexity_analyzer.analyze(prompt)
        
        # Determine required capabilities
        required_capabilities = self._determine_required_capabilities(prompt, context)
        
        # Filter compatible models
        compatible_models = []
        for model, specs in self.model_capabilities.items():
            if complexity <= specs["max_complexity"]:
                if any(cap in specs["capabilities"] for cap in required_capabilities):
                    compatible_models.append((model, specs))
        
        if not compatible_models:
            # Fallback to most capable
            return "gpt-4"
        
        # Select most cost-effective
        compatible_models.sort(key=lambda x: x[1]["cost_multiplier"])
        
        return compatible_models[0][0]
    
    def _determine_required_capabilities(self, prompt: str, 
                                        context: Dict[str, Any]) -> List[str]:
        """Determine required model capabilities"""
        
        capabilities = []
        
        prompt_lower = prompt.lower()
        
        if "code" in prompt_lower or "implement" in prompt_lower:
            capabilities.append("coding")
        
        if "analyze" in prompt_lower or "reasoning" in prompt_lower:
            capabilities.append("reasoning")
        
        if "creative" in prompt_lower or "generate" in prompt_lower:
            capabilities.append("creative")
        
        if len(prompt) > 4000:
            capabilities.append("long_context")
        
        if not capabilities:
            capabilities.append("general")
        
        return capabilities

class ComplexityAnalyzer:
    """Analyze prompt complexity"""
    
    async def analyze(self, prompt: str) -> float:
        """Analyze complexity of prompt (0-1)"""
        
        complexity_score = 0.0
        
        # Length factor
        length = len(prompt)
        if length > 2000:
            complexity_score += 0.3
        elif length > 1000:
            complexity_score += 0.2
        elif length > 500:
            complexity_score += 0.1
        
        # Technical terms
        technical_terms = [
            "algorithm", "optimize", "architecture", "implement",
            "analyze", "debug", "refactor", "security", "performance"
        ]
        
        prompt_lower = prompt.lower()
        technical_count = sum(1 for term in technical_terms if term in prompt_lower)
        complexity_score += min(technical_count * 0.05, 0.3)
        
        # Question complexity
        if "?" in prompt:
            question_count = prompt.count("?")
            complexity_score += min(question_count * 0.05, 0.2)
        
        # Code blocks
        if "```" in prompt or "def " in prompt or "class " in prompt:
            complexity_score += 0.2
        
        return min(complexity_score, 1.0)

class CompressionEngine:
    """Compress and decompress text for token savings"""
    
    async def compress(self, text: str) -> Dict[str, Any]:
        """Compress text while maintaining meaning"""
        
        original_length = len(text)
        
        # Remove redundancy
        compressed = self._remove_redundancy(text)
        
        # Abbreviate common phrases
        compressed = self._abbreviate_phrases(compressed)
        
        # Remove filler words
        compressed = self._remove_fillers(compressed)
        
        return {
            "success": len(compressed) < original_length * 0.9,
            "original_text": text,
            "compressed_text": compressed,
            "compression_ratio": len(compressed) / original_length,
            "tokens_saved": (original_length - len(compressed)) // 4
        }
    
    async def summarize(self, text: str) -> Dict[str, Any]:
        """Summarize long text"""
        
        # Simple extractive summarization
        sentences = text.split('.')
        
        if len(sentences) <= 3:
            return {
                "success": False,
                "summary": text,
                "tokens": len(text) // 4
            }
        
        # Score sentences by importance (simple keyword frequency)
        scores = []
        keywords = self._extract_keywords(text)
        
        for sentence in sentences:
            score = sum(1 for keyword in keywords if keyword in sentence.lower())
            scores.append((sentence, score))
        
        # Sort by score and take top sentences
        scores.sort(key=lambda x: x[1], reverse=True)
        summary_sentences = [s[0] for s in scores[:max(3, len(sentences) // 3)]]
        
        # Reconstruct in original order
        summary = '. '.join([s for s in sentences if s in summary_sentences])
        
        return {
            "success": True,
            "summary": summary,
            "tokens": len(summary) // 4,
            "compression_ratio": len(summary) / len(text)
        }
    
    def _remove_redundancy(self, text: str) -> str:
        """Remove redundant text"""
        
        # Remove repeated phrases
        lines = text.split('\n')
        seen = set()
        unique_lines = []
        
        for line in lines:
            line_hash = hash(line.strip().lower())
            if line_hash not in seen or not line.strip():
                seen.add(line_hash)
                unique_lines.append(line)
        
        return '\n'.join(unique_lines)
    
    def _abbreviate_phrases(self, text: str) -> str:
        """Abbreviate common phrases"""
        
        abbreviations = {
            "for example": "e.g.",
            "that is": "i.e.",
            "et cetera": "etc.",
            "versus": "vs.",
            "approximately": "~",
            "greater than": ">",
            "less than": "<",
            "equal to": "="
        }
        
        for phrase, abbr in abbreviations.items():
            text = text.replace(phrase, abbr)
            text = text.replace(phrase.title(), abbr)
        
        return text
    
    def _remove_fillers(self, text: str) -> str:
        """Remove filler words"""
        
        fillers = [
            "basically", "actually", "literally", "obviously",
            "simply", "just", "really", "very", "quite"
        ]
        
        for filler in fillers:
            text = re.sub(r'\b' + filler + r'\b\s*', '', text, flags=re.IGNORECASE)
        
        return text
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract keywords from text"""
        
        # Simple keyword extraction
        words = text.lower().split()
        
        # Remove common words
        stopwords = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at',
            'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were'
        }
        
        keywords = [w for w in words if w not in stopwords and len(w) > 3]
        
        # Return most frequent
        from collections import Counter
        word_counts = Counter(keywords)
        
        return [word for word, _ in word_counts.most_common(10)]

class ContextManager:
    """Manage context for optimal inclusion"""
    
    async def prune_context(self, context: Dict[str, Any], 
                           prompt: str) -> Dict[str, Any]:
        """Prune context to only relevant parts"""
        
        if not context:
            return {"pruned": False, "context": context}
        
        # Identify relevant keys based on prompt
        relevant_keys = self._identify_relevant_keys(prompt, context)
        
        # Build pruned context
        pruned = {}
        for key in relevant_keys:
            if key in context:
                pruned[key] = context[key]
        
        return {
            "pruned": len(pruned) < len(context),
            "context": pruned,
            "keys_removed": len(context) - len(pruned)
        }
    
    def _identify_relevant_keys(self, prompt: str, 
                               context: Dict[str, Any]) -> List[str]:
        """Identify relevant context keys"""
        
        relevant = []
        prompt_lower = prompt.lower()
        
        for key in context.keys():
            # Check if key is mentioned in prompt
            if key.lower() in prompt_lower:
                relevant.append(key)
            # Check if key contains critical information
            elif any(critical in key.lower() for critical in ["error", "required", "must"]):
                relevant.append(key)
        
        return relevant

class UsageTracker:
    """Track token usage and patterns"""
    
    def __init__(self):
        self.usage_history = deque(maxlen=10000)
        self.usage_by_agent = defaultdict(list)
        self.usage_by_model = defaultdict(list)
    
    async def record(self, usage: TokenUsage):
        """Record token usage"""
        
        self.usage_history.append(usage)
        
        if usage.agent_id:
            self.usage_by_agent[usage.agent_id].append(usage)
        
        self.usage_by_model[usage.model].append(usage)
    
    async def get_analytics(self, period: str, agent_id: str = None) -> Dict[str, Any]:
        """Get usage analytics"""
        
        # Filter by period
        now = datetime.utcnow()
        if period == "daily":
            cutoff = now - timedelta(days=1)
        elif period == "weekly":
            cutoff = now - timedelta(weeks=1)
        elif period == "monthly":
            cutoff = now - timedelta(days=30)
        else:
            cutoff = datetime.min
        
        # Filter usage
        filtered_usage = [u for u in self.usage_history if u.timestamp >= cutoff]
        
        if agent_id:
            filtered_usage = [u for u in filtered_usage if u.agent_id == agent_id]
        
        # Calculate analytics
        total_tokens = sum(u.total_tokens for u in filtered_usage)
        total_cost = sum(u.cost for u in filtered_usage)
        cache_hits = sum(1 for u in filtered_usage if u.cache_hit)
        
        return {
            "period": period,
            "total_tokens": total_tokens,
            "total_cost": total_cost,
            "request_count": len(filtered_usage),
            "cache_hit_rate": cache_hits / max(len(filtered_usage), 1),
            "avg_tokens_per_request": total_tokens / max(len(filtered_usage), 1),
            "avg_cost_per_request": total_cost / max(len(filtered_usage), 1),
            "usage_by_model": self._aggregate_by_model(filtered_usage),
            "optimization_strategies_used": self._aggregate_strategies(filtered_usage)
        }
    
    async def analyze_patterns(self, agent_id: str) -> Dict[str, Any]:
        """Analyze usage patterns for an agent"""
        
        agent_usage = self.usage_by_agent.get(agent_id, [])
        
        if not agent_usage:
            return {
                "avg_tokens": 0,
                "cache_hit_rate": 0,
                "model_tier": "standard",
                "avg_complexity": 0
            }
        
        recent_usage = agent_usage[-100:]  # Last 100 requests
        
        avg_tokens = sum(u.total_tokens for u in recent_usage) / len(recent_usage)
        cache_hits = sum(1 for u in recent_usage if u.cache_hit)
        cache_hit_rate = cache_hits / len(recent_usage)
        
        # Determine primary model tier
        model_tiers = [self._get_model_tier(u.model) for u in recent_usage]
        from collections import Counter
        tier_counts = Counter(model_tiers)
        primary_tier = tier_counts.most_common(1)[0][0] if tier_counts else "standard"
        
        return {
            "avg_tokens": avg_tokens,
            "cache_hit_rate": cache_hit_rate,
            "model_tier": primary_tier,
            "avg_complexity": 0.5  # Placeholder
        }
    
    def _aggregate_by_model(self, usage_list: List[TokenUsage]) -> Dict[str, Any]:
        """Aggregate usage by model"""
        
        by_model = defaultdict(lambda: {"tokens": 0, "cost": 0, "count": 0})
        
        for usage in usage_list:
            by_model[usage.model]["tokens"] += usage.total_tokens
            by_model[usage.model]["cost"] += usage.cost
            by_model[usage.model]["count"] += 1
        
        return dict(by_model)
    
    def _aggregate_strategies(self, usage_list: List[TokenUsage]) -> Dict[str, int]:
        """Aggregate optimization strategies used"""
        
        strategy_counts = defaultdict(int)
        
        for usage in usage_list:
            for strategy in usage.optimization_applied:
                strategy_counts[strategy.value] += 1
        
        return dict(strategy_counts)
    
    def _get_model_tier(self, model: str) -> str:
        """Get model tier"""
        
        if "gpt-4" in model or "opus" in model:
            return "premium"
        elif "3.5" in model or "sonnet" in model:
            return "standard"
        else:
            return "efficient"

class CostCalculator:
    """Calculate costs and savings"""
    
    def __init__(self):
        self.model_costs = {
            "gpt-4": {"input": 0.03 / 1000, "output": 0.06 / 1000},
            "gpt-3.5-turbo": {"input": 0.001 / 1000, "output": 0.002 / 1000},
            "claude-3-opus": {"input": 0.015 / 1000, "output": 0.075 / 1000},
            "claude-3-sonnet": {"input": 0.003 / 1000, "output": 0.015 / 1000},
            "claude-3-haiku": {"input": 0.00025 / 1000, "output": 0.00125 / 1000}
        }
    
    def calculate_cost(self, input_tokens: int, output_tokens: int, 
                      model: str) -> float:
        """Calculate cost for token usage"""
        
        costs = self.model_costs.get(model, self.model_costs["gpt-3.5-turbo"])
        
        input_cost = input_tokens * costs["input"]
        output_cost = output_tokens * costs["output"]
        
        return input_cost + output_cost
    
    def calculate_savings(self, original_tokens: int, optimized_tokens: int, 
                         model: str) -> float:
        """Calculate cost savings from optimization"""
        
        costs = self.model_costs.get(model, self.model_costs["gpt-3.5-turbo"])
        
        tokens_saved = original_tokens - optimized_tokens
        savings = tokens_saved * costs["input"]
        
        return savings
    
    def breakdown_costs(self, usage_by_model: Dict[str, Any]) -> Dict[str, Any]:
        """Break down costs by model"""
        
        breakdown = {}
        total_cost = 0
        
        for model, usage in usage_by_model.items():
            model_cost = usage.get("cost", 0)
            breakdown[model] = {
                "cost": model_cost,
                "percentage": 0,  # Will calculate after total
                "tokens": usage.get("tokens", 0),
                "requests": usage.get("count", 0)
            }
            total_cost += model_cost
        
        # Calculate percentages
        for model in breakdown:
            if total_cost > 0:
                breakdown[model]["percentage"] = breakdown[model]["cost"] / total_cost
        
        breakdown["total"] = total_cost
        
        return breakdown

class BudgetManager:
    """Manage cost budgets and limits"""
    
    def __init__(self, budget_config: Dict[str, Any]):
        self.budget = CostBudget(**budget_config)
        self.usage_today = defaultdict(float)
        self.usage_month = defaultdict(float)
        self.last_reset_daily = datetime.utcnow().date()
        self.last_reset_monthly = datetime.utcnow().replace(day=1).date()
    
    async def check_budget(self, agent_id: str = None) -> Dict[str, Any]:
        """Check if within budget"""
        
        self._reset_if_needed()
        
        # Check daily limit
        daily_total = sum(self.usage_today.values())
        if daily_total >= self.budget.daily_limit * self.budget.hard_stop_threshold:
            return {
                "allowed": False,
                "reason": "Daily budget exceeded",
                "limit": self.budget.daily_limit,
                "used": daily_total
            }
        
        # Check monthly limit
        monthly_total = sum(self.usage_month.values())
        if monthly_total >= self.budget.monthly_limit * self.budget.hard_stop_threshold:
            return {
                "allowed": False,
                "reason": "Monthly budget exceeded",
                "limit": self.budget.monthly_limit,
                "used": monthly_total
            }
        
        # Check per-agent limit
        if agent_id:
            agent_daily = self.usage_today.get(agent_id, 0)
            if agent_daily >= self.budget.per_agent_limit:
                return {
                    "allowed": False,
                    "reason": "Agent budget exceeded",
                    "limit": self.budget.per_agent_limit,
                    "used": agent_daily
                }
        
        return {
            "allowed": True,
            "daily_remaining": self.budget.daily_limit - daily_total,
            "monthly_remaining": self.budget.monthly_limit - monthly_total
        }
    
    async def update_usage(self, agent_id: str, cost: float):
        """Update usage tracking"""
        
        self._reset_if_needed()
        
        self.usage_today[agent_id] += cost
        self.usage_month[agent_id] += cost
        
        # Check for alerts
        daily_total = sum(self.usage_today.values())
        if daily_total >= self.budget.daily_limit * self.budget.alert_threshold:
            await self._send_alert("Daily budget alert", daily_total, self.budget.daily_limit)
        
        monthly_total = sum(self.usage_month.values())
        if monthly_total >= self.budget.monthly_limit * self.budget.alert_threshold:
            await self._send_alert("Monthly budget alert", monthly_total, self.budget.monthly_limit)
    
    def _reset_if_needed(self):
        """Reset usage counters if needed"""
        
        today = datetime.utcnow().date()
        
        # Reset daily
        if today > self.last_reset_daily:
            self.usage_today.clear()
            self.last_reset_daily = today
        
        # Reset monthly
        month_start = today.replace(day=1)
        if month_start > self.last_reset_monthly:
            self.usage_month.clear()
            self.last_reset_monthly = month_start
    
    async def _send_alert(self, message: str, used: float, limit: float):
        """Send budget alert"""
        
        print(f"⚠️ BUDGET ALERT: {message}")
        print(f"   Used: ${used:.2f} / ${limit:.2f} ({used/limit*100:.1f}%)")

# Example usage

async def main():
    """Example usage of Token Optimization System"""
    
    # Initialize optimization system
    optimizer = TokenOptimizationSystem()
    
    # Example prompt
    prompt = """
    Please analyze the following code and provide detailed feedback on:
    1. Code quality and best practices
    2. Performance optimization opportunities
    3. Security vulnerabilities
    4. Testing recommendations
    5. Documentation improvements
    
    The code should follow industry standards and be production-ready.
    Please ensure all feedback is actionable and specific.
    """
    
    # Optimize the prompt
    print("🔧 Optimizing prompt...")
    optimization_result = await optimizer.optimize_request(
        prompt=prompt,
        agent_id="developer",
        context={"task_type": "code_review"}
    )
    
    print(f"✅ Optimization complete:")
    print(f"   Original tokens: {optimization_result.get('original_tokens', 'N/A')}")
    print(f"   Optimized tokens: {optimization_result.get('optimized_tokens', 'N/A')}")
    print(f"   Tokens saved: {optimization_result.get('tokens_saved', 0)}")
    print(f"   Cost saved: ${optimization_result.get('cost_saved', 0):.4f}")
    print(f"   Model selected: {optimization_result.get('model_selected', 'N/A')}")
    print(f"   Strategies: {optimization_result.get('optimization_strategies', [])}")
    
    # Track usage
    usage = TokenUsage(
        model="gpt-3.5-turbo",
        input_tokens=optimization_result.get('optimized_tokens', 0),
        output_tokens=150,
        total_tokens=optimization_result.get('optimized_tokens', 0) + 150,
        cost=0.002,
        agent_id="developer",
        optimization_applied=optimization_result.get('optimization_strategies', [])
    )
    
    await optimizer.track_usage(usage)
    
    # Get analytics
    print("\n📊 Usage Analytics:")
    analytics = await optimizer.get_usage_analytics("daily", "developer")
    print(f"   Total tokens: {analytics['total_tokens']}")
    print(f"   Total cost: ${analytics['total_cost']:.4f}")
    print(f"   Cache hit rate: {analytics['cache_hit_rate']:.1%}")
    print(f"   Avg tokens/request: {analytics['avg_tokens_per_request']:.0f}")

if __name__ == "__main__":
    asyncio.run(main())