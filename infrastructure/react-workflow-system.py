#!/usr/bin/env python3
"""
ReAct Workflow Automation System - Phase 2 Implementation
Reasoning and Acting patterns for autonomous agent workflows
Based on LangGraph and AutoGen patterns for workflow orchestration
"""

import asyncio
import json
import time
from typing import Dict, List, Any, Optional, Tuple, Callable, Union
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import hashlib
from collections import defaultdict, deque
import networkx as nx
from abc import ABC, abstractmethod

# Workflow Types and States

class WorkflowState(Enum):
    """Workflow execution states"""
    PENDING = "pending"
    REASONING = "reasoning"
    ACTING = "acting"
    OBSERVING = "observing"
    COMPLETED = "completed"
    FAILED = "failed"
    PAUSED = "paused"
    CANCELLED = "cancelled"

class ActionType(Enum):
    """Types of actions in workflows"""
    TOOL_USE = "tool_use"
    AGENT_CALL = "agent_call"
    API_REQUEST = "api_request"
    DATABASE_QUERY = "database_query"
    COMPUTATION = "computation"
    DECISION = "decision"
    PARALLEL = "parallel"
    SEQUENTIAL = "sequential"

class ReasoningType(Enum):
    """Types of reasoning strategies"""
    CHAIN_OF_THOUGHT = "chain_of_thought"
    TREE_OF_THOUGHT = "tree_of_thought"
    REFLEXION = "reflexion"
    SELF_CONSISTENCY = "self_consistency"
    LEAST_TO_MOST = "least_to_most"
    ANALOGICAL = "analogical"

@dataclass
class WorkflowNode:
    """Node in workflow graph"""
    id: str
    name: str
    node_type: str  # reason, act, observe, decide
    function: Optional[Callable] = None
    dependencies: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    retry_policy: Dict[str, Any] = field(default_factory=dict)
    timeout_seconds: int = 300

@dataclass
class WorkflowEdge:
    """Edge in workflow graph"""
    source: str
    target: str
    condition: Optional[Callable] = None
    weight: float = 1.0
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ReasoningStep:
    """Individual reasoning step"""
    step_id: str
    thought: str
    evidence: List[str]
    confidence: float
    next_action: Optional[str] = None
    alternatives: List[str] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.utcnow)

@dataclass
class ActionStep:
    """Individual action step"""
    step_id: str
    action_type: ActionType
    action: str
    parameters: Dict[str, Any]
    expected_outcome: str
    actual_outcome: Optional[str] = None
    success: Optional[bool] = None
    timestamp: datetime = field(default_factory=datetime.utcnow)

@dataclass
class ObservationStep:
    """Individual observation step"""
    step_id: str
    observation: str
    source: str
    reliability: float
    implications: List[str]
    timestamp: datetime = field(default_factory=datetime.utcnow)

@dataclass
class WorkflowExecution:
    """Workflow execution context"""
    workflow_id: str
    execution_id: str
    state: WorkflowState
    current_node: Optional[str]
    reasoning_steps: List[ReasoningStep]
    action_steps: List[ActionStep]
    observation_steps: List[ObservationStep]
    context: Dict[str, Any]
    start_time: datetime
    end_time: Optional[datetime] = None
    error: Optional[str] = None

