import asyncio
import json
import time
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Set
import numpy as np
import pandas as pd
import networkx as nx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from prometheus_client import Counter, Gauge, Histogram, generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response
import uvicorn
import redis
from scipy import stats
from scipy.spatial.distance import pdist, squareform
from sklearn.cluster import KMeans, DBSCAN
from sklearn.manifold import TSNE
from sklearn.preprocessing import StandardScaler
from collections import defaultdict, deque
import warnings
warnings.filterwarnings('ignore')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI
app = FastAPI(title="AI Emergence Detection Service", version="1.0.0")

# Redis connection
redis_client = redis.Redis(host='redis', port=6379, decode_responses=True)

# Prometheus metrics
emergence_events = Counter('emergence_events_total', 'Total emergence events detected', ['emergence_type', 'magnitude'])
emergence_score = Gauge('emergence_score', 'Emergence score for agent clusters', ['cluster_id', 'emergence_type'])
collective_intelligence = Gauge('collective_intelligence_score', 'Collective intelligence score', ['agent_group'])
swarm_coherence = Gauge('swarm_coherence_score', 'Swarm coherence measurement', ['swarm_id'])
phase_transition_indicator = Gauge('phase_transition_indicator', 'Phase transition detection', ['system_level'])
information_flow = Gauge('information_flow_rate', 'Information flow between agents', ['source_group', 'target_group'])
complexity_measure = Gauge('system_complexity_measure', 'System complexity measurement', ['measurement_type'])

# Data models
class EmergenceEvent(BaseModel):
    event_id: str
    emergence_type: str  # swarm_intelligence, collective_behavior, phase_transition, etc.
    magnitude: float
    confidence: float
    timestamp: datetime
    involved_agents: List[str]
    description: str
    characteristics: Dict[str, any]
    predicted_evolution: Dict[str, any]

class AgentInteraction(BaseModel):
    source_agent: str
    target_agent: str
    interaction_type: str
    strength: float
    timestamp: datetime
    metadata: Dict[str, any]

class SystemState(BaseModel):
    timestamp: datetime
    total_agents: int
    active_agents: int
    network_density: float
    average_connectivity: float
    cluster_count: int
    entropy: float
    complexity_score: float

