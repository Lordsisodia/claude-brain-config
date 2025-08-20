#!/usr/bin/env python3
"""
ML ROUTING VALIDATION FRAMEWORK
Comprehensive testing and validation for ML-based predictive routing system
"""

import asyncio
import json
import numpy as np
import time
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
import logging
from pathlib import Path

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ValidationResult:
    """Result of a validation test"""
    test_name: str
    passed: bool
    score: float
    details: Dict[str, Any]
    execution_time: float
    error_message: Optional[str] = None

@dataclass
class PerformanceMetric:
    """Performance metric for ML system"""
    metric_name: str
    value: float
    target_value: float
    tolerance: float
    passed: bool
    
class MLRoutingValidator:
    """Comprehensive validation framework for ML routing system"""
    
    def __init__(self, ml_routing_system):
        self.ml_system = ml_routing_system
        self.validation_results = []
        self.performance_metrics = []
        self.test_data_generator = TestDataGenerator()
        
        # Validation thresholds
        self.thresholds = {
            'prediction_time': 0.1,  # < 100ms
            'classification_accuracy': 0.8,  # > 80%
            'prediction_accuracy': 0.7,  # > 70%
            'confidence_threshold': 0.6,  # > 60%
            'load_balance_score': 0.7,  # > 70%
            'cost_efficiency': 100,  # Quality/Cost ratio
            'time_efficiency': 0.05  # Quality/Time ratio
        }
        
        print("✅ ML ROUTING VALIDATION FRAMEWORK INITIALIZED")
        print(f"   🎯 Validation thresholds configured")
        print(f"   📊 Performance metrics tracking enabled")
        print()
    
    async def run_comprehensive_validation(self) -> Dict[str, Any]:
        """Run comprehensive validation suite"""
        
        print("🔬 COMPREHENSIVE ML ROUTING VALIDATION")
        print("=" * 80)
        print()
        
        validation_start = time.time()
        
        # Test categories
        test_categories = [
            ("🧠 Neural Classification Tests", self._test_neural_classification),
            ("🤖 Agent Selection Tests", self._test_agent_selection),
            ("📊 Performance Prediction Tests", self._test_performance_prediction),
            ("⚡ Real-time Optimization Tests", self._test_realtime_optimization),
            ("🔮 End-to-End Routing Tests", self._test_end_to_end_routing),
            ("📈 Performance Benchmarks", self._test_performance_benchmarks),
            ("🛡️ Robustness Tests", self._test_robustness),
            ("🎯 Accuracy Validation", self._test_prediction_accuracy)
        ]
        
        category_results = {}
        
        for category_name, test_function in test_categories:
            print(f"{category_name}")
            print("-" * 60)
            
            category_start = time.time()
            category_result = await test_function()
            category_time = time.time() - category_start
            
            category_results[category_name] = {
                'results': category_result,
                'execution_time': category_time,
                'passed_tests': sum(1 for r in category_result if r.passed),
                'total_tests': len(category_result),
                'success_rate': sum(1 for r in category_result if r.passed) / max(len(category_result), 1)
            }
            
            print(f"   ✅ Passed: {category_results[category_name]['passed_tests']}/{category_results[category_name]['total_tests']}")
            print(f"   ⏱️ Time: {category_time:.3f}s")
            print()
        
        total_validation_time = time.time() - validation_start
        
        # Generate comprehensive report
        validation_report = self._generate_validation_report(category_results, total_validation_time)
        
        # Save validation results
        self._save_validation_results(validation_report)
        
        print("🎯 VALIDATION SUMMARY:")
        print("=" * 80)
        print(f"Total tests: {validation_report['total_tests']}")
        print(f"Passed tests: {validation_report['passed_tests']}")
        print(f"Success rate: {validation_report['overall_success_rate']:.1%}")
        print(f"Total time: {total_validation_time:.3f}s")
        print(f"Grade: {validation_report['overall_grade']}")
        
        if validation_report['critical_issues']:
            print(f"\n⚠️ CRITICAL ISSUES: {len(validation_report['critical_issues'])}")
            for issue in validation_report['critical_issues']:
                print(f"   - {issue}")
        
        if validation_report['recommendations']:
            print(f"\n💡 RECOMMENDATIONS:")
            for rec in validation_report['recommendations']:
                print(f"   - {rec}")
        
        return validation_report
    
    async def _test_neural_classification(self) -> List[ValidationResult]:
        """Test neural task classification system"""
        
        results = []
        
        # Test 1: Feature extraction consistency
        test_task = "Build a scalable microservices architecture"
        features1 = self.ml_system.task_classifier.extract_features(test_task)
        features2 = self.ml_system.task_classifier.extract_features(test_task)
        
        feature_consistency = np.allclose(features1, features2, rtol=1e-10)
        results.append(ValidationResult(
            "Feature Extraction Consistency",
            feature_consistency,
            1.0 if feature_consistency else 0.0,
            {"features_match": feature_consistency},
            0.001
        ))
        
        # Test 2: Feature dimensionality
        correct_dims = len(features1) == 50
        results.append(ValidationResult(
            "Feature Dimensionality",
            correct_dims,
            1.0 if correct_dims else 0.0,
            {"expected_dims": 50, "actual_dims": len(features1)},
            0.001
        ))
        
        # Test 3: Classification consistency
        start_time = time.time()
        complexity1, conf1 = self.ml_system.task_classifier.predict(test_task)
        complexity2, conf2 = self.ml_system.task_classifier.predict(test_task)
        prediction_time = time.time() - start_time
        
        classification_consistent = complexity1 == complexity2
        within_time_limit = prediction_time < self.thresholds['prediction_time']
        
        results.append(ValidationResult(
            "Classification Consistency",
            classification_consistent,
            1.0 if classification_consistent else 0.0,
            {"complexity1": complexity1, "complexity2": complexity2, "conf1": conf1, "conf2": conf2},
            prediction_time
        ))
        
        results.append(ValidationResult(
            "Prediction Time Performance",
            within_time_limit,
            min(1.0, self.thresholds['prediction_time'] / prediction_time) if prediction_time > 0 else 1.0,
            {"prediction_time": prediction_time, "threshold": self.thresholds['prediction_time']},
            prediction_time
        ))
        
        # Test 4: Complexity progression
        complexity_tasks = [
            ("Format code", 0, 2),  # Simple
            ("Implement API", 2, 4),  # Moderate
            ("Design architecture", 4, 6),  # Complex
            ("Build AI platform", 6, 8)  # Mega
        ]
        
        complexity_progression_correct = True
        complexity_results = {}
        
        for task_desc, min_expected, max_expected in complexity_tasks:
            complexity, confidence = self.ml_system.task_classifier.predict(task_desc)
            complexity_results[task_desc] = {"complexity": complexity, "confidence": confidence}
            
            if not (min_expected <= complexity <= max_expected):
                complexity_progression_correct = False
        
        results.append(ValidationResult(
            "Complexity Progression",
            complexity_progression_correct,
            1.0 if complexity_progression_correct else 0.5,
            {"complexity_results": complexity_results},
            0.01
        ))
        
        return results
    
    async def _test_agent_selection(self) -> List[ValidationResult]:
        """Test agent selection optimization"""
        
        results = []
        
        # Test 1: Team composition validity
        sample_features = np.random.random(50)
        available_agents = ['cerebras_ultra', 'gemini_flash', 'groq_lightning', 'scaleway_eu']
        
        start_time = time.time()
        optimal_team = self.ml_system.agent_optimizer.optimize_team_composition(
            sample_features, available_agents
        )
        selection_time = time.time() - start_time
        
        team_valid = (
            isinstance(optimal_team, list) and
            len(optimal_team) > 0 and
            all(agent in available_agents for agent in optimal_team)
        )
        
        results.append(ValidationResult(
            "Team Composition Validity",
            team_valid,
            1.0 if team_valid else 0.0,
            {"optimal_team": optimal_team, "team_size": len(optimal_team)},
            selection_time
        ))
        
        # Test 2: Selection performance
        within_time_limit = selection_time < 0.05  # 50ms limit
        results.append(ValidationResult(
            "Selection Performance",
            within_time_limit,
            min(1.0, 0.05 / selection_time) if selection_time > 0 else 1.0,
            {"selection_time": selection_time},
            selection_time
        ))
        
        # Test 3: Constraint handling
        constraints = {"max_agents": 2, "min_quality": 0.8}
        constrained_team = self.ml_system.agent_optimizer.optimize_team_composition(
            sample_features, available_agents, constraints
        )
        
        constraint_respected = len(constrained_team) <= constraints["max_agents"]
        results.append(ValidationResult(
            "Constraint Handling",
            constraint_respected,
            1.0 if constraint_respected else 0.0,
            {"constrained_team": constrained_team, "constraints": constraints},
            0.01
        ))
        
        # Test 4: Performance prediction
        for agent in optimal_team:
            prediction = self.ml_system.agent_optimizer.predict_agent_performance(agent, sample_features)
            
            prediction_valid = (
                isinstance(prediction, dict) and
                'quality' in prediction and
                'time' in prediction and
                'cost' in prediction and
                0 <= prediction['quality'] <= 1 and
                prediction['time'] > 0 and
                prediction['cost'] > 0
            )
            
            results.append(ValidationResult(
                f"Agent Performance Prediction ({agent})",
                prediction_valid,
                1.0 if prediction_valid else 0.0,
                {"prediction": prediction},
                0.001
            ))
        
        return results
    
    async def _test_performance_prediction(self) -> List[ValidationResult]:
        """Test performance prediction engine"""
        
        results = []
        
        sample_features = np.random.random(50)
        sample_team = ['cerebras_ultra', 'gemini_flash']
        
        # Test 1: Prediction structure
        start_time = time.time()
        prediction = self.ml_system.performance_predictor.predict_with_uncertainty(
            sample_features, sample_team
        )
        prediction_time = time.time() - start_time
        
        structure_valid = (
            isinstance(prediction, dict) and
            'predictions' in prediction and
            'uncertainty_bounds' in prediction and
            'confidence' in prediction and
            isinstance(prediction['predictions'], dict) and
            'quality' in prediction['predictions'] and
            'time' in prediction['predictions'] and
            'cost' in prediction['predictions']
        )
        
        results.append(ValidationResult(
            "Prediction Structure",
            structure_valid,
            1.0 if structure_valid else 0.0,
            {"prediction_structure": list(prediction.keys()) if isinstance(prediction, dict) else None},
            prediction_time
        ))
        
        # Test 2: Uncertainty bounds validity
        if structure_valid:
            bounds_valid = True
            for metric, bounds in prediction['uncertainty_bounds'].items():
                if not (isinstance(bounds, tuple) and len(bounds) == 2 and bounds[0] <= bounds[1]):
                    bounds_valid = False
                    break
            
            results.append(ValidationResult(
                "Uncertainty Bounds Validity",
                bounds_valid,
                1.0 if bounds_valid else 0.0,
                {"uncertainty_bounds": prediction['uncertainty_bounds']},
                0.001
            ))
        
        # Test 3: Value ranges
        if structure_valid:
            values_in_range = (
                0 <= prediction['predictions']['quality'] <= 1 and
                prediction['predictions']['time'] > 0 and
                prediction['predictions']['cost'] > 0 and
                0 <= prediction['confidence'] <= 1
            )
            
            results.append(ValidationResult(
                "Prediction Value Ranges",
                values_in_range,
                1.0 if values_in_range else 0.0,
                {"predictions": prediction['predictions'], "confidence": prediction['confidence']},
                0.001
            ))
        
        # Test 4: Performance
        within_time_limit = prediction_time < 0.05
        results.append(ValidationResult(
            "Prediction Performance",
            within_time_limit,
            min(1.0, 0.05 / prediction_time) if prediction_time > 0 else 1.0,
            {"prediction_time": prediction_time},
            prediction_time
        ))
        
        return results
    
    async def _test_realtime_optimization(self) -> List[ValidationResult]:
        """Test real-time optimization engine"""
        
        results = []
        
        # Test 1: Load balancing
        available_agents = ['cerebras_ultra', 'gemini_flash', 'groq_lightning', 'scaleway_eu']
        original_team = ['cerebras_ultra', 'gemini_flash']
        
        # Set different loads
        self.ml_system.real_time_optimizer.update_agent_load('cerebras_ultra', 0.9)  # High load
        self.ml_system.real_time_optimizer.update_agent_load('gemini_flash', 0.3)   # Low load
        self.ml_system.real_time_optimizer.update_agent_load('groq_lightning', 0.2) # Low load
        
        balanced_team = self.ml_system.real_time_optimizer.get_load_balanced_team(
            original_team, available_agents
        )
        
        load_balance_improved = 'groq_lightning' in balanced_team or 'gemini_flash' in balanced_team
        results.append(ValidationResult(
            "Load Balancing",
            load_balance_improved,
            1.0 if load_balance_improved else 0.5,
            {"original_team": original_team, "balanced_team": balanced_team},
            0.01
        ))
        
        # Test 2: Execution parameter optimization
        execution_params = self.ml_system.real_time_optimizer.optimize_execution_parameters(
            5, balanced_team  # Complexity 5, balanced team
        )
        
        params_valid = (
            isinstance(execution_params, dict) and
            'timeout_seconds' in execution_params and
            'retry_count' in execution_params and
            'quality_target' in execution_params and
            execution_params['timeout_seconds'] > 0 and
            execution_params['retry_count'] >= 1 and
            0 <= execution_params['quality_target'] <= 1
        )
        
        results.append(ValidationResult(
            "Execution Parameters",
            params_valid,
            1.0 if params_valid else 0.0,
            {"execution_params": execution_params},
            0.001
        ))
        
        # Test 3: Adaptive timeout scaling
        low_complexity_params = self.ml_system.real_time_optimizer.optimize_execution_parameters(2, ['cerebras_ultra'])
        high_complexity_params = self.ml_system.real_time_optimizer.optimize_execution_parameters(7, balanced_team)
        
        timeout_scaling = (
            high_complexity_params['timeout_seconds'] > low_complexity_params['timeout_seconds']
        )
        
        results.append(ValidationResult(
            "Adaptive Timeout Scaling",
            timeout_scaling,
            1.0 if timeout_scaling else 0.0,
            {
                "low_complexity_timeout": low_complexity_params['timeout_seconds'],
                "high_complexity_timeout": high_complexity_params['timeout_seconds']
            },
            0.001
        ))
        
        return results
    
    async def _test_end_to_end_routing(self) -> List[ValidationResult]:
        """Test complete end-to-end routing pipeline"""
        
        results = []
        
        test_tasks = [
            "Format JavaScript code",
            "Implement REST API with authentication",
            "Design scalable microservices architecture",
            "Build quantum-resistant AI platform"
        ]
        
        for i, task in enumerate(test_tasks):
            start_time = time.time()
            
            try:
                prediction = await self.ml_system.predict_optimal_routing(task)
                routing_time = time.time() - start_time
                
                # Check prediction validity
                prediction_valid = (
                    hasattr(prediction, 'predicted_orchestration_type') and
                    hasattr(prediction, 'predicted_agent_combination') and
                    hasattr(prediction, 'estimated_quality') and
                    hasattr(prediction, 'estimated_cost') and
                    hasattr(prediction, 'estimated_time') and
                    hasattr(prediction, 'confidence_score') and
                    isinstance(prediction.predicted_agent_combination, list) and
                    len(prediction.predicted_agent_combination) > 0 and
                    0 <= prediction.estimated_quality <= 1 and
                    prediction.estimated_cost > 0 and
                    prediction.estimated_time > 0 and
                    0 <= prediction.confidence_score <= 1
                )
                
                results.append(ValidationResult(
                    f"End-to-End Routing Task {i+1}",
                    prediction_valid,
                    1.0 if prediction_valid else 0.0,
                    {
                        "task": task[:50] + "...",
                        "orchestration": prediction.predicted_orchestration_type if prediction_valid else None,
                        "team_size": len(prediction.predicted_agent_combination) if prediction_valid else 0,
                        "routing_time": routing_time
                    },
                    routing_time
                ))
                
                # Check routing time performance
                within_time_limit = routing_time < self.thresholds['prediction_time']
                results.append(ValidationResult(
                    f"Routing Performance Task {i+1}",
                    within_time_limit,
                    min(1.0, self.thresholds['prediction_time'] / routing_time) if routing_time > 0 else 1.0,
                    {"routing_time": routing_time, "threshold": self.thresholds['prediction_time']},
                    routing_time
                ))
                
            except Exception as e:
                results.append(ValidationResult(
                    f"End-to-End Routing Task {i+1}",
                    False,
                    0.0,
                    {"error": str(e)},
                    time.time() - start_time,
                    str(e)
                ))
        
        return results
    
    async def _test_performance_benchmarks(self) -> List[ValidationResult]:
        """Test performance benchmarks"""
        
        results = []
        
        # Benchmark 1: Throughput test
        test_tasks = [f"Test task {i}: implement feature X" for i in range(20)]
        
        start_time = time.time()
        successful_predictions = 0
        
        for task in test_tasks:
            try:
                prediction = await self.ml_system.predict_optimal_routing(task)
                if hasattr(prediction, 'confidence_score') and prediction.confidence_score > 0.5:
                    successful_predictions += 1
            except:
                pass
        
        throughput_time = time.time() - start_time
        throughput = len(test_tasks) / throughput_time
        
        throughput_target = 10  # 10 predictions per second
        throughput_passed = throughput >= throughput_target
        
        results.append(ValidationResult(
            "Throughput Benchmark",
            throughput_passed,
            min(1.0, throughput / throughput_target),
            {
                "throughput": throughput,
                "target": throughput_target,
                "successful_predictions": successful_predictions,
                "total_tasks": len(test_tasks)
            },
            throughput_time
        ))
        
        # Benchmark 2: Memory usage (simplified)
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        memory_before = process.memory_info().rss / 1024 / 1024  # MB
        
        # Process multiple tasks
        for _ in range(10):
            await self.ml_system.predict_optimal_routing("Complex task with multiple requirements")
        
        memory_after = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = memory_after - memory_before
        
        memory_limit = 50  # 50 MB increase limit
        memory_passed = memory_increase < memory_limit
        
        results.append(ValidationResult(
            "Memory Usage Benchmark",
            memory_passed,
            max(0.0, min(1.0, 1.0 - memory_increase / memory_limit)),
            {
                "memory_before": memory_before,
                "memory_after": memory_after,
                "memory_increase": memory_increase,
                "limit": memory_limit
            },
            0.1
        ))
        
        return results
    
    async def _test_robustness(self) -> List[ValidationResult]:
        """Test system robustness"""
        
        results = []
        
        # Test 1: Empty task handling
        try:
            prediction = await self.ml_system.predict_optimal_routing("")
            empty_task_handled = True
            error = None
        except Exception as e:
            empty_task_handled = False
            error = str(e)
        
        results.append(ValidationResult(
            "Empty Task Handling",
            empty_task_handled,
            1.0 if empty_task_handled else 0.5,  # 0.5 because graceful failure is acceptable
            {"error": error},
            0.01
        ))
        
        # Test 2: Very long task handling
        very_long_task = "This is a very long task description. " * 100
        
        try:
            start_time = time.time()
            prediction = await self.ml_system.predict_optimal_routing(very_long_task)
            long_task_time = time.time() - start_time
            long_task_handled = True
            within_reasonable_time = long_task_time < 1.0  # 1 second limit
        except Exception as e:
            long_task_handled = False
            within_reasonable_time = False
            long_task_time = 0
        
        results.append(ValidationResult(
            "Long Task Handling",
            long_task_handled and within_reasonable_time,
            (1.0 if long_task_handled else 0.0) * (1.0 if within_reasonable_time else 0.5),
            {"handled": long_task_handled, "time": long_task_time},
            long_task_time
        ))
        
        # Test 3: Special characters handling
        special_task = "Task with spëcial chàracters and symbols: @#$%^&*()[]{}|\\:;\"'<>?,./"
        
        try:
            prediction = await self.ml_system.predict_optimal_routing(special_task)
            special_chars_handled = True
        except Exception as e:
            special_chars_handled = False
        
        results.append(ValidationResult(
            "Special Characters Handling",
            special_chars_handled,
            1.0 if special_chars_handled else 0.0,
            {"task_length": len(special_task)},
            0.01
        ))
        
        # Test 4: Concurrent requests
        concurrent_tasks = [f"Concurrent task {i}" for i in range(5)]
        
        try:
            start_time = time.time()
            concurrent_predictions = await asyncio.gather(*[
                self.ml_system.predict_optimal_routing(task) for task in concurrent_tasks
            ])
            concurrent_time = time.time() - start_time
            concurrent_handled = len(concurrent_predictions) == len(concurrent_tasks)
        except Exception as e:
            concurrent_handled = False
            concurrent_time = 0
        
        results.append(ValidationResult(
            "Concurrent Requests",
            concurrent_handled,
            1.0 if concurrent_handled else 0.0,
            {"tasks_count": len(concurrent_tasks), "time": concurrent_time},
            concurrent_time
        ))
        
        return results
    
    async def _test_prediction_accuracy(self) -> List[ValidationResult]:
        """Test prediction accuracy with synthetic data"""
        
        results = []
        
        # Generate synthetic test data
        test_cases = self.test_data_generator.generate_accuracy_test_cases()
        
        correct_predictions = 0
        total_predictions = len(test_cases)
        prediction_errors = {'quality': [], 'time': [], 'cost': []}
        
        for test_case in test_cases:
            try:
                prediction = await self.ml_system.predict_optimal_routing(test_case['task'])
                
                # Compare with expected values (synthetic ground truth)
                expected = test_case['expected']
                
                quality_error = abs(prediction.estimated_quality - expected['quality'])
                time_error = abs(prediction.estimated_time - expected['time']) / max(expected['time'], 1.0)
                cost_error = abs(prediction.estimated_cost - expected['cost']) / max(expected['cost'], 0.0001)
                
                prediction_errors['quality'].append(quality_error)
                prediction_errors['time'].append(time_error)
                prediction_errors['cost'].append(cost_error)
                
                # Consider prediction correct if errors are within tolerance
                if (quality_error < 0.3 and time_error < 0.5 and cost_error < 0.5):
                    correct_predictions += 1
                    
            except Exception as e:
                logger.warning(f"Prediction failed for test case: {e}")
        
        accuracy = correct_predictions / max(total_predictions, 1)
        accuracy_passed = accuracy >= self.thresholds['prediction_accuracy']
        
        results.append(ValidationResult(
            "Overall Prediction Accuracy",
            accuracy_passed,
            accuracy,
            {
                "correct_predictions": correct_predictions,
                "total_predictions": total_predictions,
                "accuracy": accuracy,
                "mean_quality_error": np.mean(prediction_errors['quality']) if prediction_errors['quality'] else 0,
                "mean_time_error": np.mean(prediction_errors['time']) if prediction_errors['time'] else 0,
                "mean_cost_error": np.mean(prediction_errors['cost']) if prediction_errors['cost'] else 0
            },
            1.0
        ))
        
        # Individual metric accuracy
        for metric, errors in prediction_errors.items():
            if errors:
                mean_error = np.mean(errors)
                error_threshold = 0.3 if metric == 'quality' else 0.5
                metric_accuracy = 1.0 - min(1.0, mean_error / error_threshold)
                
                results.append(ValidationResult(
                    f"{metric.title()} Prediction Accuracy",
                    mean_error < error_threshold,
                    metric_accuracy,
                    {"mean_error": mean_error, "threshold": error_threshold},
                    0.1
                ))
        
        return results
    
    def _generate_validation_report(self, category_results: Dict, total_time: float) -> Dict:
        """Generate comprehensive validation report"""
        
        all_results = []
        for category_data in category_results.values():
            all_results.extend(category_data['results'])
        
        total_tests = len(all_results)
        passed_tests = sum(1 for r in all_results if r.passed)
        overall_success_rate = passed_tests / max(total_tests, 1)
        
        # Calculate grade
        if overall_success_rate >= 0.9:
            grade = "A"
        elif overall_success_rate >= 0.8:
            grade = "B"
        elif overall_success_rate >= 0.7:
            grade = "C"
        elif overall_success_rate >= 0.6:
            grade = "D"
        else:
            grade = "F"
        
        # Identify critical issues
        critical_issues = []
        for result in all_results:
            if not result.passed and result.score < 0.5:
                critical_issues.append(f"{result.test_name}: {result.error_message or 'Performance below threshold'}")
        
        # Generate recommendations
        recommendations = []
        
        if overall_success_rate < 0.8:
            recommendations.append("Overall system performance needs improvement")
        
        # Category-specific recommendations
        for category_name, category_data in category_results.items():
            if category_data['success_rate'] < 0.7:
                recommendations.append(f"Focus on improving {category_name.lower()}")
        
        # Performance-specific recommendations
        slow_tests = [r for r in all_results if r.execution_time > 0.1]
        if len(slow_tests) > total_tests * 0.3:
            recommendations.append("Optimize system performance - many operations are slow")
        
        if len(critical_issues) > 0:
            recommendations.append("Address critical issues before production deployment")
        
        return {
            'timestamp': datetime.now().isoformat(),
            'total_tests': total_tests,
            'passed_tests': passed_tests,
            'failed_tests': total_tests - passed_tests,
            'overall_success_rate': overall_success_rate,
            'overall_grade': grade,
            'total_validation_time': total_time,
            'category_results': category_results,
            'critical_issues': critical_issues[:10],  # Limit to top 10
            'recommendations': recommendations[:10],   # Limit to top 10
            'detailed_results': [
                {
                    'test_name': r.test_name,
                    'passed': r.passed,
                    'score': r.score,
                    'execution_time': r.execution_time,
                    'details': r.details
                } for r in all_results
            ]
        }
    
    def _save_validation_results(self, report: Dict):
        """Save validation results to file"""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"ml_routing_validation_report_{timestamp}.json"
        
        try:
            with open(filename, 'w') as f:
                json.dump(report, f, indent=2, default=str)
            
            print(f"📁 Validation report saved: {filename}")
            
        except Exception as e:
            logger.error(f"Failed to save validation report: {e}")

