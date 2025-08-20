# Quantum Optimization Engine Integration Guide

## 🚀 Quick Start Integration

### 1. Basic Agent Team Optimization

```python
from quantum_agent_optimizers import QuantumAgentCompositionOptimizer, Agent, Task

# Define your agents
agents = [
    Agent("claude_premium", "reasoning", 0.95, 0.85, 0.002, 0.95, 0.2, ["reasoning", "analysis"]),
    Agent("cerebras_ultra", "architecture", 0.90, 0.95, 0.001, 0.90, 0.25, ["architecture", "system_design"]),
    # ... add more agents
]

# Define your optimization task
task = Task(
    name="complex_ai_system",
    complexity=0.9,
    estimated_tokens=10000,
    required_expertise=["reasoning", "architecture", "security"],
    priority=0.95,
    quality_requirements=0.85
)

# Run quantum optimization
optimizer = QuantumAgentCompositionOptimizer(agents)
result = await optimizer.optimize_team_composition(task, {'max_team_size': 5})

print(f"Optimal team: {result['best_team']['agent_names']}")
print(f"Quality: {result['performance_metrics']['team_quality']:.3f}")
```

### 2. Hybrid Classical-Quantum Optimization

```python
from hybrid_quantum_integration import HybridClassicalQuantumOptimizer
from quantum_agent_optimizers import Resource

# Define resources
resources = [
    Resource("cpu_cluster", 1000.0, 200.0, 0.01, "cpu"),
    Resource("gpu_farm", 500.0, 100.0, 0.05, "gpu"),
    # ... add more resources
]

# Initialize hybrid optimizer
hybrid_optimizer = HybridClassicalQuantumOptimizer(agents, resources)

# Run hybrid optimization
result = await hybrid_optimizer.hybrid_agent_team_optimization(task)

print(f"Classical time: {result.classical_time:.3f}s")
print(f"Quantum time: {result.quantum_time:.3f}s")
print(f"Improvement: {result.improvement_over_classical*100:.1f}%")
```

### 3. Multi-Objective Optimization

```python
from quantum_scheduling_optimizer import QuantumMultiObjectiveOptimizer, MultiObjective

# Define objectives
objectives = [
    MultiObjective("cost", 0.3, minimize=True),
    MultiObjective("quality", 0.4, minimize=False),
    MultiObjective("speed", 0.3, minimize=False)
]

# Solution generator (customize for your domain)
def solution_generator():
    return {
        'cost': np.random.uniform(0.001, 0.01),
        'quality': np.random.uniform(0.7, 1.0),
        'speed': np.random.uniform(0.6, 1.0)
    }

# Run multi-objective optimization
optimizer = QuantumMultiObjectiveOptimizer()
result = optimizer.quantum_pareto_optimization(objectives, solution_generator, 500)

print(f"Pareto solutions found: {result['pareto_solutions']}")
print(f"Best compromise: {result['best_compromise_solution']['composite_fitness']:.3f}")
```

## 🔧 Advanced Configuration

### Quantum Algorithm Parameters

```python
# Quantum Annealing Configuration
from quantum_optimization_engine import QuantumInspiredAnnealing

annealer = QuantumInspiredAnnealing(
    initial_temperature=1000.0,    # Starting temperature
    cooling_rate=0.95,             # Temperature reduction rate
    quantum_tunneling_rate=0.15    # Quantum tunneling probability
)

# Quantum Evolution Configuration
from quantum_optimization_engine import QuantumEvolutionaryAlgorithm

evolution = QuantumEvolutionaryAlgorithm(
    population_size=100,           # Population size
    mutation_rate=0.1,             # Mutation probability
    crossover_rate=0.8,            # Crossover probability
    quantum_superposition_factor=0.3  # Quantum effects strength
)
```

### Performance Tuning

```python
# For high-performance scenarios
constraints = {
    'max_team_size': 8,           # Larger teams for complex tasks
    'min_quality': 0.9,           # Higher quality requirements
    'max_cost': 0.05,             # Cost constraints
    'timeout': 60.0               # Maximum optimization time
}

# For real-time scenarios  
constraints = {
    'max_team_size': 4,           # Smaller teams for speed
    'min_quality': 0.8,           # Balanced quality
    'timeout': 5.0                # Fast optimization
}
```

## 🔗 Integration with Existing Systems

### ML Routing System Integration

```python
# If you have the ML routing system available
try:
    from ml_predictive_routing_system import MLPredictiveRoutingSystem
    
    ml_routing = MLPredictiveRoutingSystem()
    hybrid_optimizer = HybridClassicalQuantumOptimizer(agents, resources)
    hybrid_optimizer.ml_routing_system = ml_routing
    
    print("✅ ML routing integration enabled")
except ImportError:
    print("⚠️  ML routing not available, using quantum-only optimization")
```

### Custom Objective Functions

