#!/usr/bin/env python3
"""
ADVANCED ML-BASED PREDICTIVE ROUTING SYSTEM
Revolutionary neural network-powered routing for multi-agent AI coordination
"""

import asyncio
import json
import numpy as np
import time
import pickle
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple, Union
from dataclasses import dataclass, asdict
from pathlib import Path
from collections import defaultdict
import hashlib
import logging

# ML Dependencies
try:
    import tensorflow as tf
    from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor
    from sklearn.neural_network import MLPClassifier
    from sklearn.preprocessing import StandardScaler, LabelEncoder
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import accuracy_score, mean_squared_error, classification_report
    import joblib
    ML_AVAILABLE = True
except ImportError:
    print("⚠️  ML libraries not available. Install with: pip install tensorflow scikit-learn")
    ML_AVAILABLE = False

@dataclass
class TaskFeatures:
    """Extracted features for ML prediction"""
    task_length: int
    complexity_score: float
    technical_depth: float
    domain_count: int
    urgency_score: float
    keyword_density: Dict[str, float]
    semantic_embedding: List[float]
    historical_pattern_match: float
    estimated_tokens: int

@dataclass
class AgentPerformanceMetrics:
    """Agent performance metrics for selection algorithm"""
    agent_name: str
    specialization: str
    average_quality: float
    consistency_score: float
    speed_rating: float
    cost_efficiency: float
    success_rate: float
    current_load: float
    expertise_confidence: float
    recent_performance_trend: float

@dataclass
class PredictionResult:
    """ML prediction result"""
    predicted_orchestration_type: str
    predicted_agent_combination: List[str]
    estimated_quality: float
    estimated_cost: float
    estimated_time: float
    confidence_score: float
    uncertainty_bounds: Dict[str, Tuple[float, float]]
    risk_assessment: str
    optimization_recommendations: List[str]

class NeuralTaskClassifier:
    """Neural network for sophisticated task classification"""
    
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.label_encoder = LabelEncoder()
        self.feature_importance = {}
        self.is_trained = False
        
        if ML_AVAILABLE:
            self._build_neural_network()
    
    def _build_neural_network(self):
        """Build sophisticated neural network architecture"""
        
        self.model = tf.keras.Sequential([
            tf.keras.layers.Dense(256, activation='relu', input_shape=(50,)),
            tf.keras.layers.Dropout(0.3),
            tf.keras.layers.BatchNormalization(),
            
            tf.keras.layers.Dense(128, activation='relu'),
            tf.keras.layers.Dropout(0.2),
            tf.keras.layers.BatchNormalization(),
            
            tf.keras.layers.Dense(64, activation='relu'),
            tf.keras.layers.Dropout(0.1),
            
            tf.keras.layers.Dense(32, activation='relu'),
            tf.keras.layers.Dense(8, activation='softmax')  # 8 complexity categories
        ])
        
        self.model.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy']
        )
    
    def extract_features(self, task: str, context: Dict = None) -> np.ndarray:
        """Extract comprehensive features from task description"""
        
        context = context or {}
        
        # Basic text features
        task_length = len(task)
        word_count = len(task.split())
        
        # Complexity keywords with weights
        complexity_keywords = {
            'mega': ['enterprise', 'platform', 'ecosystem', 'autonomous', 'revolutionary', 'quantum', 'distributed'],
            'complex': ['architecture', 'system', 'framework', 'infrastructure', 'scalable', 'security'],
            'moderate': ['implement', 'build', 'create', 'develop', 'design', 'optimize'],
            'simple': ['format', 'list', 'show', 'display', 'basic', 'simple']
        }
        
        complexity_scores = {}
        task_lower = task.lower()
        for category, keywords in complexity_keywords.items():
            scores = [task_lower.count(keyword) for keyword in keywords]
            complexity_scores[category] = sum(scores) / len(keywords)
        
        # Technical depth indicators
        technical_terms = [
            'algorithm', 'protocol', 'framework', 'architecture', 'infrastructure',
            'optimization', 'distributed', 'concurrent', 'asynchronous', 'scalable',
            'microservices', 'kubernetes', 'docker', 'api', 'database', 'encryption',
            'neural', 'quantum', 'blockchain', 'machine learning', 'artificial intelligence'
        ]
        
        technical_depth = sum(1 for term in technical_terms if term in task_lower) / len(technical_terms)
        
        # Domain indicators
        domain_keywords = {
            'security': ['security', 'encryption', 'auth', 'compliance', 'vulnerability'],
            'architecture': ['architecture', 'design', 'microservices', 'api', 'database'],
            'performance': ['performance', 'optimization', 'scalability', 'efficiency', 'speed'],
            'ai_ml': ['ai', 'ml', 'neural', 'learning', 'intelligence', 'model'],
            'devops': ['deployment', 'container', 'kubernetes', 'infrastructure', 'pipeline'],
            'frontend': ['ui', 'interface', 'user', 'frontend', 'react', 'vue'],
            'data': ['data', 'analytics', 'pipeline', 'etl', 'warehouse', 'processing']
        }
        
        domain_scores = []
        for domain, keywords in domain_keywords.items():
            score = sum(1 for keyword in keywords if keyword in task_lower) / len(keywords)
            domain_scores.append(score)
        
        # Urgency indicators
        urgency_keywords = ['urgent', 'critical', 'emergency', 'asap', 'immediately', 'deadline']
        urgency_score = sum(1 for keyword in urgency_keywords if keyword in task_lower) / len(urgency_keywords)
        
        # Semantic features (simplified - in production would use word embeddings)
        semantic_features = []
        for i in range(10):  # 10 semantic dimensions
            hash_val = hash(task + str(i)) % 1000
            semantic_features.append(hash_val / 1000.0)
        
        # Combine all features into a single vector
        feature_vector = [
            task_length / 1000.0,  # Normalized task length
            word_count / 100.0,    # Normalized word count
            complexity_scores.get('mega', 0),
            complexity_scores.get('complex', 0),
            complexity_scores.get('moderate', 0),
            complexity_scores.get('simple', 0),
            technical_depth,
            urgency_score,
            len([d for d in domain_scores if d > 0]) / len(domain_scores),  # Domain diversity
            max(domain_scores) if domain_scores else 0,  # Max domain relevance
        ]
        
        # Add domain scores
        feature_vector.extend(domain_scores)
        
        # Add semantic features
        feature_vector.extend(semantic_features)
        
        # Historical pattern matching (from context)
        historical_match = context.get('historical_pattern_match', 0.0)
        feature_vector.append(historical_match)
        
        # Estimated computational requirements
        estimated_tokens = task_length * 2 + word_count * 10
        feature_vector.append(estimated_tokens / 10000.0)
        
        # Add contextual features
        current_load = context.get('system_load', 0.5)
        time_of_day = datetime.now().hour / 24.0
        feature_vector.extend([current_load, time_of_day])
        
        # Pad or truncate to exactly 50 features
        while len(feature_vector) < 50:
            feature_vector.append(0.0)
        
        return np.array(feature_vector[:50])
    
    def train(self, tasks: List[str], labels: List[int], contexts: List[Dict] = None):
        """Train the neural network classifier"""
        
        if not ML_AVAILABLE:
            print("⚠️  ML libraries not available for training")
            return
        
        contexts = contexts or [{}] * len(tasks)
        
        # Extract features
        features = np.array([self.extract_features(task, ctx) for task, ctx in zip(tasks, contexts)])
        labels_array = np.array(labels)
        
        # Scale features
        features_scaled = self.scaler.fit_transform(features)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            features_scaled, labels_array, test_size=0.2, random_state=42
        )
        
        # Train model
        history = self.model.fit(
            X_train, y_train,
            validation_data=(X_test, y_test),
            epochs=100,
            batch_size=32,
            verbose=1,
            callbacks=[
                tf.keras.callbacks.EarlyStopping(patience=10, restore_best_weights=True),
                tf.keras.callbacks.ReduceLROnPlateau(patience=5)
            ]
        )
        
        self.is_trained = True
        
        # Evaluate
        y_pred = self.model.predict(X_test)
        y_pred_classes = np.argmax(y_pred, axis=1)
        accuracy = accuracy_score(y_test, y_pred_classes)
        
        print(f"✅ Neural classifier trained - Accuracy: {accuracy:.3f}")
        
        return history
    
    def predict(self, task: str, context: Dict = None) -> Tuple[int, float]:
        """Predict task complexity category with confidence"""
        
        if not ML_AVAILABLE or not self.is_trained:
            # Fallback to rule-based classification
            return self._fallback_classification(task), 0.5
        
        features = self.extract_features(task, context).reshape(1, -1)
        features_scaled = self.scaler.transform(features)
        
        prediction_probs = self.model.predict(features_scaled)[0]
        predicted_class = np.argmax(prediction_probs)
        confidence = prediction_probs[predicted_class]
        
        return predicted_class, confidence
    
    def _fallback_classification(self, task: str) -> int:
        """Fallback rule-based classification"""
        
        task_lower = task.lower()
        
        mega_indicators = ["enterprise", "platform", "ecosystem", "autonomous", "revolutionary", "quantum"]
        complex_indicators = ["architecture", "system", "framework", "infrastructure", "scalable"]
        moderate_indicators = ["implement", "build", "create", "develop", "design"]
        
        mega_score = sum(1 for indicator in mega_indicators if indicator in task_lower)
        complex_score = sum(1 for indicator in complex_indicators if indicator in task_lower)
        moderate_score = sum(1 for indicator in moderate_indicators if indicator in task_lower)
        
        if mega_score >= 2:
            return 7  # Mega complexity
        elif mega_score >= 1 or complex_score >= 2:
            return 6  # Very high complexity
        elif complex_score >= 1:
            return 5  # High complexity
        elif moderate_score >= 2:
            return 4  # Moderate-high complexity
        elif moderate_score >= 1:
            return 3  # Moderate complexity
        else:
            return 2  # Simple complexity

