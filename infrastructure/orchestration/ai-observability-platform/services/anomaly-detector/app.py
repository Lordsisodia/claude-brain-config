import asyncio
import json
import time
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import numpy as np
import pandas as pd
from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from prometheus_client import Counter, Gauge, Histogram, generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response
import uvicorn
import redis
from elasticsearch import AsyncElasticsearch

# ML imports for anomaly detection
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN
from river import anomaly, preprocessing
from pyod.models.auto_encoder import AutoEncoder
from pyod.models.lof import LOF
from pyod.models.lstm_ae import LSTM_AE
import tensorflow as tf
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI
app = FastAPI(title="AI Anomaly Detection Service", version="1.0.0")

# Redis and Elasticsearch connections
redis_client = redis.Redis(host='redis', port=6379, decode_responses=True)
es_client = AsyncElasticsearch([{'host': 'elasticsearch', 'port': 9200}])

# Prometheus metrics
anomalies_detected = Counter('anomalies_detected_total', 'Total anomalies detected', ['anomaly_type', 'severity'])
anomaly_score = Gauge('anomaly_score', 'Anomaly score for agents', ['agent_id', 'detector_type'])
detection_latency = Histogram('anomaly_detection_latency_seconds', 'Time to detect anomalies')
false_positive_rate = Gauge('anomaly_false_positive_rate', 'False positive rate', ['detector_type'])
detection_accuracy = Gauge('anomaly_detection_accuracy', 'Detection accuracy', ['detector_type'])

# Data models
class AnomalyAlert(BaseModel):
    agent_id: str
    anomaly_type: str
    severity: str  # low, medium, high, critical
    score: float
    timestamp: datetime
    description: str
    metadata: Dict[str, any]
    suggested_actions: List[str]

class DetectionResult(BaseModel):
    is_anomaly: bool
    confidence: float
    anomaly_type: str
    score: float
    features_contributing: List[str]

