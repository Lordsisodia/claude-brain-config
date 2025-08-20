#!/usr/bin/env python3
"""
Dask-based Distributed AI Computing for Billion-Scale Orchestration
Handles massive parallel computations, distributed arrays, and AI model processing
"""

import asyncio
import json
import logging
import os
import time
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Any, Union, Tuple
import numpy as np
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
import pickle
import warnings
warnings.filterwarnings('ignore')

import dask
import dask.array as da
import dask.dataframe as dd
import dask.bag as db
from dask import delayed, compute, persist
from dask.distributed import Client, as_completed, LocalCluster, Scheduler, Worker
from dask.distributed import get_worker, wait, fire_and_forget
import dask_ml.model_selection as dms
from dask_ml.wrappers import ParallelPostFit
import xgboost as xgb
from sklearn.model_selection import train_test_split
import prometheus_client

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class ComputeConfig:
    """Configuration for Dask distributed computing"""
    cluster_type: str = "distributed"  # local, distributed, kubernetes
    scheduler_address: Optional[str] = None
    n_workers: int = 10
    threads_per_worker: int = 4
    memory_per_worker: str = "4GB"
    worker_resources: Dict[str, int] = field(default_factory=dict)
    chunk_size: Union[int, str] = "128MB"
    max_memory_usage: str = "80%"
    spill_to_disk: bool = True
    dashboard_port: int = 8787
    serialization_format: str = "pickle"

@dataclass
class AIWorkloadConfig:
    """Configuration for AI workload processing"""
    workload_id: str
    workload_type: str  # inference, training, data_processing, feature_extraction
    model_type: str = "transformer"
    batch_size: int = 32
    data_sources: List[str] = field(default_factory=list)
    output_format: str = "parquet"
    distributed_strategy: str = "data_parallel"  # data_parallel, model_parallel, pipeline_parallel
    fault_tolerance: str = "high"
    checkpoint_interval: int = 1000  # batches
    resource_requirements: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ScalingPolicy:
    """Auto-scaling policy for dynamic resource management"""
    min_workers: int = 5
    max_workers: int = 1000
    scale_up_threshold: float = 0.8  # CPU utilization
    scale_down_threshold: float = 0.3
    scale_up_cooldown: int = 300  # seconds
    scale_down_cooldown: int = 600
    target_memory_usage: float = 0.7
    aggressive_scaling: bool = False

# Prometheus metrics for billion-scale monitoring
compute_tasks_total = prometheus_client.Counter('dask_ai_tasks_total', 'Total AI compute tasks', ['workload_type', 'status'])
compute_duration = prometheus_client.Histogram('dask_ai_compute_seconds', 'Compute task duration', ['workload_type'])
worker_utilization = prometheus_client.Gauge('dask_worker_utilization', 'Worker resource utilization', ['worker_id', 'resource'])
data_throughput = prometheus_client.Gauge('dask_data_throughput_bytes_per_second', 'Data processing throughput', ['workload_id'])
memory_usage = prometheus_client.Gauge('dask_memory_usage_bytes', 'Memory usage', ['component'])