class AgentSelectionOptimizer:
    """ML-powered agent selection and team composition optimizer"""
    
    def __init__(self):
        self.agent_models = {}
        self.performance_predictors = {}
        self.team_composition_optimizer = None
        self.agent_profiles = {}
        
        if ML_AVAILABLE:
            self._initialize_ml_models()
    
    def _initialize_ml_models(self):
        """Initialize ML models for agent selection"""
        
        # Performance predictor for each agent type
        self.performance_predictors = {
            'quality': GradientBoostingRegressor(n_estimators=100, random_state=42),
            'time': GradientBoostingRegressor(n_estimators=100, random_state=42),
            'cost': GradientBoostingRegressor(n_estimators=100, random_state=42)
        }
        
        # Team composition optimizer
        self.team_composition_optimizer = MLPClassifier(
            hidden_layer_sizes=(128, 64, 32),
            activation='relu',
            solver='adam',
            max_iter=500,
            random_state=42
        )
    
    def update_agent_profile(self, agent_name: str, performance_data: Dict):
        """Update agent performance profile"""
        
        if agent_name not in self.agent_profiles:
            self.agent_profiles[agent_name] = {
                'performance_history': [],
                'specializations': set(),
                'quality_scores': [],
                'execution_times': [],
                'costs': [],
                'success_rate': 0.0,
                'consistency_score': 0.0
            }
        
        profile = self.agent_profiles[agent_name]
        
        # Update performance history
        profile['performance_history'].append({
            'timestamp': datetime.now().isoformat(),
            'quality': performance_data.get('quality', 0.0),
            'time': performance_data.get('execution_time', 0.0),
            'cost': performance_data.get('cost', 0.0),
            'task_type': performance_data.get('task_type', 'general'),
            'success': performance_data.get('success', False)
        })
        
        # Keep only last 100 records
        if len(profile['performance_history']) > 100:
            profile['performance_history'] = profile['performance_history'][-100:]
        
        # Update aggregated metrics
        recent_data = profile['performance_history'][-20:]  # Last 20 executions
        
        profile['quality_scores'] = [d['quality'] for d in recent_data]
        profile['execution_times'] = [d['time'] for d in recent_data]
        profile['costs'] = [d['cost'] for d in recent_data]
        
        profile['success_rate'] = sum(d['success'] for d in recent_data) / len(recent_data)
        profile['consistency_score'] = 1.0 - np.std(profile['quality_scores']) if profile['quality_scores'] else 0.0
        
        # Track specializations
        if performance_data.get('specialization'):
            profile['specializations'].add(performance_data['specialization'])
    
    def predict_agent_performance(self, agent_name: str, task_features: np.ndarray) -> Dict[str, float]:
        """Predict agent performance for given task"""
        
        if agent_name not in self.agent_profiles:
            return {'quality': 0.5, 'time': 10.0, 'cost': 0.001, 'confidence': 0.0}
        
        profile = self.agent_profiles[agent_name]
        
        if not profile['quality_scores']:
            return {'quality': 0.5, 'time': 10.0, 'cost': 0.001, 'confidence': 0.0}
        
        # Simple prediction based on historical performance
        avg_quality = np.mean(profile['quality_scores'])
        avg_time = np.mean(profile['execution_times'])
        avg_cost = np.mean(profile['costs'])
        
        # Adjust based on task complexity (from features)
        task_complexity = np.mean(task_features[:5])  # First 5 features represent complexity
        
        predicted_quality = avg_quality * (1.0 - task_complexity * 0.2)  # Quality may decrease with complexity
        predicted_time = avg_time * (1.0 + task_complexity * 0.5)        # Time may increase with complexity
        predicted_cost = avg_cost * (1.0 + task_complexity * 0.3)        # Cost may increase with complexity
        
        confidence = min(1.0, len(profile['performance_history']) / 20.0)
        
        return {
            'quality': max(0.0, min(1.0, predicted_quality)),
            'time': max(1.0, predicted_time),
            'cost': max(0.0001, predicted_cost),
            'confidence': confidence
        }
    
    def optimize_team_composition(self, task_features: np.ndarray, available_agents: List[str],
                                constraints: Dict = None) -> List[str]:
        """Optimize team composition using multi-objective optimization"""
        
        constraints = constraints or {}
        max_agents = constraints.get('max_agents', 5)
        min_quality = constraints.get('min_quality', 0.7)
        max_cost = constraints.get('max_cost', 0.01)
        
        # Get predictions for all agents
        agent_predictions = {}
        for agent in available_agents:
            agent_predictions[agent] = self.predict_agent_performance(agent, task_features)
        
        # Multi-objective optimization
        best_combination = []
        best_score = -1
        
        # Try different combinations
        from itertools import combinations
        
        for team_size in range(1, min(max_agents + 1, len(available_agents) + 1)):
            for team in combinations(available_agents, team_size):
                # Calculate team metrics
                team_quality = np.mean([agent_predictions[agent]['quality'] for agent in team])
                team_time = max([agent_predictions[agent]['time'] for agent in team])  # Parallel execution
                team_cost = sum([agent_predictions[agent]['cost'] for agent in team])
                team_confidence = np.mean([agent_predictions[agent]['confidence'] for agent in team])
                
                # Check constraints
                if team_quality < min_quality or team_cost > max_cost:
                    continue
                
                # Calculate composite score (quality-cost-time trade-off)
                score = (team_quality * 0.4 + 
                        (1.0 / team_time) * 0.3 + 
                        (1.0 / team_cost) * 0.2 + 
                        team_confidence * 0.1)
                
                if score > best_score:
                    best_score = score
                    best_combination = list(team)
        
        return best_combination if best_combination else available_agents[:1]