class EmergenceDetector:
    def __init__(self):
        self.interaction_history = defaultdict(deque)
        self.agent_states = {}
        self.network_graph = nx.Graph()
        self.emergence_thresholds = {
            'swarm_intelligence': 0.7,
            'collective_behavior': 0.6,
            'phase_transition': 0.8,
            'self_organization': 0.65,
            'collective_learning': 0.75
        }
        self.history_window = 1000  # Keep last 1000 interactions
        
    async def analyze_system_emergence(self, agents_data: List[Dict[str, any]], interactions: List[AgentInteraction]) -> List[EmergenceEvent]:
        """Main emergence detection function"""
        events = []
        
        # Update system state
        await self._update_system_state(agents_data, interactions)
        
        # Detect different types of emergence
        swarm_events = await self._detect_swarm_intelligence(agents_data)
        collective_events = await self._detect_collective_behavior(agents_data, interactions)
        phase_events = await self._detect_phase_transitions()
        self_org_events = await self._detect_self_organization(interactions)
        learning_events = await self._detect_collective_learning(agents_data)
        
        events.extend(swarm_events)
        events.extend(collective_events)
        events.extend(phase_events)
        events.extend(self_org_events)
        events.extend(learning_events)
        
        # Store events for analysis
        for event in events:
            await self._store_emergence_event(event)
            
            # Update Prometheus metrics
            emergence_events.labels(
                emergence_type=event.emergence_type,
                magnitude=self._get_magnitude_category(event.magnitude)
            ).inc()
        
        return events

    async def _update_system_state(self, agents_data: List[Dict[str, any]], interactions: List[AgentInteraction]):
        """Update the internal state representation of the system"""
        current_time = datetime.now()
        
        # Update agent states
        for agent_data in agents_data:
            agent_id = agent_data.get('agent_id')
            if agent_id:
                self.agent_states[agent_id] = {
                    'state': agent_data,
                    'last_update': current_time
                }
        
        # Update interaction history
        for interaction in interactions:
            key = f"{interaction.source_agent}-{interaction.target_agent}"
            self.interaction_history[key].append({
                'timestamp': interaction.timestamp,
                'type': interaction.interaction_type,
                'strength': interaction.strength,
                'metadata': interaction.metadata
            })
            
            # Maintain history window
            if len(self.interaction_history[key]) > self.history_window:
                self.interaction_history[key].popleft()
        
        # Update network graph
        await self._update_network_graph(interactions)
        
        # Calculate system-level metrics
        await self._calculate_system_metrics()

    async def _update_network_graph(self, interactions: List[AgentInteraction]):
        """Update the network graph representation"""
        # Clear old edges (older than 1 hour)
        cutoff_time = datetime.now() - timedelta(hours=1)
        edges_to_remove = []
        
        for u, v, data in self.network_graph.edges(data=True):
            if data.get('timestamp', cutoff_time) < cutoff_time:
                edges_to_remove.append((u, v))
        
        for edge in edges_to_remove:
            self.network_graph.remove_edge(*edge)
        
        # Add new interactions
        for interaction in interactions:
            if interaction.strength > 0.1:  # Filter weak interactions
                if self.network_graph.has_edge(interaction.source_agent, interaction.target_agent):
                    # Update existing edge
                    current_weight = self.network_graph[interaction.source_agent][interaction.target_agent].get('weight', 0)
                    self.network_graph[interaction.source_agent][interaction.target_agent]['weight'] = current_weight + interaction.strength
                else:
                    # Add new edge
                    self.network_graph.add_edge(
                        interaction.source_agent,
                        interaction.target_agent,
                        weight=interaction.strength,
                        timestamp=interaction.timestamp,
                        interaction_type=interaction.interaction_type
                    )

    async def _calculate_system_metrics(self):
        """Calculate system-level complexity and emergence metrics"""
        try:
            # Network metrics
            if len(self.network_graph.nodes()) > 0:
                density = nx.density(self.network_graph)
                avg_clustering = nx.average_clustering(self.network_graph)
                
                # Connected components
                components = list(nx.connected_components(self.network_graph))
                largest_component_size = max(len(c) for c in components) if components else 0
                
                # Calculate entropy of degree distribution
                degrees = [d for n, d in self.network_graph.degree()]
                if degrees:
                    degree_counts = np.bincount(degrees)
                    degree_probs = degree_counts / sum(degree_counts)
                    entropy = -sum(p * np.log2(p) for p in degree_probs if p > 0)
                else:
                    entropy = 0
                
                # Update Prometheus metrics
                complexity_measure.labels(measurement_type='network_density').set(density)
                complexity_measure.labels(measurement_type='clustering_coefficient').set(avg_clustering)
                complexity_measure.labels(measurement_type='entropy').set(entropy)
                complexity_measure.labels(measurement_type='largest_component_ratio').set(
                    largest_component_size / len(self.network_graph.nodes())
                )
                
        except Exception as e:
            logger.error(f"Error calculating system metrics: {e}")

    async def _detect_swarm_intelligence(self, agents_data: List[Dict[str, any]]) -> List[EmergenceEvent]:
        """Detect swarm intelligence emergence"""
        events = []
        
        try:
            if len(agents_data) < 5:  # Need minimum agents for swarm behavior
                return events
            
            # Extract intelligence metrics
            intelligence_scores = []
            agent_ids = []
            
            for agent_data in agents_data:
                intelligence_metrics = agent_data.get('intelligence_metrics', {})
                if intelligence_metrics:
                    # Aggregate intelligence score
                    score = np.mean(list(intelligence_metrics.values()))
                    intelligence_scores.append(score)
                    agent_ids.append(agent_data.get('agent_id'))
            
            if len(intelligence_scores) < 5:
                return events
            
            intelligence_array = np.array(intelligence_scores)
            
            # Detect collective intelligence patterns
            collective_score = await self._calculate_collective_intelligence(intelligence_array, agent_ids)
            
            # Check for swarm coherence
            coherence_score = await self._calculate_swarm_coherence(intelligence_array)
            
            # Detect emergence based on thresholds and patterns
            if collective_score > self.emergence_thresholds['swarm_intelligence']:
                event = EmergenceEvent(
                    event_id=f"swarm_{int(time.time())}",
                    emergence_type="swarm_intelligence",
                    magnitude=collective_score,
                    confidence=min(collective_score * 1.2, 1.0),
                    timestamp=datetime.now(),
                    involved_agents=agent_ids,
                    description=f"Swarm intelligence detected with collective score {collective_score:.3f}",
                    characteristics={
                        'collective_intelligence_score': collective_score,
                        'coherence_score': coherence_score,
                        'participating_agents': len(agent_ids),
                        'intelligence_distribution': {
                            'mean': float(np.mean(intelligence_array)),
                            'std': float(np.std(intelligence_array)),
                            'min': float(np.min(intelligence_array)),
                            'max': float(np.max(intelligence_array))
                        }
                    },
                    predicted_evolution={
                        'expected_growth_rate': 0.1,
                        'sustainability_score': coherence_score,
                        'risk_factors': ['agent_dropout', 'performance_degradation']
                    }
                )
                events.append(event)
                
                # Update metrics
                collective_intelligence.labels(agent_group='swarm').set(collective_score)
                swarm_coherence.labels(swarm_id='main').set(coherence_score)
                
        except Exception as e:
            logger.error(f"Error in swarm intelligence detection: {e}")
        
        return events

    async def _calculate_collective_intelligence(self, intelligence_scores: np.ndarray, agent_ids: List[str]) -> float:
        """Calculate collective intelligence score"""
        # Factor 1: Average intelligence level
        avg_intelligence = np.mean(intelligence_scores)
        
        # Factor 2: Intelligence diversity (entropy)
        hist, _ = np.histogram(intelligence_scores, bins=10, density=True)
        diversity = -sum(p * np.log2(p) for p in hist if p > 0)
        normalized_diversity = diversity / np.log2(10)  # Normalize by max possible entropy
        
        # Factor 3: Synergy detection (non-linear intelligence gains)
        expected_collective = np.sum(intelligence_scores)
        
        # Calculate synergy by comparing with interaction-weighted performance
        synergy_score = await self._calculate_synergy_score(agent_ids, intelligence_scores)
        
        # Factor 4: Stability of collective performance
        stability_score = 1.0 - (np.std(intelligence_scores) / (np.mean(intelligence_scores) + 1e-8))
        
        # Weighted combination
        collective_score = (
            0.3 * avg_intelligence +
            0.25 * normalized_diversity +
            0.25 * synergy_score +
            0.2 * stability_score
        )
        
        return min(collective_score, 1.0)

    async def _calculate_synergy_score(self, agent_ids: List[str], intelligence_scores: np.ndarray) -> float:
        """Calculate synergy score based on agent interactions"""
        if len(agent_ids) < 2:
            return 0.0
        
        synergy_scores = []
        
        for i, agent_id in enumerate(agent_ids):
            # Find agents this agent interacts with
            interacting_agents = []
            interaction_strengths = []
            
            for key, interactions in self.interaction_history.items():
                if agent_id in key:
                    other_agent = key.replace(agent_id, '').replace('-', '')
                    if other_agent in agent_ids:
                        other_idx = agent_ids.index(other_agent)
                        if interactions:
                            avg_strength = np.mean([int_data['strength'] for int_data in interactions])
                            interacting_agents.append(other_idx)
                            interaction_strengths.append(avg_strength)
            
            if interacting_agents:
                # Calculate expected vs actual performance considering interactions
                interacting_scores = intelligence_scores[interacting_agents]
                interaction_weights = np.array(interaction_strengths)
                
                # Weighted average of interacting agents' intelligence
                weighted_neighbor_intelligence = np.average(interacting_scores, weights=interaction_weights)
                
                # Synergy: how much this agent's performance exceeds what would be expected
                # based on its own intelligence and neighbor influence
                expected_performance = 0.7 * intelligence_scores[i] + 0.3 * weighted_neighbor_intelligence
                actual_performance = intelligence_scores[i]
                
                synergy = max(0, (actual_performance - expected_performance) / (expected_performance + 1e-8))
                synergy_scores.append(synergy)
        
        return np.mean(synergy_scores) if synergy_scores else 0.0

    async def _calculate_swarm_coherence(self, intelligence_scores: np.ndarray) -> float:
        """Calculate swarm coherence based on behavioral alignment"""
        if len(intelligence_scores) < 2:
            return 0.0
        
        # Coherence factors
        factors = []
        
        # 1. Intelligence score variance (lower variance = higher coherence)
        variance_coherence = 1.0 / (1.0 + np.var(intelligence_scores))
        factors.append(variance_coherence)
        
        # 2. Network connectivity coherence
        if len(self.network_graph.nodes()) > 1:
            try:
                avg_clustering = nx.average_clustering(self.network_graph)
                factors.append(avg_clustering)
            except:
                factors.append(0.0)
        
        # 3. Temporal coherence (consistency over time)
        temporal_coherence = await self._calculate_temporal_coherence()
        factors.append(temporal_coherence)
        
        return np.mean(factors)

    async def _calculate_temporal_coherence(self) -> float:
        """Calculate temporal coherence of agent behaviors"""
        try:
            # Get recent system states
            states_key = "system_states"
            recent_states = redis_client.lrange(states_key, 0, 9)  # Last 10 states
            
            if len(recent_states) < 3:
                return 0.5  # Default coherence
            
            # Parse states and calculate coherence metrics
            parsed_states = [json.loads(state) for state in recent_states]
            
            # Calculate variance in key metrics over time
            metrics = ['network_density', 'average_connectivity', 'entropy']
            coherence_scores = []
            
            for metric in metrics:
                values = [state.get(metric, 0) for state in parsed_states]
                if values:
                    # Lower variance over time indicates higher coherence
                    variance = np.var(values)
                    mean_value = np.mean(values)
                    if mean_value > 0:
                        coherence = 1.0 / (1.0 + variance / mean_value)
                        coherence_scores.append(coherence)
            
            return np.mean(coherence_scores) if coherence_scores else 0.5
            
        except Exception as e:
            logger.error(f"Error calculating temporal coherence: {e}")
            return 0.5

    async def _detect_collective_behavior(self, agents_data: List[Dict[str, any]], interactions: List[AgentInteraction]) -> List[EmergenceEvent]:
        """Detect collective behavior patterns"""
        events = []
        
        try:
            if len(agents_data) < 3:
                return events
            
            # Analyze behavior synchronization
            synchronization_score = await self._calculate_behavior_synchronization(agents_data)
            
            # Detect coordinated actions
            coordination_score = await self._detect_coordinated_actions(interactions)
            
            # Calculate collective behavior score
            collective_behavior_score = (synchronization_score + coordination_score) / 2
            
            if collective_behavior_score > self.emergence_thresholds['collective_behavior']:
                involved_agents = [agent['agent_id'] for agent in agents_data]
                
                event = EmergenceEvent(
                    event_id=f"collective_{int(time.time())}",
                    emergence_type="collective_behavior",
                    magnitude=collective_behavior_score,
                    confidence=collective_behavior_score * 0.9,
                    timestamp=datetime.now(),
                    involved_agents=involved_agents,
                    description=f"Collective behavior detected with score {collective_behavior_score:.3f}",
                    characteristics={
                        'synchronization_score': synchronization_score,
                        'coordination_score': coordination_score,
                        'behavior_patterns': await self._identify_behavior_patterns(agents_data),
                        'interaction_density': len(interactions) / max(len(agents_data) ** 2, 1)
                    },
                    predicted_evolution={
                        'stability_prediction': synchronization_score,
                        'growth_potential': coordination_score,
                        'breakdown_risk': 1.0 - collective_behavior_score
                    }
                )
                events.append(event)
                
        except Exception as e:
            logger.error(f"Error in collective behavior detection: {e}")
        
        return events

    async def _calculate_behavior_synchronization(self, agents_data: List[Dict[str, any]]) -> float:
        """Calculate behavior synchronization score"""
        try:
            # Extract behavioral features
            features = []
            for agent_data in agents_data:
                feature_vector = [
                    agent_data.get('response_time', 0),
                    agent_data.get('cpu_usage', 0),
                    agent_data.get('memory_usage', 0),
                    agent_data.get('queue_length', 0),
                ]
                
                # Add intelligence metrics
                intelligence_metrics = agent_data.get('intelligence_metrics', {})
                feature_vector.extend([
                    intelligence_metrics.get('accuracy', 0),
                    intelligence_metrics.get('coherence', 0),
                    intelligence_metrics.get('efficiency', 0),
                ])
                
                features.append(feature_vector)
            
            if len(features) < 2:
                return 0.0
            
            features_array = np.array(features)
            
            # Calculate pairwise correlations
            correlations = []
            for i in range(len(features_array[0])):
                feature_column = features_array[:, i]
                if np.std(feature_column) > 1e-8:  # Avoid division by zero
                    # Calculate correlation coefficient between agents for this feature
                    for j in range(len(features_array)):
                        for k in range(j + 1, len(features_array)):
                            correlation = np.corrcoef([features_array[j, i], features_array[k, i]])[0, 1]
                            if not np.isnan(correlation):
                                correlations.append(abs(correlation))
            
            # Synchronization score is average absolute correlation
            return np.mean(correlations) if correlations else 0.0
            
        except Exception as e:
            logger.error(f"Error calculating behavior synchronization: {e}")
            return 0.0

    async def _detect_coordinated_actions(self, interactions: List[AgentInteraction]) -> float:
        """Detect coordinated actions among agents"""
        try:
            if len(interactions) < 2:
                return 0.0
            
            # Group interactions by time windows
            time_windows = defaultdict(list)
            window_size = 60  # 1 minute windows
            
            for interaction in interactions:
                window = int(interaction.timestamp.timestamp() // window_size)
                time_windows[window].append(interaction)
            
            coordination_scores = []
            
            for window, window_interactions in time_windows.items():
                if len(window_interactions) < 2:
                    continue
                
                # Calculate coordination within this time window
                # Factor 1: Temporal clustering (actions happening at similar times)
                timestamps = [int.timestamp() for int in window_interactions]
                temporal_variance = np.var(timestamps)
                temporal_coordination = 1.0 / (1.0 + temporal_variance)
                
                # Factor 2: Action similarity (similar interaction types)
                interaction_types = [int.interaction_type for int in window_interactions]
                type_diversity = len(set(interaction_types)) / len(interaction_types)
                type_coordination = 1.0 - type_diversity
                
                # Factor 3: Strength similarity (similar interaction strengths)
                strengths = [int.strength for int in window_interactions]
                strength_variance = np.var(strengths) if len(strengths) > 1 else 0
                strength_coordination = 1.0 / (1.0 + strength_variance)
                
                window_coordination = (temporal_coordination + type_coordination + strength_coordination) / 3
                coordination_scores.append(window_coordination)
            
            return np.mean(coordination_scores) if coordination_scores else 0.0
            
        except Exception as e:
            logger.error(f"Error detecting coordinated actions: {e}")
            return 0.0

    async def _identify_behavior_patterns(self, agents_data: List[Dict[str, any]]) -> Dict[str, any]:
        """Identify common behavior patterns"""
        patterns = {
            'dominant_behavior': 'unknown',
            'behavior_clusters': [],
            'pattern_strength': 0.0
        }
        
        try:
            if len(agents_data) < 3:
                return patterns
            
            # Extract behavior features for clustering
            features = []
            agent_ids = []
            
            for agent_data in agents_data:
                feature_vector = [
                    agent_data.get('response_time', 0),
                    agent_data.get('error_rate', 0),
                    agent_data.get('cpu_usage', 0),
                    agent_data.get('queue_length', 0),
                ]
                
                features.append(feature_vector)
                agent_ids.append(agent_data.get('agent_id'))
            
            features_array = np.array(features)
            
            # Standardize features
            scaler = StandardScaler()
            features_scaled = scaler.fit_transform(features_array)
            
            # Perform clustering to identify behavior patterns
            n_clusters = min(3, len(agents_data) // 2)
            if n_clusters >= 2:
                kmeans = KMeans(n_clusters=n_clusters, random_state=42)
                cluster_labels = kmeans.fit_predict(features_scaled)
                
                # Analyze clusters
                cluster_info = []
                for i in range(n_clusters):
                    cluster_agents = [agent_ids[j] for j, label in enumerate(cluster_labels) if label == i]
                    cluster_features = features_scaled[cluster_labels == i]
                    
                    cluster_info.append({
                        'cluster_id': i,
                        'agents': cluster_agents,
                        'size': len(cluster_agents),
                        'centroid': kmeans.cluster_centers_[i].tolist(),
                        'inertia': np.mean(np.sum((cluster_features - kmeans.cluster_centers_[i]) ** 2, axis=1))
                    })
                
                patterns['behavior_clusters'] = cluster_info
                patterns['pattern_strength'] = 1.0 - (kmeans.inertia_ / len(features_array))
                
                # Identify dominant behavior (largest cluster)
                largest_cluster = max(cluster_info, key=lambda x: x['size'])
                patterns['dominant_behavior'] = f"cluster_{largest_cluster['cluster_id']}"
                
        except Exception as e:
            logger.error(f"Error identifying behavior patterns: {e}")
        
        return patterns

    async def _detect_phase_transitions(self) -> List[EmergenceEvent]:
        """Detect phase transitions in the system"""
        events = []
        
        try:
            # Get recent system metrics
            recent_metrics = await self._get_recent_system_metrics(window_hours=2)
            
            if len(recent_metrics) < 10:  # Need sufficient data
                return events
            
            # Analyze different metrics for phase transitions
            metrics_to_analyze = ['network_density', 'entropy', 'clustering_coefficient']
            
            for metric_name in metrics_to_analyze:
                metric_values = [m.get(metric_name, 0) for m in recent_metrics]
                
                if len(metric_values) < 5:
                    continue
                
                # Detect phase transition using change point detection
                transition_detected, transition_strength = await self._detect_change_point(metric_values)
                
                if transition_detected and transition_strength > self.emergence_thresholds['phase_transition']:
                    event = EmergenceEvent(
                        event_id=f"phase_transition_{metric_name}_{int(time.time())}",
                        emergence_type="phase_transition",
                        magnitude=transition_strength,
                        confidence=transition_strength * 0.8,
                        timestamp=datetime.now(),
                        involved_agents=list(self.agent_states.keys()),
                        description=f"Phase transition detected in {metric_name}",
                        characteristics={
                            'metric_name': metric_name,
                            'transition_strength': transition_strength,
                            'pre_transition_mean': np.mean(metric_values[:len(metric_values)//2]),
                            'post_transition_mean': np.mean(metric_values[len(metric_values)//2:]),
                            'transition_point': len(metric_values) // 2
                        },
                        predicted_evolution={
                            'stabilization_time': '10-30 minutes',
                            'new_equilibrium_prediction': np.mean(metric_values[len(metric_values)//2:]),
                            'reversal_probability': 0.3
                        }
                    )
                    events.append(event)
                    
                    # Update metrics
                    phase_transition_indicator.labels(system_level=metric_name).set(transition_strength)
                    
        except Exception as e:
            logger.error(f"Error in phase transition detection: {e}")
        
        return events

    async def _detect_change_point(self, time_series: List[float]) -> Tuple[bool, float]:
        """Detect change points in time series using statistical methods"""
        try:
            if len(time_series) < 6:
                return False, 0.0
            
            series = np.array(time_series)
            n = len(series)
            
            # Use cumulative sum (CUSUM) approach
            mean_overall = np.mean(series)
            cumsum = np.cumsum(series - mean_overall)
            
            # Find the point where cumulative sum deviates most from zero
            max_deviation = np.max(np.abs(cumsum))
            change_point = np.argmax(np.abs(cumsum))
            
            # Calculate the strength of the change
            if change_point > 0 and change_point < n - 1:
                before_mean = np.mean(series[:change_point])
                after_mean = np.mean(series[change_point:])
                
                # Normalized change strength
                overall_std = np.std(series)
                if overall_std > 1e-8:
                    change_strength = abs(after_mean - before_mean) / overall_std
                    
                    # Consider it a significant change if strength > 2 (2 standard deviations)
                    is_change = change_strength > 2.0
                    return is_change, min(change_strength / 4.0, 1.0)  # Normalize to [0, 1]
            
            return False, 0.0
            
        except Exception as e:
            logger.error(f"Error in change point detection: {e}")
            return False, 0.0

    async def _detect_self_organization(self, interactions: List[AgentInteraction]) -> List[EmergenceEvent]:
        """Detect self-organization patterns"""
        events = []
        
        try:
            if len(interactions) < 10:
                return events
            
            # Analyze network evolution for self-organization
            organization_score = await self._calculate_self_organization_score(interactions)
            
            if organization_score > self.emergence_thresholds['self_organization']:
                involved_agents = list(set([i.source_agent for i in interactions] + [i.target_agent for i in interactions]))
                
                event = EmergenceEvent(
                    event_id=f"self_org_{int(time.time())}",
                    emergence_type="self_organization",
                    magnitude=organization_score,
                    confidence=organization_score * 0.85,
                    timestamp=datetime.now(),
                    involved_agents=involved_agents,
                    description=f"Self-organization detected with score {organization_score:.3f}",
                    characteristics={
                        'organization_score': organization_score,
                        'network_modularity': await self._calculate_modularity(),
                        'emergent_hierarchy': await self._detect_emergent_hierarchy(),
                        'adaptation_rate': await self._calculate_adaptation_rate()
                    },
                    predicted_evolution={
                        'structure_stability': organization_score,
                        'adaptation_capacity': organization_score * 0.8,
                        'optimization_potential': 1.0 - organization_score
                    }
                )
                events.append(event)
                
        except Exception as e:
            logger.error(f"Error in self-organization detection: {e}")
        
        return events

    async def _calculate_self_organization_score(self, interactions: List[AgentInteraction]) -> float:
        """Calculate self-organization score based on network properties"""
        try:
            if len(self.network_graph.nodes()) < 3:
                return 0.0
            
            scores = []
            
            # 1. Network modularity (communities forming)
            try:
                modularity = await self._calculate_modularity()
                scores.append(modularity)
            except:
                scores.append(0.0)
            
            # 2. Small-world properties
            try:
                clustering = nx.average_clustering(self.network_graph)
                if len(self.network_graph.nodes()) > 2:
                    path_length = nx.average_shortest_path_length(self.network_graph)
                    # Compare with random graph
                    n = len(self.network_graph.nodes())
                    m = len(self.network_graph.edges())
                    random_clustering = (2 * m) / (n * (n - 1)) if n > 1 else 0
                    random_path_length = np.log(n) / np.log(2 * m / n) if m > 0 else float('inf')
                    
                    small_world_score = (clustering / max(random_clustering, 1e-8)) / (path_length / max(random_path_length, 1e-8))
                    scores.append(min(small_world_score / 10, 1.0))  # Normalize
                else:
                    scores.append(0.0)
            except:
                scores.append(0.0)
            
            # 3. Degree distribution (scale-free properties)
            degrees = [d for n, d in self.network_graph.degree()]
            if degrees and max(degrees) > 0:
                # Check for power-law distribution
                degree_counts = np.bincount(degrees)
                non_zero_counts = degree_counts[degree_counts > 0]
                if len(non_zero_counts) > 2:
                    # Simple power-law check (more sophisticated methods exist)
                    log_degrees = np.log(range(1, len(non_zero_counts) + 1))
                    log_counts = np.log(non_zero_counts)
                    correlation = np.corrcoef(log_degrees, log_counts)[0, 1]
                    power_law_score = abs(correlation) if not np.isnan(correlation) else 0
                    scores.append(power_law_score)
                else:
                    scores.append(0.0)
            else:
                scores.append(0.0)
            
            return np.mean(scores) if scores else 0.0
            
        except Exception as e:
            logger.error(f"Error calculating self-organization score: {e}")
            return 0.0

    async def _calculate_modularity(self) -> float:
        """Calculate network modularity"""
        try:
            if len(self.network_graph.nodes()) < 3:
                return 0.0
            
            # Use community detection to calculate modularity
            communities = nx.community.greedy_modularity_communities(self.network_graph)
            modularity = nx.community.modularity(self.network_graph, communities)
            return max(0, modularity)
            
        except Exception as e:
            logger.error(f"Error calculating modularity: {e}")
            return 0.0

    async def _detect_emergent_hierarchy(self) -> Dict[str, any]:
        """Detect emergent hierarchical structures"""
        hierarchy = {
            'levels': 0,
            'hub_nodes': [],
            'hierarchy_strength': 0.0
        }
        
        try:
            if len(self.network_graph.nodes()) < 3:
                return hierarchy
            
            # Calculate centrality measures
            degree_centrality = nx.degree_centrality(self.network_graph)
            betweenness_centrality = nx.betweenness_centrality(self.network_graph)
            
            # Identify hub nodes (high centrality)
            centrality_threshold = 0.7
            hub_nodes = [
                node for node, centrality in degree_centrality.items()
                if centrality > centrality_threshold
            ]
            
            # Calculate hierarchy levels based on centrality distribution
            centrality_values = list(degree_centrality.values())
            if centrality_values:
                # Use k-means clustering on centrality values to identify levels
                centrality_array = np.array(centrality_values).reshape(-1, 1)
                
                optimal_k = min(3, len(centrality_values))
                if optimal_k >= 2:
                    kmeans = KMeans(n_clusters=optimal_k, random_state=42)
                    levels = kmeans.fit_predict(centrality_array)
                    
                    hierarchy['levels'] = len(set(levels))
                    hierarchy['hub_nodes'] = hub_nodes
                    
                    # Calculate hierarchy strength (how well-separated the levels are)
                    if len(set(levels)) > 1:
                        hierarchy['hierarchy_strength'] = kmeans.score(centrality_array) / len(centrality_values)
            
        except Exception as e:
            logger.error(f"Error detecting emergent hierarchy: {e}")
        
        return hierarchy

    async def _calculate_adaptation_rate(self) -> float:
        """Calculate how quickly the system adapts to changes"""
        try:
            # Get network snapshots over time
            snapshots = await self._get_network_snapshots(hours=1)
            
            if len(snapshots) < 3:
                return 0.0
            
            # Calculate rate of structural change
            change_rates = []
            
            for i in range(1, len(snapshots)):
                prev_snapshot = snapshots[i-1]
                curr_snapshot = snapshots[i]
                
                # Calculate structural similarity (Jaccard index of edges)
                prev_edges = set(prev_snapshot.get('edges', []))
                curr_edges = set(curr_snapshot.get('edges', []))
                
                if prev_edges or curr_edges:
                    intersection = len(prev_edges.intersection(curr_edges))
                    union = len(prev_edges.union(curr_edges))
                    similarity = intersection / union if union > 0 else 1.0
                    change_rate = 1.0 - similarity
                    change_rates.append(change_rate)
            
            # Adaptation rate is average change rate
            return np.mean(change_rates) if change_rates else 0.0
            
        except Exception as e:
            logger.error(f"Error calculating adaptation rate: {e}")
            return 0.0

    async def _detect_collective_learning(self, agents_data: List[Dict[str, any]]) -> List[EmergenceEvent]:
        """Detect collective learning emergence"""
        events = []
        
        try:
            if len(agents_data) < 3:
                return events
            
            # Analyze collective improvement over time
            learning_score = await self._calculate_collective_learning_score(agents_data)
            
            if learning_score > self.emergence_thresholds['collective_learning']:
                involved_agents = [agent['agent_id'] for agent in agents_data]
                
                event = EmergenceEvent(
                    event_id=f"collective_learning_{int(time.time())}",
                    emergence_type="collective_learning",
                    magnitude=learning_score,
                    confidence=learning_score * 0.9,
                    timestamp=datetime.now(),
                    involved_agents=involved_agents,
                    description=f"Collective learning detected with score {learning_score:.3f}",
                    characteristics={
                        'learning_score': learning_score,
                        'improvement_rate': await self._calculate_improvement_rate(agents_data),
                        'knowledge_sharing_score': await self._calculate_knowledge_sharing_score(),
                        'learning_acceleration': await self._calculate_learning_acceleration()
                    },
                    predicted_evolution={
                        'learning_trajectory': 'exponential',
                        'saturation_point': learning_score * 1.3,
                        'knowledge_transfer_efficiency': learning_score
                    }
                )
                events.append(event)
                
        except Exception as e:
            logger.error(f"Error in collective learning detection: {e}")
        
        return events

    async def _calculate_collective_learning_score(self, agents_data: List[Dict[str, any]]) -> float:
        """Calculate collective learning score"""
        try:
            # Get historical performance data
            historical_performance = await self._get_historical_performance(hours=24)
            
            if len(historical_performance) < 5:
                return 0.0
            
            # Calculate performance trends
            timestamps = [p['timestamp'] for p in historical_performance]
            performance_scores = [p['avg_intelligence'] for p in historical_performance]
            
            if len(performance_scores) < 3:
                return 0.0
            
            # Calculate learning curve (improvement over time)
            x = np.arange(len(performance_scores))
            
            # Fit linear trend
            slope, intercept, r_value, p_value, std_err = stats.linregress(x, performance_scores)
            
            # Learning score based on positive trend and correlation strength
            if slope > 0 and p_value < 0.05:  # Significant positive trend
                learning_score = min(slope * len(performance_scores) + abs(r_value), 1.0)
                return learning_score
            
            return 0.0
            
        except Exception as e:
            logger.error(f"Error calculating collective learning score: {e}")
            return 0.0

    async def _calculate_improvement_rate(self, agents_data: List[Dict[str, any]]) -> float:
        """Calculate the rate of improvement in agent performance"""
        try:
            current_performance = []
            for agent_data in agents_data:
                intelligence_metrics = agent_data.get('intelligence_metrics', {})
                if intelligence_metrics:
                    avg_intelligence = np.mean(list(intelligence_metrics.values()))
                    current_performance.append(avg_intelligence)
            
            if not current_performance:
                return 0.0
            
            current_avg = np.mean(current_performance)
            
            # Get performance from 1 hour ago
            historical_data = await self._get_historical_performance(hours=1)
            if historical_data:
                historical_avg = historical_data[-1].get('avg_intelligence', current_avg)
                improvement_rate = (current_avg - historical_avg) / max(historical_avg, 1e-8)
                return max(0, improvement_rate)
            
            return 0.0
            
        except Exception as e:
            logger.error(f"Error calculating improvement rate: {e}")
            return 0.0

    async def _calculate_knowledge_sharing_score(self) -> float:
        """Calculate knowledge sharing effectiveness"""
        try:
            # Analyze information flow patterns
            if len(self.interaction_history) == 0:
                return 0.0
            
            # Calculate information flow entropy
            flow_strengths = []
            for interactions in self.interaction_history.values():
                if interactions:
                    avg_strength = np.mean([i['strength'] for i in interactions])
                    flow_strengths.append(avg_strength)
            
            if not flow_strengths:
                return 0.0
            
            # Higher entropy in flow strengths indicates more distributed knowledge sharing
            flow_array = np.array(flow_strengths)
            normalized_flows = flow_array / (np.sum(flow_array) + 1e-8)
            
            entropy = -np.sum(normalized_flows * np.log2(normalized_flows + 1e-8))
            max_entropy = np.log2(len(normalized_flows))
            
            knowledge_sharing_score = entropy / max_entropy if max_entropy > 0 else 0.0
            return knowledge_sharing_score
            
        except Exception as e:
            logger.error(f"Error calculating knowledge sharing score: {e}")
            return 0.0

    async def _calculate_learning_acceleration(self) -> float:
        """Calculate if learning is accelerating"""
        try:
            historical_data = await self._get_historical_performance(hours=6)
            
            if len(historical_data) < 4:
                return 0.0
            
            performance_scores = [p['avg_intelligence'] for p in historical_data]
            
            # Calculate second derivative (acceleration)
            first_diff = np.diff(performance_scores)
            second_diff = np.diff(first_diff)
            
            # Positive second derivative indicates acceleration
            avg_acceleration = np.mean(second_diff)
            return max(0, avg_acceleration)
            
        except Exception as e:
            logger.error(f"Error calculating learning acceleration: {e}")
            return 0.0

    # Helper methods for data retrieval and storage
    async def _get_recent_system_metrics(self, window_hours: int = 2) -> List[Dict[str, any]]:
        """Get recent system metrics from Redis"""
        try:
            metrics_key = "system_metrics"
            cutoff_time = time.time() - (window_hours * 3600)
            
            # Get metrics with timestamps
            metrics_data = redis_client.zrangebyscore(
                metrics_key, cutoff_time, '+inf', withscores=True
            )
            
            metrics = []
            for data, timestamp in metrics_data:
                parsed_data = json.loads(data)
                parsed_data['timestamp'] = timestamp
                metrics.append(parsed_data)
            
            return metrics
            
        except Exception as e:
            logger.error(f"Error getting recent system metrics: {e}")
            return []

    async def _get_historical_performance(self, hours: int = 24) -> List[Dict[str, any]]:
        """Get historical performance data"""
        try:
            performance_key = "historical_performance"
            cutoff_time = time.time() - (hours * 3600)
            
            performance_data = redis_client.zrangebyscore(
                performance_key, cutoff_time, '+inf', withscores=True
            )
            
            performance = []
            for data, timestamp in performance_data:
                parsed_data = json.loads(data)
                parsed_data['timestamp'] = timestamp
                performance.append(parsed_data)
            
            return performance
            
        except Exception as e:
            logger.error(f"Error getting historical performance: {e}")
            return []

    async def _get_network_snapshots(self, hours: int = 1) -> List[Dict[str, any]]:
        """Get network snapshots over time"""
        try:
            snapshots_key = "network_snapshots"
            cutoff_time = time.time() - (hours * 3600)
            
            snapshot_data = redis_client.zrangebyscore(
                snapshots_key, cutoff_time, '+inf', withscores=True
            )
            
            snapshots = []
            for data, timestamp in snapshot_data:
                parsed_data = json.loads(data)
                parsed_data['timestamp'] = timestamp
                snapshots.append(parsed_data)
            
            return snapshots
            
        except Exception as e:
            logger.error(f"Error getting network snapshots: {e}")
            return []

    async def _store_emergence_event(self, event: EmergenceEvent):
        """Store emergence event for analysis"""
        try:
            event_data = {
                'event_id': event.event_id,
                'emergence_type': event.emergence_type,
                'magnitude': event.magnitude,
                'confidence': event.confidence,
                'timestamp': event.timestamp.isoformat(),
                'involved_agents': event.involved_agents,
                'description': event.description,
                'characteristics': event.characteristics,
                'predicted_evolution': event.predicted_evolution
            }
            
            # Store in Redis with expiry
            events_key = "emergence_events"
            redis_client.zadd(events_key, {json.dumps(event_data): time.time()})
            
            # Keep only recent events (last 7 days)
            cutoff_time = time.time() - (7 * 24 * 3600)
            redis_client.zremrangebyscore(events_key, 0, cutoff_time)
            
            logger.info(f"Stored emergence event: {event.event_id}")
            
        except Exception as e:
            logger.error(f"Error storing emergence event: {e}")

    def _get_magnitude_category(self, magnitude: float) -> str:
        """Categorize emergence magnitude"""
        if magnitude >= 0.8:
            return 'critical'
        elif magnitude >= 0.6:
            return 'high'
        elif magnitude >= 0.4:
            return 'medium'
        else:
            return 'low'

# Initialize emergence detector
emergence_detector = EmergenceDetector()

# API endpoints
@app.post("/analyze")
async def analyze_emergence(agents_data: List[Dict[str, any]], interactions: List[AgentInteraction]):
    """Analyze system for emergence patterns"""
    events = await emergence_detector.analyze_system_emergence(agents_data, interactions)
    return {"emergence_events": events, "count": len(events)}

@app.get("/events")
async def get_emergence_events(hours: int = 24):
    """Get recent emergence events"""
    try:
        events_key = "emergence_events"
        cutoff_time = time.time() - (hours * 3600)
        
        event_data = redis_client.zrangebyscore(
            events_key, cutoff_time, '+inf', withscores=True
        )
        
        events = []
        for data, timestamp in event_data:
            parsed_data = json.loads(data)
            events.append(parsed_data)
        
        return {"events": events, "count": len(events)}
        
    except Exception as e:
        logger.error(f"Error getting emergence events: {e}")
        return {"events": [], "count": 0}

@app.get("/network/analysis")
async def get_network_analysis():
    """Get current network analysis"""
    try:
        analysis = {
            'node_count': len(emergence_detector.network_graph.nodes()),
            'edge_count': len(emergence_detector.network_graph.edges()),
            'density': nx.density(emergence_detector.network_graph) if len(emergence_detector.network_graph.nodes()) > 0 else 0,
            'clustering': nx.average_clustering(emergence_detector.network_graph) if len(emergence_detector.network_graph.nodes()) > 0 else 0,
            'connected_components': len(list(nx.connected_components(emergence_detector.network_graph))),
        }
        
        # Add centrality measures for top nodes
        if len(emergence_detector.network_graph.nodes()) > 0:
            degree_centrality = nx.degree_centrality(emergence_detector.network_graph)
            top_nodes = sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)[:10]
            analysis['top_nodes_by_centrality'] = top_nodes
        
        return analysis
        
    except Exception as e:
        logger.error(f"Error getting network analysis: {e}")
        return {"error": str(e)}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.get("/metrics")
async def get_metrics():
    """Prometheus metrics endpoint"""
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8082)