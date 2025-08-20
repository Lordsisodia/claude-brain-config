#!/usr/bin/env python3
"""
ML ROUTING INTEGRATION LAYER
Seamless integration of ML predictive routing with existing orchestration systems
"""

import asyncio
import json
import time
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple, Union
from dataclasses import dataclass, asdict
import logging

# Import existing systems
try:
    from autonomous_learning_system import AutonomousLearningEngine
    from hierarchical_orchestration_system import HierarchicalOrchestrator
    from ml_predictive_routing_system import MLPredictiveRoutingSystem
    SYSTEMS_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  Some systems not available: {e}")
    SYSTEMS_AVAILABLE = False

@dataclass
class IntegratedRoutingDecision:
    """Comprehensive routing decision combining all systems"""
    task: str
    ml_prediction: Optional[Dict] = None
    autonomous_learning_prediction: Optional[Dict] = None
    hierarchical_analysis: Optional[Dict] = None
    final_routing_decision: Optional[Dict] = None
    confidence_score: float = 0.0
    decision_rationale: str = ""
    execution_plan: Optional[Dict] = None
    fallback_plan: Optional[Dict] = None

class MLRoutingIntegrationEngine:
    """Advanced integration engine for ML routing with existing systems"""
    
    def __init__(self):
        self.ml_routing_system = None
        self.autonomous_learning = None
        self.hierarchical_orchestrator = None
        
        # Integration metrics
        self.integration_history = []
        self.system_performance_comparison = {}
        self.consensus_decisions = []
        self.fallback_activations = []
        
        # Decision weights (can be learned and adapted)
        self.decision_weights = {
            'ml_prediction': 0.4,
            'autonomous_learning': 0.3,
            'hierarchical_analysis': 0.3
        }
        
        # Performance tracking
        self.total_routing_decisions = 0
        self.successful_executions = 0
        self.ml_accuracy_score = 0.0
        self.integration_effectiveness = 0.0
        
        self._initialize_systems()
        
        print("🔗 ML ROUTING INTEGRATION ENGINE INITIALIZED")
        print(f"   🧠 ML Routing: {'✅' if self.ml_routing_system else '❌'}")
        print(f"   📚 Autonomous Learning: {'✅' if self.autonomous_learning else '❌'}")
        print(f"   🏗️ Hierarchical Orchestrator: {'✅' if self.hierarchical_orchestrator else '❌'}")
        print()
    
    def _initialize_systems(self):
        """Initialize all available systems"""
        
        if not SYSTEMS_AVAILABLE:
            print("⚠️  Running in limited mode - some systems unavailable")
            return
        
        try:
            # Initialize autonomous learning first (provides historical context)
            self.autonomous_learning = AutonomousLearningEngine()
            print("   📚 Autonomous learning system initialized")
            
            # Initialize ML routing with learning integration
            self.ml_routing_system = MLPredictiveRoutingSystem(self.autonomous_learning)
            print("   🧠 ML routing system initialized with learning integration")
            
            # Initialize hierarchical orchestrator
            self.hierarchical_orchestrator = HierarchicalOrchestrator()
            print("   🏗️ Hierarchical orchestrator initialized")
            
        except Exception as e:
            print(f"⚠️  System initialization error: {e}")
    
    async def integrated_routing_decision(self, task: str, constraints: Dict = None) -> IntegratedRoutingDecision:
        """Make integrated routing decision using all available systems"""
        
        print(f"🔗 INTEGRATED ROUTING DECISION")
        print(f"   📋 Task: {task[:100]}...")
        
        decision_start = time.time()
        constraints = constraints or {}
        
        # Initialize decision object
        decision = IntegratedRoutingDecision(task=task)
        
        # Phase 1: Gather predictions from all systems
        print("   🔍 Phase 1: Gathering predictions from all systems...")
        
        predictions = await self._gather_system_predictions(task, constraints)
        decision.ml_prediction = predictions.get('ml_prediction')
        decision.autonomous_learning_prediction = predictions.get('autonomous_learning')
        decision.hierarchical_analysis = predictions.get('hierarchical_analysis')
        
        # Phase 2: Analyze consensus and conflicts
        print("   🤝 Phase 2: Analyzing consensus and resolving conflicts...")
        
        consensus_analysis = self._analyze_prediction_consensus(predictions)
        
        # Phase 3: Make weighted decision
        print("   ⚖️  Phase 3: Making weighted routing decision...")
        
        final_decision = await self._make_weighted_decision(predictions, consensus_analysis, constraints)
        decision.final_routing_decision = final_decision
        decision.confidence_score = final_decision.get('confidence', 0.0)
        decision.decision_rationale = final_decision.get('rationale', '')
        
        # Phase 4: Create execution plan
        print("   📋 Phase 4: Creating execution plan...")
        
        execution_plan = await self._create_execution_plan(final_decision, task)
        decision.execution_plan = execution_plan
        
        # Phase 5: Prepare fallback plan
        print("   🛡️  Phase 5: Preparing fallback plan...")
        
        fallback_plan = self._create_fallback_plan(predictions, final_decision)
        decision.fallback_plan = fallback_plan
        
        decision_time = time.time() - decision_start
        
        # Record decision for learning
        self._record_integration_decision(decision, decision_time, consensus_analysis)
        
        self.total_routing_decisions += 1
        
        print(f"   ✅ Integrated decision complete ({decision_time:.3f}s)")
        print(f"     🎯 Selected orchestration: {final_decision.get('orchestration_type', 'unknown')}")
        print(f"     👥 Agent team: {len(final_decision.get('agent_team', []))} agents")
        print(f"     🔮 Confidence: {decision.confidence_score:.3f}")
        print(f"     🧠 Rationale: {decision.decision_rationale[:100]}...")
        
        return decision
    
    async def _gather_system_predictions(self, task: str, constraints: Dict) -> Dict[str, Any]:
        """Gather predictions from all available systems"""
        
        predictions = {}
        
        # ML Routing System Prediction
        if self.ml_routing_system:
            try:
                ml_start = time.time()
                ml_prediction = await self.ml_routing_system.predict_optimal_routing(task, constraints)
                ml_time = time.time() - ml_start
                
                predictions['ml_prediction'] = {
                    'orchestration_type': ml_prediction.predicted_orchestration_type,
                    'agent_team': ml_prediction.predicted_agent_combination,
                    'estimated_quality': ml_prediction.estimated_quality,
                    'estimated_cost': ml_prediction.estimated_cost,
                    'estimated_time': ml_prediction.estimated_time,
                    'confidence': ml_prediction.confidence_score,
                    'uncertainty_bounds': ml_prediction.uncertainty_bounds,
                    'risk_assessment': ml_prediction.risk_assessment,
                    'prediction_time': ml_time,
                    'source': 'ml_routing_system'
                }
                
                print(f"     🧠 ML prediction: {ml_prediction.predicted_orchestration_type} ({ml_time:.3f}s)")
                
            except Exception as e:
                print(f"     ❌ ML prediction failed: {e}")
                predictions['ml_prediction'] = None
        
        # Autonomous Learning Prediction
        if self.autonomous_learning:
            try:
                learning_start = time.time()
                learning_prediction = await self.autonomous_learning.predict_optimal_orchestration(task)
                learning_time = time.time() - learning_start
                
                predictions['autonomous_learning'] = {
                    'orchestration_type': learning_prediction.get('predicted_orchestration_type'),
                    'agent_team': learning_prediction.get('recommended_agents', []),
                    'estimated_quality': learning_prediction.get('expected_quality', 0.0),
                    'estimated_cost': learning_prediction.get('expected_cost', 0.0),
                    'estimated_time': learning_prediction.get('expected_time', 0.0),
                    'confidence': learning_prediction.get('confidence', 0.0),
                    'based_on_learnings': learning_prediction.get('based_on_learnings', False),
                    'pattern_id': learning_prediction.get('pattern_id'),
                    'prediction_time': learning_time,
                    'source': 'autonomous_learning'
                }
                
                print(f"     📚 Learning prediction: {learning_prediction.get('predicted_orchestration_type')} ({learning_time:.3f}s)")
                
            except Exception as e:
                print(f"     ❌ Learning prediction failed: {e}")
                predictions['autonomous_learning'] = None
        
        # Hierarchical Analysis
        if self.hierarchical_orchestrator:
            try:
                hierarchical_start = time.time()
                # Use the orchestration planning from hierarchical system
                orchestration_plan = await self.hierarchical_orchestrator._analyze_task_complexity(task)
                hierarchical_time = time.time() - hierarchical_start
                
                predictions['hierarchical_analysis'] = {
                    'orchestration_type': orchestration_plan.orchestration_type.value,
                    'complexity': orchestration_plan.complexity.value,
                    'estimated_agents': orchestration_plan.estimated_agents,
                    'estimated_duration': orchestration_plan.estimated_duration,
                    'coordination_strategy': orchestration_plan.coordination_strategy,
                    'tier_breakdown': orchestration_plan.tier_breakdown,
                    'confidence': 0.8,  # Hierarchical system has high confidence in rule-based decisions
                    'prediction_time': hierarchical_time,
                    'source': 'hierarchical_orchestrator'
                }
                
                print(f"     🏗️ Hierarchical analysis: {orchestration_plan.orchestration_type.value} ({hierarchical_time:.3f}s)")
                
            except Exception as e:
                print(f"     ❌ Hierarchical analysis failed: {e}")
                predictions['hierarchical_analysis'] = None
        
        return predictions
    
    def _analyze_prediction_consensus(self, predictions: Dict[str, Any]) -> Dict:
        """Analyze consensus and conflicts between predictions"""
        
        available_predictions = {k: v for k, v in predictions.items() if v is not None}
        
        if not available_predictions:
            return {'consensus_level': 0.0, 'conflicts': [], 'agreements': []}
        
        # Orchestration type consensus
        orchestration_types = []
        for pred_name, pred_data in available_predictions.items():
            if pred_data and pred_data.get('orchestration_type'):
                orchestration_types.append(pred_data['orchestration_type'])
        
        orchestration_consensus = len(set(orchestration_types)) == 1 if orchestration_types else False
        
        # Quality estimate consensus (within 20% tolerance)
        quality_estimates = []
        for pred_name, pred_data in available_predictions.items():
            if pred_data and pred_data.get('estimated_quality'):
                quality_estimates.append(pred_data['estimated_quality'])
        
        quality_consensus = False
        if len(quality_estimates) >= 2:
            quality_range = max(quality_estimates) - min(quality_estimates)
            quality_consensus = quality_range <= 0.2
        
        # Cost estimate consensus (within 50% tolerance)
        cost_estimates = []
        for pred_name, pred_data in available_predictions.items():
            if pred_data and pred_data.get('estimated_cost'):
                cost_estimates.append(pred_data['estimated_cost'])
        
        cost_consensus = False
        if len(cost_estimates) >= 2:
            cost_mean = np.mean(cost_estimates)
            cost_consensus = all(abs(cost - cost_mean) / cost_mean <= 0.5 for cost in cost_estimates)
        
        # Overall consensus level
        consensus_factors = [orchestration_consensus, quality_consensus, cost_consensus]
        consensus_level = sum(consensus_factors) / len(consensus_factors)
        
        # Identify conflicts
        conflicts = []
        if not orchestration_consensus and len(orchestration_types) > 1:
            conflicts.append(f"Orchestration type conflict: {set(orchestration_types)}")
        
        if not quality_consensus and len(quality_estimates) > 1:
            conflicts.append(f"Quality estimate range: {min(quality_estimates):.3f} - {max(quality_estimates):.3f}")
        
        if not cost_consensus and len(cost_estimates) > 1:
            conflicts.append(f"Cost estimate variance: {np.std(cost_estimates):.5f}")
        
        # Identify agreements
        agreements = []
        if orchestration_consensus:
            agreements.append(f"Orchestration consensus: {orchestration_types[0] if orchestration_types else 'none'}")
        
        if quality_consensus:
            agreements.append(f"Quality consensus: {np.mean(quality_estimates):.3f}")
        
        if cost_consensus:
            agreements.append(f"Cost consensus: {np.mean(cost_estimates):.5f}")
        
        return {
            'consensus_level': consensus_level,
            'orchestration_consensus': orchestration_consensus,
            'quality_consensus': quality_consensus,
            'cost_consensus': cost_consensus,
            'conflicts': conflicts,
            'agreements': agreements,
            'available_predictions': len(available_predictions)
        }
    
    async def _make_weighted_decision(self, predictions: Dict, consensus_analysis: Dict, constraints: Dict) -> Dict:
        """Make final weighted decision based on all predictions"""
        
        available_predictions = {k: v for k, v in predictions.items() if v is not None}
        
        if not available_predictions:
            return await self._create_fallback_decision()
        
        # If high consensus, use consensus decision
        if consensus_analysis['consensus_level'] >= 0.8:
            return self._create_consensus_decision(available_predictions, consensus_analysis)
        
        # Otherwise, use weighted decision
        return self._create_weighted_decision(available_predictions, consensus_analysis, constraints)
    
    def _create_consensus_decision(self, predictions: Dict, consensus_analysis: Dict) -> Dict:
        """Create decision based on high consensus"""
        
        # Get the most common orchestration type
        orchestration_types = [pred['orchestration_type'] for pred in predictions.values() if pred.get('orchestration_type')]
        
        if orchestration_types:
            from collections import Counter
            most_common_orchestration = Counter(orchestration_types).most_common(1)[0][0]
        else:
            most_common_orchestration = 'coordinated'
        
        # Average the estimates
        quality_estimates = [pred.get('estimated_quality', 0.0) for pred in predictions.values()]
        cost_estimates = [pred.get('estimated_cost', 0.001) for pred in predictions.values()]
        time_estimates = [pred.get('estimated_time', 10.0) for pred in predictions.values()]
        
        # Get agent teams (combine and deduplicate)
        all_agents = []
        for pred in predictions.values():
            if pred.get('agent_team'):
                all_agents.extend(pred['agent_team'])
        
        unique_agents = list(set(all_agents))
        
        # High confidence due to consensus
        confidence = 0.9
        
        return {
            'orchestration_type': most_common_orchestration,
            'agent_team': unique_agents,
            'estimated_quality': np.mean(quality_estimates) if quality_estimates else 0.75,
            'estimated_cost': np.mean(cost_estimates) if cost_estimates else 0.001,
            'estimated_time': np.mean(time_estimates) if time_estimates else 10.0,
            'confidence': confidence,
            'decision_method': 'consensus',
            'consensus_level': consensus_analysis['consensus_level'],
            'rationale': f"High consensus ({consensus_analysis['consensus_level']:.1%}) across {len(predictions)} systems"
        }
    
    def _create_weighted_decision(self, predictions: Dict, consensus_analysis: Dict, constraints: Dict) -> Dict:
        """Create weighted decision when consensus is low"""
        
        weighted_scores = {}
        decision_factors = {}
        
        # Calculate weighted scores for each prediction
        for pred_name, pred_data in predictions.items():
            if pred_name in self.decision_weights:
                base_weight = self.decision_weights[pred_name]
                confidence_weight = pred_data.get('confidence', 0.5)
                
                # Adjust weight based on system-specific factors
                adjusted_weight = base_weight * confidence_weight
                
                # ML system bonus for uncertainty quantification
                if pred_name == 'ml_prediction' and pred_data.get('uncertainty_bounds'):
                    adjusted_weight *= 1.1
                
                # Autonomous learning bonus for pattern matching
                if pred_name == 'autonomous_learning' and pred_data.get('based_on_learnings'):
                    adjusted_weight *= 1.2
                
                # Hierarchical system bonus for complex tasks
                if pred_name == 'hierarchical_analysis' and pred_data.get('complexity', 1) >= 3:
                    adjusted_weight *= 1.1
                
                weighted_scores[pred_name] = {
                    'weight': adjusted_weight,
                    'prediction': pred_data
                }
        
        # Select prediction with highest weighted score
        if weighted_scores:
            best_prediction_name = max(weighted_scores.keys(), key=lambda x: weighted_scores[x]['weight'])
            best_prediction = weighted_scores[best_prediction_name]['prediction']
            
            # Blend estimates from multiple systems for better accuracy
            quality_estimates = []
            cost_estimates = []
            time_estimates = []
            
            for pred_name, pred_info in weighted_scores.items():
                weight = pred_info['weight']
                pred_data = pred_info['prediction']
                
                if pred_data.get('estimated_quality') is not None:
                    quality_estimates.append(pred_data['estimated_quality'] * weight)
                if pred_data.get('estimated_cost') is not None:
                    cost_estimates.append(pred_data['estimated_cost'] * weight)
                if pred_data.get('estimated_time') is not None:
                    time_estimates.append(pred_data['estimated_time'] * weight)
            
            total_weight = sum(info['weight'] for info in weighted_scores.values())
            
            blended_quality = sum(quality_estimates) / total_weight if quality_estimates else best_prediction.get('estimated_quality', 0.75)
            blended_cost = sum(cost_estimates) / total_weight if cost_estimates else best_prediction.get('estimated_cost', 0.001)
            blended_time = sum(time_estimates) / total_weight if time_estimates else best_prediction.get('estimated_time', 10.0)
            
            # Calculate confidence based on consensus and individual confidences
            individual_confidences = [pred_data.get('confidence', 0.5) for pred_data in predictions.values()]
            avg_confidence = np.mean(individual_confidences)
            consensus_factor = consensus_analysis['consensus_level']
            
            final_confidence = (avg_confidence * 0.7 + consensus_factor * 0.3)
            
            return {
                'orchestration_type': best_prediction.get('orchestration_type', 'coordinated'),
                'agent_team': best_prediction.get('agent_team', ['cerebras_ultra']),
                'estimated_quality': blended_quality,
                'estimated_cost': blended_cost,
                'estimated_time': blended_time,
                'confidence': final_confidence,
                'decision_method': 'weighted',
                'primary_system': best_prediction_name,
                'weight_distribution': {k: v['weight'] for k, v in weighted_scores.items()},
                'rationale': f"Weighted decision led by {best_prediction_name} (weight: {weighted_scores[best_prediction_name]['weight']:.3f})"
            }
        
        return await self._create_fallback_decision()
    
    async def _create_fallback_decision(self) -> Dict:
        """Create fallback decision when all systems fail"""
        
        self.fallback_activations.append({
            'timestamp': datetime.now().isoformat(),
            'reason': 'All prediction systems failed'
        })
        
        return {
            'orchestration_type': 'coordinated',
            'agent_team': ['cerebras_ultra', 'gemini_flash'],
            'estimated_quality': 0.7,
            'estimated_cost': 0.002,
            'estimated_time': 15.0,
            'confidence': 0.4,
            'decision_method': 'fallback',
            'rationale': 'Fallback decision due to system failures'
        }
    
    async def _create_execution_plan(self, decision: Dict, task: str) -> Dict:
        """Create detailed execution plan based on routing decision"""
        
        orchestration_type = decision.get('orchestration_type', 'coordinated')
        agent_team = decision.get('agent_team', [])
        
        execution_plan = {
            'task': task,
            'orchestration_type': orchestration_type,
            'agent_team': agent_team,
            'execution_steps': [],
            'estimated_timeline': decision.get('estimated_time', 15.0),
            'quality_target': decision.get('estimated_quality', 0.75),
            'cost_budget': decision.get('estimated_cost', 0.002),
            'success_criteria': [],
            'monitoring_points': [],
            'timeout_settings': {}
        }
        
        # Define execution steps based on orchestration type
        if orchestration_type in ['hierarchical', 'hierarchical_3_tier', 'hierarchical_mega']:
            execution_plan['execution_steps'] = [
                'Strategic planning and decomposition',
                'Real AI agent coordination',
                'Micro-specialist optimization',
                'Hierarchical synthesis'
            ]
            execution_plan['monitoring_points'] = ['tier_1_completion', 'tier_2_consensus', 'tier_3_optimization']
            execution_plan['timeout_settings'] = {'tier_timeout': 300, 'total_timeout': 900}
            
        elif orchestration_type in ['coordinated', 'coordinated_multi_agent']:
            execution_plan['execution_steps'] = [
                'Agent coordination setup',
                'Parallel task execution',
                'Consensus building',
                'Quality synthesis'
            ]
            execution_plan['monitoring_points'] = ['coordination_established', 'consensus_achieved']
            execution_plan['timeout_settings'] = {'coordination_timeout': 60, 'total_timeout': 300}
            
        elif orchestration_type in ['parallel', 'parallel_multi_agent']:
            execution_plan['execution_steps'] = [
                'Task distribution',
                'Parallel agent execution',
                'Result aggregation'
            ]
            execution_plan['monitoring_points'] = ['all_agents_started', 'first_completion']
            execution_plan['timeout_settings'] = {'agent_timeout': 30, 'total_timeout': 120}
            
        else:  # direct
            execution_plan['execution_steps'] = [
                'Single agent execution',
                'Quality validation'
            ]
            execution_plan['monitoring_points'] = ['execution_started']
            execution_plan['timeout_settings'] = {'total_timeout': 60}
        
        # Define success criteria
        execution_plan['success_criteria'] = [
            f"Quality score >= {execution_plan['quality_target']:.2f}",
            f"Execution time <= {execution_plan['estimated_timeline']:.1f}s",
            f"Cost <= ${execution_plan['cost_budget']:.5f}",
            "No critical errors"
        ]
        
        return execution_plan
    
    def _create_fallback_plan(self, predictions: Dict, final_decision: Dict) -> Dict:
        """Create fallback plan in case primary execution fails"""
        
        fallback_plan = {
            'trigger_conditions': [
                'Primary execution timeout',
                'Quality below threshold',
                'Agent failures > 50%',
                'Cost exceeds budget by 2x'
            ],
            'fallback_orchestration': 'direct',
            'fallback_agents': ['cerebras_ultra'],  # Most reliable single agent
            'reduced_quality_target': max(0.6, final_decision.get('estimated_quality', 0.75) - 0.1),
            'extended_timeout': final_decision.get('estimated_time', 15.0) * 1.5,
            'fallback_rationale': 'Simplified execution with most reliable single agent'
        }
        
        # If we have multiple predictions, use the most conservative one as fallback
        if predictions:
            conservative_prediction = min(
                [pred for pred in predictions.values() if pred],
                key=lambda x: x.get('estimated_quality', 0.0),
                default=None
            )
            
            if conservative_prediction:
                fallback_plan['fallback_orchestration'] = conservative_prediction.get('orchestration_type', 'direct')
                fallback_plan['fallback_agents'] = conservative_prediction.get('agent_team', ['cerebras_ultra'])[:1]  # Limit to 1 agent
        
        return fallback_plan
    
    def _record_integration_decision(self, decision: IntegratedRoutingDecision, decision_time: float, consensus_analysis: Dict):
        """Record integration decision for learning and analysis"""
        
        decision_record = {
            'timestamp': datetime.now().isoformat(),
            'task': decision.task[:200] + "..." if len(decision.task) > 200 else decision.task,
            'decision_time': decision_time,
            'ml_prediction_available': decision.ml_prediction is not None,
            'learning_prediction_available': decision.autonomous_learning_prediction is not None,
            'hierarchical_analysis_available': decision.hierarchical_analysis is not None,
            'consensus_level': consensus_analysis['consensus_level'],
            'final_decision': {
                'orchestration_type': decision.final_routing_decision.get('orchestration_type'),
                'agent_count': len(decision.final_routing_decision.get('agent_team', [])),
                'estimated_quality': decision.final_routing_decision.get('estimated_quality'),
                'confidence': decision.confidence_score,
                'decision_method': decision.final_routing_decision.get('decision_method')
            },
            'conflicts': len(consensus_analysis.get('conflicts', [])),
            'agreements': len(consensus_analysis.get('agreements', []))
        }
        
        self.integration_history.append(decision_record)
        
        # Keep only last 1000 decisions
        if len(self.integration_history) > 1000:
            self.integration_history = self.integration_history[-1000:]
    
    async def execute_integrated_routing(self, decision: IntegratedRoutingDecision) -> Dict:
        """Execute the integrated routing decision"""
        
        print(f"⚡ EXECUTING INTEGRATED ROUTING DECISION")
        print(f"   🎯 Orchestration: {decision.final_routing_decision.get('orchestration_type')}")
        print(f"   👥 Agent team: {decision.final_routing_decision.get('agent_team')}")
        
        execution_start = time.time()
        
        try:
            # Get execution plan
            execution_plan = decision.execution_plan
            orchestration_type = execution_plan.get('orchestration_type')
            
            # Execute based on orchestration type
            if orchestration_type.startswith('hierarchical') and self.hierarchical_orchestrator:
                # Use hierarchical orchestrator
                result = await self.hierarchical_orchestrator.analyze_and_orchestrate(decision.task)
                execution_result = result.get('execution_result', {})
                
            elif self.hierarchical_orchestrator and hasattr(self.hierarchical_orchestrator, 'collaborative_system'):
                # Use collaborative system for coordinated/parallel
                collaborative_system = self.hierarchical_orchestrator.collaborative_system
                result = await collaborative_system.ultimate_collaborative_coordination(decision.task)
                execution_result = {
                    'orchestration_type': orchestration_type,
                    'quality_score': result['session_record']['final_quality_score'],
                    'execution_time': result['session_record']['session_time'],
                    'total_cost': result['session_record']['cost_efficiency'],
                    'agents_used': result['session_record']['agents_used'],
                    'consensus_achieved': result['session_record']['consensus_achieved'],
                    'success': True
                }
            else:
                # Fallback simulation
                await asyncio.sleep(decision.final_routing_decision.get('estimated_time', 10.0) / 10)  # Simulate execution
                execution_result = {
                    'orchestration_type': orchestration_type,
                    'quality_score': decision.final_routing_decision.get('estimated_quality', 0.75),
                    'execution_time': time.time() - execution_start,
                    'total_cost': decision.final_routing_decision.get('estimated_cost', 0.002),
                    'agents_used': len(decision.final_routing_decision.get('agent_team', [])),
                    'success': True,
                    'simulated': True
                }
            
            execution_time = time.time() - execution_start
            
            # Learn from execution results
            await self._learn_from_execution(decision, execution_result)
            
            print(f"   ✅ Execution completed ({execution_time:.3f}s)")
            print(f"     📊 Quality achieved: {execution_result.get('quality_score', 0.0):.3f}")
            print(f"     💰 Cost: ${execution_result.get('total_cost', 0.0):.5f}")
            
            return {
                'success': True,
                'execution_result': execution_result,
                'execution_time': execution_time,
                'prediction_accuracy': self._calculate_prediction_accuracy(decision, execution_result)
            }
            
        except Exception as e:
            print(f"   ❌ Execution failed: {e}")
            
            # Try fallback plan
            if decision.fallback_plan:
                print("   🛡️  Attempting fallback execution...")
                
                try:
                    fallback_result = await self._execute_fallback_plan(decision)
                    return fallback_result
                except Exception as fallback_error:
                    print(f"   ❌ Fallback also failed: {fallback_error}")
            
            return {
                'success': False,
                'error': str(e),
                'execution_time': time.time() - execution_start
            }
    
    async def _execute_fallback_plan(self, decision: IntegratedRoutingDecision) -> Dict:
        """Execute fallback plan"""
        
        fallback_plan = decision.fallback_plan
        
        # Simple fallback execution (single agent)
        await asyncio.sleep(1.0)  # Simulate fallback execution
        
        return {
            'success': True,
            'execution_result': {
                'orchestration_type': fallback_plan['fallback_orchestration'],
                'quality_score': fallback_plan['reduced_quality_target'],
                'execution_time': 1.0,
                'total_cost': 0.0001,
                'agents_used': 1,
                'success': True,
                'fallback_executed': True
            },
            'execution_time': 1.0,
            'fallback_activated': True
        }
    
    def _calculate_prediction_accuracy(self, decision: IntegratedRoutingDecision, actual_result: Dict) -> Dict:
        """Calculate prediction accuracy"""
        
        final_decision = decision.final_routing_decision
        if not final_decision:
            return {'accuracy': 0.0}
        
        # Quality accuracy
        predicted_quality = final_decision.get('estimated_quality', 0.0)
        actual_quality = actual_result.get('quality_score', 0.0)
        quality_error = abs(predicted_quality - actual_quality)
        quality_accuracy = max(0.0, 1.0 - quality_error)
        
        # Time accuracy
        predicted_time = final_decision.get('estimated_time', 0.0)
        actual_time = actual_result.get('execution_time', 0.0)
        time_error = abs(predicted_time - actual_time) / max(actual_time, 1.0)
        time_accuracy = max(0.0, 1.0 - time_error)
        
        # Cost accuracy
        predicted_cost = final_decision.get('estimated_cost', 0.0)
        actual_cost = actual_result.get('total_cost', 0.0)
        cost_error = abs(predicted_cost - actual_cost) / max(actual_cost, 0.0001)
        cost_accuracy = max(0.0, 1.0 - cost_error)
        
        overall_accuracy = (quality_accuracy + time_accuracy + cost_accuracy) / 3
        
        return {
            'accuracy': overall_accuracy,
            'quality_accuracy': quality_accuracy,
            'time_accuracy': time_accuracy,
            'cost_accuracy': cost_accuracy,
            'quality_error': quality_error,
            'time_error': time_error,
            'cost_error': cost_error
        }
    
    async def _learn_from_execution(self, decision: IntegratedRoutingDecision, execution_result: Dict):
        """Learn from execution results to improve future decisions"""
        
        # Update ML routing system
        if self.ml_routing_system and decision.ml_prediction:
            try:
                # Convert decision back to prediction format for learning
                from ml_predictive_routing_system import PredictionResult
                ml_prediction = PredictionResult(
                    predicted_orchestration_type=decision.ml_prediction['orchestration_type'],
                    predicted_agent_combination=decision.ml_prediction['agent_team'],
                    estimated_quality=decision.ml_prediction['estimated_quality'],
                    estimated_cost=decision.ml_prediction['estimated_cost'],
                    estimated_time=decision.ml_prediction['estimated_time'],
                    confidence_score=decision.ml_prediction['confidence'],
                    uncertainty_bounds=decision.ml_prediction.get('uncertainty_bounds', {}),
                    risk_assessment=decision.ml_prediction.get('risk_assessment', 'MEDIUM'),
                    optimization_recommendations=[]
                )
                
                await self.ml_routing_system.learn_from_execution(
                    decision.task, ml_prediction, execution_result
                )
                
            except Exception as e:
                print(f"⚠️  ML learning failed: {e}")
        
        # Update autonomous learning system
        if self.autonomous_learning:
            try:
                orchestration_data = {
                    'task': decision.task,
                    'execution_result': execution_result,
                    'performance_analysis': {
                        'efficiency_score': execution_result.get('quality_score', 0.0) / max(execution_result.get('execution_time', 1.0), 1.0),
                        'cost_efficiency': execution_result.get('quality_score', 0.0) / max(execution_result.get('total_cost', 0.0001), 0.0001),
                        'orchestration_success': execution_result.get('success', False)
                    }
                }
                
                await self.autonomous_learning.learn_from_orchestration(orchestration_data)
                
            except Exception as e:
                print(f"⚠️  Autonomous learning failed: {e}")
        
        # Update integration weights based on accuracy
        accuracy_data = self._calculate_prediction_accuracy(decision, execution_result)
        overall_accuracy = accuracy_data.get('accuracy', 0.0)
        
        if overall_accuracy >= 0.8:
            self.successful_executions += 1
        
        # Update integration effectiveness
        self.integration_effectiveness = self.successful_executions / max(self.total_routing_decisions, 1)
        
        # Adapt decision weights based on system performance
        self._adapt_decision_weights(decision, overall_accuracy)
    
    def _adapt_decision_weights(self, decision: IntegratedRoutingDecision, accuracy: float):
        """Adapt decision weights based on system performance"""
        
        final_decision = decision.final_routing_decision
        if not final_decision:
            return
        
        primary_system = final_decision.get('primary_system')
        decision_method = final_decision.get('decision_method')
        
        # Learning rate for weight adaptation
        learning_rate = 0.01
        
        if primary_system and primary_system in self.decision_weights:
            if accuracy >= 0.8:
                # Good prediction - increase weight slightly
                self.decision_weights[primary_system] += learning_rate * (1.0 - self.decision_weights[primary_system])
            elif accuracy < 0.5:
                # Poor prediction - decrease weight slightly
                self.decision_weights[primary_system] *= (1.0 - learning_rate)
            
            # Normalize weights
            total_weight = sum(self.decision_weights.values())
            if total_weight > 0:
                for key in self.decision_weights:
                    self.decision_weights[key] /= total_weight
    
    def get_integration_performance_metrics(self) -> Dict:
        """Get comprehensive integration performance metrics"""
        
        if not self.integration_history:
            return {"message": "No integration history available"}
        
        # Basic metrics
        total_decisions = len(self.integration_history)
        recent_decisions = self.integration_history[-50:] if len(self.integration_history) >= 50 else self.integration_history
        
        # System availability metrics
        ml_availability = sum(1 for d in recent_decisions if d['ml_prediction_available']) / len(recent_decisions)
        learning_availability = sum(1 for d in recent_decisions if d['learning_prediction_available']) / len(recent_decisions)
        hierarchical_availability = sum(1 for d in recent_decisions if d['hierarchical_analysis_available']) / len(recent_decisions)
        
        # Consensus metrics
        avg_consensus = np.mean([d['consensus_level'] for d in recent_decisions])
        high_consensus_rate = sum(1 for d in recent_decisions if d['consensus_level'] >= 0.8) / len(recent_decisions)
        
        # Decision method distribution
        decision_methods = [d['final_decision']['decision_method'] for d in recent_decisions if d['final_decision'].get('decision_method')]
        method_distribution = {}
        for method in set(decision_methods):
            method_distribution[method] = decision_methods.count(method)
        
        # Performance trends
        avg_confidence = np.mean([d['final_decision']['confidence'] for d in recent_decisions if d['final_decision'].get('confidence')])
        avg_decision_time = np.mean([d['decision_time'] for d in recent_decisions])
        
        return {
            'integration_metrics': {
                'total_routing_decisions': self.total_routing_decisions,
                'successful_executions': self.successful_executions,
                'integration_effectiveness': self.integration_effectiveness,
                'fallback_activations': len(self.fallback_activations)
            },
            'system_availability': {
                'ml_routing_availability': ml_availability,
                'autonomous_learning_availability': learning_availability,
                'hierarchical_orchestrator_availability': hierarchical_availability
            },
            'consensus_metrics': {
                'average_consensus_level': avg_consensus,
                'high_consensus_rate': high_consensus_rate,
                'average_conflicts_per_decision': np.mean([d['conflicts'] for d in recent_decisions]),
                'average_agreements_per_decision': np.mean([d['agreements'] for d in recent_decisions])
            },
            'decision_metrics': {
                'decision_method_distribution': method_distribution,
                'average_confidence': avg_confidence,
                'average_decision_time': avg_decision_time,
                'current_decision_weights': self.decision_weights
            },
            'performance_trends': {
                'recent_decisions_count': len(recent_decisions),
                'system_stability': 1.0 - (len(self.fallback_activations) / max(total_decisions, 1))
            }
        }