class AnomalyDetector:
    def __init__(self):
        self.detectors = {}
        self.scalers = {}
        self.thresholds = {
            'statistical': 3.0,  # Z-score threshold
            'isolation': 0.1,    # Contamination rate
            'clustering': 0.5,   # DBSCAN eps
            'lstm': 0.3,         # LSTM threshold
        }
        self.initialize_detectors()
        
    def initialize_detectors(self):
        """Initialize various anomaly detection models"""
        # Statistical detector (Z-score based)
        self.detectors['statistical'] = {
            'mean': {},
            'std': {},
            'last_update': time.time()
        }
        
        # Isolation Forest
        self.detectors['isolation'] = IsolationForest(
            contamination=self.thresholds['isolation'],
            random_state=42,
            n_estimators=100
        )
        
        # Local Outlier Factor
        self.detectors['lof'] = LOF(contamination=self.thresholds['isolation'])
        
        # AutoEncoder for deep anomaly detection
        self.detectors['autoencoder'] = AutoEncoder(
            hidden_neurons=[64, 32, 16, 32, 64],
            epochs=50,
            batch_size=32,
            contamination=self.thresholds['isolation']
        )
        
        # LSTM AutoEncoder for time series anomalies
        self.detectors['lstm'] = LSTM_AE(
            contamination=self.thresholds['isolation'],
            epochs=50,
            batch_size=32
        )
        
        # Online learning detector using River
        self.detectors['online'] = anomaly.HalfSpaceTrees(
            n_trees=10,
            height=8,
            window_size=250
        )
        
        # DBSCAN for clustering-based anomaly detection
        self.detectors['clustering'] = DBSCAN(
            eps=self.thresholds['clustering'],
            min_samples=5
        )
        
        # Standard scaler for normalization
        self.scalers['standard'] = StandardScaler()
        
        logger.info("Initialized all anomaly detectors")

    async def detect_anomalies(self, agent_id: str, metrics: Dict[str, any]) -> List[AnomalyAlert]:
        """Main anomaly detection function"""
        start_time = time.time()
        alerts = []
        
        try:
            # Prepare feature vector
            features = self._extract_features(metrics)
            if len(features) == 0:
                return alerts
            
            # Run different detection algorithms
            detection_results = await self._run_all_detectors(agent_id, features, metrics)
            
            # Generate alerts based on detection results
            for detector_type, result in detection_results.items():
                if result.is_anomaly:
                    alert = await self._create_alert(agent_id, result, metrics)
                    alerts.append(alert)
                    
                    # Update Prometheus metrics
                    anomalies_detected.labels(
                        anomaly_type=result.anomaly_type,
                        severity=alert.severity
                    ).inc()
                    
                    anomaly_score.labels(
                        agent_id=agent_id,
                        detector_type=detector_type
                    ).set(result.score)
            
            # Store results for learning
            await self._store_detection_results(agent_id, detection_results, metrics)
            
            # Update detection latency metric
            detection_latency.observe(time.time() - start_time)
            
            return alerts
            
        except Exception as e:
            logger.error(f"Error in anomaly detection for agent {agent_id}: {e}")
            return []

    def _extract_features(self, metrics: Dict[str, any]) -> np.ndarray:
        """Extract numerical features from metrics"""
        features = []
        
        # Basic performance metrics
        features.extend([
            metrics.get('response_time', 0.0),
            metrics.get('cpu_usage', 0.0),
            metrics.get('memory_usage', 0.0),
            metrics.get('error_rate', 0.0),
            metrics.get('queue_length', 0.0),
            metrics.get('throughput', 0.0),
        ])
        
        # AI-specific metrics
        intelligence_metrics = metrics.get('intelligence_metrics', {})
        features.extend([
            intelligence_metrics.get('accuracy', 0.0),
            intelligence_metrics.get('coherence', 0.0),
            intelligence_metrics.get('efficiency', 0.0),
            intelligence_metrics.get('adaptability', 0.0),
        ])
        
        # Token usage metrics
        features.extend([
            metrics.get('input_tokens', 0.0),
            metrics.get('output_tokens', 0.0),
            metrics.get('token_rate', 0.0),
        ])
        
        # Model performance metrics
        features.extend([
            metrics.get('inference_time', 0.0),
            metrics.get('model_load_time', 0.0),
            metrics.get('context_length', 0.0),
        ])
        
        return np.array(features, dtype=float)

    async def _run_all_detectors(self, agent_id: str, features: np.ndarray, metrics: Dict[str, any]) -> Dict[str, DetectionResult]:
        """Run all anomaly detection algorithms"""
        results = {}
        
        # Statistical anomaly detection
        results['statistical'] = await self._statistical_detection(agent_id, features)
        
        # Isolation Forest
        results['isolation'] = await self._isolation_forest_detection(features)
        
        # Local Outlier Factor
        results['lof'] = await self._lof_detection(features)
        
        # AutoEncoder
        results['autoencoder'] = await self._autoencoder_detection(features)
        
        # Online learning
        results['online'] = await self._online_detection(features)
        
        # Clustering-based
        results['clustering'] = await self._clustering_detection(features)
        
        # Time series anomaly detection
        results['timeseries'] = await self._timeseries_detection(agent_id, features)
        
        # Behavioral anomaly detection
        results['behavioral'] = await self._behavioral_detection(agent_id, metrics)
        
        return results

    async def _statistical_detection(self, agent_id: str, features: np.ndarray) -> DetectionResult:
        """Statistical anomaly detection using Z-score"""
        try:
            # Get historical stats for this agent
            stats_key = f"stats:{agent_id}"
            stats_data = redis_client.get(stats_key)
            
            if stats_data:
                stats = json.loads(stats_data)
                mean = np.array(stats['mean'])
                std = np.array(stats['std'])
                count = stats['count']
            else:
                mean = features
                std = np.ones_like(features)
                count = 1
            
            # Calculate Z-scores
            z_scores = np.abs((features - mean) / (std + 1e-8))
            max_z_score = np.max(z_scores)
            
            # Update running statistics
            count += 1
            alpha = 1.0 / count if count < 100 else 0.1
            mean = (1 - alpha) * mean + alpha * features
            std = np.sqrt((1 - alpha) * std**2 + alpha * (features - mean)**2)
            
            # Store updated stats
            updated_stats = {
                'mean': mean.tolist(),
                'std': std.tolist(),
                'count': count,
                'last_update': time.time()
            }
            redis_client.set(stats_key, json.dumps(updated_stats), ex=86400)  # 24 hour expiry
            
            is_anomaly = max_z_score > self.thresholds['statistical']
            
            return DetectionResult(
                is_anomaly=is_anomaly,
                confidence=min(max_z_score / self.thresholds['statistical'], 1.0),
                anomaly_type='statistical',
                score=float(max_z_score),
                features_contributing=[f"feature_{i}" for i, z in enumerate(z_scores) if z > 2.0]
            )
            
        except Exception as e:
            logger.error(f"Statistical detection error: {e}")
            return DetectionResult(
                is_anomaly=False, confidence=0.0, anomaly_type='statistical',
                score=0.0, features_contributing=[]
            )

    async def _isolation_forest_detection(self, features: np.ndarray) -> DetectionResult:
        """Isolation Forest anomaly detection"""
        try:
            # Get training data from Redis
            training_data = await self._get_training_data('isolation')
            
            if len(training_data) > 100:  # Need enough data to train
                X_train = np.array(training_data)
                self.detectors['isolation'].fit(X_train)
                
                prediction = self.detectors['isolation'].predict(features.reshape(1, -1))[0]
                anomaly_score = -self.detectors['isolation'].score_samples(features.reshape(1, -1))[0]
                
                is_anomaly = prediction == -1
                confidence = min(anomaly_score / 0.5, 1.0)  # Normalize score
                
                return DetectionResult(
                    is_anomaly=is_anomaly,
                    confidence=confidence,
                    anomaly_type='isolation',
                    score=float(anomaly_score),
                    features_contributing=[]
                )
            
        except Exception as e:
            logger.error(f"Isolation Forest detection error: {e}")
        
        return DetectionResult(
            is_anomaly=False, confidence=0.0, anomaly_type='isolation',
            score=0.0, features_contributing=[]
        )

    async def _lof_detection(self, features: np.ndarray) -> DetectionResult:
        """Local Outlier Factor detection"""
        try:
            training_data = await self._get_training_data('lof')
            
            if len(training_data) > 50:
                X_train = np.array(training_data)
                self.detectors['lof'].fit(X_train)
                
                prediction = self.detectors['lof'].predict(features.reshape(1, -1))[0]
                lof_score = self.detectors['lof'].decision_function(features.reshape(1, -1))[0]
                
                is_anomaly = prediction == 1  # LOF returns 1 for outliers
                confidence = min(abs(lof_score) / 2.0, 1.0)
                
                return DetectionResult(
                    is_anomaly=is_anomaly,
                    confidence=confidence,
                    anomaly_type='lof',
                    score=float(abs(lof_score)),
                    features_contributing=[]
                )
                
        except Exception as e:
            logger.error(f"LOF detection error: {e}")
        
        return DetectionResult(
            is_anomaly=False, confidence=0.0, anomaly_type='lof',
            score=0.0, features_contributing=[]
        )

    async def _autoencoder_detection(self, features: np.ndarray) -> DetectionResult:
        """AutoEncoder-based anomaly detection"""
        try:
            training_data = await self._get_training_data('autoencoder')
            
            if len(training_data) > 200:
                X_train = np.array(training_data)
                self.detectors['autoencoder'].fit(X_train)
                
                prediction = self.detectors['autoencoder'].predict(features.reshape(1, -1))[0]
                ae_score = self.detectors['autoencoder'].decision_function(features.reshape(1, -1))[0]
                
                is_anomaly = prediction == 1
                confidence = min(abs(ae_score) / 1.0, 1.0)
                
                return DetectionResult(
                    is_anomaly=is_anomaly,
                    confidence=confidence,
                    anomaly_type='autoencoder',
                    score=float(abs(ae_score)),
                    features_contributing=[]
                )
                
        except Exception as e:
            logger.error(f"AutoEncoder detection error: {e}")
        
        return DetectionResult(
            is_anomaly=False, confidence=0.0, anomaly_type='autoencoder',
            score=0.0, features_contributing=[]
        )

    async def _online_detection(self, features: np.ndarray) -> DetectionResult:
        """Online learning anomaly detection using River"""
        try:
            # Create feature dict for River
            feature_dict = {f'f{i}': float(val) for i, val in enumerate(features)}
            
            # Get anomaly score
            anomaly_score = self.detectors['online'].score_one(feature_dict)
            
            # Update the online model
            self.detectors['online'].learn_one(feature_dict)
            
            # Determine if anomaly (threshold-based)
            threshold = 0.7
            is_anomaly = anomaly_score > threshold
            confidence = min(anomaly_score / threshold, 1.0)
            
            return DetectionResult(
                is_anomaly=is_anomaly,
                confidence=confidence,
                anomaly_type='online',
                score=float(anomaly_score),
                features_contributing=[]
            )
            
        except Exception as e:
            logger.error(f"Online detection error: {e}")
            return DetectionResult(
                is_anomaly=False, confidence=0.0, anomaly_type='online',
                score=0.0, features_contributing=[]
            )

    async def _clustering_detection(self, features: np.ndarray) -> DetectionResult:
        """Clustering-based anomaly detection using DBSCAN"""
        try:
            training_data = await self._get_training_data('clustering')
            
            if len(training_data) > 50:
                X_train = np.array(training_data + [features.tolist()])
                
                # Normalize data
                X_scaled = self.scalers['standard'].fit_transform(X_train)
                
                # Perform clustering
                clusters = self.detectors['clustering'].fit_predict(X_scaled)
                
                # Last point is our test point
                test_cluster = clusters[-1]
                is_anomaly = test_cluster == -1  # -1 indicates outlier in DBSCAN
                
                # Calculate confidence based on distance to nearest cluster
                if is_anomaly:
                    # Find distance to nearest non-outlier point
                    non_outlier_indices = np.where(clusters[:-1] != -1)[0]
                    if len(non_outlier_indices) > 0:
                        distances = np.linalg.norm(
                            X_scaled[-1:] - X_scaled[non_outlier_indices], axis=1
                        )
                        min_distance = np.min(distances)
                        confidence = min(min_distance / 2.0, 1.0)
                    else:
                        confidence = 1.0
                else:
                    confidence = 0.0
                
                return DetectionResult(
                    is_anomaly=is_anomaly,
                    confidence=confidence,
                    anomaly_type='clustering',
                    score=confidence,
                    features_contributing=[]
                )
                
        except Exception as e:
            logger.error(f"Clustering detection error: {e}")
        
        return DetectionResult(
            is_anomaly=False, confidence=0.0, anomaly_type='clustering',
            score=0.0, features_contributing=[]
        )

    async def _timeseries_detection(self, agent_id: str, features: np.ndarray) -> DetectionResult:
        """Time series anomaly detection"""
        try:
            # Get historical data for this agent
            ts_key = f"timeseries:{agent_id}"
            ts_data = redis_client.lrange(ts_key, 0, -1)
            
            if len(ts_data) > 10:
                # Convert to numpy array
                historical_features = np.array([json.loads(d) for d in ts_data])
                
                # Calculate rolling statistics
                window_size = min(10, len(historical_features))
                recent_data = historical_features[-window_size:]
                
                # Calculate anomaly score based on deviation from recent trend
                mean_recent = np.mean(recent_data, axis=0)
                std_recent = np.std(recent_data, axis=0) + 1e-8
                
                z_scores = np.abs((features - mean_recent) / std_recent)
                max_z_score = np.max(z_scores)
                
                threshold = 2.5
                is_anomaly = max_z_score > threshold
                confidence = min(max_z_score / threshold, 1.0)
                
                # Store current features for future analysis
                redis_client.lpush(ts_key, json.dumps(features.tolist()))
                redis_client.ltrim(ts_key, 0, 99)  # Keep last 100 data points
                
                return DetectionResult(
                    is_anomaly=is_anomaly,
                    confidence=confidence,
                    anomaly_type='timeseries',
                    score=float(max_z_score),
                    features_contributing=[f"feature_{i}" for i, z in enumerate(z_scores) if z > 2.0]
                )
            else:
                # Not enough data, store current point
                redis_client.lpush(ts_key, json.dumps(features.tolist()))
                
        except Exception as e:
            logger.error(f"Time series detection error: {e}")
        
        return DetectionResult(
            is_anomaly=False, confidence=0.0, anomaly_type='timeseries',
            score=0.0, features_contributing=[]
        )

    async def _behavioral_detection(self, agent_id: str, metrics: Dict[str, any]) -> DetectionResult:
        """Behavioral anomaly detection for AI agents"""
        try:
            # Get agent's behavioral profile
            profile_key = f"behavior:{agent_id}"
            profile_data = redis_client.get(profile_key)
            
            if profile_data:
                profile = json.loads(profile_data)
            else:
                # Initialize behavioral profile
                profile = {
                    'typical_response_pattern': [],
                    'typical_error_pattern': [],
                    'typical_intelligence_scores': {},
                    'interaction_patterns': [],
                    'update_count': 0
                }
            
            # Analyze current behavior
            current_behavior = {
                'response_time': metrics.get('response_time', 0),
                'error_rate': metrics.get('error_rate', 0),
                'intelligence_score': np.mean(list(metrics.get('intelligence_metrics', {}).values())),
                'request_pattern': metrics.get('request_pattern', 'unknown'),
                'timestamp': time.time()
            }
            
            # Compare with typical behavior
            anomaly_score = 0.0
            contributing_factors = []
            
            # Response time anomaly
            if profile['typical_response_pattern']:
                avg_response = np.mean(profile['typical_response_pattern'])
                if current_behavior['response_time'] > avg_response * 3:
                    anomaly_score += 0.3
                    contributing_factors.append('response_time')
            
            # Intelligence score anomaly
            if profile['typical_intelligence_scores']:
                avg_intelligence = np.mean(list(profile['typical_intelligence_scores'].values()))
                if current_behavior['intelligence_score'] < avg_intelligence * 0.5:
                    anomaly_score += 0.4
                    contributing_factors.append('intelligence_degradation')
            
            # Error rate anomaly
            if profile['typical_error_pattern']:
                avg_error_rate = np.mean(profile['typical_error_pattern'])
                if current_behavior['error_rate'] > avg_error_rate * 5:
                    anomaly_score += 0.3
                    contributing_factors.append('error_rate')
            
            # Update behavioral profile
            profile['typical_response_pattern'].append(current_behavior['response_time'])
            profile['typical_error_pattern'].append(current_behavior['error_rate'])
            profile['typical_intelligence_scores'][str(int(time.time()))] = current_behavior['intelligence_score']
            profile['update_count'] += 1
            
            # Keep only recent data (last 100 points)
            for key in ['typical_response_pattern', 'typical_error_pattern']:
                profile[key] = profile[key][-100:]
            
            # Keep only recent intelligence scores (last 24 hours)
            cutoff_time = time.time() - 86400
            profile['typical_intelligence_scores'] = {
                k: v for k, v in profile['typical_intelligence_scores'].items()
                if float(k) > cutoff_time
            }
            
            # Store updated profile
            redis_client.set(profile_key, json.dumps(profile), ex=86400 * 7)  # 7 day expiry
            
            is_anomaly = anomaly_score > 0.5
            confidence = min(anomaly_score, 1.0)
            
            return DetectionResult(
                is_anomaly=is_anomaly,
                confidence=confidence,
                anomaly_type='behavioral',
                score=anomaly_score,
                features_contributing=contributing_factors
            )
            
        except Exception as e:
            logger.error(f"Behavioral detection error: {e}")
            return DetectionResult(
                is_anomaly=False, confidence=0.0, anomaly_type='behavioral',
                score=0.0, features_contributing=[]
            )

    async def _get_training_data(self, detector_type: str, limit: int = 1000) -> List[List[float]]:
        """Get training data for ML models"""
        try:
            training_key = f"training_data:{detector_type}"
            data = redis_client.lrange(training_key, 0, limit - 1)
            return [json.loads(d) for d in data]
        except Exception as e:
            logger.error(f"Error getting training data: {e}")
            return []

    async def _store_detection_results(self, agent_id: str, results: Dict[str, DetectionResult], metrics: Dict[str, any]):
        """Store detection results for learning and analysis"""
        try:
            # Store in Elasticsearch for analysis
            doc = {
                'agent_id': agent_id,
                'timestamp': datetime.now().isoformat(),
                'metrics': metrics,
                'detection_results': {
                    detector_type: {
                        'is_anomaly': result.is_anomaly,
                        'confidence': result.confidence,
                        'score': result.score,
                        'features_contributing': result.features_contributing
                    }
                    for detector_type, result in results.items()
                },
                'features': self._extract_features(metrics).tolist()
            }
            
            await es_client.index(
                index=f"anomaly-detection-{datetime.now().strftime('%Y-%m')}",
                document=doc
            )
            
            # Store features for training data
            features = self._extract_features(metrics)
            for detector_type in ['isolation', 'lof', 'autoencoder', 'clustering']:
                training_key = f"training_data:{detector_type}"
                redis_client.lpush(training_key, json.dumps(features.tolist()))
                redis_client.ltrim(training_key, 0, 9999)  # Keep last 10k points
                
        except Exception as e:
            logger.error(f"Error storing detection results: {e}")

    async def _create_alert(self, agent_id: str, result: DetectionResult, metrics: Dict[str, any]) -> AnomalyAlert:
        """Create an anomaly alert"""
        # Determine severity based on confidence and anomaly type
        if result.confidence > 0.9:
            severity = 'critical'
        elif result.confidence > 0.7:
            severity = 'high'
        elif result.confidence > 0.5:
            severity = 'medium'
        else:
            severity = 'low'
        
        # Generate description and suggested actions
        description = f"Anomaly detected using {result.anomaly_type} detector with confidence {result.confidence:.2f}"
        
        suggested_actions = []
        if result.anomaly_type == 'statistical':
            suggested_actions.extend([
                "Check agent configuration",
                "Review recent changes",
                "Monitor for pattern continuation"
            ])
        elif result.anomaly_type == 'behavioral':
            suggested_actions.extend([
                "Investigate agent intelligence degradation",
                "Check model performance",
                "Review training data quality"
            ])
        elif result.anomaly_type == 'timeseries':
            suggested_actions.extend([
                "Analyze trending patterns",
                "Check for resource constraints",
                "Review workload distribution"
            ])
        
        return AnomalyAlert(
            agent_id=agent_id,
            anomaly_type=result.anomaly_type,
            severity=severity,
            score=result.score,
            timestamp=datetime.now(),
            description=description,
            metadata={
                'confidence': result.confidence,
                'features_contributing': result.features_contributing,
                'detector_type': result.anomaly_type,
                'metrics_snapshot': metrics
            },
            suggested_actions=suggested_actions
        )