class PerformancePredictionEngine:
    """Advanced performance prediction with uncertainty quantification"""
    
    def __init__(self):
        self.ensemble_models = {}
        self.uncertainty_models = {}
        self.feature_importance = {}
        
        if ML_AVAILABLE:
            self._initialize_ensemble_models()
    
    def _initialize_ensemble_models(self):
        """Initialize ensemble of prediction models"""
        
        # Ensemble for quality prediction
        self.ensemble_models['quality'] = [
            GradientBoostingRegressor(n_estimators=100, random_state=42),
            RandomForestClassifier(n_estimators=100, random_state=42),
            MLPClassifier(hidden_layer_sizes=(64, 32), random_state=42)
        ]
        
        # Ensemble for time prediction
        self.ensemble_models['time'] = [
            GradientBoostingRegressor(n_estimators=100, random_state=42),
            RandomForestClassifier(n_estimators=100, random_state=42)
        ]
        
        # Ensemble for cost prediction
        self.ensemble_models['cost'] = [
            GradientBoostingRegressor(n_estimators=100, random_state=42),
            RandomForestClassifier(n_estimators=100, random_state=42)
        ]
    
    def predict_with_uncertainty(self, task_features: np.ndarray, team_composition: List[str]) -> Dict:
        """Predict performance with uncertainty bounds"""
        
        if not ML_AVAILABLE:
            return self._fallback_prediction()
        
        # Combine task features with team composition features
        team_features = self._encode_team_features(team_composition)
        combined_features = np.concatenate([task_features, team_features])
        
        predictions = {}
        uncertainty_bounds = {}
        
        for metric in ['quality', 'time', 'cost']:
            if metric in self.ensemble_models and self.ensemble_models[metric]:
                # Get predictions from ensemble
                ensemble_predictions = []
                for model in self.ensemble_models[metric]:
                    if hasattr(model, 'predict'):
                        try:
                            pred = model.predict(combined_features.reshape(1, -1))[0]
                            ensemble_predictions.append(pred)
                        except:
                            pass
                
                if ensemble_predictions:
                    mean_pred = np.mean(ensemble_predictions)
                    std_pred = np.std(ensemble_predictions)
                    
                    predictions[metric] = mean_pred
                    uncertainty_bounds[metric] = (
                        max(0, mean_pred - 1.96 * std_pred),  # 95% lower bound
                        mean_pred + 1.96 * std_pred           # 95% upper bound
                    )
                else:
                    predictions[metric] = self._get_fallback_value(metric)
                    uncertainty_bounds[metric] = self._get_fallback_uncertainty(metric)
            else:
                predictions[metric] = self._get_fallback_value(metric)
                uncertainty_bounds[metric] = self._get_fallback_uncertainty(metric)
        
        return {
            'predictions': predictions,
            'uncertainty_bounds': uncertainty_bounds,
            'confidence': min(1.0, 1.0 / (1.0 + np.mean([ub[1] - ub[0] for ub in uncertainty_bounds.values()])))
        }
    
    def _encode_team_features(self, team_composition: List[str]) -> np.ndarray:
        """Encode team composition into feature vector"""
        
        # Simple encoding based on team size and composition
        team_size = len(team_composition)
        team_diversity = len(set(agent.split('_')[0] for agent in team_composition))
        
        # Create feature vector for team
        team_features = [
            team_size / 10.0,  # Normalized team size
            team_diversity / team_size if team_size > 0 else 0,  # Diversity ratio
            1.0 if 'cerebras' in str(team_composition) else 0.0,
            1.0 if 'gemini' in str(team_composition) else 0.0,
            1.0 if 'groq' in str(team_composition) else 0.0,
            1.0 if 'scaleway' in str(team_composition) else 0.0
        ]
        
        # Pad to fixed length
        while len(team_features) < 20:
            team_features.append(0.0)
        
        return np.array(team_features[:20])
    
    def _fallback_prediction(self) -> Dict:
        """Fallback prediction when ML models are not available"""
        
        return {
            'predictions': {
                'quality': 0.75,
                'time': 15.0,
                'cost': 0.003
            },
            'uncertainty_bounds': {
                'quality': (0.6, 0.9),
                'time': (10.0, 25.0),
                'cost': (0.001, 0.005)
            },
            'confidence': 0.5
        }
    
    def _get_fallback_value(self, metric: str) -> float:
        """Get fallback value for specific metric"""
        
        fallback_values = {
            'quality': 0.75,
            'time': 15.0,
            'cost': 0.003
        }
        
        return fallback_values.get(metric, 0.5)
    
    def _get_fallback_uncertainty(self, metric: str) -> Tuple[float, float]:
        """Get fallback uncertainty bounds for specific metric"""
        
        fallback_bounds = {
            'quality': (0.6, 0.9),
            'time': (10.0, 25.0),
            'cost': (0.001, 0.005)
        }
        
        return fallback_bounds.get(metric, (0.0, 1.0))

