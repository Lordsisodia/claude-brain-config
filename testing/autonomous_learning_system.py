#!/usr/bin/env python3
"""
AUTONOMOUS LEARNING SYSTEM
Self-improving AI coordination through continuous learning
"""

import asyncio
import json
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from pathlib import Path
import hashlib
import pickle

@dataclass
class LearningPattern:
    """Pattern learned from orchestration history"""
    pattern_id: str
    task_characteristics: Dict[str, Any]
    optimal_agents: List[str]
    optimal_orchestration_type: str
    average_quality: float
    average_cost: float
    average_time: float
    success_rate: float
    confidence_score: float
    usage_count: int
    last_updated: str

@dataclass
class PerformanceMetric:
    """Performance metric for learning"""
    metric_name: str
    agent_name: str
    task_type: str
    value: float
    timestamp: str
    context: Dict[str, Any]

class AutonomousLearningEngine:
    """Revolutionary autonomous learning system for AI coordination"""
    
    def __init__(self):
        self.learning_patterns = {}
        self.performance_history = []
        self.agent_expertise_map = {}
        self.task_complexity_model = {}
        self.optimization_rules = {}
        
        # Learning parameters
        self.learning_rate = 0.1
        self.pattern_confidence_threshold = 0.7
        self.minimum_pattern_samples = 3
        self.memory_decay_factor = 0.95
        
        # Performance tracking
        self.total_learning_sessions = 0
        self.patterns_discovered = 0
        self.optimization_improvements = 0
        self.predictive_accuracy = 0.0
        
        print("🧠 AUTONOMOUS LEARNING SYSTEM INITIALIZED")
        print("   📊 Learning Rate: 0.1")
        print("   🎯 Confidence Threshold: 0.7")
        print("   💾 Memory Decay: 0.95")
        print()
    
    async def learn_from_orchestration(self, orchestration_data: Dict) -> Dict:
        """Learn from orchestration execution and outcomes"""
        
        print("🧠 AUTONOMOUS LEARNING SESSION")
        print(f"   📋 Learning from: {orchestration_data.get('task', 'Unknown task')[:50]}...")
        
        learning_start = time.time()
        
        # Extract learning features
        features = self._extract_learning_features(orchestration_data)
        
        # Update agent expertise mapping
        self._update_agent_expertise(orchestration_data, features)
        
        # Discover or update patterns
        pattern_updates = await self._discover_update_patterns(orchestration_data, features)
        
        # Learn optimization rules
        optimization_updates = self._learn_optimization_rules(orchestration_data, features)
        
        # Update predictive models
        model_updates = self._update_predictive_models(orchestration_data, features)
        
        # Record performance metrics
        self._record_performance_metrics(orchestration_data, features)
        
        learning_time = time.time() - learning_start
        self.total_learning_sessions += 1
        
        learning_summary = {
            'learning_session_id': f"learn_{int(time.time()*1000)}",
            'task_analyzed': orchestration_data.get('task', 'Unknown'),
            'features_extracted': len(features),
            'patterns_updated': len(pattern_updates),
            'optimization_rules_learned': len(optimization_updates),
            'model_improvements': len(model_updates),
            'learning_time': learning_time,
            'learning_effectiveness': self._calculate_learning_effectiveness(pattern_updates, optimization_updates),
            'timestamp': datetime.now().isoformat()
        }
        
        print(f"   ✅ Patterns updated: {len(pattern_updates)}")
        print(f"   🔧 Optimizations learned: {len(optimization_updates)}")
        print(f"   📈 Models improved: {len(model_updates)}")
        print(f"   ⚡ Learning time: {learning_time:.3f}s")
        
        return learning_summary
    
    def _extract_learning_features(self, orchestration_data: Dict) -> Dict:
        """Extract features for learning from orchestration data"""
        
        task = orchestration_data.get('task', '')
        execution_result = orchestration_data.get('execution_result', {})
        performance_analysis = orchestration_data.get('performance_analysis', {})
        
        # Task characteristics
        task_features = {
            'task_length': len(task),
            'complexity_keywords': self._count_complexity_keywords(task),
            'domain_indicators': self._identify_domain_indicators(task),
            'urgency_indicators': self._detect_urgency_indicators(task),
            'technical_depth': self._assess_technical_depth(task)
        }
        
        # Execution characteristics
        execution_features = {
            'orchestration_type': execution_result.get('orchestration_type', 'unknown'),
            'agents_used': execution_result.get('agents_used', 0),
            'quality_score': execution_result.get('quality_score', 0.0),
            'total_cost': execution_result.get('total_cost', 0.0),
            'execution_time': execution_result.get('execution_time', 0.0),
            'consensus_achieved': execution_result.get('consensus_achieved', False),
            'breakthrough_achieved': execution_result.get('breakthrough_achieved', False)
        }
        
        # Performance characteristics
        performance_features = {
            'efficiency_score': performance_analysis.get('efficiency_score', 0.0),
            'cost_efficiency': performance_analysis.get('cost_efficiency', 0.0),
            'time_efficiency': performance_analysis.get('time_efficiency', 0.0),
            'quality_per_agent': performance_analysis.get('quality_per_agent', 0.0),
            'orchestration_success': performance_analysis.get('orchestration_success', False)
        }
        
        return {
            **task_features,
            **execution_features,
            **performance_features,
            'timestamp': datetime.now().isoformat()
        }
    
    def _count_complexity_keywords(self, task: str) -> Dict[str, int]:
        """Count complexity-indicating keywords"""
        
        keyword_categories = {
            'mega': ['enterprise', 'platform', 'ecosystem', 'autonomous', 'revolutionary', 'quantum', 'distributed'],
            'complex': ['architecture', 'system', 'framework', 'infrastructure', 'scalable', 'security'],
            'moderate': ['implement', 'build', 'create', 'develop', 'design', 'optimize'],
            'simple': ['format', 'list', 'show', 'display', 'basic', 'simple']
        }
        
        task_lower = task.lower()
        counts = {}
        
        for category, keywords in keyword_categories.items():
            counts[category] = sum(1 for keyword in keywords if keyword in task_lower)
        
        return counts
    
    def _identify_domain_indicators(self, task: str) -> List[str]:
        """Identify domain/specialization indicators"""
        
        domain_keywords = {
            'security': ['security', 'encryption', 'auth', 'compliance', 'vulnerability'],
            'architecture': ['architecture', 'design', 'microservices', 'api', 'database'],
            'performance': ['performance', 'optimization', 'scalability', 'efficiency', 'speed'],
            'ai_ml': ['ai', 'ml', 'neural', 'learning', 'intelligence', 'model'],
            'devops': ['deployment', 'container', 'kubernetes', 'infrastructure', 'pipeline'],
            'frontend': ['ui', 'interface', 'user', 'frontend', 'react', 'vue'],
            'data': ['data', 'analytics', 'pipeline', 'etl', 'warehouse', 'processing']
        }
        
        task_lower = task.lower()
        identified_domains = []
        
        for domain, keywords in domain_keywords.items():
            if any(keyword in task_lower for keyword in keywords):
                identified_domains.append(domain)
        
        return identified_domains
    
    def _detect_urgency_indicators(self, task: str) -> Dict[str, bool]:
        """Detect urgency and priority indicators"""
        
        urgency_indicators = {
            'high_priority': ['urgent', 'critical', 'emergency', 'asap', 'immediately'],
            'time_sensitive': ['deadline', 'quickly', 'fast', 'rapid', 'rush'],
            'quality_focus': ['high-quality', 'excellent', 'perfect', 'best', 'optimal'],
            'cost_sensitive': ['budget', 'cheap', 'affordable', 'cost-effective', 'economical']
        }
        
        task_lower = task.lower()
        indicators = {}
        
        for indicator_type, keywords in urgency_indicators.items():
            indicators[indicator_type] = any(keyword in task_lower for keyword in keywords)
        
        return indicators
    
    def _assess_technical_depth(self, task: str) -> float:
        """Assess technical depth/complexity on 0-1 scale"""
        
        technical_terms = [
            'algorithm', 'protocol', 'framework', 'architecture', 'infrastructure',
            'optimization', 'distributed', 'concurrent', 'asynchronous', 'scalable',
            'microservices', 'kubernetes', 'docker', 'api', 'database', 'encryption',
            'neural', 'quantum', 'blockchain', 'machine learning', 'artificial intelligence'
        ]
        
        task_lower = task.lower()
        technical_count = sum(1 for term in technical_terms if term in task_lower)
        
        # Normalize to 0-1 scale
        max_possible_terms = len(technical_terms)
        technical_depth = min(1.0, technical_count / max(max_possible_terms * 0.3, 1))
        
        return technical_depth
    
    def _update_agent_expertise(self, orchestration_data: Dict, features: Dict):
        """Update agent expertise mapping based on performance"""
        
        execution_result = orchestration_data.get('execution_result', {})
        
        # Extract agent performance data
        if 'real_ai_results' in orchestration_data:
            real_results = orchestration_data['real_ai_results']
            if 'successful_agents' in real_results:
                for agent_data in real_results['successful_agents']:
                    agent_name = agent_data.get('agent_name')
                    specialization = agent_data.get('specialization')
                    quality_score = agent_data.get('quality_metrics', {}).get('overall_score', 0.0)
                    
                    if agent_name:
                        if agent_name not in self.agent_expertise_map:
                            self.agent_expertise_map[agent_name] = {
                                'specializations': {},
                                'performance_history': [],
                                'average_quality': 0.0,
                                'task_count': 0,
                                'expertise_confidence': 0.0
                            }
                        
                        agent_profile = self.agent_expertise_map[agent_name]
                        
                        # Update specialization performance
                        if specialization not in agent_profile['specializations']:
                            agent_profile['specializations'][specialization] = {
                                'quality_scores': [],
                                'task_types': [],
                                'average_quality': 0.0
                            }
                        
                        spec_data = agent_profile['specializations'][specialization]
                        spec_data['quality_scores'].append(quality_score)
                        spec_data['task_types'].append(features.get('domain_indicators', []))
                        spec_data['average_quality'] = np.mean(spec_data['quality_scores'])
                        
                        # Update overall performance
                        agent_profile['performance_history'].append({
                            'quality_score': quality_score,
                            'specialization': specialization,
                            'task_domains': features.get('domain_indicators', []),
                            'timestamp': datetime.now().isoformat()
                        })
                        
                        # Keep only last 50 performances
                        if len(agent_profile['performance_history']) > 50:
                            agent_profile['performance_history'] = agent_profile['performance_history'][-50:]
                        
                        # Update averages
                        agent_profile['task_count'] += 1
                        agent_profile['average_quality'] = np.mean([
                            p['quality_score'] for p in agent_profile['performance_history']
                        ])
                        
                        # Calculate expertise confidence based on consistency
                        if len(agent_profile['performance_history']) >= 3:
                            quality_scores = [p['quality_score'] for p in agent_profile['performance_history']]
                            quality_std = np.std(quality_scores)
                            agent_profile['expertise_confidence'] = max(0.0, 1.0 - quality_std)
    
    async def _discover_update_patterns(self, orchestration_data: Dict, features: Dict) -> List[Dict]:
        """Discover new patterns or update existing ones"""
        
        pattern_updates = []
        
        # Create pattern signature based on task characteristics
        pattern_signature = self._create_pattern_signature(features)
        
        execution_result = orchestration_data.get('execution_result', {})
        performance_analysis = orchestration_data.get('performance_analysis', {})
        
        # Check if pattern exists
        if pattern_signature in self.learning_patterns:
            # Update existing pattern
            pattern = self.learning_patterns[pattern_signature]
            
            # Update performance metrics with exponential moving average
            alpha = self.learning_rate
            pattern.average_quality = (1 - alpha) * pattern.average_quality + alpha * features['quality_score']
            pattern.average_cost = (1 - alpha) * pattern.average_cost + alpha * features['total_cost']
            pattern.average_time = (1 - alpha) * pattern.average_time + alpha * features['execution_time']
            
            # Update success rate
            current_success = 1.0 if features['orchestration_success'] else 0.0
            pattern.success_rate = (1 - alpha) * pattern.success_rate + alpha * current_success
            
            # Update confidence based on consistency
            pattern.usage_count += 1
            pattern.confidence_score = min(1.0, pattern.usage_count / 10.0) * pattern.success_rate
            pattern.last_updated = datetime.now().isoformat()
            
            pattern_updates.append({
                'action': 'updated',
                'pattern_id': pattern_signature,
                'confidence': pattern.confidence_score
            })
            
        else:
            # Create new pattern
            new_pattern = LearningPattern(
                pattern_id=pattern_signature,
                task_characteristics=self._extract_task_characteristics(features),
                optimal_agents=self._extract_optimal_agents(orchestration_data),
                optimal_orchestration_type=features['orchestration_type'],
                average_quality=features['quality_score'],
                average_cost=features['total_cost'],
                average_time=features['execution_time'],
                success_rate=1.0 if features['orchestration_success'] else 0.0,
                confidence_score=0.1,  # Low initial confidence
                usage_count=1,
                last_updated=datetime.now().isoformat()
            )
            
            self.learning_patterns[pattern_signature] = new_pattern
            self.patterns_discovered += 1
            
            pattern_updates.append({
                'action': 'created',
                'pattern_id': pattern_signature,
                'confidence': new_pattern.confidence_score
            })
        
        return pattern_updates
    
    def _create_pattern_signature(self, features: Dict) -> str:
        """Create unique signature for pattern matching"""
        
        # Create signature based on key task characteristics
        signature_components = [
            str(features.get('complexity_keywords', {})),
            str(sorted(features.get('domain_indicators', []))),
            str(features.get('urgency_indicators', {})),
            f"tech_depth_{features.get('technical_depth', 0.0):.1f}",
            f"agents_{features.get('agents_used', 0)}"
        ]
        
        signature_string = "_".join(signature_components)
        
        # Create hash for consistent pattern identification
        return hashlib.md5(signature_string.encode()).hexdigest()[:16]
    
    def _extract_task_characteristics(self, features: Dict) -> Dict:
        """Extract key task characteristics for pattern"""
        
        return {
            'complexity_level': max(features.get('complexity_keywords', {}), key=lambda k: features['complexity_keywords'].get(k, 0), default='simple'),
            'primary_domains': features.get('domain_indicators', [])[:3],  # Top 3 domains
            'technical_depth': features.get('technical_depth', 0.0),
            'urgency_profile': features.get('urgency_indicators', {}),
            'estimated_agents_needed': features.get('agents_used', 1)
        }
    
    def _extract_optimal_agents(self, orchestration_data: Dict) -> List[str]:
        """Extract optimal agent combination from successful orchestration"""
        
        optimal_agents = []
        
        # Extract from real AI results
        if 'real_ai_results' in orchestration_data:
            real_results = orchestration_data['real_ai_results']
            if 'successful_agents' in real_results:
                for agent_data in real_results['successful_agents']:
                    agent_name = agent_data.get('agent_name')
                    quality_score = agent_data.get('quality_metrics', {}).get('overall_score', 0.0)
                    
                    if agent_name and quality_score >= 0.7:  # Only include high-quality agents
                        optimal_agents.append(agent_name)
        
        # Fallback to execution result data
        if not optimal_agents and 'execution_result' in orchestration_data:
            result = orchestration_data['execution_result']
            if result.get('orchestration_success', False):
                # Extract agent names from orchestration type
                orch_type = result.get('orchestration_type', '')
                if 'hierarchical' in orch_type:
                    optimal_agents = ['cerebras_ultra', 'gemini_flash', 'groq_lightning', 'scaleway_eu']
                elif 'coordinated' in orch_type or 'collaborative' in orch_type:
                    optimal_agents = ['cerebras_ultra', 'gemini_flash', 'groq_lightning', 'scaleway_eu']
                elif 'parallel' in orch_type:
                    optimal_agents = ['cerebras_ultra', 'gemini_flash', 'groq_lightning']
                else:
                    optimal_agents = ['cerebras_ultra']
        
        return optimal_agents
    
    def _learn_optimization_rules(self, orchestration_data: Dict, features: Dict) -> List[Dict]:
        """Learn optimization rules from successful orchestrations"""
        
        optimization_updates = []
        
        if features.get('orchestration_success', False):
            # Rule: High-quality agents for complex tasks
            if features.get('technical_depth', 0.0) > 0.7 and features.get('quality_score', 0.0) > 0.8:
                rule_id = "high_quality_for_complex"
                if rule_id not in self.optimization_rules:
                    self.optimization_rules[rule_id] = {
                        'condition': 'technical_depth > 0.7',
                        'action': 'prioritize_high_quality_agents',
                        'confidence': 0.1,
                        'success_count': 0
                    }
                
                rule = self.optimization_rules[rule_id]
                rule['success_count'] += 1
                rule['confidence'] = min(1.0, rule['success_count'] / 10.0)
                
                optimization_updates.append({
                    'rule_id': rule_id,
                    'confidence': rule['confidence']
                })
            
            # Rule: Parallel execution for moderate complexity
            if (features.get('agents_used', 0) >= 3 and 
                features.get('efficiency_score', 0.0) > 0.5 and
                features.get('technical_depth', 0.0) < 0.7):
                
                rule_id = "parallel_for_moderate"
                if rule_id not in self.optimization_rules:
                    self.optimization_rules[rule_id] = {
                        'condition': 'moderate_complexity and multiple_domains',
                        'action': 'use_parallel_orchestration',
                        'confidence': 0.1,
                        'success_count': 0
                    }
                
                rule = self.optimization_rules[rule_id]
                rule['success_count'] += 1
                rule['confidence'] = min(1.0, rule['success_count'] / 10.0)
                
                optimization_updates.append({
                    'rule_id': rule_id,
                    'confidence': rule['confidence']
                })
            
            # Rule: Cost optimization for simple tasks
            if (features.get('agents_used', 0) == 1 and 
                features.get('total_cost', 0.0) < 0.001 and
                features.get('quality_score', 0.0) > 0.6):
                
                rule_id = "cost_optimize_simple"
                if rule_id not in self.optimization_rules:
                    self.optimization_rules[rule_id] = {
                        'condition': 'simple_task and cost_sensitive',
                        'action': 'use_single_efficient_agent',
                        'confidence': 0.1,
                        'success_count': 0
                    }
                
                rule = self.optimization_rules[rule_id]
                rule['success_count'] += 1
                rule['confidence'] = min(1.0, rule['success_count'] / 10.0)
                
                optimization_updates.append({
                    'rule_id': rule_id,
                    'confidence': rule['confidence']
                })
        
        self.optimization_improvements += len(optimization_updates)
        return optimization_updates
    
    def _update_predictive_models(self, orchestration_data: Dict, features: Dict) -> List[Dict]:
        """Update predictive models for task complexity and agent selection"""
        
        model_updates = []
        
        # Update task complexity model
        actual_complexity = features.get('orchestration_type', 'direct')
        predicted_complexity = self._predict_task_complexity_from_features(features)
        
        if actual_complexity != predicted_complexity:
            # Model needs updating
            complexity_key = f"complexity_prediction_{features.get('technical_depth', 0.0):.1f}"
            
            if complexity_key not in self.task_complexity_model:
                self.task_complexity_model[complexity_key] = {
                    'predictions': [],
                    'actuals': [],
                    'accuracy': 0.0
                }
            
            model = self.task_complexity_model[complexity_key]
            model['predictions'].append(predicted_complexity)
            model['actuals'].append(actual_complexity)
            
            # Calculate accuracy
            if len(model['predictions']) >= 5:
                correct_predictions = sum(1 for p, a in zip(model['predictions'], model['actuals']) if p == a)
                model['accuracy'] = correct_predictions / len(model['predictions'])
                
                model_updates.append({
                    'model': 'task_complexity',
                    'key': complexity_key,
                    'accuracy': model['accuracy']
                })
        
        return model_updates
    
    def _predict_task_complexity_from_features(self, features: Dict) -> str:
        """Predict task complexity from features (simplified)"""
        
        complexity_keywords = features.get('complexity_keywords', {})
        technical_depth = features.get('technical_depth', 0.0)
        domain_count = len(features.get('domain_indicators', []))
        
        mega_score = complexity_keywords.get('mega', 0)
        complex_score = complexity_keywords.get('complex', 0)
        
        if mega_score >= 2 or technical_depth > 0.8 or domain_count >= 4:
            return 'hierarchical'
        elif complex_score >= 2 or technical_depth > 0.6 or domain_count >= 3:
            return 'coordinated'
        elif domain_count >= 2 or technical_depth > 0.3:
            return 'parallel'
        else:
            return 'direct'
    
    def _record_performance_metrics(self, orchestration_data: Dict, features: Dict):
        """Record performance metrics for analysis"""
        
        metrics = [
            PerformanceMetric(
                metric_name='quality_score',
                agent_name='system',
                task_type=features.get('orchestration_type', 'unknown'),
                value=features.get('quality_score', 0.0),
                timestamp=datetime.now().isoformat(),
                context={'technical_depth': features.get('technical_depth', 0.0)}
            ),
            PerformanceMetric(
                metric_name='efficiency_score',
                agent_name='system',
                task_type=features.get('orchestration_type', 'unknown'),
                value=features.get('efficiency_score', 0.0),
                timestamp=datetime.now().isoformat(),
                context={'agents_used': features.get('agents_used', 0)}
            ),
            PerformanceMetric(
                metric_name='cost_efficiency',
                agent_name='system',
                task_type=features.get('orchestration_type', 'unknown'),
                value=features.get('cost_efficiency', 0.0),
                timestamp=datetime.now().isoformat(),
                context={'total_cost': features.get('total_cost', 0.0)}
            )
        ]
        
        self.performance_history.extend(metrics)
        
        # Keep only last 1000 metrics
        if len(self.performance_history) > 1000:
            self.performance_history = self.performance_history[-1000:]
    
    def _calculate_learning_effectiveness(self, pattern_updates: List[Dict], optimization_updates: List[Dict]) -> float:
        """Calculate effectiveness of learning session"""
        
        pattern_score = len(pattern_updates) * 0.3
        optimization_score = len(optimization_updates) * 0.5
        
        # Bonus for high-confidence patterns
        confidence_bonus = sum(
            update.get('confidence', 0.0) * 0.2 
            for update in pattern_updates + optimization_updates
        )
        
        effectiveness = min(1.0, pattern_score + optimization_score + confidence_bonus)
        return effectiveness
    
    async def predict_optimal_orchestration(self, task: str) -> Dict:
        """Predict optimal orchestration approach using learned patterns"""
        
        print(f"🔮 PREDICTIVE ORCHESTRATION ANALYSIS")
        print(f"   📋 Task: {task[:50]}...")
        
        # Extract features from task
        mock_orchestration_data = {
            'task': task,
            'execution_result': {'agents_used': 1, 'quality_score': 0.5, 'total_cost': 0.001, 'execution_time': 1.0},
            'performance_analysis': {'efficiency_score': 0.5}
        }
        
        features = self._extract_learning_features(mock_orchestration_data)
        
        # Find matching patterns
        matching_patterns = self._find_matching_patterns(features)
        
        if matching_patterns:
            # Select best pattern based on confidence and performance
            best_pattern = max(matching_patterns, key=lambda p: p.confidence_score * p.average_quality)
            
            prediction = {
                'predicted_orchestration_type': best_pattern.optimal_orchestration_type,
                'recommended_agents': best_pattern.optimal_agents,
                'expected_quality': best_pattern.average_quality,
                'expected_cost': best_pattern.average_cost,
                'expected_time': best_pattern.average_time,
                'confidence': best_pattern.confidence_score,
                'pattern_id': best_pattern.pattern_id,
                'based_on_learnings': True
            }
            
            print(f"   🎯 Predicted orchestration: {prediction['predicted_orchestration_type']}")
            print(f"   🤖 Recommended agents: {len(prediction['recommended_agents'])}")
            print(f"   📊 Expected quality: {prediction['expected_quality']:.3f}")
            print(f"   🔮 Confidence: {prediction['confidence']:.3f}")
            
        else:
            # Fallback to rule-based prediction
            prediction = self._fallback_prediction(features)
            prediction['based_on_learnings'] = False
            
            print(f"   ⚠️ No matching patterns, using fallback prediction")
            print(f"   🎯 Predicted orchestration: {prediction['predicted_orchestration_type']}")
        
        return prediction
    
    def _find_matching_patterns(self, features: Dict) -> List[LearningPattern]:
        """Find patterns that match current task features"""
        
        matching_patterns = []
        
        for pattern in self.learning_patterns.values():
            if pattern.confidence_score < self.pattern_confidence_threshold:
                continue
            
            # Calculate similarity between features and pattern characteristics
            similarity = self._calculate_pattern_similarity(features, pattern.task_characteristics)
            
            if similarity > 0.7:  # 70% similarity threshold
                matching_patterns.append(pattern)
        
        return matching_patterns
    
    def _calculate_pattern_similarity(self, features: Dict, pattern_characteristics: Dict) -> float:
        """Calculate similarity between task features and pattern characteristics"""
        
        similarity_scores = []
        
        # Domain similarity
        task_domains = set(features.get('domain_indicators', []))
        pattern_domains = set(pattern_characteristics.get('primary_domains', []))
        
        if task_domains or pattern_domains:
            domain_similarity = len(task_domains & pattern_domains) / max(len(task_domains | pattern_domains), 1)
            similarity_scores.append(domain_similarity)
        
        # Technical depth similarity
        task_depth = features.get('technical_depth', 0.0)
        pattern_depth = pattern_characteristics.get('technical_depth', 0.0)
        depth_similarity = 1.0 - abs(task_depth - pattern_depth)
        similarity_scores.append(depth_similarity)
        
        # Complexity similarity
        task_complexity = features.get('complexity_keywords', {})
        pattern_complexity = pattern_characteristics.get('complexity_level', 'simple')
        
        # Simple complexity matching
        if task_complexity and pattern_complexity:
            task_max_complexity = max(task_complexity, key=task_complexity.get)
            complexity_similarity = 1.0 if task_max_complexity == pattern_complexity else 0.5
            similarity_scores.append(complexity_similarity)
        
        return np.mean(similarity_scores) if similarity_scores else 0.0
    
    def _fallback_prediction(self, features: Dict) -> Dict:
        """Fallback prediction when no patterns match"""
        
        technical_depth = features.get('technical_depth', 0.0)
        domain_count = len(features.get('domain_indicators', []))
        complexity_keywords = features.get('complexity_keywords', {})
        
        if technical_depth > 0.8 or complexity_keywords.get('mega', 0) >= 2:
            orchestration_type = 'hierarchical'
            recommended_agents = ['cerebras_ultra', 'gemini_flash', 'groq_lightning', 'scaleway_eu']
            expected_quality = 0.8
            expected_cost = 0.004
            expected_time = 20.0
        elif technical_depth > 0.6 or complexity_keywords.get('complex', 0) >= 2:
            orchestration_type = 'coordinated'
            recommended_agents = ['cerebras_ultra', 'gemini_flash', 'groq_lightning', 'scaleway_eu']
            expected_quality = 0.75
            expected_cost = 0.0003
            expected_time = 15.0
        elif domain_count >= 2 or technical_depth > 0.3:
            orchestration_type = 'parallel'
            recommended_agents = ['cerebras_ultra', 'gemini_flash', 'groq_lightning']
            expected_quality = 0.7
            expected_cost = 0.0002
            expected_time = 10.0
        else:
            orchestration_type = 'direct'
            recommended_agents = ['cerebras_ultra']
            expected_quality = 0.65
            expected_cost = 0.0001
            expected_time = 5.0
        
        return {
            'predicted_orchestration_type': orchestration_type,
            'recommended_agents': recommended_agents,
            'expected_quality': expected_quality,
            'expected_cost': expected_cost,
            'expected_time': expected_time,
            'confidence': 0.5,  # Lower confidence for fallback
            'pattern_id': 'fallback'
        }
    
    def get_learning_insights(self) -> Dict:
        """Get comprehensive learning insights"""
        
        if not self.learning_patterns:
            return {"message": "No learning patterns discovered yet"}
        
        # Pattern analysis
        total_patterns = len(self.learning_patterns)
        high_confidence_patterns = sum(1 for p in self.learning_patterns.values() if p.confidence_score >= self.pattern_confidence_threshold)
        avg_pattern_quality = np.mean([p.average_quality for p in self.learning_patterns.values()])
        
        # Agent expertise analysis
        agent_count = len(self.agent_expertise_map)
        avg_agent_confidence = np.mean([
            agent['expertise_confidence'] 
            for agent in self.agent_expertise_map.values() 
            if agent['expertise_confidence'] > 0
        ]) if self.agent_expertise_map else 0.0
        
        # Performance trends
        recent_metrics = self.performance_history[-50:] if len(self.performance_history) >= 50 else self.performance_history
        avg_recent_quality = np.mean([m.value for m in recent_metrics if m.metric_name == 'quality_score']) if recent_metrics else 0.0
        
        return {
            'learning_statistics': {
                'total_learning_sessions': self.total_learning_sessions,
                'patterns_discovered': self.patterns_discovered,
                'optimization_improvements': self.optimization_improvements,
                'total_patterns': total_patterns,
                'high_confidence_patterns': high_confidence_patterns,
                'pattern_confidence_rate': high_confidence_patterns / max(total_patterns, 1)
            },
            'pattern_insights': {
                'average_pattern_quality': avg_pattern_quality,
                'most_successful_pattern': max(self.learning_patterns.values(), key=lambda p: p.average_quality).pattern_id if self.learning_patterns else None,
                'most_used_pattern': max(self.learning_patterns.values(), key=lambda p: p.usage_count).pattern_id if self.learning_patterns else None
            },
            'agent_expertise': {
                'agents_tracked': agent_count,
                'average_expertise_confidence': avg_agent_confidence,
                'total_performance_records': len(self.performance_history)
            },
            'optimization_rules': {
                'total_rules_learned': len(self.optimization_rules),
                'high_confidence_rules': sum(1 for r in self.optimization_rules.values() if r['confidence'] >= 0.7)
            },
            'performance_trends': {
                'recent_average_quality': avg_recent_quality,
                'learning_effectiveness': self._calculate_overall_learning_effectiveness()
            }
        }
    
    def _calculate_overall_learning_effectiveness(self) -> float:
        """Calculate overall learning effectiveness"""
        
        if not self.learning_patterns:
            return 0.0
        
        # Factors: pattern confidence, agent expertise, optimization rules
        pattern_effectiveness = np.mean([p.confidence_score for p in self.learning_patterns.values()])
        
        agent_effectiveness = np.mean([
            agent['expertise_confidence'] 
            for agent in self.agent_expertise_map.values()
        ]) if self.agent_expertise_map else 0.0
        
        rule_effectiveness = np.mean([
            rule['confidence'] 
            for rule in self.optimization_rules.values()
        ]) if self.optimization_rules else 0.0
        
        overall_effectiveness = (pattern_effectiveness * 0.4 + agent_effectiveness * 0.3 + rule_effectiveness * 0.3)
        return overall_effectiveness
    
    def save_learning_state(self, filepath: str = "autonomous_learning_state.json"):
        """Save learning state for persistence"""
        
        learning_state = {
            'learning_patterns': {pid: asdict(pattern) for pid, pattern in self.learning_patterns.items()},
            'agent_expertise_map': self.agent_expertise_map,
            'optimization_rules': self.optimization_rules,
            'performance_metrics': {
                'total_learning_sessions': self.total_learning_sessions,
                'patterns_discovered': self.patterns_discovered,
                'optimization_improvements': self.optimization_improvements
            },
            'last_saved': datetime.now().isoformat()
        }
        
        with open(filepath, 'w') as f:
            json.dump(learning_state, f, indent=2)
        
        print(f"🧠 Learning state saved to: {filepath}")