class ReActWorkflowSystem:
    """
    Advanced ReAct (Reasoning and Acting) workflow automation system
    Enables autonomous execution of complex multi-step workflows
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or self._default_config()
        self.workflow_registry = WorkflowRegistry()
        self.reasoning_engine = ReasoningEngine()
        self.action_executor = ActionExecutor()
        self.observation_processor = ObservationProcessor()
        self.workflow_orchestrator = WorkflowOrchestrator()
        self.execution_monitor = ExecutionMonitor()
        self.workflow_optimizer = WorkflowOptimizer()
        self.active_executions = {}
        
    def _default_config(self) -> Dict[str, Any]:
        """Default workflow configuration"""
        return {
            "max_reasoning_steps": 10,
            "max_action_retries": 3,
            "default_timeout": 300,
            "parallel_execution_enabled": True,
            "max_parallel_workflows": 5,
            "observation_confidence_threshold": 0.7,
            "reasoning_strategy": ReasoningType.CHAIN_OF_THOUGHT,
            "enable_reflexion": True,
            "enable_self_correction": True,
            "checkpoint_enabled": True,
            "checkpoint_interval": 60
        }
    
    async def create_workflow(self, name: str, description: str) -> str:
        """Create a new workflow"""
        
        workflow_id = self._generate_id()
        
        workflow = {
            "id": workflow_id,
            "name": name,
            "description": description,
            "nodes": {},
            "edges": [],
            "created_at": datetime.utcnow(),
            "metadata": {}
        }
        
        self.workflow_registry.register(workflow_id, workflow)
        
        return workflow_id
    
    async def add_reasoning_node(self, workflow_id: str, name: str,
                                reasoning_prompt: str,
                                reasoning_type: ReasoningType = None) -> str:
        """Add reasoning node to workflow"""
        
        node_id = self._generate_id()
        reasoning_type = reasoning_type or self.config["reasoning_strategy"]
        
        node = WorkflowNode(
            id=node_id,
            name=name,
            node_type="reason",
            function=lambda ctx: self.reasoning_engine.reason(
                reasoning_prompt, ctx, reasoning_type
            ),
            metadata={"prompt": reasoning_prompt, "type": reasoning_type.value}
        )
        
        self.workflow_registry.add_node(workflow_id, node)
        
        return node_id
    
    async def add_action_node(self, workflow_id: str, name: str,
                            action_type: ActionType,
                            action_function: Callable) -> str:
        """Add action node to workflow"""
        
        node_id = self._generate_id()
        
        node = WorkflowNode(
            id=node_id,
            name=name,
            node_type="act",
            function=action_function,
            metadata={"action_type": action_type.value}
        )
        
        self.workflow_registry.add_node(workflow_id, node)
        
        return node_id
    
    async def add_observation_node(self, workflow_id: str, name: str,
                                  observation_source: str) -> str:
        """Add observation node to workflow"""
        
        node_id = self._generate_id()
        
        node = WorkflowNode(
            id=node_id,
            name=name,
            node_type="observe",
            function=lambda ctx: self.observation_processor.observe(
                observation_source, ctx
            ),
            metadata={"source": observation_source}
        )
        
        self.workflow_registry.add_node(workflow_id, node)
        
        return node_id
    
    async def connect_nodes(self, workflow_id: str, source_id: str,
                          target_id: str, condition: Callable = None) -> bool:
        """Connect two nodes in workflow"""
        
        edge = WorkflowEdge(
            source=source_id,
            target=target_id,
            condition=condition
        )
        
        self.workflow_registry.add_edge(workflow_id, edge)
        
        return True
    
    async def execute_workflow(self, workflow_id: str,
                             initial_context: Dict[str, Any] = None) -> WorkflowExecution:
        """Execute a workflow"""
        
        # Create execution context
        execution_id = self._generate_id()
        execution = WorkflowExecution(
            workflow_id=workflow_id,
            execution_id=execution_id,
            state=WorkflowState.PENDING,
            current_node=None,
            reasoning_steps=[],
            action_steps=[],
            observation_steps=[],
            context=initial_context or {},
            start_time=datetime.utcnow()
        )
        
        # Register active execution
        self.active_executions[execution_id] = execution
        
        # Start execution
        try:
            result = await self.workflow_orchestrator.execute(
                workflow_id, execution, self.config
            )
            execution.state = WorkflowState.COMPLETED
            execution.end_time = datetime.utcnow()
        except Exception as e:
            execution.state = WorkflowState.FAILED
            execution.error = str(e)
            execution.end_time = datetime.utcnow()
        finally:
            # Clean up
            if execution_id in self.active_executions:
                del self.active_executions[execution_id]
        
        return execution
    
    async def execute_react_loop(self, task: str, context: Dict[str, Any] = None,
                                max_iterations: int = None) -> Dict[str, Any]:
        """Execute ReAct reasoning-acting loop for a task"""
        
        max_iterations = max_iterations or self.config["max_reasoning_steps"]
        
        execution_context = context or {}
        execution_context["task"] = task
        
        reasoning_steps = []
        action_steps = []
        observation_steps = []
        
        for iteration in range(max_iterations):
            # Reasoning phase
            reasoning_result = await self.reasoning_engine.reason(
                task, execution_context, self.config["reasoning_strategy"]
            )
            reasoning_steps.append(reasoning_result["step"])
            
            # Check if task is complete
            if reasoning_result.get("task_complete"):
                break
            
            # Acting phase
            if reasoning_result.get("next_action"):
                action_result = await self.action_executor.execute(
                    reasoning_result["next_action"],
                    execution_context
                )
                action_steps.append(action_result["step"])
                
                # Update context with action results
                execution_context.update(action_result.get("outputs", {}))
            
            # Observation phase
            observation_result = await self.observation_processor.observe(
                "action_outcome", execution_context
            )
            observation_steps.append(observation_result["step"])
            
            # Reflexion phase (if enabled)
            if self.config["enable_reflexion"]:
                reflexion_result = await self._reflect_on_progress(
                    reasoning_steps, action_steps, observation_steps
                )
                execution_context["reflexion"] = reflexion_result
        
        return {
            "task": task,
            "completed": reasoning_steps[-1].next_action is None if reasoning_steps else False,
            "reasoning_steps": reasoning_steps,
            "action_steps": action_steps,
            "observation_steps": observation_steps,
            "final_context": execution_context,
            "iterations": len(reasoning_steps)
        }
    
    async def _reflect_on_progress(self, reasoning_steps: List[ReasoningStep],
                                  action_steps: List[ActionStep],
                                  observation_steps: List[ObservationStep]) -> Dict[str, Any]:
        """Reflect on progress and adjust strategy"""
        
        # Analyze success rate
        successful_actions = sum(1 for a in action_steps if a.success)
        success_rate = successful_actions / max(len(action_steps), 1)
        
        # Analyze reasoning confidence
        avg_confidence = sum(r.confidence for r in reasoning_steps) / max(len(reasoning_steps), 1)
        
        # Generate insights
        insights = []
        
        if success_rate < 0.5:
            insights.append("Low action success rate - consider alternative approaches")
        
        if avg_confidence < 0.6:
            insights.append("Low reasoning confidence - gather more information")
        
        # Check for loops
        recent_actions = [a.action for a in action_steps[-3:]]
        if len(recent_actions) == 3 and len(set(recent_actions)) == 1:
            insights.append("Detected action loop - break pattern")
        
        return {
            "success_rate": success_rate,
            "avg_confidence": avg_confidence,
            "insights": insights,
            "should_adjust_strategy": success_rate < 0.3 or avg_confidence < 0.5
        }
    
    def _generate_id(self) -> str:
        """Generate unique ID"""
        return hashlib.md5(
            f"{datetime.utcnow().isoformat()}{id(self)}".encode()
        ).hexdigest()[:12]

class WorkflowRegistry:
    """Registry for workflow definitions"""
    
    def __init__(self):
        self.workflows = {}
        self.templates = self._load_templates()
    
    def register(self, workflow_id: str, workflow: Dict[str, Any]):
        """Register a workflow"""
        self.workflows[workflow_id] = workflow
    
    def add_node(self, workflow_id: str, node: WorkflowNode):
        """Add node to workflow"""
        if workflow_id in self.workflows:
            self.workflows[workflow_id]["nodes"][node.id] = node
    
    def add_edge(self, workflow_id: str, edge: WorkflowEdge):
        """Add edge to workflow"""
        if workflow_id in self.workflows:
            self.workflows[workflow_id]["edges"].append(edge)
    
    def get_workflow(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        """Get workflow by ID"""
        return self.workflows.get(workflow_id)
    
    def _load_templates(self) -> Dict[str, Any]:
        """Load workflow templates"""
        return {
            "code_review": self._create_code_review_template(),
            "bug_fix": self._create_bug_fix_template(),
            "feature_implementation": self._create_feature_template(),
            "data_analysis": self._create_data_analysis_template()
        }
    
    def _create_code_review_template(self) -> Dict[str, Any]:
        """Create code review workflow template"""
        return {
            "name": "Code Review Workflow",
            "description": "Automated code review with reasoning",
            "nodes": [
                {"type": "reason", "prompt": "Analyze code structure and patterns"},
                {"type": "act", "action": "run_static_analysis"},
                {"type": "observe", "source": "analysis_results"},
                {"type": "reason", "prompt": "Identify potential issues"},
                {"type": "act", "action": "generate_review_comments"},
                {"type": "observe", "source": "review_output"}
            ]
        }
    
    def _create_bug_fix_template(self) -> Dict[str, Any]:
        """Create bug fix workflow template"""
        return {
            "name": "Bug Fix Workflow",
            "description": "Automated bug diagnosis and fixing",
            "nodes": [
                {"type": "reason", "prompt": "Analyze bug symptoms"},
                {"type": "act", "action": "reproduce_bug"},
                {"type": "observe", "source": "reproduction_results"},
                {"type": "reason", "prompt": "Identify root cause"},
                {"type": "act", "action": "implement_fix"},
                {"type": "act", "action": "run_tests"},
                {"type": "observe", "source": "test_results"},
                {"type": "reason", "prompt": "Verify fix effectiveness"}
            ]
        }
    
    def _create_feature_template(self) -> Dict[str, Any]:
        """Create feature implementation template"""
        return {
            "name": "Feature Implementation Workflow",
            "description": "End-to-end feature development",
            "nodes": [
                {"type": "reason", "prompt": "Understand requirements"},
                {"type": "act", "action": "design_architecture"},
                {"type": "reason", "prompt": "Plan implementation steps"},
                {"type": "act", "action": "implement_backend"},
                {"type": "act", "action": "implement_frontend"},
                {"type": "act", "action": "write_tests"},
                {"type": "observe", "source": "implementation_status"},
                {"type": "act", "action": "run_integration_tests"},
                {"type": "observe", "source": "test_results"}
            ]
        }
    
    def _create_data_analysis_template(self) -> Dict[str, Any]:
        """Create data analysis template"""
        return {
            "name": "Data Analysis Workflow",
            "description": "Automated data analysis and insights",
            "nodes": [
                {"type": "reason", "prompt": "Understand analysis objectives"},
                {"type": "act", "action": "load_data"},
                {"type": "observe", "source": "data_characteristics"},
                {"type": "reason", "prompt": "Determine analysis approach"},
                {"type": "act", "action": "clean_data"},
                {"type": "act", "action": "perform_analysis"},
                {"type": "observe", "source": "analysis_results"},
                {"type": "reason", "prompt": "Interpret findings"},
                {"type": "act", "action": "generate_visualizations"},
                {"type": "act", "action": "create_report"}
            ]
        }

class ReasoningEngine:
    """Engine for reasoning steps"""
    
    async def reason(self, prompt: str, context: Dict[str, Any],
                    reasoning_type: ReasoningType) -> Dict[str, Any]:
        """Perform reasoning based on type"""
        
        if reasoning_type == ReasoningType.CHAIN_OF_THOUGHT:
            return await self._chain_of_thought(prompt, context)
        elif reasoning_type == ReasoningType.TREE_OF_THOUGHT:
            return await self._tree_of_thought(prompt, context)
        elif reasoning_type == ReasoningType.REFLEXION:
            return await self._reflexion(prompt, context)
        elif reasoning_type == ReasoningType.SELF_CONSISTENCY:
            return await self._self_consistency(prompt, context)
        else:
            return await self._chain_of_thought(prompt, context)
    
    async def _chain_of_thought(self, prompt: str, 
                               context: Dict[str, Any]) -> Dict[str, Any]:
        """Chain of thought reasoning"""
        
        # Build reasoning chain
        thoughts = []
        
        # Initial understanding
        thoughts.append(f"Understanding the task: {prompt}")
        
        # Analyze context
        if context:
            thoughts.append(f"Context analysis: {self._summarize_context(context)}")
        
        # Generate reasoning steps
        steps = [
            "What is the goal?",
            "What information do I have?",
            "What information do I need?",
            "What actions can I take?",
            "What is the best next action?"
        ]
        
        for step in steps:
            thought = f"{step} - Based on analysis..."
            thoughts.append(thought)
        
        # Determine next action
        next_action = self._determine_next_action(prompt, context)
        
        # Calculate confidence
        confidence = self._calculate_confidence(thoughts, context)
        
        step = ReasoningStep(
            step_id=self._generate_id(),
            thought=" -> ".join(thoughts),
            evidence=self._extract_evidence(context),
            confidence=confidence,
            next_action=next_action,
            alternatives=self._generate_alternatives(next_action)
        )
        
        return {
            "step": step,
            "thoughts": thoughts,
            "next_action": next_action,
            "task_complete": next_action is None,
            "confidence": confidence
        }
    
    async def _tree_of_thought(self, prompt: str,
                              context: Dict[str, Any]) -> Dict[str, Any]:
        """Tree of thought reasoning with exploration"""
        
        # Generate thought tree
        root_thought = f"Task: {prompt}"
        
        # Generate branches (different approaches)
        branches = []
        approaches = [
            "Direct approach",
            "Incremental approach",
            "Parallel approach",
            "Alternative approach"
        ]
        
        for approach in approaches:
            branch = {
                "approach": approach,
                "thoughts": [f"Using {approach}: ..."],
                "score": self._score_approach(approach, context)
            }
            branches.append(branch)
        
        # Select best branch
        best_branch = max(branches, key=lambda b: b["score"])
        
        step = ReasoningStep(
            step_id=self._generate_id(),
            thought=f"Selected {best_branch['approach']}",
            evidence=best_branch["thoughts"],
            confidence=best_branch["score"],
            next_action=self._determine_next_action(prompt, context),
            alternatives=[b["approach"] for b in branches if b != best_branch]
        )
        
        return {
            "step": step,
            "tree": branches,
            "selected": best_branch,
            "task_complete": False
        }
    
    async def _reflexion(self, prompt: str,
                        context: Dict[str, Any]) -> Dict[str, Any]:
        """Reflexion-based reasoning with self-improvement"""
        
        # Check for previous attempts
        previous_attempts = context.get("previous_attempts", [])
        
        thoughts = []
        
        if previous_attempts:
            # Reflect on previous attempts
            thoughts.append("Reflecting on previous attempts:")
            for attempt in previous_attempts:
                thoughts.append(f"  - {attempt['action']}: {attempt['outcome']}")
            
            # Learn from mistakes
            thoughts.append("Learning: Avoid previously failed approaches")
        
        # Generate new approach
        thoughts.append("New approach based on reflection")
        
        step = ReasoningStep(
            step_id=self._generate_id(),
            thought=" | ".join(thoughts),
            evidence=previous_attempts,
            confidence=0.7 + (0.1 * len(previous_attempts)),  # Increase confidence with experience
            next_action=self._determine_next_action(prompt, context, exclude=previous_attempts)
        )
        
        return {
            "step": step,
            "reflection": thoughts,
            "learned": len(previous_attempts) > 0
        }
    
    async def _self_consistency(self, prompt: str,
                               context: Dict[str, Any]) -> Dict[str, Any]:
        """Self-consistency reasoning with multiple paths"""
        
        # Generate multiple reasoning paths
        paths = []
        num_paths = 3
        
        for i in range(num_paths):
            path = await self._chain_of_thought(
                prompt + f" (path {i+1})", context
            )
            paths.append(path)
        
        # Vote on best action
        action_votes = defaultdict(int)
        for path in paths:
            if path.get("next_action"):
                action_votes[path["next_action"]] += 1
        
        # Select most consistent action
        if action_votes:
            best_action = max(action_votes.items(), key=lambda x: x[1])
            consensus_action = best_action[0]
            consensus_score = best_action[1] / num_paths
        else:
            consensus_action = None
            consensus_score = 0
        
        step = ReasoningStep(
            step_id=self._generate_id(),
            thought=f"Consensus from {num_paths} reasoning paths",
            evidence=[p["step"].thought for p in paths],
            confidence=consensus_score,
            next_action=consensus_action
        )
        
        return {
            "step": step,
            "paths": paths,
            "consensus": consensus_score,
            "task_complete": consensus_action is None
        }
    
    def _determine_next_action(self, prompt: str, context: Dict[str, Any],
                              exclude: List[Any] = None) -> Optional[str]:
        """Determine next action based on reasoning"""
        
        # Simple action determination (would be more sophisticated in production)
        if "code" in prompt.lower():
            if "review" in prompt.lower():
                return "run_code_review"
            elif "fix" in prompt.lower():
                return "implement_fix"
            else:
                return "write_code"
        elif "test" in prompt.lower():
            return "run_tests"
        elif "analyze" in prompt.lower():
            return "perform_analysis"
        
        # Check if task seems complete
        if context.get("results") or context.get("output"):
            return None  # Task complete
        
        return "gather_information"
    
    def _calculate_confidence(self, thoughts: List[str],
                            context: Dict[str, Any]) -> float:
        """Calculate confidence in reasoning"""
        
        confidence = 0.5  # Base confidence
        
        # Increase confidence based on evidence
        if context.get("evidence"):
            confidence += 0.2
        
        # Increase confidence based on thought depth
        if len(thoughts) > 5:
            confidence += 0.1
        
        # Increase confidence if previous actions succeeded
        if context.get("previous_success"):
            confidence += 0.2
        
        return min(confidence, 1.0)
    
    def _extract_evidence(self, context: Dict[str, Any]) -> List[str]:
        """Extract evidence from context"""
        
        evidence = []
        
        if "observations" in context:
            evidence.extend(context["observations"])
        
        if "facts" in context:
            evidence.extend(context["facts"])
        
        if "data" in context:
            evidence.append(f"Data available: {list(context['data'].keys())}")
        
        return evidence
    
    def _generate_alternatives(self, action: Optional[str]) -> List[str]:
        """Generate alternative actions"""
        
        if not action:
            return []
        
        alternatives = []
        
        if action == "write_code":
            alternatives = ["review_existing_code", "design_first", "write_tests_first"]
        elif action == "run_tests":
            alternatives = ["run_specific_test", "run_integration_tests", "manual_testing"]
        elif action == "gather_information":
            alternatives = ["ask_user", "search_documentation", "analyze_context"]
        
        return alternatives[:2]  # Return top 2 alternatives
    
    def _summarize_context(self, context: Dict[str, Any]) -> str:
        """Summarize context for reasoning"""
        
        summary_parts = []
        
        if "task" in context:
            summary_parts.append(f"Task: {context['task'][:50]}...")
        
        if "previous_actions" in context:
            summary_parts.append(f"Actions taken: {len(context['previous_actions'])}")
        
        if "results" in context:
            summary_parts.append("Results available")
        
        return " | ".join(summary_parts) if summary_parts else "Empty context"
    
    def _score_approach(self, approach: str, context: Dict[str, Any]) -> float:
        """Score an approach based on context"""
        
        # Simple scoring (would be more sophisticated in production)
        scores = {
            "Direct approach": 0.7,
            "Incremental approach": 0.8,
            "Parallel approach": 0.6,
            "Alternative approach": 0.5
        }
        
        base_score = scores.get(approach, 0.5)
        
        # Adjust based on context
        if context.get("complexity") == "high" and approach == "Incremental approach":
            base_score += 0.1
        
        if context.get("time_constraint") and approach == "Direct approach":
            base_score += 0.1
        
        return min(base_score, 1.0)
    
    def _generate_id(self) -> str:
        """Generate unique ID"""
        return hashlib.md5(
            f"{datetime.utcnow().isoformat()}{id(self)}".encode()
        ).hexdigest()[:8]

class ActionExecutor:
    """Execute actions in workflows"""
    
    async def execute(self, action: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute an action"""
        
        action_step = ActionStep(
            step_id=self._generate_id(),
            action_type=self._determine_action_type(action),
            action=action,
            parameters=self._extract_parameters(action, context),
            expected_outcome=self._predict_outcome(action)
        )
        
        try:
            # Execute based on action type
            if action == "write_code":
                result = await self._execute_write_code(context)
            elif action == "run_tests":
                result = await self._execute_run_tests(context)
            elif action == "run_code_review":
                result = await self._execute_code_review(context)
            elif action == "implement_fix":
                result = await self._execute_implement_fix(context)
            elif action == "gather_information":
                result = await self._execute_gather_info(context)
            else:
                result = await self._execute_generic(action, context)
            
            action_step.actual_outcome = result.get("outcome", "Completed")
            action_step.success = result.get("success", True)
            
            return {
                "step": action_step,
                "outputs": result.get("outputs", {}),
                "success": action_step.success
            }
            
        except Exception as e:
            action_step.actual_outcome = f"Error: {str(e)}"
            action_step.success = False
            
            return {
                "step": action_step,
                "outputs": {},
                "success": False,
                "error": str(e)
            }
    
    async def _execute_write_code(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute code writing action"""
        
        # Simulate code writing (would integrate with actual code generation in production)
        code = """
def example_function(param):
    # Generated code
    return param * 2
        """
        
        return {
            "success": True,
            "outcome": "Code written successfully",
            "outputs": {
                "code": code,
                "language": "python",
                "lines": 4
            }
        }
    
    async def _execute_run_tests(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute test running action"""
        
        # Simulate test execution
        return {
            "success": True,
            "outcome": "Tests executed",
            "outputs": {
                "tests_run": 10,
                "tests_passed": 9,
                "tests_failed": 1,
                "coverage": 0.85
            }
        }
    
    async def _execute_code_review(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute code review action"""
        
        return {
            "success": True,
            "outcome": "Code review completed",
            "outputs": {
                "issues_found": 3,
                "severity": "medium",
                "suggestions": ["Add error handling", "Improve naming", "Add tests"]
            }
        }
    
    async def _execute_implement_fix(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute fix implementation"""
        
        return {
            "success": True,
            "outcome": "Fix implemented",
            "outputs": {
                "files_modified": 2,
                "lines_changed": 15,
                "fix_type": "bug_fix"
            }
        }
    
    async def _execute_gather_info(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute information gathering"""
        
        return {
            "success": True,
            "outcome": "Information gathered",
            "outputs": {
                "sources_consulted": 3,
                "relevant_info": ["Documentation found", "Similar issues identified"],
                "confidence": 0.8
            }
        }
    
    async def _execute_generic(self, action: str, 
                              context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute generic action"""
        
        return {
            "success": True,
            "outcome": f"Action '{action}' executed",
            "outputs": {
                "action": action,
                "context_keys": list(context.keys())
            }
        }
    
    def _determine_action_type(self, action: str) -> ActionType:
        """Determine action type"""
        
        if "tool" in action.lower():
            return ActionType.TOOL_USE
        elif "agent" in action.lower():
            return ActionType.AGENT_CALL
        elif "api" in action.lower():
            return ActionType.API_REQUEST
        elif "database" in action.lower() or "query" in action.lower():
            return ActionType.DATABASE_QUERY
        else:
            return ActionType.COMPUTATION
    
    def _extract_parameters(self, action: str, 
                           context: Dict[str, Any]) -> Dict[str, Any]:
        """Extract parameters for action"""
        
        params = {}
        
        # Extract relevant context
        if "input" in context:
            params["input"] = context["input"]
        
        if "config" in context:
            params["config"] = context["config"]
        
        params["action"] = action
        
        return params
    
    def _predict_outcome(self, action: str) -> str:
        """Predict expected outcome"""
        
        predictions = {
            "write_code": "Code will be generated",
            "run_tests": "Tests will be executed",
            "gather_information": "Information will be collected",
            "implement_fix": "Fix will be applied"
        }
        
        return predictions.get(action, f"Action '{action}' will be completed")
    
    def _generate_id(self) -> str:
        """Generate unique ID"""
        return hashlib.md5(
            f"{datetime.utcnow().isoformat()}{id(self)}".encode()
        ).hexdigest()[:8]

class ObservationProcessor:
    """Process observations from actions"""
    
    async def observe(self, source: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Process observation from source"""
        
        observation = self._extract_observation(source, context)
        
        step = ObservationStep(
            step_id=self._generate_id(),
            observation=observation,
            source=source,
            reliability=self._assess_reliability(source, context),
            implications=self._derive_implications(observation, context)
        )
        
        return {
            "step": step,
            "observation": observation,
            "reliable": step.reliability > 0.7,
            "actionable": len(step.implications) > 0
        }
    
    def _extract_observation(self, source: str, 
                           context: Dict[str, Any]) -> str:
        """Extract observation from context"""
        
        if source == "action_outcome":
            if "outputs" in context:
                return f"Action produced outputs: {list(context['outputs'].keys())}"
            else:
                return "Action completed without outputs"
        
        elif source == "test_results":
            if "tests_passed" in context:
                return f"Tests: {context.get('tests_passed')}/{context.get('tests_run')} passed"
            else:
                return "Test results not available"
        
        elif source == "analysis_results":
            if "issues_found" in context:
                return f"Analysis found {context.get('issues_found')} issues"
            else:
                return "Analysis complete"
        
        else:
            return f"Observation from {source}"
    
    def _assess_reliability(self, source: str, 
                           context: Dict[str, Any]) -> float:
        """Assess observation reliability"""
        
        # Base reliability by source
        reliability_scores = {
            "test_results": 0.9,
            "action_outcome": 0.8,
            "analysis_results": 0.85,
            "user_input": 1.0,
            "external_api": 0.7
        }
        
        base_reliability = reliability_scores.get(source, 0.5)
        
        # Adjust based on context
        if context.get("verified"):
            base_reliability += 0.1
        
        if context.get("error"):
            base_reliability -= 0.2
        
        return max(0, min(1, base_reliability))
    
    def _derive_implications(self, observation: str, 
                           context: Dict[str, Any]) -> List[str]:
        """Derive implications from observation"""
        
        implications = []
        
        if "passed" in observation and "tests" in observation.lower():
            implications.append("Code quality verified")
            implications.append("Can proceed with deployment")
        
        if "issues" in observation:
            implications.append("Requires attention before proceeding")
            implications.append("May need code revision")
        
        if "completed" in observation:
            implications.append("Ready for next step")
        
        return implications
    
    def _generate_id(self) -> str:
        """Generate unique ID"""
        return hashlib.md5(
            f"{datetime.utcnow().isoformat()}{id(self)}".encode()
        ).hexdigest()[:8]

class WorkflowOrchestrator:
    """Orchestrate workflow execution"""
    
    async def execute(self, workflow_id: str, execution: WorkflowExecution,
                     config: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a workflow"""
        
        workflow = WorkflowRegistry().get_workflow(workflow_id)
        if not workflow:
            raise ValueError(f"Workflow {workflow_id} not found")
        
        # Build execution graph
        graph = self._build_graph(workflow)
        
        # Execute nodes in order
        executed_nodes = set()
        
        while len(executed_nodes) < len(workflow["nodes"]):
            # Find next executable node
            next_node = self._get_next_node(graph, executed_nodes, execution)
            
            if not next_node:
                break
            
            # Execute node
            execution.current_node = next_node.id
            execution.state = self._get_state_for_node_type(next_node.node_type)
            
            result = await self._execute_node(next_node, execution.context)
            
            # Update execution based on result
            self._update_execution(execution, next_node, result)
            
            executed_nodes.add(next_node.id)
        
        return {
            "executed_nodes": len(executed_nodes),
            "total_nodes": len(workflow["nodes"]),
            "final_context": execution.context
        }
    
    def _build_graph(self, workflow: Dict[str, Any]) -> nx.DiGraph:
        """Build execution graph from workflow"""
        
        graph = nx.DiGraph()
        
        # Add nodes
        for node_id, node in workflow["nodes"].items():
            graph.add_node(node_id, data=node)
        
        # Add edges
        for edge in workflow["edges"]:
            graph.add_edge(edge.source, edge.target, data=edge)
        
        return graph
    
    def _get_next_node(self, graph: nx.DiGraph, executed: set,
                      execution: WorkflowExecution) -> Optional[WorkflowNode]:
        """Get next node to execute"""
        
        for node_id in graph.nodes():
            if node_id in executed:
                continue
            
            # Check if dependencies are satisfied
            predecessors = list(graph.predecessors(node_id))
            if all(p in executed for p in predecessors):
                return graph.nodes[node_id]["data"]
        
        return None
    
    async def _execute_node(self, node: WorkflowNode,
                          context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a workflow node"""
        
        if node.function:
            return await node.function(context)
        else:
            return {"success": True, "output": f"Node {node.name} executed"}
    
    def _update_execution(self, execution: WorkflowExecution,
                        node: WorkflowNode, result: Dict[str, Any]):
        """Update execution with node results"""
        
        if node.node_type == "reason":
            if "step" in result:
                execution.reasoning_steps.append(result["step"])
        elif node.node_type == "act":
            if "step" in result:
                execution.action_steps.append(result["step"])
        elif node.node_type == "observe":
            if "step" in result:
                execution.observation_steps.append(result["step"])
        
        # Update context with outputs
        if "outputs" in result:
            execution.context.update(result["outputs"])
    
    def _get_state_for_node_type(self, node_type: str) -> WorkflowState:
        """Get workflow state for node type"""
        
        state_map = {
            "reason": WorkflowState.REASONING,
            "act": WorkflowState.ACTING,
            "observe": WorkflowState.OBSERVING
        }
        
        return state_map.get(node_type, WorkflowState.ACTING)

class ExecutionMonitor:
    """Monitor workflow executions"""
    
    def __init__(self):
        self.metrics = defaultdict(list)
        self.alerts = []
    
    async def monitor(self, execution: WorkflowExecution):
        """Monitor an execution"""
        
        # Track metrics
        self.metrics["execution_time"].append(
            (execution.end_time - execution.start_time).total_seconds()
            if execution.end_time else 0
        )
        
        self.metrics["reasoning_steps"].append(len(execution.reasoning_steps))
        self.metrics["action_steps"].append(len(execution.action_steps))
        
        # Check for issues
        if execution.state == WorkflowState.FAILED:
            self.alerts.append({
                "type": "failure",
                "execution_id": execution.execution_id,
                "error": execution.error,
                "timestamp": datetime.utcnow()
            })
        
        # Check for long execution
        if execution.end_time:
            duration = (execution.end_time - execution.start_time).total_seconds()
            if duration > 300:  # 5 minutes
                self.alerts.append({
                    "type": "slow_execution",
                    "execution_id": execution.execution_id,
                    "duration": duration,
                    "timestamp": datetime.utcnow()
                })

class WorkflowOptimizer:
    """Optimize workflow execution"""
    
    def optimize(self, workflow: Dict[str, Any],
                execution_history: List[WorkflowExecution]) -> Dict[str, Any]:
        """Optimize workflow based on history"""
        
        optimizations = []
        
        # Analyze execution patterns
        avg_duration = self._calculate_avg_duration(execution_history)
        failure_rate = self._calculate_failure_rate(execution_history)
        
        # Generate optimizations
        if avg_duration > 60:
            optimizations.append({
                "type": "parallelize",
                "reason": "Long average execution time",
                "suggestion": "Consider parallel execution of independent nodes"
            })
        
        if failure_rate > 0.2:
            optimizations.append({
                "type": "add_retry",
                "reason": "High failure rate",
                "suggestion": "Add retry logic to failure-prone nodes"
            })
        
        # Identify bottlenecks
        bottlenecks = self._identify_bottlenecks(execution_history)
        for bottleneck in bottlenecks:
            optimizations.append({
                "type": "optimize_node",
                "node": bottleneck,
                "suggestion": f"Optimize node {bottleneck} - it's a performance bottleneck"
            })
        
        return {
            "optimizations": optimizations,
            "metrics": {
                "avg_duration": avg_duration,
                "failure_rate": failure_rate
            }
        }
    
    def _calculate_avg_duration(self, history: List[WorkflowExecution]) -> float:
        """Calculate average execution duration"""
        
        durations = []
        for execution in history:
            if execution.end_time:
                duration = (execution.end_time - execution.start_time).total_seconds()
                durations.append(duration)
        
        return sum(durations) / len(durations) if durations else 0
    
    def _calculate_failure_rate(self, history: List[WorkflowExecution]) -> float:
        """Calculate failure rate"""
        
        if not history:
            return 0
        
        failures = sum(1 for e in history if e.state == WorkflowState.FAILED)
        return failures / len(history)
    
    def _identify_bottlenecks(self, history: List[WorkflowExecution]) -> List[str]:
        """Identify performance bottlenecks"""
        
        node_durations = defaultdict(list)
        
        # Collect node execution times (simplified)
        for execution in history:
            if execution.current_node:
                # Would need more detailed timing in production
                node_durations[execution.current_node].append(1.0)
        
        # Find slowest nodes
        bottlenecks = []
        for node, durations in node_durations.items():
            avg_duration = sum(durations) / len(durations)
            if avg_duration > 5.0:  # Threshold
                bottlenecks.append(node)
        
        return bottlenecks

# Example usage

async def main():
    """Example usage of ReAct Workflow System"""
    
    # Initialize workflow system
    workflow_system = ReActWorkflowSystem()
    
    # Example 1: Execute ReAct loop for a task
    print("🔄 Executing ReAct loop for code review task...")
    result = await workflow_system.execute_react_loop(
        task="Review the authentication module for security vulnerabilities",
        context={"module": "auth.py", "priority": "high"}
    )
    
    print(f"✅ Task completed: {result['completed']}")
    print(f"   Iterations: {result['iterations']}")
    print(f"   Actions taken: {len(result['action_steps'])}")
    
    # Example 2: Create and execute custom workflow
    print("\n📋 Creating custom bug fix workflow...")
    workflow_id = await workflow_system.create_workflow(
        name="Bug Fix Workflow",
        description="Automated bug diagnosis and fixing"
    )
    
    # Add nodes
    reason_node = await workflow_system.add_reasoning_node(
        workflow_id,
        "Analyze Bug",
        "Analyze the bug report and identify potential causes"
    )
    
    action_node = await workflow_system.add_action_node(
        workflow_id,
        "Reproduce Bug",
        ActionType.TOOL_USE,
        lambda ctx: {"success": True, "reproduced": True}
    )
    
    observe_node = await workflow_system.add_observation_node(
        workflow_id,
        "Check Results",
        "test_results"
    )
    
    # Connect nodes
    await workflow_system.connect_nodes(workflow_id, reason_node, action_node)
    await workflow_system.connect_nodes(workflow_id, action_node, observe_node)
    
    # Execute workflow
    print("▶️  Executing workflow...")
    execution = await workflow_system.execute_workflow(
        workflow_id,
        {"bug_report": "Login fails with valid credentials"}
    )
    
    print(f"✅ Workflow execution completed")
    print(f"   State: {execution.state.value}")
    print(f"   Reasoning steps: {len(execution.reasoning_steps)}")
    print(f"   Actions taken: {len(execution.action_steps)}")
    print(f"   Observations: {len(execution.observation_steps)}")

if __name__ == "__main__":
    asyncio.run(main())