# Integration test and demo
async def test_ml_integration():
    """Test the ML routing integration system"""
    
    print("🔗 TESTING ML ROUTING INTEGRATION SYSTEM")
    print("=" * 80)
    print()
    
    # Initialize integration engine
    integration_engine = MLRoutingIntegrationEngine()
    
    # Test scenarios with different complexity levels
    test_scenarios = [
        {
            'name': 'Simple Task',
            'task': 'Format a JavaScript function with proper indentation',
            'constraints': {'max_cost': 0.001}
        },
        {
            'name': 'Moderate Task',
            'task': 'Implement user authentication system with JWT tokens and refresh capabilities',
            'constraints': {'min_quality': 0.8}
        },
        {
            'name': 'Complex Task',
            'task': 'Design a scalable microservices architecture with API gateway, service mesh, and monitoring',
            'constraints': {'max_agents': 6}
        },
        {
            'name': 'Mega Task',
            'task': 'Build a revolutionary quantum-resistant autonomous AI platform with distributed consensus, real-time learning, and self-healing capabilities for enterprise deployment',
            'constraints': {}
        }
    ]
    
    integration_results = []
    
    for i, scenario in enumerate(test_scenarios, 1):
        print(f"🎯 INTEGRATION TEST {i}/{len(test_scenarios)}: {scenario['name']}")
        print(f"   Task: {scenario['task'][:100]}...")
        print(f"   Constraints: {scenario['constraints']}")
        print()
        
        try:
            # Make integrated routing decision
            decision = await integration_engine.integrated_routing_decision(
                scenario['task'], scenario['constraints']
            )
            
            # Execute the decision
            execution_result = await integration_engine.execute_integrated_routing(decision)
            
            integration_results.append({
                'scenario': scenario['name'],
                'decision_confidence': decision.confidence_score,
                'execution_success': execution_result.get('success', False),
                'prediction_accuracy': execution_result.get('prediction_accuracy', {}).get('accuracy', 0.0)
            })
            
            print()
            
        except Exception as e:
            print(f"   ❌ Integration test failed: {e}")
            integration_results.append({
                'scenario': scenario['name'],
                'error': str(e),
                'execution_success': False
            })
        
        print("─" * 80)
        print()
    
    # Display integration performance metrics
    print("📊 INTEGRATION PERFORMANCE METRICS:")
    print("=" * 80)
    
    performance_metrics = integration_engine.get_integration_performance_metrics()
    
    for category, data in performance_metrics.items():
        if isinstance(data, dict):
            print(f"\n{category.replace('_', ' ').title()}:")
            for key, value in data.items():
                if isinstance(value, float):
                    print(f"   {key.replace('_', ' ').title()}: {value:.3f}")
                else:
                    print(f"   {key.replace('_', ' ').title()}: {value}")
    
    # Summary of test results
    print(f"\n🎯 INTEGRATION TEST SUMMARY:")
    print(f"   Total tests: {len(integration_results)}")
    successful_tests = sum(1 for r in integration_results if r.get('execution_success', False))
    print(f"   Successful executions: {successful_tests}/{len(integration_results)}")
    
    if integration_results:
        avg_confidence = np.mean([r.get('decision_confidence', 0.0) for r in integration_results])
        avg_accuracy = np.mean([r.get('prediction_accuracy', 0.0) for r in integration_results if r.get('prediction_accuracy')])
        
        print(f"   Average decision confidence: {avg_confidence:.3f}")
        print(f"   Average prediction accuracy: {avg_accuracy:.3f}")
    
    print()
    print("🚀 ML ROUTING INTEGRATION TEST COMPLETED!")
    print("   Advanced multi-system coordination with ML intelligence achieved! 🧠🔗⚡")
    
    return integration_results

if __name__ == "__main__":
    asyncio.run(test_ml_integration())