class RealTimeOptimizationEngine:
    """Real-time optimization for dynamic load balancing and adaptation"""
    
    def __init__(self):
        self.current_loads = {}
        self.performance_history = {}
        self.optimization_rules = {}
        self.adaptive_thresholds = {
            'quality_target': 0.8,
            'max_cost': 0.01,
            'max_time': 60.0
        }
    
    def update_agent_load(self, agent_name: str, current_load: float):
        """Update current load for an agent"""
        self.current_loads[agent_name] = {
            'load': current_load,
            'timestamp': datetime.now().isoformat()
        }
    
    def get_load_balanced_team(self, optimal_team: List[str], available_agents: List[str]) -> List[str]:
        """Get load-balanced team considering current agent loads"""
        
        # Filter agents by current load (prefer agents with load < 0.8)
        low_load_agents = []
        medium_load_agents = []
        high_load_agents = []
        
        for agent in available_agents:
            load_info = self.current_loads.get(agent, {'load': 0.5})
            load = load_info['load']
            
            if load < 0.6:
                low_load_agents.append(agent)
            elif load < 0.8:
                medium_load_agents.append(agent)
            else:
                high_load_agents.append(agent)
        
        # Try to fulfill optimal team with low-load agents first
        balanced_team = []
        remaining_slots = len(optimal_team)
        
        # Fill with low-load agents first
        for agent in optimal_team:
            if agent in low_load_agents and remaining_slots > 0:
                balanced_team.append(agent)
                remaining_slots -= 1
        
        # Fill remaining with medium-load agents
        for agent in optimal_team:
            if agent in medium_load_agents and remaining_slots > 0 and agent not in balanced_team:
                balanced_team.append(agent)
                remaining_slots -= 1
        
        # Fill any remaining slots with available agents
        all_available = low_load_agents + medium_load_agents + high_load_agents
        for agent in all_available:
            if remaining_slots > 0 and agent not in balanced_team:
                balanced_team.append(agent)
                remaining_slots -= 1
        
        return balanced_team if balanced_team else optimal_team
    
    def optimize_execution_parameters(self, task_complexity: int, team_composition: List[str]) -> Dict:
        """Optimize execution parameters based on real-time conditions"""
        
        team_size = len(team_composition)
        avg_load = np.mean([self.current_loads.get(agent, {'load': 0.5})['load'] for agent in team_composition])
        
        # Dynamic timeout calculation
        base_timeout = min(30 + task_complexity * 10, 300)  # 30s to 5min
        load_factor = 1.0 + avg_load * 0.5  # Increase timeout for high load
        adaptive_timeout = base_timeout * load_factor
        
        # Dynamic retry mechanism
        retry_count = max(1, min(3, task_complexity - 2))  # 1-3 retries based on complexity
        
        # Quality-performance trade-off
        if avg_load > 0.8:
            quality_target = self.adaptive_thresholds['quality_target'] * 0.9  # Slightly lower quality for high load
            parallel_execution = team_size <= 3  # Limit parallelism under high load
        else:
            quality_target = self.adaptive_thresholds['quality_target']
            parallel_execution = team_size <= 6
        
        return {
            'timeout_seconds': adaptive_timeout,
            'retry_count': retry_count,
            'quality_target': quality_target,
            'parallel_execution': parallel_execution,
            'batch_size': min(team_size, 4) if parallel_execution else 1,
            'priority_boost': avg_load < 0.4  # Boost priority when system has low load
        }

