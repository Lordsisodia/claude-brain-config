"""
Kubernetes Operator for Massive AI Agent Orchestration
Custom operator to manage 10,000+ AI agents across distributed Kubernetes clusters
Based on modern Kubernetes patterns for scalable AI workloads
"""

import kopf
import kubernetes
import asyncio
import yaml
import logging
import json
import time
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from kubernetes import client, config
from kubernetes.client.rest import ApiException
from concurrent.futures import ThreadPoolExecutor
import threading

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class AIAgentSpec:
    """Specification for an AI agent deployment"""
    name: str
    replicas: int
    image: str
    resources: Dict[str, Any]
    model_config: Dict[str, Any]
    scaling_policy: Dict[str, Any]

@dataclass
class SwarmStatus:
    """Status of the AI agent swarm"""
    total_agents: int
    healthy_agents: int
    failed_agents: int
    processing_tasks: int
    completed_tasks: int
    last_update: str

class MassiveAISwarmOperator:
    """Kubernetes operator for managing massive AI agent swarms"""
    
    def __init__(self):
        self.k8s_client = None
        self.apps_v1 = None
        self.core_v1 = None
        self.custom_objects_api = None
        self.executor = ThreadPoolExecutor(max_workers=50)
        
        # Initialize Kubernetes client
        self._initialize_k8s_client()
        
        # Create Custom Resource Definitions
        self._create_crd_definitions()
    
    def _initialize_k8s_client(self):
        """Initialize Kubernetes client"""
        try:
            # Try to load in-cluster config first
            config.load_incluster_config()
            logger.info("Loaded in-cluster Kubernetes configuration")
        except:
            try:
                # Fall back to local kubeconfig
                config.load_kube_config()
                logger.info("Loaded local Kubernetes configuration")
            except:
                logger.error("Could not load Kubernetes configuration")
                raise
        
        self.k8s_client = client.ApiClient()
        self.apps_v1 = client.AppsV1Api()
        self.core_v1 = client.CoreV1Api()
        self.custom_objects_api = client.CustomObjectsApi()
        self.hpa_v1 = client.AutoscalingV1Api()
    
    def _create_crd_definitions(self):
        """Create Custom Resource Definitions for AI agents"""
        
        # AI Agent Swarm CRD
        swarm_crd = {
            "apiVersion": "apiextensions.k8s.io/v1",
            "kind": "CustomResourceDefinition",
            "metadata": {
                "name": "aiswarms.ai.massive.io"
            },
            "spec": {
                "group": "ai.massive.io",
                "versions": [{
                    "name": "v1",
                    "served": True,
                    "storage": True,
                    "schema": {
                        "openAPIV3Schema": {
                            "type": "object",
                            "properties": {
                                "spec": {
                                    "type": "object",
                                    "properties": {
                                        "agents": {"type": "array"},
                                        "totalAgents": {"type": "integer"},
                                        "scalingPolicy": {"type": "object"},
                                        "workflowStages": {"type": "array"}
                                    }
                                },
                                "status": {
                                    "type": "object",
                                    "properties": {
                                        "healthyAgents": {"type": "integer"},
                                        "failedAgents": {"type": "integer"},
                                        "processingTasks": {"type": "integer"}
                                    }
                                }
                            }
                        }
                    }
                }],
                "scope": "Namespaced",
                "names": {
                    "plural": "aiswarms",
                    "singular": "aiswarm",
                    "kind": "AISwarm"
                }
            }
        }
        
        try:
            api_extensions = client.ApiextensionsV1Api()
            api_extensions.create_custom_resource_definition(swarm_crd)
            logger.info("Created AISwarm CRD")
        except ApiException as e:
            if e.status == 409:  # Already exists
                logger.info("AISwarm CRD already exists")
            else:
                logger.error(f"Error creating CRD: {e}")

    def create_ai_agent_deployment(self, agent_spec: AIAgentSpec, namespace: str = "default") -> str:
        """Create Kubernetes deployment for AI agents"""
        
        deployment = client.V1Deployment(
            api_version="apps/v1",
            kind="Deployment",
            metadata=client.V1ObjectMeta(
                name=agent_spec.name,
                namespace=namespace,
                labels={
                    "app": agent_spec.name,
                    "component": "ai-agent",
                    "managed-by": "massive-ai-operator"
                }
            ),
            spec=client.V1DeploymentSpec(
                replicas=agent_spec.replicas,
                selector=client.V1LabelSelector(
                    match_labels={"app": agent_spec.name}
                ),
                template=client.V1PodTemplateSpec(
                    metadata=client.V1ObjectMeta(
                        labels={
                            "app": agent_spec.name,
                            "component": "ai-agent"
                        }
                    ),
                    spec=client.V1PodSpec(
                        containers=[
                            client.V1Container(
                                name="ai-agent",
                                image=agent_spec.image,
                                resources=client.V1ResourceRequirements(
                                    requests=agent_spec.resources.get("requests", {}),
                                    limits=agent_spec.resources.get("limits", {})
                                ),
                                env=[
                                    client.V1EnvVar(name="AGENT_ID", value=agent_spec.name),
                                    client.V1EnvVar(name="MODEL_CONFIG", value=json.dumps(agent_spec.model_config)),
                                    client.V1EnvVar(name="SCALING_POLICY", value=json.dumps(agent_spec.scaling_policy))
                                ],
                                ports=[
                                    client.V1ContainerPort(container_port=8080, name="http"),
                                    client.V1ContainerPort(container_port=9090, name="metrics")
                                ],
                                liveness_probe=client.V1Probe(
                                    http_get=client.V1HTTPGetAction(
                                        path="/health",
                                        port=8080
                                    ),
                                    initial_delay_seconds=30,
                                    period_seconds=10
                                ),
                                readiness_probe=client.V1Probe(
                                    http_get=client.V1HTTPGetAction(
                                        path="/ready",
                                        port=8080
                                    ),
                                    initial_delay_seconds=10,
                                    period_seconds=5
                                )
                            )
                        ],
                        restart_policy="Always"
                    )
                ),
                strategy=client.V1DeploymentStrategy(
                    type="RollingUpdate",
                    rolling_update=client.V1RollingUpdateDeployment(
                        max_unavailable="25%",
                        max_surge="25%"
                    )
                )
            )
        )
        
        try:
            response = self.apps_v1.create_namespaced_deployment(
                namespace=namespace,
                body=deployment
            )
            logger.info(f"Created deployment {agent_spec.name} with {agent_spec.replicas} replicas")
            return response.metadata.name
            
        except ApiException as e:
            logger.error(f"Error creating deployment {agent_spec.name}: {e}")
            raise

    def create_horizontal_pod_autoscaler(self, deployment_name: str, namespace: str = "default",
                                       min_replicas: int = 1, max_replicas: int = 1000,
                                       target_cpu: int = 70) -> str:
        """Create HPA for automatic scaling based on metrics"""
        
        hpa = client.V1HorizontalPodAutoscaler(
            api_version="autoscaling/v1",
            kind="HorizontalPodAutoscaler",
            metadata=client.V1ObjectMeta(
                name=f"{deployment_name}-hpa",
                namespace=namespace
            ),
            spec=client.V1HorizontalPodAutoscalerSpec(
                scale_target_ref=client.V1CrossVersionObjectReference(
                    api_version="apps/v1",
                    kind="Deployment",
                    name=deployment_name
                ),
                min_replicas=min_replicas,
                max_replicas=max_replicas,
                target_cpu_utilization_percentage=target_cpu
            )
        )
        
        try:
            response = self.hpa_v1.create_namespaced_horizontal_pod_autoscaler(
                namespace=namespace,
                body=hpa
            )
            logger.info(f"Created HPA for {deployment_name}: {min_replicas}-{max_replicas} replicas")
            return response.metadata.name
            
        except ApiException as e:
            logger.error(f"Error creating HPA for {deployment_name}: {e}")
            raise

    def create_service(self, deployment_name: str, namespace: str = "default") -> str:
        """Create Kubernetes service for AI agent deployment"""
        
        service = client.V1Service(
            api_version="v1",
            kind="Service",
            metadata=client.V1ObjectMeta(
                name=f"{deployment_name}-service",
                namespace=namespace,
                labels={
                    "app": deployment_name,
                    "component": "ai-agent-service"
                }
            ),
            spec=client.V1ServiceSpec(
                selector={"app": deployment_name},
                ports=[
                    client.V1ServicePort(
                        name="http",
                        port=80,
                        target_port=8080,
                        protocol="TCP"
                    ),
                    client.V1ServicePort(
                        name="metrics",
                        port=9090,
                        target_port=9090,
                        protocol="TCP"
                    )
                ],
                type="ClusterIP"
            )
        )
        
        try:
            response = self.core_v1.create_namespaced_service(
                namespace=namespace,
                body=service
            )
            logger.info(f"Created service for {deployment_name}")
            return response.metadata.name
            
        except ApiException as e:
            logger.error(f"Error creating service for {deployment_name}: {e}")
            raise

    def deploy_massive_swarm(self, total_agents: int = 10000, namespace: str = "default") -> Dict[str, Any]:
        """Deploy massive AI agent swarm across Kubernetes cluster"""
        
        logger.info(f"Deploying massive swarm: {total_agents} agents")
        
        # Calculate deployment strategy
        agents_per_deployment = 200  # Reasonable pod count per deployment
        num_deployments = (total_agents + agents_per_deployment - 1) // agents_per_deployment
        
        deployment_results = []
        
        # Create agent groups with different specializations
        agent_groups = [
            {
                "name": "data-processors",
                "count": num_deployments // 4,
                "image": "ai-registry/data-processor:latest",
                "resources": {
                    "requests": {"cpu": "0.5", "memory": "1Gi"},
                    "limits": {"cpu": "2", "memory": "4Gi"}
                },
                "model_config": {"type": "data_processing", "batch_size": 64}
            },
            {
                "name": "feature-extractors", 
                "count": num_deployments // 4,
                "image": "ai-registry/feature-extractor:latest",
                "resources": {
                    "requests": {"cpu": "1", "memory": "2Gi", "nvidia.com/gpu": "0.25"},
                    "limits": {"cpu": "4", "memory": "8Gi", "nvidia.com/gpu": "1"}
                },
                "model_config": {"type": "feature_extraction", "model_size": "large"}
            },
            {
                "name": "model-trainers",
                "count": num_deployments // 4,
                "image": "ai-registry/model-trainer:latest", 
                "resources": {
                    "requests": {"cpu": "2", "memory": "4Gi", "nvidia.com/gpu": "0.5"},
                    "limits": {"cpu": "8", "memory": "16Gi", "nvidia.com/gpu": "2"}
                },
                "model_config": {"type": "model_training", "distributed": True}
            },
            {
                "name": "inference-engines",
                "count": num_deployments - (3 * (num_deployments // 4)),
                "image": "ai-registry/inference-engine:latest",
                "resources": {
                    "requests": {"cpu": "0.5", "memory": "1Gi", "nvidia.com/gpu": "0.1"},
                    "limits": {"cpu": "2", "memory": "4Gi", "nvidia.com/gpu": "0.5"}
                },
                "model_config": {"type": "inference", "batch_size": 32, "max_seq_length": 512}
            }
        ]
        
        # Deploy each agent group
        for group in agent_groups:
            for i in range(group["count"]):
                deployment_name = f"{group['name']}-{i:03d}"
                
                agent_spec = AIAgentSpec(
                    name=deployment_name,
                    replicas=agents_per_deployment,
                    image=group["image"],
                    resources=group["resources"],
                    model_config=group["model_config"],
                    scaling_policy={
                        "min_replicas": 1,
                        "max_replicas": agents_per_deployment * 2,
                        "target_cpu": 70,
                        "scale_up_stabilization": 60,
                        "scale_down_stabilization": 300
                    }
                )
                
                try:
                    # Create deployment
                    deployment_name = self.create_ai_agent_deployment(agent_spec, namespace)
                    
                    # Create service
                    service_name = self.create_service(deployment_name, namespace)
                    
                    # Create HPA for auto-scaling
                    hpa_name = self.create_horizontal_pod_autoscaler(
                        deployment_name, 
                        namespace,
                        min_replicas=agent_spec.scaling_policy["min_replicas"],
                        max_replicas=agent_spec.scaling_policy["max_replicas"],
                        target_cpu=agent_spec.scaling_policy["target_cpu"]
                    )
                    
                    deployment_results.append({
                        "deployment": deployment_name,
                        "service": service_name,
                        "hpa": hpa_name,
                        "replicas": agent_spec.replicas,
                        "group": group["name"]
                    })
                    
                except Exception as e:
                    logger.error(f"Failed to deploy {deployment_name}: {e}")
        
        # Create AI Swarm custom resource
        swarm_cr = self._create_swarm_custom_resource(deployment_results, total_agents, namespace)
        
        logger.info(f"Massive swarm deployment completed: {len(deployment_results)} deployments")
        
        return {
            "total_deployments": len(deployment_results),
            "total_agents": total_agents,
            "deployments": deployment_results,
            "swarm_resource": swarm_cr,
            "namespace": namespace
        }

    def _create_swarm_custom_resource(self, deployments: List[Dict], total_agents: int, namespace: str) -> str:
        """Create custom resource to track swarm state"""
        
        swarm_spec = {
            "apiVersion": "ai.massive.io/v1",
            "kind": "AISwarm",
            "metadata": {
                "name": "massive-ai-swarm",
                "namespace": namespace
            },
            "spec": {
                "totalAgents": total_agents,
                "deployments": deployments,
                "scalingPolicy": {
                    "autoScale": True,
                    "maxAgents": total_agents * 2,
                    "scaleMetrics": ["cpu", "memory", "task_queue_length"]
                },
                "workflowStages": [
                    {"name": "data_processing", "parallelism": total_agents // 4},
                    {"name": "feature_extraction", "parallelism": total_agents // 4},
                    {"name": "model_training", "parallelism": total_agents // 4},
                    {"name": "inference", "parallelism": total_agents // 4}
                ]
            },
            "status": {
                "healthyAgents": 0,
                "failedAgents": 0,
                "processingTasks": 0,
                "lastUpdate": time.strftime("%Y-%m-%dT%H:%M:%SZ")
            }
        }
        
        try:
            response = self.custom_objects_api.create_namespaced_custom_object(
                group="ai.massive.io",
                version="v1",
                namespace=namespace,
                plural="aiswarms",
                body=swarm_spec
            )
            logger.info("Created AISwarm custom resource")
            return response["metadata"]["name"]
            
        except ApiException as e:
            logger.error(f"Error creating AISwarm custom resource: {e}")
            raise

    async def monitor_swarm_health(self, namespace: str = "default", duration_seconds: int = 300):
        """Monitor health of the entire AI agent swarm"""
        
        logger.info(f"Starting swarm health monitoring for {duration_seconds} seconds")
        
        start_time = time.time()
        while time.time() - start_time < duration_seconds:
            try:
                # Get all deployments with AI agent labels
                deployments = self.apps_v1.list_namespaced_deployment(
                    namespace=namespace,
                    label_selector="managed-by=massive-ai-operator"
                )
                
                total_replicas = 0
                ready_replicas = 0
                unavailable_replicas = 0
                
                for deployment in deployments.items:
                    status = deployment.status
                    total_replicas += status.replicas or 0
                    ready_replicas += status.ready_replicas or 0
                    unavailable_replicas += status.unavailable_replicas or 0
                
                # Get pod statistics
                pods = self.core_v1.list_namespaced_pod(
                    namespace=namespace,
                    label_selector="component=ai-agent"
                )
                
                running_pods = sum(1 for pod in pods.items if pod.status.phase == "Running")
                failed_pods = sum(1 for pod in pods.items if pod.status.phase == "Failed")
                pending_pods = sum(1 for pod in pods.items if pod.status.phase == "Pending")
                
                # Update swarm status
                await self._update_swarm_status(
                    namespace, 
                    healthy_agents=ready_replicas,
                    failed_agents=unavailable_replicas,
                    running_pods=running_pods,
                    failed_pods=failed_pods,
                    pending_pods=pending_pods
                )
                
                logger.info(f"Swarm Health - Deployments: {len(deployments.items)}, "
                          f"Total Agents: {total_replicas}, Ready: {ready_replicas}, "
                          f"Failed: {unavailable_replicas}, Running Pods: {running_pods}")
                
            except Exception as e:
                logger.error(f"Error monitoring swarm health: {e}")
            
            await asyncio.sleep(30)  # Monitor every 30 seconds

    async def _update_swarm_status(self, namespace: str, **status_updates):
        """Update AI Swarm custom resource status"""
        try:
            # Get current swarm resource
            swarm = self.custom_objects_api.get_namespaced_custom_object(
                group="ai.massive.io",
                version="v1",
                namespace=namespace,
                plural="aiswarms",
                name="massive-ai-swarm"
            )
            
            # Update status
            swarm["status"].update(status_updates)
            swarm["status"]["lastUpdate"] = time.strftime("%Y-%m-%dT%H:%M:%SZ")
            
            # Patch the resource
            self.custom_objects_api.patch_namespaced_custom_object(
                group="ai.massive.io",
                version="v1",
                namespace=namespace,
                plural="aiswarms",
                name="massive-ai-swarm",
                body=swarm
            )
            
        except ApiException as e:
            logger.error(f"Error updating swarm status: {e}")

    def scale_swarm(self, namespace: str, target_agents: int):
        """Dynamically scale the entire swarm"""
        logger.info(f"Scaling swarm to {target_agents} agents")
        
        try:
            # Get all deployments
            deployments = self.apps_v1.list_namespaced_deployment(
                namespace=namespace,
                label_selector="managed-by=massive-ai-operator"
            )
            
            agents_per_deployment = target_agents // len(deployments.items)
            remainder = target_agents % len(deployments.items)
            
            # Scale each deployment
            for i, deployment in enumerate(deployments.items):
                # Distribute remainder across first few deployments
                new_replicas = agents_per_deployment + (1 if i < remainder else 0)
                
                # Update deployment replicas
                deployment.spec.replicas = new_replicas
                
                self.apps_v1.patch_namespaced_deployment(
                    name=deployment.metadata.name,
                    namespace=namespace,
                    body=deployment
                )
                
                logger.info(f"Scaled {deployment.metadata.name} to {new_replicas} replicas")
            
        except ApiException as e:
            logger.error(f"Error scaling swarm: {e}")

    def cleanup_swarm(self, namespace: str = "default"):
        """Clean up all swarm resources"""
        logger.info("Cleaning up AI agent swarm")
        
        try:
            # Delete all deployments
            deployments = self.apps_v1.list_namespaced_deployment(
                namespace=namespace,
                label_selector="managed-by=massive-ai-operator"
            )
            
            for deployment in deployments.items:
                self.apps_v1.delete_namespaced_deployment(
                    name=deployment.metadata.name,
                    namespace=namespace
                )
                logger.info(f"Deleted deployment {deployment.metadata.name}")
            
            # Delete all services
            services = self.core_v1.list_namespaced_service(
                namespace=namespace,
                label_selector="component=ai-agent-service"
            )
            
            for service in services.items:
                self.core_v1.delete_namespaced_service(
                    name=service.metadata.name,
                    namespace=namespace
                )
                logger.info(f"Deleted service {service.metadata.name}")
            
            # Delete all HPAs
            hpas = self.hpa_v1.list_namespaced_horizontal_pod_autoscaler(namespace=namespace)
            for hpa in hpas.items:
                if "ai-agent" in hpa.metadata.name:
                    self.hpa_v1.delete_namespaced_horizontal_pod_autoscaler(
                        name=hpa.metadata.name,
                        namespace=namespace
                    )
                    logger.info(f"Deleted HPA {hpa.metadata.name}")
            
            # Delete swarm custom resource
            try:
                self.custom_objects_api.delete_namespaced_custom_object(
                    group="ai.massive.io",
                    version="v1",
                    namespace=namespace,
                    plural="aiswarms",
                    name="massive-ai-swarm"
                )
                logger.info("Deleted AISwarm custom resource")
            except ApiException:
                pass  # May not exist
            
            logger.info("Swarm cleanup completed")
            
        except ApiException as e:
            logger.error(f"Error during cleanup: {e}")

# Kopf operator event handlers (for production deployment)
@kopf.on.create('ai.massive.io', 'v1', 'aiswarms')
async def create_ai_swarm(spec, name, namespace, **kwargs):
    """Handle AISwarm resource creation"""
    logger.info(f"Creating AI swarm {name} in namespace {namespace}")
    
    operator = MassiveAISwarmOperator()
    total_agents = spec.get('totalAgents', 1000)
    
    result = operator.deploy_massive_swarm(total_agents, namespace)
    
    return {'message': f'AI swarm created with {result["total_agents"]} agents'}

@kopf.on.update('ai.massive.io', 'v1', 'aiswarms')
async def update_ai_swarm(spec, name, namespace, **kwargs):
    """Handle AISwarm resource updates"""
    logger.info(f"Updating AI swarm {name}")
    
    operator = MassiveAISwarmOperator()
    total_agents = spec.get('totalAgents', 1000)
    
    operator.scale_swarm(namespace, total_agents)
    
    return {'message': f'AI swarm updated to {total_agents} agents'}

@kopf.on.delete('ai.massive.io', 'v1', 'aiswarms')
async def delete_ai_swarm(name, namespace, **kwargs):
    """Handle AISwarm resource deletion"""
    logger.info(f"Deleting AI swarm {name}")
    
    operator = MassiveAISwarmOperator()
    operator.cleanup_swarm(namespace)
    
    return {'message': 'AI swarm deleted successfully'}

# Example usage
async def main():
    """Main execution function for testing"""
    
    operator = MassiveAISwarmOperator()
    
    try:
        # Deploy massive swarm (10,000 agents)
        logger.info("Deploying massive AI agent swarm...")
        result = operator.deploy_massive_swarm(total_agents=10000, namespace="ai-swarm")
        
        logger.info(f"Deployment completed: {result['total_deployments']} deployments")
        logger.info(f"Total agents: {result['total_agents']}")
        
        # Monitor swarm for 10 minutes
        await operator.monitor_swarm_health(namespace="ai-swarm", duration_seconds=600)
        
        # Test scaling
        logger.info("Testing swarm scaling...")
        operator.scale_swarm("ai-swarm", 15000)
        
        # Monitor after scaling
        await operator.monitor_swarm_health(namespace="ai-swarm", duration_seconds=300)
        
    except KeyboardInterrupt:
        logger.info("Shutdown requested...")
    except Exception as e:
        logger.error(f"Error in main execution: {e}")
    finally:
        # Clean up resources
        operator.cleanup_swarm("ai-swarm")

if __name__ == "__main__":
    asyncio.run(main())