# Initialize anomaly detector
anomaly_detector = AnomalyDetector()

# API endpoints
@app.post("/detect/{agent_id}")
async def detect_anomalies(agent_id: str, metrics: Dict[str, any]):
    """Detect anomalies for a specific agent"""
    alerts = await anomaly_detector.detect_anomalies(agent_id, metrics)
    return {"alerts": alerts, "count": len(alerts)}

@app.get("/agents/{agent_id}/anomalies")
async def get_agent_anomalies(agent_id: str, hours: int = 24):
    """Get recent anomalies for an agent"""
    try:
        query = {
            "query": {
                "bool": {
                    "must": [
                        {"match": {"agent_id": agent_id}},
                        {"range": {"timestamp": {"gte": f"now-{hours}h"}}}
                    ]
                }
            },
            "sort": [{"timestamp": {"order": "desc"}}],
            "size": 100
        }
        
        response = await es_client.search(
            index="anomaly-detection-*",
            body=query
        )
        
        anomalies = [hit["_source"] for hit in response["hits"]["hits"]]
        return {"anomalies": anomalies, "count": len(anomalies)}
        
    except Exception as e:
        logger.error(f"Error getting anomalies: {e}")
        return {"anomalies": [], "count": 0}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.get("/metrics")
async def get_metrics():
    """Prometheus metrics endpoint"""
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8081)