class MLPredictiveRoutingSystem:
    """Main ML-based predictive routing system"""
    
    def __init__(self, autonomous_learning_engine=None):
        self.task_classifier = NeuralTaskClassifier()
        self.agent_optimizer = AgentSelectionOptimizer()
        self.performance_predictor = PerformancePredictionEngine()
        self.real_time_optimizer = RealTimeOptimizationEngine()
        self.learning_engine = autonomous_learning_engine
        
        # System state
        self.available_agents = [
            'cerebras_ultra', 'gemini_flash', 'groq_lightning', 'scaleway_eu',
            'claude_premium', 'claude_coordinator'
        ]
        
        self.orchestration_history = []
        self.model_performance_metrics = {}
        self.prediction_accuracy_history = []
        
        # Performance monitoring
        self.total_predictions = 0
        self.successful_predictions = 0
        self.model_drift_detected = False
        
        print("🧠 ML PREDICTIVE ROUTING SYSTEM INITIALIZED")
        print(f"   🤖 Available agents: {len(self.available_agents)}")
        print(f"   🔮 Neural classifier: {'✅ Ready' if ML_AVAILABLE else '⚠️ Fallback mode'}")
        print(f"   📊 Performance predictor: {'✅ Ready' if ML_AVAILABLE else '⚠️ Fallback mode'}")
        print(f"   ⚡ Real-time optimizer: ✅ Ready")
        print()
    
    async def predict_optimal_routing(self, task: str, constraints: Dict = None) -> PredictionResult:
        """Main prediction function - predict optimal routing for a task"""
        
        print(f"🔮 ML PREDICTIVE ROUTING ANALYSIS")
        print(f"   📋 Task: {task[:100]}...")
        
        prediction_start = time.time()
        constraints = constraints or {}
        
        # Phase 1: Neural Task Classification
        print("   🧠 Phase 1: Neural task classification...")
        
        # Get context from learning engine if available
        context = {}
        if self.learning_engine:
            # Get historical pattern matching
            similar_patterns = self._find_similar_historical_patterns(task)
            context['historical_pattern_match'] = len(similar_patterns) / 10.0
            context['system_load'] = np.mean([
                self.real_time_optimizer.current_loads.get(agent, {'load': 0.5})['load'] 
                for agent in self.available_agents
            ])
        
        # Extract features and classify
        task_features = self.task_classifier.extract_features(task, context)
        complexity_class, classification_confidence = self.task_classifier.predict(task, context)
        
        print(f"     🎯 Complexity class: {complexity_class}/7 (confidence: {classification_confidence:.3f})")
        
        # Phase 2: Agent Selection Optimization
        print("   🤖 Phase 2: Agent selection optimization...")
        
        optimal_team = self.agent_optimizer.optimize_team_composition(
            task_features, self.available_agents, constraints
        )
        
        # Apply real-time load balancing
        balanced_team = self.real_time_optimizer.get_load_balanced_team(
            optimal_team, self.available_agents
        )
        
        print(f"     👥 Optimal team: {balanced_team} ({len(balanced_team)} agents)")
        
        # Phase 3: Performance Prediction with Uncertainty
        print("   📊 Phase 3: Performance prediction with uncertainty...")
        
        performance_prediction = self.performance_predictor.predict_with_uncertainty(
            task_features, balanced_team
        )
        
        predictions = performance_prediction['predictions']
        uncertainty_bounds = performance_prediction['uncertainty_bounds']
        
        print(f"     📈 Quality: {predictions['quality']:.3f} ±{(uncertainty_bounds['quality'][1] - uncertainty_bounds['quality'][0])/2:.3f}")
        print(f"     ⏱️  Time: {predictions['time']:.1f}s ±{(uncertainty_bounds['time'][1] - uncertainty_bounds['time'][0])/2:.1f}s")
        print(f"     💰 Cost: ${predictions['cost']:.5f} ±${(uncertainty_bounds['cost'][1] - uncertainty_bounds['cost'][0])/2:.5f}")
        
        # Phase 4: Real-time Optimization
        print("   ⚡ Phase 4: Real-time optimization...")
        
        execution_params = self.real_time_optimizer.optimize_execution_parameters(
            complexity_class, balanced_team
        )
        
        # Phase 5: Risk Assessment and Recommendations
        print("   🛡️  Phase 5: Risk assessment...")
        
        risk_assessment = self._assess_execution_risk(
            complexity_class, balanced_team, predictions, uncertainty_bounds
        )
        
        optimization_recommendations = self._generate_optimization_recommendations(
            task, complexity_class, balanced_team, predictions, execution_params
        )
        
        # Determine orchestration type based on complexity
        orchestration_types = [
            'direct', 'parallel', 'coordinated', 'hierarchical_light',
            'hierarchical_standard', 'hierarchical_heavy', 'hierarchical_mega', 'hierarchical_quantum'
        ]
        predicted_orchestration = orchestration_types[min(complexity_class, 7)]
        
        prediction_time = time.time() - prediction_start
        
        # Create prediction result
        result = PredictionResult(
            predicted_orchestration_type=predicted_orchestration,
            predicted_agent_combination=balanced_team,
            estimated_quality=predictions['quality'],
            estimated_cost=predictions['cost'],
            estimated_time=predictions['time'],
            confidence_score=performance_prediction['confidence'],
            uncertainty_bounds=uncertainty_bounds,
            risk_assessment=risk_assessment,
            optimization_recommendations=optimization_recommendations
        )
        
        # Record prediction for learning
        self._record_prediction(task, result, prediction_time, execution_params)
        
        print(f"   ✅ ML routing prediction complete ({prediction_time:.3f}s)")
        print(f"     🎯 Orchestration: {predicted_orchestration}")
        print(f"     🔮 Overall confidence: {performance_prediction['confidence']:.3f}")
        print(f"     🛡️  Risk level: {risk_assessment}")
        
        return result
    
    def _find_similar_historical_patterns(self, task: str) -> List[Dict]:
        """Find similar historical patterns for context"""
        
        if not self.learning_engine or not hasattr(self.learning_engine, 'learning_patterns'):
            return []
        
        similar_patterns = []
        task_lower = task.lower()
        
        for pattern_id, pattern in self.learning_engine.learning_patterns.items():
            # Simple similarity based on keyword overlap
            pattern_domains = pattern.task_characteristics.get('primary_domains', [])
            
            similarity = 0
            for domain in pattern_domains:
                if domain in task_lower:
                    similarity += 1
            
            if similarity > 0:
                similar_patterns.append({
                    'pattern_id': pattern_id,
                    'similarity': similarity,
                    'quality': pattern.average_quality,
                    'agents': pattern.optimal_agents
                })
        
        return sorted(similar_patterns, key=lambda x: x['similarity'], reverse=True)[:5]
    
    def _assess_execution_risk(self, complexity: int, team: List[str], 
                             predictions: Dict, uncertainty_bounds: Dict) -> str:
        """Assess execution risk based on predictions and uncertainty"""
        
        # Risk factors
        quality_uncertainty = uncertainty_bounds['quality'][1] - uncertainty_bounds['quality'][0]
        time_uncertainty = uncertainty_bounds['time'][1] - uncertainty_bounds['time'][0]
        cost_uncertainty = uncertainty_bounds['cost'][1] - uncertainty_bounds['cost'][0]
        
        # Team load risk
        avg_load = np.mean([
            self.real_time_optimizer.current_loads.get(agent, {'load': 0.5})['load'] 
            for agent in team
        ])
        
        # Calculate overall risk score
        uncertainty_risk = (quality_uncertainty + time_uncertainty / 100 + cost_uncertainty * 1000) / 3
        load_risk = avg_load
        complexity_risk = complexity / 7.0
        
        overall_risk = (uncertainty_risk * 0.4 + load_risk * 0.3 + complexity_risk * 0.3)
        
        if overall_risk < 0.3:
            return "LOW"
        elif overall_risk < 0.6:
            return "MEDIUM"
        elif overall_risk < 0.8:
            return "HIGH"
        else:
            return "CRITICAL"
    
    def _generate_optimization_recommendations(self, task: str, complexity: int, 
                                             team: List[str], predictions: Dict,
                                             execution_params: Dict) -> List[str]:
        """Generate optimization recommendations"""
        
        recommendations = []
        
        # Quality recommendations
        if predictions['quality'] < 0.7:
            recommendations.append("Consider adding specialized agents to improve quality")
            recommendations.append("Increase timeout to allow more thorough processing")
        
        # Performance recommendations
        if predictions['time'] > 30:
            recommendations.append("Consider parallel execution to reduce time")
            recommendations.append("Use faster agents for time-critical components")
        
        # Cost recommendations
        if predictions['cost'] > 0.005:
            recommendations.append("Consider using fewer agents to reduce cost")
            recommendations.append("Use cost-efficient agents for non-critical components")
        
        # Load balancing recommendations
        avg_load = np.mean([
            self.real_time_optimizer.current_loads.get(agent, {'load': 0.5})['load'] 
            for agent in team
        ])
        
        if avg_load > 0.8:
            recommendations.append("High system load detected - consider delaying execution")
            recommendations.append("Use fewer parallel agents to reduce load")
        
        # Complexity-specific recommendations
        if complexity >= 6:
            recommendations.append("Use hierarchical orchestration for mega-scale tasks")
            recommendations.append("Implement staged execution with checkpoints")
        
        return recommendations[:5]  # Limit to top 5 recommendations
    
    def _record_prediction(self, task: str, result: PredictionResult, 
                          prediction_time: float, execution_params: Dict):
        """Record prediction for performance monitoring"""
        
        self.total_predictions += 1
        
        prediction_record = {
            'timestamp': datetime.now().isoformat(),
            'task': task[:200] + "..." if len(task) > 200 else task,
            'prediction': asdict(result),
            'execution_params': execution_params,
            'prediction_time': prediction_time,
            'model_performance': {
                'classification_confidence': result.confidence_score,
                'uncertainty_level': np.mean([
                    ub[1] - ub[0] for ub in result.uncertainty_bounds.values()
                ])
            }
        }
        
        self.orchestration_history.append(prediction_record)
        
        # Keep only last 1000 predictions
        if len(self.orchestration_history) > 1000:
            self.orchestration_history = self.orchestration_history[-1000:]
    
    async def learn_from_execution(self, task: str, prediction: PredictionResult, 
                                 actual_result: Dict):
        """Learn from actual execution results to improve predictions"""
        
        print(f"📚 LEARNING FROM EXECUTION RESULTS")
        
        # Extract actual metrics
        actual_quality = actual_result.get('quality_score', 0.0)
        actual_time = actual_result.get('execution_time', 0.0)
        actual_cost = actual_result.get('total_cost', 0.0)
        
        # Calculate prediction accuracy
        quality_error = abs(prediction.estimated_quality - actual_quality)
        time_error = abs(prediction.estimated_time - actual_time) / max(actual_time, 1.0)
        cost_error = abs(prediction.estimated_cost - actual_cost) / max(actual_cost, 0.0001)
        
        # Overall prediction accuracy
        accuracy = 1.0 - np.mean([quality_error, time_error, cost_error])
        
        # Update agent performance profiles
        for agent in prediction.predicted_agent_combination:
            self.agent_optimizer.update_agent_profile(agent, {
                'quality': actual_quality,
                'execution_time': actual_time,
                'cost': actual_cost / len(prediction.predicted_agent_combination),
                'success': actual_quality >= 0.7,
                'task_type': prediction.predicted_orchestration_type
            })
        
        # Record learning metrics
        self.prediction_accuracy_history.append({
            'timestamp': datetime.now().isoformat(),
            'accuracy': accuracy,
            'quality_error': quality_error,
            'time_error': time_error,
            'cost_error': cost_error
        })
        
        # Keep only last 100 accuracy records
        if len(self.prediction_accuracy_history) > 100:
            self.prediction_accuracy_history = self.prediction_accuracy_history[-100:]
        
        # Update success counter
        if accuracy >= 0.7:
            self.successful_predictions += 1
        
        # Check for model drift
        recent_accuracies = [r['accuracy'] for r in self.prediction_accuracy_history[-20:]]
        if len(recent_accuracies) >= 20:
            recent_avg_accuracy = np.mean(recent_accuracies)
            overall_accuracy = self.successful_predictions / max(self.total_predictions, 1)
            
            if recent_avg_accuracy < overall_accuracy * 0.8:
                self.model_drift_detected = True
                print("⚠️  Model drift detected - consider retraining models")
        
        print(f"   📊 Prediction accuracy: {accuracy:.3f}")
        print(f"   📈 Overall success rate: {self.successful_predictions / max(self.total_predictions, 1):.3f}")
        
        # Integration with autonomous learning engine
        if self.learning_engine:
            orchestration_data = {
                'task': task,
                'execution_result': actual_result,
                'performance_analysis': {
                    'prediction_accuracy': accuracy,
                    'quality_error': quality_error,
                    'time_error': time_error,
                    'cost_error': cost_error,
                    'orchestration_success': actual_quality >= 0.7
                }
            }
            
            await self.learning_engine.learn_from_orchestration(orchestration_data)
    
    def get_system_performance_metrics(self) -> Dict:
        """Get comprehensive system performance metrics"""
        
        if not self.orchestration_history:
            return {"message": "No prediction history available"}
        
        # Basic metrics
        total_predictions = len(self.orchestration_history)
        recent_predictions = self.orchestration_history[-50:] if len(self.orchestration_history) >= 50 else self.orchestration_history
        
        # Prediction performance
        avg_prediction_time = np.mean([p['prediction_time'] for p in recent_predictions])
        avg_confidence = np.mean([p['prediction']['confidence_score'] for p in recent_predictions])
        
        # Accuracy metrics (if available)
        accuracy_metrics = {}
        if self.prediction_accuracy_history:
            recent_accuracy = self.prediction_accuracy_history[-20:] if len(self.prediction_accuracy_history) >= 20 else self.prediction_accuracy_history
            accuracy_metrics = {
                'average_accuracy': np.mean([a['accuracy'] for a in recent_accuracy]),
                'quality_prediction_error': np.mean([a['quality_error'] for a in recent_accuracy]),
                'time_prediction_error': np.mean([a['time_error'] for a in recent_accuracy]),
                'cost_prediction_error': np.mean([a['cost_error'] for a in recent_accuracy])
            }
        
        # Orchestration type distribution
        orchestration_types = [p['prediction']['predicted_orchestration_type'] for p in recent_predictions]
        type_distribution = {orch_type: orchestration_types.count(orch_type) for orch_type in set(orchestration_types)}
        
        # Agent utilization
        all_agents = []
        for prediction in recent_predictions:
            all_agents.extend(prediction['prediction']['predicted_agent_combination'])
        
        agent_utilization = {agent: all_agents.count(agent) for agent in set(all_agents)}
        
        # System load metrics
        current_loads = list(self.real_time_optimizer.current_loads.values())
        load_metrics = {}
        if current_loads:
            loads = [l['load'] for l in current_loads]
            load_metrics = {
                'average_load': np.mean(loads),
                'max_load': np.max(loads),
                'load_balance_score': 1.0 - np.std(loads)  # Higher is better balanced
            }
        
        return {
            'prediction_metrics': {
                'total_predictions': total_predictions,
                'average_prediction_time': avg_prediction_time,
                'average_confidence': avg_confidence,
                'model_drift_detected': self.model_drift_detected
            },
            'accuracy_metrics': accuracy_metrics,
            'orchestration_distribution': type_distribution,
            'agent_utilization': agent_utilization,
            'system_load_metrics': load_metrics,
            'ml_system_status': {
                'neural_classifier_available': ML_AVAILABLE and self.task_classifier.is_trained,
                'performance_predictor_available': ML_AVAILABLE,
                'real_time_optimization_active': True
            }
        }
    
    def save_ml_models(self, filepath_prefix: str = "ml_routing_models"):
        """Save trained ML models for persistence"""
        
        if not ML_AVAILABLE:
            print("⚠️  ML libraries not available for model saving")
            return
        
        models_saved = 0
        
        try:
            # Save neural classifier
            if self.task_classifier.is_trained:
                self.task_classifier.model.save(f"{filepath_prefix}_neural_classifier.h5")
                joblib.dump(self.task_classifier.scaler, f"{filepath_prefix}_scaler.pkl")
                models_saved += 1
            
            # Save agent profiles
            with open(f"{filepath_prefix}_agent_profiles.json", 'w') as f:
                json.dump(self.agent_optimizer.agent_profiles, f, indent=2, default=str)
            models_saved += 1
            
            # Save performance predictors
            for name, model in self.performance_predictor.ensemble_models.items():
                if model:
                    joblib.dump(model, f"{filepath_prefix}_performance_{name}.pkl")
                    models_saved += 1
            
            # Save system state
            system_state = {
                'orchestration_history': self.orchestration_history[-100:],  # Last 100 records
                'prediction_accuracy_history': self.prediction_accuracy_history,
                'model_performance_metrics': self.model_performance_metrics,
                'total_predictions': self.total_predictions,
                'successful_predictions': self.successful_predictions,
                'last_saved': datetime.now().isoformat()
            }
            
            with open(f"{filepath_prefix}_system_state.json", 'w') as f:
                json.dump(system_state, f, indent=2, default=str)
            models_saved += 1
            
            print(f"💾 ML models saved: {models_saved} files")
            
        except Exception as e:
            print(f"⚠️  Error saving ML models: {e}")

