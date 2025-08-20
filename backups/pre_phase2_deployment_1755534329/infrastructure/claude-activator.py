#!/usr/bin/env python3
"""
Claude Smart Activation Engine
Auto-loads complementary intelligence systems based on context and success patterns
"""

import json
import time
from pathlib import Path
from typing import Dict, List, Set, Tuple
from datetime import datetime, timedelta

class SmartActivationEngine:
    def __init__(self, claude_dir: str = "/Users/shaansisodia/.claude"):
        self.claude_dir = Path(claude_dir)
        self.patterns_file = self.claude_dir / "analytics" / "activation_patterns.json"
        self.success_file = self.claude_dir / "analytics" / "success_metrics.json"
        
        # Load learned patterns
        self.patterns = self._load_patterns()
        self.success_metrics = self._load_success_metrics()
        
        # Predefined activation configurations
        self.activation_configs = {
            'auto_analyze': {
                'triggers': ['analyze', 'review', 'examine', 'understand'],
                'intelligence': [
                    'task-intelligence-system',
                    'context-optimization-system',
                    'codebase-intelligence-system'
                ],
                'optional': [
                    'chain-of-thought-intelligence',
                    'performance-intelligence-system'
                ],
                'mode': 'analysis'
            },
            
            'auto_reasoning': {
                'triggers': ['complex', 'think', 'solve', 'difficult'],
                'intelligence': [
                    'chain-of-thought-intelligence',
                    'extended-thinking-intelligence',
                    'meta-reasoning-simplicity-detector'
                ],
                'optional': [
                    'constitutional-ai-intelligence',
                    'prompt-optimization-intelligence'
                ],
                'mode': 'deep_reasoning'
            },
            
            'auto_development': {
                'triggers': ['build', 'code', 'implement', 'develop'],
                'intelligence': [
                    'command-execution-intelligence',
                    'codebase-intelligence-system',
                    'performance-intelligence-system'
                ],
                'optional': [
                    'adaptive-intelligence-system',
                    'ecosystem-orchestration-intelligence'
                ],
                'mode': 'development'
            },
            
            'auto_architecture': {
                'triggers': ['design', 'architect', 'structure', 'system'],
                'intelligence': [
                    'codebase-intelligence-system',
                    'deep-navigation-intelligence',
                    'ecosystem-orchestration-intelligence'
                ],
                'optional': [
                    'multi-agent-orchestration-intelligence',
                    'adaptive-intelligence-system'
                ],
                'mode': 'architecture'
            },
            
            'auto_deployment': {
                'triggers': ['deploy', 'production', 'release', 'ship'],
                'intelligence': [
                    'ecosystem-orchestration-intelligence',
                    'command-execution-intelligence',
                    'performance-intelligence-system'
                ],
                'optional': [
                    'multi-agent-orchestration-intelligence',
                    'adaptive-intelligence-system'
                ],
                'mode': 'deployment'
            },
            
            'auto_optimization': {
                'triggers': ['optimize', 'performance', 'speed', 'improve'],
                'intelligence': [
                    'performance-intelligence-system',
                    'compute-optimization-intelligence',
                    'token-economy-intelligence'
                ],
                'optional': [
                    'model-routing-intelligence',
                    'context-optimization-system'
                ],
                'mode': 'optimization'
            }
        }
    
    def detect_context(self, input_text: str, user_history: List[str] = None) -> Dict:
        """Detect context and recommend activation pattern"""
        input_lower = input_text.lower()
        detected_patterns = []
        confidence_scores = {}
        
        # Check trigger words
        for pattern_name, config in self.activation_configs.items():
            triggers = config.get('triggers', [])
            matches = sum(1 for trigger in triggers if trigger in input_lower)
            
            if matches > 0:
                confidence = matches / len(triggers)
                detected_patterns.append(pattern_name)
                confidence_scores[pattern_name] = confidence
        
        # Analyze user history for patterns
        if user_history:
            history_patterns = self._analyze_history_patterns(user_history)
            for pattern, score in history_patterns.items():
                if pattern in confidence_scores:
                    confidence_scores[pattern] += score * 0.3
                else:
                    confidence_scores[pattern] = score * 0.2
                    detected_patterns.append(pattern)
        
        # Apply learned patterns
        learned_recommendations = self._apply_learned_patterns(input_text)
        for pattern, score in learned_recommendations.items():
            if pattern in confidence_scores:
                confidence_scores[pattern] += score * 0.2
            else:
                confidence_scores[pattern] = score * 0.15
                detected_patterns.append(pattern)
        
        # Sort by confidence
        sorted_patterns = sorted(detected_patterns, key=lambda p: confidence_scores.get(p, 0), reverse=True)
        
        return {
            'detected_patterns': sorted_patterns[:3],
            'confidence_scores': confidence_scores,
            'recommended_activation': sorted_patterns[0] if sorted_patterns else None,
            'strength': confidence_scores.get(sorted_patterns[0], 0) if sorted_patterns else 0
        }
    
    def auto_activate(self, pattern_name: str, context: Dict = None) -> Dict:
        """Automatically activate intelligence systems for pattern"""
        if pattern_name not in self.activation_configs:
            return {'error': f'Unknown pattern: {pattern_name}'}
        
        config = self.activation_configs[pattern_name]
        
        # Base intelligence systems
        activated_systems = config['intelligence'].copy()
        
        # Add optional systems based on context and success patterns
        optional_systems = config.get('optional', [])
        for system in optional_systems:
            if self._should_include_optional(system, pattern_name, context):
                activated_systems.append(system)
        
        # Apply learned optimizations
        optimized_systems = self._apply_optimizations(activated_systems, pattern_name)
        
        activation_result = {
            'pattern': pattern_name,
            'mode': config.get('mode', 'general'),
            'activated_systems': optimized_systems,
            'system_count': len(optimized_systems),
            'activation_time': datetime.now().isoformat(),
            'expected_capabilities': self._describe_capabilities(optimized_systems),
            'success_prediction': self._predict_success(optimized_systems, pattern_name)
        }
        
        # Track activation for learning
        self._track_activation(activation_result)
        
        return activation_result
    
    def learn_from_feedback(self, activation_id: str, success: bool, metrics: Dict = None):
        """Learn from activation success/failure"""
        feedback_entry = {
            'activation_id': activation_id,
            'success': success,
            'timestamp': datetime.now().isoformat(),
            'metrics': metrics or {}
        }
        
        self.success_metrics.setdefault('feedback', []).append(feedback_entry)
        
        # Update success patterns
        self._update_success_patterns(feedback_entry)
        
        # Save learned data
        self._save_success_metrics()
    
    def get_recommendations(self, current_systems: List[str]) -> Dict:
        """Get recommendations for complementary systems"""
        recommendations = {
            'add_systems': [],
            'remove_systems': [],
            'optimization_suggestions': [],
            'predicted_improvements': {}
        }
        
        # Find missing complementary systems
        current_categories = self._categorize_systems(current_systems)
        
        # Recommend based on successful patterns
        successful_combinations = self._get_successful_combinations()
        for combo in successful_combinations:
            if set(current_systems).issubset(set(combo['systems'])):
                missing = set(combo['systems']) - set(current_systems)
                for system in missing:
                    recommendations['add_systems'].append({
                        'system': system,
                        'reason': f"Part of successful pattern (success rate: {combo['success_rate']:.1%})",
                        'confidence': combo['success_rate']
                    })
        
        # Identify potentially redundant systems
        for system in current_systems:
            if self._is_potentially_redundant(system, current_systems):
                recommendations['remove_systems'].append({
                    'system': system,
                    'reason': 'Potentially redundant with current combination',
                    'confidence': 0.6
                })
        
        # Performance optimization suggestions
        perf_suggestions = self._get_performance_suggestions(current_systems)
        recommendations['optimization_suggestions'] = perf_suggestions
        
        return recommendations
    
    def analyze_usage_patterns(self, days: int = 30) -> Dict:
        """Analyze usage patterns over time"""
        cutoff_date = datetime.now() - timedelta(days=days)
        
        recent_activations = [
            a for a in self.patterns.get('activations', [])
            if datetime.fromisoformat(a.get('timestamp', '2020-01-01')) > cutoff_date
        ]
        
        analysis = {
            'total_activations': len(recent_activations),
            'most_used_patterns': self._get_top_patterns(recent_activations),
            'success_rates': self._calculate_success_rates(recent_activations),
            'optimization_opportunities': self._find_optimization_opportunities(recent_activations),
            'trending_combinations': self._find_trending_combinations(recent_activations)
        }
        
        return analysis
    
    def _should_include_optional(self, system: str, pattern: str, context: Dict) -> bool:
        """Decide whether to include optional system"""
        # Check success patterns
        historical_success = self._get_system_success_rate(system, pattern)
        if historical_success > 0.7:
            return True
        
        # Check context indicators
        if context:
            complexity_indicators = context.get('complexity_indicators', [])
            if system == 'constitutional-ai-intelligence' and 'high_complexity' in complexity_indicators:
                return True
            if system == 'multi-agent-orchestration-intelligence' and 'team_collaboration' in complexity_indicators:
                return True
        
        return False
    
    def _apply_optimizations(self, systems: List[str], pattern: str) -> List[str]:
        """Apply learned optimizations to system selection"""
        optimized = systems.copy()
        
        # Remove systems with low success rates for this pattern
        optimized = [s for s in optimized if self._get_system_success_rate(s, pattern) > 0.3]
        
        # Add high-performing systems for this pattern
        high_performers = self._get_high_performing_systems(pattern)
        for system in high_performers:
            if system not in optimized:
                optimized.append(system)
        
        return optimized
    
    def _predict_success(self, systems: List[str], pattern: str) -> float:
        """Predict success probability for system combination"""
        if not self.success_metrics.get('feedback'):
            return 0.5  # Default moderate confidence
        
        # Look for similar combinations in history
        similar_combinations = []
        for feedback in self.success_metrics['feedback']:
            activation = feedback.get('activation', {})
            if activation.get('pattern') == pattern:
                historical_systems = set(activation.get('activated_systems', []))
                current_systems = set(systems)
                
                # Calculate overlap
                overlap = len(historical_systems.intersection(current_systems))
                total = len(historical_systems.union(current_systems))
                similarity = overlap / total if total > 0 else 0
                
                if similarity > 0.5:
                    similar_combinations.append({
                        'similarity': similarity,
                        'success': feedback['success']
                    })
        
        if similar_combinations:
            # Weight by similarity
            weighted_success = sum(
                combo['success'] * combo['similarity'] 
                for combo in similar_combinations
            )
            total_weight = sum(combo['similarity'] for combo in similar_combinations)
            return weighted_success / total_weight if total_weight > 0 else 0.5
        
        return 0.5
    
    def _load_patterns(self) -> Dict:
        """Load activation patterns from file"""
        try:
            if self.patterns_file.exists():
                with open(self.patterns_file, 'r') as f:
                    return json.load(f)
        except Exception:
            pass
        
        return {'activations': [], 'learned_patterns': {}}
    
    def _save_patterns(self):
        """Save patterns to file"""
        try:
            self.patterns_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.patterns_file, 'w') as f:
                json.dump(self.patterns, f, indent=2)
        except Exception:
            pass
    
    def _load_success_metrics(self) -> Dict:
        """Load success metrics from file"""
        try:
            if self.success_file.exists():
                with open(self.success_file, 'r') as f:
                    return json.load(f)
        except Exception:
            pass
        
        return {'feedback': [], 'success_patterns': {}}
    
    def _save_success_metrics(self):
        """Save success metrics to file"""
        try:
            self.success_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.success_file, 'w') as f:
                json.dump(self.success_metrics, f, indent=2)
        except Exception:
            pass
    
    def _get_system_success_rate(self, system: str, pattern: str) -> float:
        """Get historical success rate for system in pattern"""
        if not self.success_metrics.get('feedback'):
            return 0.5  # Default moderate success rate
        
        relevant_feedback = []
        for feedback in self.success_metrics['feedback']:
            activation = feedback.get('activation', {})
            if (activation.get('pattern') == pattern and 
                system in activation.get('activated_systems', [])):
                relevant_feedback.append(feedback['success'])
        
        if relevant_feedback:
            return sum(relevant_feedback) / len(relevant_feedback)
        return 0.5
    
    def _get_high_performing_systems(self, pattern: str) -> List[str]:
        """Get systems with high success rates for pattern"""
        if not self.success_metrics.get('feedback'):
            return []
        
        system_scores = {}
        for feedback in self.success_metrics['feedback']:
            activation = feedback.get('activation', {})
            if activation.get('pattern') == pattern:
                for system in activation.get('activated_systems', []):
                    if system not in system_scores:
                        system_scores[system] = []
                    system_scores[system].append(feedback['success'])
        
        # Calculate average success rates
        high_performers = []
        for system, successes in system_scores.items():
            avg_success = sum(successes) / len(successes)
            if avg_success > 0.7:
                high_performers.append(system)
        
        return high_performers
    
    def _analyze_history_patterns(self, history: List[str]) -> Dict[str, float]:
        """Analyze user history for pattern detection"""
        patterns = {}
        
        # Simple keyword-based pattern detection
        history_text = ' '.join(history).lower()
        
        for pattern_name, config in self.activation_configs.items():
            triggers = config.get('triggers', [])
            matches = sum(1 for trigger in triggers if trigger in history_text)
            if matches > 0:
                patterns[pattern_name] = min(matches / len(triggers), 1.0)
        
        return patterns
    
    def _apply_learned_patterns(self, input_text: str) -> Dict[str, float]:
        """Apply machine learned patterns"""
        # Placeholder for ML-based pattern recognition
        # In a real implementation, this would use trained models
        learned = {}
        
        input_lower = input_text.lower()
        
        # Simple rule-based learning simulation
        if 'complex' in input_lower and 'analysis' in input_lower:
            learned['auto_reasoning'] = 0.8
        if 'deploy' in input_lower and 'production' in input_lower:
            learned['auto_deployment'] = 0.9
        if 'optimize' in input_lower:
            learned['auto_optimization'] = 0.7
        
        return learned
    
    def _categorize_systems(self, systems: List[str]) -> Set[str]:
        """Categorize list of systems"""
        categories = set()
        
        for system in systems:
            if 'reasoning' in system or 'thinking' in system:
                categories.add('reasoning')
            elif 'memory' in system or 'context' in system:
                categories.add('memory')
            elif 'orchestration' in system or 'agent' in system:
                categories.add('orchestration')
            elif 'performance' in system or 'optimization' in system:
                categories.add('performance')
            elif 'navigation' in system or 'codebase' in system:
                categories.add('navigation')
        
        return categories
    
    def _describe_capabilities(self, systems: List[str]) -> List[str]:
        """Describe capabilities of activated systems"""
        capabilities = []
        
        for system in systems:
            if 'reasoning' in system or 'thinking' in system:
                capabilities.append("Advanced reasoning and problem-solving")
            elif 'memory' in system or 'context' in system:
                capabilities.append("Enhanced memory and context management")
            elif 'orchestration' in system:
                capabilities.append("Multi-system coordination and automation")
            elif 'performance' in system or 'optimization' in system:
                capabilities.append("Performance monitoring and optimization")
            elif 'mcp' in system:
                capabilities.append("Intelligent tool selection and routing")
        
        return list(set(capabilities))  # Remove duplicates
    
    def _track_activation(self, result: Dict):
        """Track activation for analytics"""
        activation_entry = {
            'timestamp': result['activation_time'],
            'pattern': result['pattern'],
            'activated_systems': result['activated_systems'],
            'system_count': result['system_count'],
            'success_prediction': result['success_prediction']
        }
        
        self.patterns.setdefault('activations', []).append(activation_entry)
        self._save_patterns()
    
    def _get_successful_combinations(self) -> List[Dict]:
        """Get historically successful system combinations"""
        # Placeholder for real analytics
        return [
            {
                'systems': ['task-intelligence-system', 'context-optimization-system', 'chain-of-thought-intelligence'],
                'success_rate': 0.89,
                'use_count': 15
            },
            {
                'systems': ['ecosystem-orchestration-intelligence', 'multi-agent-orchestration-intelligence'],
                'success_rate': 0.93,
                'use_count': 8
            }
        ]
    
    def _is_potentially_redundant(self, system: str, current_systems: List[str]) -> bool:
        """Check if system might be redundant"""
        # Simple redundancy detection
        redundancy_groups = [
            ['chain-of-thought-intelligence', 'extended-thinking-intelligence'],
            ['mcp-intelligence-system', 'ecosystem-orchestration-intelligence'],
            ['context-optimization-system', 'session-memory-intelligence']
        ]
        
        for group in redundancy_groups:
            if system in group:
                # Check if another system from same group is already active
                for other in group:
                    if other != system and other in current_systems:
                        return True
        
        return False
    
    def _get_performance_suggestions(self, current_systems: List[str]) -> List[str]:
        """Get performance optimization suggestions"""
        suggestions = []
        
        # Check for missing performance optimizations
        if not any('token-economy' in s for s in current_systems):
            suggestions.append("Add token-economy-intelligence for cost optimization")
        
        if not any('performance' in s for s in current_systems):
            suggestions.append("Consider performance-intelligence-system for monitoring")
        
        if len(current_systems) > 6:
            suggestions.append("Consider reducing system count for better performance")
        
        return suggestions
    
    def _get_top_patterns(self, activations: List[Dict]) -> List[Tuple[str, int]]:
        """Get most used activation patterns"""
        from collections import Counter
        patterns = [a.get('pattern', 'unknown') for a in activations]
        return Counter(patterns).most_common(5)
    
    def _calculate_success_rates(self, activations: List[Dict]) -> Dict[str, float]:
        """Calculate success rates by pattern"""
        pattern_success = {}
        
        for activation in activations:
            pattern = activation.get('pattern', 'unknown')
            success = activation.get('success', True)  # Assume success if not specified
            
            if pattern not in pattern_success:
                pattern_success[pattern] = []
            pattern_success[pattern].append(success)
        
        # Calculate averages
        rates = {}
        for pattern, successes in pattern_success.items():
            rates[pattern] = sum(successes) / len(successes) if successes else 0.0
        
        return rates
    
    def _find_optimization_opportunities(self, activations: List[Dict]) -> List[str]:
        """Find optimization opportunities from activation history"""
        opportunities = []
        
        if len(activations) < 5:
            opportunities.append("More usage data needed for better recommendations")
        else:
            opportunities.extend([
                "Pattern detection accuracy could improve with more data",
                "Consider automated pattern learning from success feedback",
                "System combination optimization available"
            ])
        
        return opportunities
    
    def _find_trending_combinations(self, activations: List[Dict]) -> List[Dict]:
        """Find trending system combinations"""
        from collections import Counter
        
        # Get system combinations from recent activations
        combinations = []
        for activation in activations[-10:]:  # Last 10 activations
            systems = tuple(sorted(activation.get('activated_systems', [])))
            if len(systems) > 1:
                combinations.append(systems)
        
        trending = []
        for combo, count in Counter(combinations).most_common(3):
            trending.append({
                'systems': list(combo),
                'frequency': count,
                'trend': 'increasing' if count > 1 else 'stable'
            })
        
        return trending