class TestDataGenerator:
    """Generate synthetic test data for validation"""
    
    def generate_accuracy_test_cases(self) -> List[Dict]:
        """Generate test cases with expected outcomes"""
        
        test_cases = []
        
        # Simple tasks
        simple_tasks = [
            ("Format code", {'quality': 0.7, 'time': 2.0, 'cost': 0.0001}),
            ("List files", {'quality': 0.6, 'time': 1.0, 'cost': 0.0001}),
            ("Show status", {'quality': 0.8, 'time': 1.5, 'cost': 0.0001})
        ]
        
        for task, expected in simple_tasks:
            test_cases.append({'task': task, 'expected': expected})
        
        # Moderate tasks
        moderate_tasks = [
            ("Implement authentication", {'quality': 0.75, 'time': 10.0, 'cost': 0.0003}),
            ("Create API endpoint", {'quality': 0.8, 'time': 8.0, 'cost': 0.0002}),
            ("Build database schema", {'quality': 0.85, 'time': 15.0, 'cost': 0.0004})
        ]
        
        for task, expected in moderate_tasks:
            test_cases.append({'task': task, 'expected': expected})
        
        # Complex tasks
        complex_tasks = [
            ("Design microservices architecture", {'quality': 0.85, 'time': 25.0, 'cost': 0.002}),
            ("Implement distributed system", {'quality': 0.8, 'time': 30.0, 'cost': 0.003}),
            ("Build scalable platform", {'quality': 0.9, 'time': 35.0, 'cost': 0.004})
        ]
        
        for task, expected in complex_tasks:
            test_cases.append({'task': task, 'expected': expected})
        
        # Mega tasks
        mega_tasks = [
            ("Build autonomous AI platform", {'quality': 0.95, 'time': 60.0, 'cost': 0.008}),
            ("Create quantum-resistant system", {'quality': 0.9, 'time': 50.0, 'cost': 0.007}),
            ("Design revolutionary ecosystem", {'quality': 0.95, 'time': 70.0, 'cost': 0.01})
        ]
        
        for task, expected in mega_tasks:
            test_cases.append({'task': task, 'expected': expected})
        
        return test_cases