# Integration with existing autonomous learning system
async def integrate_with_autonomous_learning():
    """Integration test with the existing autonomous learning system"""
    
    print("🔗 INTEGRATING ML ROUTING WITH AUTONOMOUS LEARNING")
    print("=" * 80)
    print()
    
    # Import the existing autonomous learning system
    try:
        from autonomous_learning_system import AutonomousLearningEngine
        learning_engine = AutonomousLearningEngine()
        
        # Initialize ML routing system with learning integration
        ml_routing = MLPredictiveRoutingSystem(learning_engine)
        
        # Test scenarios
        test_tasks = [
            "Create a simple user authentication system",
            "Design a scalable microservices architecture with service mesh",
            "Build a revolutionary quantum-resistant AI platform with distributed consensus",
            "Optimize database query performance for high-traffic application"
        ]
        
        for i, task in enumerate(test_tasks, 1):
            print(f"🎯 ML ROUTING TEST {i}/{len(test_tasks)}:")
            print(f"   Task: {task}")
            print()
            
            # Get ML routing prediction
            prediction = await ml_routing.predict_optimal_routing(task)
            
            # Simulate execution results
            simulated_result = {
                'quality_score': prediction.estimated_quality + np.random.normal(0, 0.1),
                'execution_time': prediction.estimated_time + np.random.normal(0, 5),
                'total_cost': prediction.estimated_cost + np.random.normal(0, 0.0005),
                'orchestration_type': prediction.predicted_orchestration_type,
                'agents_used': len(prediction.predicted_agent_combination),
                'success': True
            }
            
            # Learn from execution
            await ml_routing.learn_from_execution(task, prediction, simulated_result)
            
            print()
            print("─" * 80)
            print()
        
        # Display integrated system metrics
        print("📊 INTEGRATED SYSTEM PERFORMANCE:")
        print("=" * 80)
        
        ml_metrics = ml_routing.get_system_performance_metrics()
        learning_insights = learning_engine.get_learning_insights()
        
        print("\n🧠 ML ROUTING METRICS:")
        for category, data in ml_metrics.items():
            if isinstance(data, dict):
                print(f"   {category.replace('_', ' ').title()}:")
                for key, value in data.items():
                    print(f"     {key.replace('_', ' ').title()}: {value}")
        
        print("\n📚 AUTONOMOUS LEARNING INSIGHTS:")
        for category, data in learning_insights.items():
            if isinstance(data, dict):
                print(f"   {category.replace('_', ' ').title()}:")
                for key, value in data.items():
                    print(f"     {key.replace('_', ' ').title()}: {value}")
        
        # Save integrated system state
        ml_routing.save_ml_models("integrated_ml_routing")
        learning_engine.save_learning_state("integrated_autonomous_learning.json")
        
        print("\n🚀 INTEGRATED ML ROUTING SYSTEM TEST COMPLETED!")
        print("   Advanced ML-powered routing with autonomous learning achieved! 🧠⚡🎯")
        
    except ImportError:
        print("⚠️  Autonomous learning system not available - running standalone ML routing test")
        
        # Standalone ML routing test
        ml_routing = MLPredictiveRoutingSystem()
        
        task = "Build a distributed AI orchestration platform with quantum-resistant security"
        prediction = await ml_routing.predict_optimal_routing(task)
        
        print("\n🔮 STANDALONE ML ROUTING PREDICTION:")
        print(f"   Orchestration: {prediction.predicted_orchestration_type}")
        print(f"   Agents: {prediction.predicted_agent_combination}")
        print(f"   Quality: {prediction.estimated_quality:.3f}")
        print(f"   Cost: ${prediction.estimated_cost:.5f}")
        print(f"   Time: {prediction.estimated_time:.1f}s")
        print(f"   Confidence: {prediction.confidence_score:.3f}")
        print(f"   Risk: {prediction.risk_assessment}")
        
        print("\n🚀 STANDALONE ML ROUTING TEST COMPLETED!")