class DaskAICompute:
    """Dask-based AI compute engine with billion-scale capabilities"""
    
    def __init__(self, config: ComputeConfig):
        self.config = config
        self.client = None
        self.cluster = None
        self.active_workloads = {}
        self.performance_metrics = {}
        self.scaling_policy = ScalingPolicy()
        
        # Initialize Dask cluster
        self._initialize_cluster()
        
        # Start monitoring
        self._start_monitoring()
        
        logger.info(f"Dask AI Compute initialized with {self.config.n_workers} workers")
    
    def _initialize_cluster(self):
        """Initialize Dask cluster based on configuration"""
        if self.config.cluster_type == "local":
            # Local cluster for development/testing
            self.cluster = LocalCluster(
                n_workers=self.config.n_workers,
                threads_per_worker=self.config.threads_per_worker,
                memory_limit=self.config.memory_per_worker,
                dashboard_address=f":{self.config.dashboard_port}",
                silence_logs=False
            )
            self.client = Client(self.cluster)
            
        elif self.config.scheduler_address:
            # Connect to existing distributed cluster
            self.client = Client(self.config.scheduler_address)
            
        else:
            # Create new distributed cluster
            self.cluster = LocalCluster(
                n_workers=self.config.n_workers,
                threads_per_worker=self.config.threads_per_worker,
                memory_limit=self.config.memory_per_worker,
                dashboard_address=f":{self.config.dashboard_port}"
            )
            self.client = Client(self.cluster)
        
        # Configure Dask settings for billion-scale operations
        dask.config.set({
            'distributed.worker.memory.target': 0.80,  # Target 80% memory usage
            'distributed.worker.memory.spill': 0.85,   # Spill at 85%
            'distributed.worker.memory.pause': 0.90,   # Pause at 90%
            'distributed.worker.memory.terminate': 0.95,  # Terminate at 95%
            'distributed.comm.timeouts.tcp': '30s',
            'distributed.comm.retry.count': 5,
            'distributed.scheduler.allowed-failures': 10,
            'distributed.scheduler.work-stealing': True,
            'array.chunk-size': self.config.chunk_size,
            'array.slicing.split_large_chunks': True
        })
        
        logger.info(f"Dask cluster initialized: {self.client}")
        logger.info(f"Dashboard available at: {self.client.dashboard_link}")
    
    def _start_monitoring(self):
        """Start Prometheus metrics server"""
        prometheus_client.start_http_server(8091)
        logger.info("Prometheus metrics server started on port 8091")
    
    async def create_massive_dataset(self, 
                                   size_gb: float = 100.0, 
                                   chunk_size: str = "100MB",
                                   data_type: str = "synthetic_text") -> da.Array:
        """Create massive synthetic dataset for billion-scale testing"""
        logger.info(f"Creating {size_gb}GB synthetic dataset of type {data_type}")
        
        if data_type == "synthetic_text":
            # Create text-like data for NLP workloads
            vocab_size = 50000
            seq_length = 512
            
            # Calculate total number of sequences needed
            bytes_per_element = 4  # int32
            elements_per_gb = (1024**3) / bytes_per_element
            total_sequences = int(size_gb * elements_per_gb / seq_length)
            
            # Create distributed array
            data = da.random.randint(
                0, vocab_size, 
                size=(total_sequences, seq_length),
                chunks=(1000, seq_length),  # 1000 sequences per chunk
                dtype=np.int32
            )
            
        elif data_type == "image_data":
            # Create image-like data for computer vision
            height, width, channels = 224, 224, 3
            bytes_per_pixel = 1  # uint8
            elements_per_gb = (1024**3) / bytes_per_pixel
            total_images = int(size_gb * elements_per_gb / (height * width * channels))
            
            data = da.random.randint(
                0, 256,
                size=(total_images, height, width, channels),
                chunks=(100, height, width, channels),  # 100 images per chunk
                dtype=np.uint8
            )
            
        elif data_type == "numerical_features":
            # Create numerical feature data for ML
            n_features = 1000
            bytes_per_element = 8  # float64
            elements_per_gb = (1024**3) / bytes_per_element
            n_samples = int(size_gb * elements_per_gb / n_features)
            
            data = da.random.random(
                size=(n_samples, n_features),
                chunks=(10000, n_features),  # 10k samples per chunk
                dtype=np.float64
            )
            
        else:
            raise ValueError(f"Unknown data type: {data_type}")
        
        logger.info(f"Dataset created: shape={data.shape}, chunks={data.chunksize}, dtype={data.dtype}")
        return data
    
    async def distributed_ai_inference(self, 
                                     config: AIWorkloadConfig,
                                     data: da.Array,
                                     model_params: Dict[str, Any]) -> da.Array:
        """Perform distributed AI inference on massive datasets"""
        logger.info(f"Starting distributed inference for workload {config.workload_id}")
        
        start_time = time.time()
        compute_tasks_total.labels(workload_type=config.workload_type, status='started').inc()
        
        # Define inference function
        @delayed
        def batch_inference(data_chunk: np.ndarray, model_params: Dict[str, Any]) -> np.ndarray:
            """Simulate AI model inference on a data chunk"""
            try:
                # Simulate model loading and inference
                batch_size = data_chunk.shape[0]
                
                if config.model_type == "transformer":
                    # Simulate transformer inference
                    hidden_size = model_params.get("hidden_size", 768)
                    vocab_size = model_params.get("vocab_size", 50000)
                    
                    # Simulate embedding lookup
                    embeddings = np.random.random((batch_size, data_chunk.shape[1], hidden_size)).astype(np.float32)
                    
                    # Simulate transformer layers (attention + FFN)
                    for layer in range(model_params.get("num_layers", 12)):
                        # Multi-head attention simulation
                        attention_weights = np.random.random((batch_size, 12, data_chunk.shape[1], data_chunk.shape[1])).astype(np.float32)
                        embeddings = embeddings @ np.random.random((hidden_size, hidden_size)).astype(np.float32)
                        
                        # FFN simulation
                        embeddings = np.maximum(0, embeddings @ np.random.random((hidden_size, hidden_size * 4)).astype(np.float32))
                        embeddings = embeddings @ np.random.random((hidden_size * 4, hidden_size)).astype(np.float32)
                    
                    # Output projection
                    logits = embeddings @ np.random.random((hidden_size, vocab_size)).astype(np.float32)
                    predictions = np.argmax(logits, axis=-1)
                    
                elif config.model_type == "cnn":
                    # Simulate CNN inference for images
                    if len(data_chunk.shape) == 4:  # Batch, Height, Width, Channels
                        # Simulate convolution layers
                        features = data_chunk.astype(np.float32) / 255.0
                        
                        for layer in range(model_params.get("num_layers", 8)):
                            # Simulate convolution + pooling
                            features = np.maximum(0, features)  # ReLU
                            if layer % 2 == 1:  # Pool every other layer
                                features = features[:, ::2, ::2, :]  # Simulated pooling
                        
                        # Global average pooling + classification
                        features = np.mean(features, axis=(1, 2))
                        predictions = np.argmax(features @ np.random.random((features.shape[1], 1000)).astype(np.float32), axis=1)
                    else:
                        predictions = np.random.randint(0, 1000, batch_size)
                        
                elif config.model_type == "linear":
                    # Simulate linear model
                    predictions = data_chunk @ np.random.random((data_chunk.shape[1], 1)).astype(np.float32)
                    predictions = predictions.flatten()
                    
                else:
                    # Generic model simulation
                    predictions = np.random.random(batch_size).astype(np.float32)
                
                # Simulate processing time based on batch size
                processing_time = batch_size * 0.001  # 1ms per sample
                time.sleep(min(processing_time, 1.0))  # Cap at 1 second
                
                return predictions
                
            except Exception as e:
                logger.error(f"Inference error in batch: {e}")
                return np.zeros(data_chunk.shape[0], dtype=np.float32)
        
        # Apply inference to all chunks
        inference_tasks = []
        for chunk in data.to_delayed().flatten():
            task = batch_inference(chunk, model_params)
            inference_tasks.append(task)
        
        # Execute all inference tasks
        logger.info(f"Executing {len(inference_tasks)} inference tasks")
        results = await self._compute_with_monitoring(inference_tasks, config.workload_id)
        
        # Combine results back into distributed array
        result_chunks = []
        for i, result in enumerate(results):
            if isinstance(result, np.ndarray):
                result_chunks.append(da.from_array(result, chunks=(len(result),)))
            else:
                logger.warning(f"Invalid result from chunk {i}: {type(result)}")
                result_chunks.append(da.zeros(data.chunks[0][i % len(data.chunks[0])], dtype=np.float32))
        
        final_result = da.concatenate(result_chunks, axis=0) if result_chunks else da.zeros(data.shape[0], dtype=np.float32)
        
        # Record metrics
        duration = time.time() - start_time
        compute_duration.labels(workload_type=config.workload_type).observe(duration)
        compute_tasks_total.labels(workload_type=config.workload_type, status='completed').inc()
        
        throughput = data.nbytes / duration if duration > 0 else 0
        data_throughput.labels(workload_id=config.workload_id).set(throughput)
        
        logger.info(f"Inference completed in {duration:.2f}s, throughput: {throughput/1024/1024:.2f} MB/s")
        
        return final_result
    
    async def distributed_training(self,
                                 config: AIWorkloadConfig,
                                 train_data: da.Array,
                                 train_labels: da.Array,
                                 model_config: Dict[str, Any]) -> Dict[str, Any]:
        """Perform distributed model training"""
        logger.info(f"Starting distributed training for workload {config.workload_id}")
        
        start_time = time.time()
        compute_tasks_total.labels(workload_type='training', status='started').inc()
        
        @delayed
        def train_model_chunk(X_chunk: np.ndarray, y_chunk: np.ndarray, model_params: Dict[str, Any]) -> Dict[str, Any]:
            """Train model on a data chunk"""
            try:
                # Simulate different training algorithms
                if model_config.get("algorithm") == "xgboost":
                    # Use XGBoost for demonstration
                    import xgboost as xgb
                    
                    # Convert to DMatrix for XGBoost
                    dtrain = xgb.DMatrix(X_chunk, label=y_chunk)
                    
                    # Training parameters
                    params = {
                        'max_depth': model_params.get('max_depth', 6),
                        'learning_rate': model_params.get('learning_rate', 0.1),
                        'objective': model_params.get('objective', 'reg:squarederror'),
                        'eval_metric': 'rmse',
                        'n_jobs': 1  # Single thread per chunk
                    }
                    
                    # Train model
                    num_rounds = model_params.get('num_rounds', 100)
                    model = xgb.train(params, dtrain, num_rounds)
                    
                    # Calculate training metrics
                    predictions = model.predict(dtrain)
                    mse = np.mean((predictions - y_chunk) ** 2)
                    
                    return {
                        'model_data': model.save_raw(),
                        'training_loss': float(mse),
                        'samples_trained': len(X_chunk),
                        'feature_importance': model.get_score(importance_type='gain')
                    }
                    
                else:
                    # Simulate neural network training
                    n_epochs = model_params.get('epochs', 10)
                    learning_rate = model_params.get('learning_rate', 0.001)
                    
                    # Simulate training loop
                    loss_history = []
                    current_loss = 1.0
                    
                    for epoch in range(n_epochs):
                        # Simulate forward/backward pass
                        current_loss *= (1 - learning_rate * np.random.uniform(0.01, 0.1))
                        current_loss += np.random.normal(0, 0.01)  # Add noise
                        loss_history.append(current_loss)
                        
                        # Simulate processing time
                        time.sleep(0.01)
                    
                    return {
                        'training_loss': float(current_loss),
                        'loss_history': loss_history,
                        'samples_trained': len(X_chunk),
                        'convergence_rate': (loss_history[0] - loss_history[-1]) / loss_history[0] if loss_history[0] > 0 else 0
                    }
                    
            except Exception as e:
                logger.error(f"Training error in chunk: {e}")
                return {
                    'training_loss': float('inf'),
                    'samples_trained': len(X_chunk),
                    'error': str(e)
                }
        
        # Create training tasks for each chunk
        training_tasks = []
        for i, (X_chunk, y_chunk) in enumerate(zip(train_data.to_delayed().flatten(), 
                                                   train_labels.to_delayed().flatten())):
            task = train_model_chunk(X_chunk, y_chunk, model_config)
            training_tasks.append(task)
        
        # Execute training tasks
        logger.info(f"Executing {len(training_tasks)} training tasks")
        chunk_results = await self._compute_with_monitoring(training_tasks, config.workload_id)
        
        # Aggregate training results
        total_samples = sum(result.get('samples_trained', 0) for result in chunk_results)
        total_loss = sum(result.get('training_loss', 0) * result.get('samples_trained', 0) 
                        for result in chunk_results)
        avg_loss = total_loss / max(total_samples, 1)
        
        successful_chunks = len([r for r in chunk_results if 'error' not in r])
        
        training_summary = {
            'workload_id': config.workload_id,
            'total_samples_trained': total_samples,
            'average_training_loss': avg_loss,
            'successful_chunks': successful_chunks,
            'total_chunks': len(chunk_results),
            'training_duration': time.time() - start_time,
            'chunk_results': chunk_results
        }
        
        # Record metrics
        duration = time.time() - start_time
        compute_duration.labels(workload_type='training').observe(duration)
        compute_tasks_total.labels(workload_type='training', status='completed').inc()
        
        logger.info(f"Training completed: {total_samples} samples, avg_loss: {avg_loss:.4f}, duration: {duration:.2f}s")
        
        return training_summary
    
    async def massive_data_processing(self,
                                    config: AIWorkloadConfig,
                                    data_sources: List[str],
                                    processing_func: Optional[callable] = None) -> dd.DataFrame:
        """Process massive datasets with Dask DataFrames"""
        logger.info(f"Starting massive data processing for workload {config.workload_id}")
        
        start_time = time.time()
        compute_tasks_total.labels(workload_type='data_processing', status='started').inc()
        
        # Load data from multiple sources
        dfs = []
        for source in data_sources:
            if source.endswith('.parquet'):
                df = dd.read_parquet(source, engine='pyarrow')
            elif source.endswith('.csv'):
                df = dd.read_csv(source, blocksize="64MB")  # 64MB chunks
            elif source.startswith('s3://'):
                df = dd.read_parquet(source, storage_options={'anon': True})
            else:
                # Create synthetic data for demonstration
                logger.info(f"Creating synthetic data for source: {source}")
                n_rows = 10_000_000  # 10M rows
                df = dd.from_pandas(
                    pd.DataFrame({
                        'id': np.arange(n_rows),
                        'feature1': np.random.randn(n_rows),
                        'feature2': np.random.randn(n_rows),
                        'category': np.random.choice(['A', 'B', 'C'], n_rows),
                        'timestamp': pd.date_range('2020-01-01', periods=n_rows, freq='1min'),
                        'target': np.random.randn(n_rows)
                    }), npartitions=100  # 100 partitions
                )
            
            dfs.append(df)
        
        # Combine all DataFrames
        if len(dfs) > 1:
            combined_df = dd.concat(dfs, ignore_index=True)
        else:
            combined_df = dfs[0]
        
        logger.info(f"Combined dataset: {len(combined_df)} rows, {len(combined_df.columns)} columns")
        
        # Apply processing function if provided
        if processing_func:
            processed_df = combined_df.map_partitions(processing_func, meta=combined_df._meta)
        else:
            # Default processing pipeline
            processed_df = combined_df.copy()
            
            # Feature engineering
            processed_df['feature1_squared'] = processed_df['feature1'] ** 2
            processed_df['feature_interaction'] = processed_df['feature1'] * processed_df['feature2']
            
            # Categorical encoding
            processed_df['category_encoded'] = processed_df['category'].map({'A': 0, 'B': 1, 'C': 2})
            
            # Time-based features
            processed_df['hour'] = processed_df['timestamp'].dt.hour
            processed_df['day_of_week'] = processed_df['timestamp'].dt.dayofweek
            
            # Statistical aggregations by category
            category_stats = processed_df.groupby('category').agg({
                'feature1': ['mean', 'std'],
                'feature2': ['mean', 'std'],
                'target': ['mean', 'std']
            })
            
            # Persist category stats for joining
            category_stats = category_stats.persist()
            
            # Join back to main DataFrame
            processed_df = processed_df.merge(category_stats, on='category', how='left')
        
        # Persist the processed DataFrame
        processed_df = processed_df.persist()
        
        # Wait for computation to complete
        await self.client.gather(processed_df.to_delayed())
        
        # Record metrics
        duration = time.time() - start_time
        compute_duration.labels(workload_type='data_processing').observe(duration)
        compute_tasks_total.labels(workload_type='data_processing', status='completed').inc()
        
        total_size = processed_df.map_partitions(lambda df: df.memory_usage(deep=True).sum()).sum().compute()
        throughput = total_size / duration if duration > 0 else 0
        data_throughput.labels(workload_id=config.workload_id).set(throughput)
        
        logger.info(f"Data processing completed in {duration:.2f}s, processed: {total_size/1024/1024:.2f} MB")
        
        return processed_df
    
    async def _compute_with_monitoring(self, tasks: List, workload_id: str):
        """Execute Dask tasks with monitoring and progress tracking"""
        logger.info(f"Computing {len(tasks)} tasks for workload {workload_id}")
        
        # Submit tasks to scheduler
        futures = self.client.compute(tasks, sync=False)
        
        # Monitor progress
        total_tasks = len(futures)
        completed = 0
        failed = 0
        
        # Progress monitoring
        start_time = time.time()
        last_update = start_time
        
        for future in as_completed(futures):
            try:
                result = await future
                completed += 1
                
                # Log progress every 10% or 60 seconds
                now = time.time()
                if (completed % max(1, total_tasks // 10) == 0) or (now - last_update > 60):
                    progress = completed / total_tasks * 100
                    elapsed = now - start_time
                    estimated_total = elapsed * total_tasks / completed if completed > 0 else 0
                    remaining = max(0, estimated_total - elapsed)
                    
                    logger.info(f"Progress: {progress:.1f}% ({completed}/{total_tasks}), "
                              f"elapsed: {elapsed:.1f}s, remaining: {remaining:.1f}s")
                    last_update = now
                
            except Exception as e:
                failed += 1
                logger.error(f"Task failed: {e}")
        
        logger.info(f"All tasks completed: {completed} successful, {failed} failed")
        
        # Collect all results
        results = []
        for future in futures:
            try:
                result = await future
                results.append(result)
            except Exception as e:
                logger.error(f"Failed to collect result: {e}")
                results.append(None)
        
        return results
    
    def get_cluster_status(self) -> Dict[str, Any]:
        """Get comprehensive cluster status"""
        if not self.client:
            return {"status": "not_initialized"}
        
        try:
            # Get scheduler info
            scheduler_info = self.client.scheduler_info()
            
            # Get worker information
            workers = {}
            for worker_id, worker_info in scheduler_info['workers'].items():
                workers[worker_id] = {
                    'host': worker_info.get('host', 'unknown'),
                    'cores': worker_info.get('nthreads', 0),
                    'memory_limit': worker_info.get('memory_limit', 0),
                    'memory_used': worker_info.get('metrics', {}).get('memory', 0),
                    'cpu_usage': worker_info.get('metrics', {}).get('cpu', 0),
                    'tasks': worker_info.get('metrics', {}).get('tasks', 0)
                }
                
                # Update Prometheus metrics
                if 'metrics' in worker_info:
                    cpu_percent = worker_info['metrics'].get('cpu', 0) * 100
                    memory_percent = (worker_info['metrics'].get('memory', 0) / 
                                    max(worker_info.get('memory_limit', 1), 1)) * 100
                    
                    worker_utilization.labels(worker_id=worker_id, resource='cpu').set(cpu_percent)
                    worker_utilization.labels(worker_id=worker_id, resource='memory').set(memory_percent)
            
            # Get task information
            task_stream = self.client.processing()
            
            return {
                'status': 'active',
                'scheduler': {
                    'address': scheduler_info.get('address', 'unknown'),
                    'workers_count': len(scheduler_info.get('workers', {})),
                    'total_cores': sum(w.get('nthreads', 0) for w in scheduler_info.get('workers', {}).values()),
                    'total_memory': sum(w.get('memory_limit', 0) for w in scheduler_info.get('workers', {}).values()),
                },
                'workers': workers,
                'tasks': {
                    'processing': len(task_stream),
                    'ready': len(self.client.ready),
                    'waiting': len(self.client.waiting),
                },
                'dashboard': self.client.dashboard_link,
                'active_workloads': list(self.active_workloads.keys())
            }
            
        except Exception as e:
            logger.error(f"Error getting cluster status: {e}")
            return {"status": "error", "error": str(e)}
    
    async def scale_cluster(self, target_workers: int) -> bool:
        """Scale the cluster to target number of workers"""
        try:
            if hasattr(self.cluster, 'scale'):
                self.cluster.scale(target_workers)
                logger.info(f"Scaling cluster to {target_workers} workers")
                return True
            else:
                logger.warning("Cluster scaling not supported for current configuration")
                return False
        except Exception as e:
            logger.error(f"Error scaling cluster: {e}")
            return False
    
    def shutdown(self):
        """Shutdown the Dask cluster and cleanup resources"""
        logger.info("Shutting down Dask AI Compute")
        
        if self.client:
            self.client.close()
        
        if self.cluster:
            self.cluster.close()
        
        logger.info("Dask cluster shutdown completed")

class DaskOrchestrator:
    """High-level orchestrator for managing multiple Dask AI compute instances"""
    
    def __init__(self):
        self.compute_instances = {}
        self.workload_registry = {}
        
    async def create_compute_instance(self, 
                                    instance_id: str, 
                                    config: ComputeConfig) -> DaskAICompute:
        """Create a new Dask compute instance"""
        logger.info(f"Creating compute instance: {instance_id}")
        
        compute = DaskAICompute(config)
        self.compute_instances[instance_id] = compute
        
        return compute
    
    async def submit_workload(self,
                            instance_id: str,
                            workload_config: AIWorkloadConfig,
                            data_config: Dict[str, Any]) -> str:
        """Submit a workload to a compute instance"""
        if instance_id not in self.compute_instances:
            raise ValueError(f"Compute instance {instance_id} not found")
        
        compute = self.compute_instances[instance_id]
        
        # Register workload
        workload_id = workload_config.workload_id
        self.workload_registry[workload_id] = {
            'config': workload_config,
            'instance_id': instance_id,
            'submitted_at': datetime.now(),
            'status': 'submitted'
        }
        
        # Execute based on workload type
        try:
            if workload_config.workload_type == 'inference':
                # Create or load data
                if 'synthetic' in data_config:
                    data = await compute.create_massive_dataset(
                        size_gb=data_config.get('size_gb', 10),
                        data_type=data_config.get('data_type', 'synthetic_text')
                    )
                
                # Run inference
                result = await compute.distributed_ai_inference(
                    workload_config, 
                    data, 
                    data_config.get('model_params', {})
                )
                
                self.workload_registry[workload_id]['status'] = 'completed'
                self.workload_registry[workload_id]['result'] = 'inference_completed'
                
            elif workload_config.workload_type == 'training':
                # Create training data
                train_data = await compute.create_massive_dataset(
                    size_gb=data_config.get('size_gb', 10),
                    data_type='numerical_features'
                )
                train_labels = da.random.random(train_data.shape[0], chunks=train_data.chunks[0])
                
                # Run training
                result = await compute.distributed_training(
                    workload_config,
                    train_data,
                    train_labels,
                    data_config.get('model_config', {})
                )
                
                self.workload_registry[workload_id]['status'] = 'completed'
                self.workload_registry[workload_id]['result'] = result
                
            elif workload_config.workload_type == 'data_processing':
                # Process data
                result = await compute.massive_data_processing(
                    workload_config,
                    data_config.get('data_sources', ['synthetic_data']),
                    data_config.get('processing_func', None)
                )
                
                self.workload_registry[workload_id]['status'] = 'completed'
                self.workload_registry[workload_id]['result'] = 'data_processing_completed'
                
            else:
                raise ValueError(f"Unknown workload type: {workload_config.workload_type}")
                
        except Exception as e:
            logger.error(f"Workload {workload_id} failed: {e}")
            self.workload_registry[workload_id]['status'] = 'failed'
            self.workload_registry[workload_id]['error'] = str(e)
        
        return workload_id
    
    def get_global_status(self) -> Dict[str, Any]:
        """Get status of all compute instances and workloads"""
        status = {
            'compute_instances': {},
            'workloads': {},
            'summary': {
                'total_instances': len(self.compute_instances),
                'total_workloads': len(self.workload_registry),
                'active_workloads': len([w for w in self.workload_registry.values() if w['status'] == 'running']),
                'completed_workloads': len([w for w in self.workload_registry.values() if w['status'] == 'completed'])
            }
        }
        
        # Get status from each compute instance
        for instance_id, compute in self.compute_instances.items():
            status['compute_instances'][instance_id] = compute.get_cluster_status()
        
        # Get workload statuses
        for workload_id, workload in self.workload_registry.items():
            status['workloads'][workload_id] = {
                'config': workload['config'].__dict__,
                'instance_id': workload['instance_id'],
                'status': workload['status'],
                'submitted_at': workload['submitted_at'].isoformat()
            }
        
        return status
    
    def shutdown_all(self):
        """Shutdown all compute instances"""
        logger.info("Shutting down all compute instances")
        
        for instance_id, compute in self.compute_instances.items():
            logger.info(f"Shutting down instance: {instance_id}")
            compute.shutdown()
        
        self.compute_instances.clear()
        logger.info("All instances shut down")

async def main():
    """Example usage of Dask AI Orchestrator for billion-scale workloads"""
    
    # Initialize orchestrator
    orchestrator = DaskOrchestrator()
    
    try:
        # Create compute instance
        compute_config = ComputeConfig(
            cluster_type="local",
            n_workers=8,
            threads_per_worker=2,
            memory_per_worker="2GB",
            chunk_size="64MB"
        )
        
        instance_id = "test-cluster-001"
        compute = await orchestrator.create_compute_instance(instance_id, compute_config)
        
        # Wait for initialization
        await asyncio.sleep(5)
        
        # Test inference workload
        inference_config = AIWorkloadConfig(
            workload_id="inference-test-001",
            workload_type="inference",
            model_type="transformer",
            batch_size=64
        )
        
        inference_data_config = {
            'synthetic': True,
            'size_gb': 1.0,  # 1GB for testing
            'data_type': 'synthetic_text',
            'model_params': {
                'hidden_size': 768,
                'num_layers': 12,
                'vocab_size': 50000
            }
        }
        
        # Submit inference workload
        workload_id = await orchestrator.submit_workload(
            instance_id, inference_config, inference_data_config
        )
        
        # Monitor progress
        for i in range(10):
            await asyncio.sleep(10)
            status = orchestrator.get_global_status()
            print(f"Iteration {i+1}: {status['summary']['active_workloads']} active workloads")
            
            # Check if workload completed
            if workload_id in status['workloads']:
                workload_status = status['workloads'][workload_id]['status']
                print(f"Workload {workload_id} status: {workload_status}")
                if workload_status in ['completed', 'failed']:
                    break
        
        # Test training workload
        training_config = AIWorkloadConfig(
            workload_id="training-test-001",
            workload_type="training",
            model_type="xgboost",
            batch_size=1000
        )
        
        training_data_config = {
            'size_gb': 0.5,
            'model_config': {
                'algorithm': 'xgboost',
                'max_depth': 6,
                'learning_rate': 0.1,
                'num_rounds': 100
            }
        }
        
        # Submit training workload
        training_workload_id = await orchestrator.submit_workload(
            instance_id, training_config, training_data_config
        )
        
        # Wait for completion
        await asyncio.sleep(30)
        
        # Final status
        final_status = orchestrator.get_global_status()
        print(f"\nFinal Status:")
        print(f"Total instances: {final_status['summary']['total_instances']}")
        print(f"Total workloads: {final_status['summary']['total_workloads']}")
        print(f"Completed workloads: {final_status['summary']['completed_workloads']}")
        
        # Print cluster status
        if instance_id in final_status['compute_instances']:
            cluster_status = final_status['compute_instances'][instance_id]
            print(f"Cluster workers: {cluster_status.get('scheduler', {}).get('workers_count', 0)}")
            print(f"Dashboard: {cluster_status.get('dashboard', 'N/A')}")
        
    except Exception as e:
        logger.error(f"Error in main execution: {e}")
    finally:
        orchestrator.shutdown_all()

if __name__ == "__main__":
    asyncio.run(main())