# Performance monitoring dashboard (simplified)
class ValidationDashboard:
    """Simple dashboard for validation results"""
    
    def __init__(self):
        self.results_history = []
    
    def add_validation_result(self, report: Dict):
        """Add validation result to history"""
        self.results_history.append(report)
        
        # Keep only last 50 validations
        if len(self.results_history) > 50:
            self.results_history = self.results_history[-50:]
    
    def generate_trend_analysis(self) -> Dict:
        """Generate trend analysis from validation history"""
        
        if len(self.results_history) < 2:
            return {"message": "Insufficient data for trend analysis"}
        
        # Calculate trends
        success_rates = [r['overall_success_rate'] for r in self.results_history]
        validation_times = [r['total_validation_time'] for r in self.results_history]
        
        success_trend = np.polyfit(range(len(success_rates)), success_rates, 1)[0]
        time_trend = np.polyfit(range(len(validation_times)), validation_times, 1)[0]
        
        return {
            'success_rate_trend': 'improving' if success_trend > 0.01 else 'declining' if success_trend < -0.01 else 'stable',
            'validation_time_trend': 'increasing' if time_trend > 0.1 else 'decreasing' if time_trend < -0.1 else 'stable',
            'current_success_rate': success_rates[-1],
            'average_success_rate': np.mean(success_rates),
            'success_rate_std': np.std(success_rates),
            'validation_count': len(self.results_history)
        }

# Main validation runner
async def run_ml_validation():
    """Run ML routing validation"""
    
    print("🔬 RUNNING ML PREDICTIVE ROUTING VALIDATION")
    print("=" * 80)
    print()
    
    try:
        # Import and initialize ML routing system
        from ml_predictive_routing_system import MLPredictiveRoutingSystem
        
        ml_system = MLPredictiveRoutingSystem()
        validator = MLRoutingValidator(ml_system)
        
        # Run comprehensive validation
        validation_report = await validator.run_comprehensive_validation()
        
        # Create dashboard and add results
        dashboard = ValidationDashboard()
        dashboard.add_validation_result(validation_report)
        
        # Generate trends (if multiple runs)
        trend_analysis = dashboard.generate_trend_analysis()
        
        print("\n📈 TREND ANALYSIS:")
        for key, value in trend_analysis.items():
            print(f"   {key.replace('_', ' ').title()}: {value}")
        
        return validation_report
        
    except ImportError:
        print("⚠️  ML Predictive Routing System not available for validation")
        return None
    except Exception as e:
        print(f"❌ Validation failed with error: {e}")
        return None

if __name__ == "__main__":
    asyncio.run(run_ml_validation())