```python
def custom_fitness_function(team_indices, task):
    """Define your own fitness evaluation"""
    # Your custom logic here
    quality_score = calculate_team_quality(team_indices, task)
    cost_score = calculate_team_cost(team_indices, task)
    efficiency_score = calculate_efficiency(team_indices, task)
    
    # Return fitness (lower is better for minimization)
    return -(quality_score * 0.5 + efficiency_score * 0.3 + (1.0/cost_score) * 0.2)

# Use in optimization
optimizer.evaluate_team_composition = custom_fitness_function
```

## 📊 Performance Monitoring

### Real-time Metrics

```python
# Enable performance tracking
optimizer.enable_monitoring = True

# Get performance metrics
metrics = optimizer.get_performance_metrics()
print(f"Average optimization time: {metrics['avg_time']:.3f}s")
print(f"Success rate: {metrics['success_rate']:.1%}")
print(f"Quality improvement: {metrics['quality_improvement']:.1%}")
```

### Adaptive Optimization

```python
# Enable adaptive parameter tuning
hybrid_optimizer.enable_adaptive_tuning = True

# The system will automatically adjust parameters based on performance
adaptive_weight = hybrid_optimizer.adaptive_hybrid_weight_tuning(
    problem_history, performance_threshold=0.05
)
print(f"Recommended hybrid weight: {adaptive_weight:.3f}")
```

## 🛡️ Error Handling & Fallbacks

### Graceful Degradation

```python
try:
    # Try quantum optimization
    result = await optimizer.optimize_team_composition(task)
except Exception as e:
    print(f"Quantum optimization failed: {e}")
    
    # Fallback to classical heuristic
    result = optimizer._classical_team_heuristic(task, constraints)
    print("Using classical fallback")
```

### Resource Management

```python
# Memory and computation limits
quantum_config = {
    'max_state_space_size': 1024,    # Limit quantum state size
    'max_iterations': 5000,          # Limit optimization iterations
    'max_evaluations': 10000,        # Limit function evaluations
    'timeout': 30.0                  # Overall timeout
}
```

## 🧪 Testing & Validation

### Unit Testing

```python
# Run comprehensive test suite
from quantum_optimization_test_suite import QuantumOptimizationTestSuite

test_suite = QuantumOptimizationTestSuite()
result = await test_suite.run_comprehensive_test_suite()

print(f"Tests passed: {result.passed_tests}/{result.total_tests}")
print(f"Success rate: {result.success_rate:.1%}")
```

### Benchmarking

```python
# Compare against classical methods
from quantum_performance_benchmarks import QuantumOptimizationBenchmarker

benchmarker = QuantumOptimizationBenchmarker()
suite_result = await benchmarker.run_comprehensive_benchmark(num_runs=3)

print(f"Quantum vs Classical speedup:")
for algo, speedup in suite_result.quantum_vs_classical_speedup.items():
    print(f"  {algo}: {speedup:.2f}x")
```

## 📈 Scaling Guidelines

### Small Scale (< 10 agents)
- Use basic quantum evolution with 50 population size
- Optimize for speed with 100 max generations
- Enable all quantum effects

### Medium Scale (10-20 agents)  
- Use hybrid optimization for best performance
- Increase population size to 100
- Enable adaptive parameter tuning

### Large Scale (20+ agents)
- Use quantum superposition search
- Limit state space size for memory efficiency
- Enable parallel processing where possible

## 🔧 Production Deployment

### Dependencies

```bash
# Core requirements
pip install numpy

# Enhanced features (optional)
pip install scipy matplotlib tensorflow scikit-learn
```

### Environment Variables

```bash
export QUANTUM_OPTIMIZATION_LOG_LEVEL=INFO
export QUANTUM_MAX_AGENTS=50
export QUANTUM_MAX_RESOURCES=20
export QUANTUM_ENABLE_BENCHMARKING=false
```

### Docker Deployment

```dockerfile
FROM python:3.9-slim

RUN pip install numpy scipy matplotlib

COPY quantum_*.py ./
COPY your_integration.py ./

CMD ["python", "your_integration.py"]
```

## 🎯 Best Practices

### 1. **Problem Size Management**
- For >30 agents, use hierarchical optimization
- For complex constraints, use quantum annealing
- For real-time needs, use hybrid optimization with classical warm-start

### 2. **Parameter Tuning**
- Start with default parameters
- Use adaptive tuning for production
- Monitor performance and adjust based on metrics

### 3. **Error Handling**
- Always implement classical fallbacks
- Set reasonable timeouts
- Log optimization attempts for analysis

### 4. **Performance Optimization**
- Cache agent and resource profiles
- Use parallel evaluation when possible
- Monitor memory usage for large problems

---

## 🚀 Ready for Revolutionary AI Coordination!

This quantum-inspired optimization engine provides exponential improvements in multi-agent coordination. Start with basic integration and gradually enable advanced features as needed.

**For support and advanced configurations, refer to the comprehensive test suite and demo applications.**