def main():
    """CLI interface for Smart Activation Engine"""
    import sys
    
    engine = SmartActivationEngine()
    
    if len(sys.argv) < 2:
        print("⚡ Claude Smart Activation Engine")
        print("Usage:")
        print("  claude-activator detect 'analyze complex system architecture'")
        print("  claude-activator activate auto_reasoning")
        print("  claude-activator recommend current_system1,current_system2")
        print("  claude-activator analytics")
        return
    
    command = sys.argv[1]
    
    if command == "detect" and len(sys.argv) > 2:
        input_text = " ".join(sys.argv[2:])
        context = engine.detect_context(input_text)
        
        print(f"🔍 Context Detection for: '{input_text}'")
        print(f"🎯 Recommended Pattern: {context['recommended_activation']}")
        print(f"📊 Confidence: {context['strength']:.1%}")
        print(f"🧠 All Detected Patterns: {', '.join(context['detected_patterns'])}")
    
    elif command == "activate" and len(sys.argv) > 2:
        pattern = sys.argv[2]
        result = engine.auto_activate(pattern)
        
        print(f"⚡ Auto-Activated Pattern: {pattern}")
        print(f"🎛️ Mode: {result['mode']}")
        print(f"🧠 Systems: {result['system_count']}")
        print(f"📈 Success Prediction: {result['success_prediction']:.1%}")
        
        for system in result['activated_systems']:
            print(f"  • {system}")
    
    elif command == "recommend" and len(sys.argv) > 2:
        current_systems = sys.argv[2].split(',')
        recommendations = engine.get_recommendations(current_systems)
        
        print(f"💡 Recommendations for: {', '.join(current_systems)}")
        
        if recommendations['add_systems']:
            print("\n➕ Suggested Additions:")
            for rec in recommendations['add_systems'][:3]:
                print(f"  • {rec['system']} - {rec['reason']}")
        
        if recommendations['optimization_suggestions']:
            print("\n🔧 Optimizations:")
            for opt in recommendations['optimization_suggestions'][:3]:
                print(f"  • {opt}")
    
    elif command == "analytics":
        analytics = engine.analyze_usage_patterns()
        
        print("📊 Usage Analytics (Last 30 days):")
        print(f"  Total Activations: {analytics['total_activations']}")
        
        if analytics['most_used_patterns']:
            print("\n🏆 Top Patterns:")
            for pattern, count in analytics['most_used_patterns'][:5]:
                print(f"  • {pattern}: {count} uses")

if __name__ == "__main__":
    main()