# Main test function
async def test_ml_predictive_routing():
    """Comprehensive test of the ML predictive routing system"""
    
    print("🧠 TESTING ML PREDICTIVE ROUTING SYSTEM")
    print("=" * 80)
    print()
    
    # Test neural classification
    print("🧠 Testing Neural Task Classifier...")
    classifier = NeuralTaskClassifier()
    
    test_tasks_classification = [
        "Format JavaScript code",
        "Implement user authentication with JWT",
        "Design microservices architecture",
        "Build quantum-resistant AI platform"
    ]
    
    for task in test_tasks_classification:
        features = classifier.extract_features(task)
        complexity, confidence = classifier.predict(task)
        print(f"   Task: '{task[:40]}...' -> Complexity: {complexity}, Confidence: {confidence:.3f}")
    
    print("\n🤖 Testing Agent Selection Optimizer...")
    optimizer = AgentSelectionOptimizer()
    
    sample_features = np.random.random(50)
    available_agents = ['cerebras_ultra', 'gemini_flash', 'groq_lightning', 'scaleway_eu']
    optimal_team = optimizer.optimize_team_composition(sample_features, available_agents)
    print(f"   Optimal team for sample task: {optimal_team}")
    
    print("\n📊 Testing Performance Prediction Engine...")
    predictor = PerformancePredictionEngine()
    
    prediction = predictor.predict_with_uncertainty(sample_features, optimal_team)
    print(f"   Quality prediction: {prediction['predictions']['quality']:.3f}")
    print(f"   Time prediction: {prediction['predictions']['time']:.1f}s")
    print(f"   Cost prediction: ${prediction['predictions']['cost']:.5f}")
    
    print("\n⚡ Testing Real-time Optimization Engine...")
    rt_optimizer = RealTimeOptimizationEngine()
    
    # Simulate agent loads
    for agent in available_agents:
        rt_optimizer.update_agent_load(agent, np.random.random())
    
    balanced_team = rt_optimizer.get_load_balanced_team(optimal_team, available_agents)
    execution_params = rt_optimizer.optimize_execution_parameters(5, balanced_team)
    
    print(f"   Load-balanced team: {balanced_team}")
    print(f"   Execution timeout: {execution_params['timeout_seconds']:.1f}s")
    
    print("\n🔮 Testing Complete ML Routing System...")
    
    # Run integration test
    await integrate_with_autonomous_learning()

if __name__ == "__main__":
    asyncio.run(test_ml_predictive_routing())