# Test the autonomous learning system
async def test_autonomous_learning():
    """Test the autonomous learning system"""
    
    print("🧠 TESTING AUTONOMOUS LEARNING SYSTEM")
    print("=" * 60)
    print()
    
    learning_engine = AutonomousLearningEngine()
    
    # Simulate orchestration data for learning
    test_orchestrations = [
        {
            'task': 'Build a scalable microservices architecture with API gateway',
            'execution_result': {
                'orchestration_type': 'coordinated_multi_agent',
                'agents_used': 4,
                'quality_score': 0.85,
                'total_cost': 0.0003,
                'execution_time': 15.0,
                'consensus_achieved': True,
                'breakthrough_achieved': False
            },
            'performance_analysis': {
                'efficiency_score': 0.8,
                'cost_efficiency': 2833.33,
                'time_efficiency': 0.057,
                'quality_per_agent': 0.21,
                'orchestration_success': True
            },
            'real_ai_results': {
                'successful_agents': [
                    {'agent_name': 'cerebras_ultra', 'specialization': 'architecture', 'quality_metrics': {'overall_score': 0.9}},
                    {'agent_name': 'gemini_flash', 'specialization': 'reasoning', 'quality_metrics': {'overall_score': 0.85}},
                    {'agent_name': 'groq_lightning', 'specialization': 'documentation', 'quality_metrics': {'overall_score': 0.8}},
                    {'agent_name': 'scaleway_eu', 'specialization': 'security', 'quality_metrics': {'overall_score': 0.75}}
                ]
            }
        },
        {
            'task': 'Format a simple JavaScript function with proper indentation',
            'execution_result': {
                'orchestration_type': 'direct_single_agent',
                'agents_used': 1,
                'quality_score': 0.7,
                'total_cost': 0.0001,
                'execution_time': 1.0,
                'orchestration_success': True
            },
            'performance_analysis': {
                'efficiency_score': 0.7,
                'cost_efficiency': 7000.0,
                'time_efficiency': 0.7,
                'quality_per_agent': 0.7,
                'orchestration_success': True
            }
        },
        {
            'task': 'Design quantum-resistant autonomous AI platform with distributed consensus',
            'execution_result': {
                'orchestration_type': 'hierarchical_3_tier',
                'agents_used': 13,
                'quality_score': 0.95,
                'total_cost': 0.004,
                'execution_time': 25.0,
                'consensus_achieved': True,
                'breakthrough_achieved': True
            },
            'performance_analysis': {
                'efficiency_score': 0.9,
                'cost_efficiency': 237.5,
                'time_efficiency': 0.038,
                'quality_per_agent': 0.073,
                'orchestration_success': True
            }
        }
    ]
    
    # Learn from orchestrations
    for i, orchestration in enumerate(test_orchestrations, 1):
        print(f"🧠 LEARNING SESSION {i}/3:")
        learning_summary = await learning_engine.learn_from_orchestration(orchestration)
        print()
    
    # Test predictive capabilities
    print("🔮 TESTING PREDICTIVE CAPABILITIES:")
    print("-" * 60)
    
    test_tasks = [
        "Create user authentication system with JWT",
        "Build enterprise blockchain infrastructure",
        "Optimize database query performance"
    ]
    
    for task in test_tasks:
        prediction = await learning_engine.predict_optimal_orchestration(task)
        print()
    
    # Display learning insights
    print("\n📊 LEARNING INSIGHTS:")
    print("=" * 60)
    insights = learning_engine.get_learning_insights()
    
    for category, data in insights.items():
        print(f"\n{category.replace('_', ' ').title()}:")
        for key, value in data.items():
            print(f"   {key.replace('_', ' ').title()}: {value}")
    
    # Save learning state
    learning_engine.save_learning_state()
    
    print("\n🧠 AUTONOMOUS LEARNING SYSTEM TEST COMPLETED!")
    print("   Self-improving AI coordination achieved! 🚀🧠✨")

if __name__ == "__main__":
    import time
    asyncio.run(test_autonomous_learning())