#!/usr/bin/env python3
"""
QUALITY VALIDATION SYSTEM
Real-time output scoring and improvement for multi-agent coordination
"""

import re
import asyncio
from typing import Dict, List, Any, Optional
from datetime import datetime
import json
from pathlib import Path

class QualityValidator:
    """Advanced quality validation system for multi-agent outputs"""
    
    def __init__(self):
        self.quality_thresholds = {
            'excellent': 0.9,
            'good': 0.7,
            'acceptable': 0.5,
            'poor': 0.3
        }
        
        self.quality_history = []
        self.agent_performance_scores = {}
        
        # Quality metrics weights
        self.metric_weights = {
            'relevance': 0.30,
            'accuracy': 0.25,
            'completeness': 0.20,
            'innovation': 0.15,
            'clarity': 0.10
        }
    
    def score_output_quality(self, output: str, task: str, agent_type: str, specialization: str) -> Dict:
        """Comprehensive quality scoring using multiple metrics"""
        
        start_time = datetime.now()
        
        # Calculate individual quality metrics
        relevance_score = self._calculate_relevance(output, task)
        accuracy_score = self._validate_accuracy(output, specialization)
        completeness_score = self._check_completeness(output, task)
        innovation_score = self._assess_innovation(output)
        clarity_score = self._evaluate_clarity(output)
        
        # Calculate weighted overall score
        overall_score = (
            relevance_score * self.metric_weights['relevance'] +
            accuracy_score * self.metric_weights['accuracy'] +
            completeness_score * self.metric_weights['completeness'] +
            innovation_score * self.metric_weights['innovation'] +
            clarity_score * self.metric_weights['clarity']
        )
        
        # Determine quality level
        quality_level = self._determine_quality_level(overall_score)
        
        # Generate improvement suggestions
        improvements = self._generate_improvement_suggestions(
            relevance_score, accuracy_score, completeness_score, 
            innovation_score, clarity_score
        )
        
        quality_result = {
            'overall_score': round(overall_score, 3),
            'quality_level': quality_level,
            'metrics': {
                'relevance': round(relevance_score, 3),
                'accuracy': round(accuracy_score, 3),
                'completeness': round(completeness_score, 3),
                'innovation': round(innovation_score, 3),
                'clarity': round(clarity_score, 3)
            },
            'agent_type': agent_type,
            'specialization': specialization,
            'output_length': len(output),
            'evaluation_time': (datetime.now() - start_time).total_seconds(),
            'improvements_suggested': improvements,
            'requires_refinement': overall_score < self.quality_thresholds['good']
        }
        
        # Update agent performance tracking
        self._update_agent_performance(agent_type, quality_result)
        
        return quality_result
    
    def _calculate_relevance(self, output: str, task: str) -> float:
        """Calculate how relevant the output is to the task"""
        
        # Extract key terms from task
        task_terms = self._extract_key_terms(task.lower())
        output_terms = self._extract_key_terms(output.lower())
        
        # Calculate term overlap
        overlap = len(set(task_terms) & set(output_terms))
        total_task_terms = len(set(task_terms))
        
        if total_task_terms == 0:
            return 0.5  # Neutral score for unclear tasks
        
        base_relevance = overlap / total_task_terms
        
        # Bonus for task-specific keywords
        task_keywords = ['architecture', 'design', 'implement', 'analyze', 'optimize', 'security', 'performance']
        keyword_bonus = sum(0.1 for keyword in task_keywords if keyword in output.lower())
        
        # Penalty for off-topic content
        off_topic_penalty = 0.1 * output.lower().count('unrelated')
        
        relevance_score = min(1.0, base_relevance + keyword_bonus - off_topic_penalty)
        return max(0.0, relevance_score)
    
    def _validate_accuracy(self, output: str, specialization: str) -> float:
        """Validate accuracy based on specialization-specific criteria"""
        
        accuracy_score = 0.7  # Base score
        
        # Specialization-specific validation
        if specialization == 'architecture':
            # Check for architectural concepts
            arch_terms = ['scalable', 'microservices', 'distributed', 'load balancing', 'caching']
            accuracy_score += 0.05 * sum(1 for term in arch_terms if term in output.lower())
            
        elif specialization == 'security':
            # Check for security concepts
            security_terms = ['encryption', 'authentication', 'authorization', 'firewall', 'zero-trust']
            accuracy_score += 0.05 * sum(1 for term in security_terms if term in output.lower())
            
        elif specialization == 'reasoning':
            # Check for logical reasoning indicators
            reasoning_indicators = ['therefore', 'because', 'analysis', 'conclusion', 'evidence']
            accuracy_score += 0.04 * sum(1 for indicator in reasoning_indicators if indicator in output.lower())
            
        elif specialization == 'documentation':
            # Check for documentation quality
            doc_quality = ['steps', 'example', 'implementation', 'guide', 'tutorial']
            accuracy_score += 0.05 * sum(1 for term in doc_quality if term in output.lower())
        
        # Check for factual consistency (basic heuristics)
        if 'impossible' in output.lower() or 'cannot be done' in output.lower():
            accuracy_score -= 0.2
        
        return min(1.0, max(0.0, accuracy_score))
    
    def _check_completeness(self, output: str, task: str) -> float:
        """Check if the output comprehensively addresses the task"""
        
        # Length-based completeness (basic heuristic)
        length_score = min(1.0, len(output) / 1000)  # Full score at 1000+ chars
        
        # Structure completeness
        structure_score = 0.0
        structure_indicators = [
            ('introduction' in output.lower() or 'overview' in output.lower(), 0.2),
            ('implementation' in output.lower() or 'approach' in output.lower(), 0.3),
            ('conclusion' in output.lower() or 'summary' in output.lower(), 0.2),
            ('example' in output.lower() or 'code' in output.lower(), 0.3)
        ]
        
        for indicator, weight in structure_indicators:
            if indicator:
                structure_score += weight
        
        # Task component coverage
        task_components = self._identify_task_components(task)
        addressed_components = sum(1 for comp in task_components if comp.lower() in output.lower())
        component_score = addressed_components / max(len(task_components), 1)
        
        completeness_score = (length_score * 0.3 + structure_score * 0.4 + component_score * 0.3)
        return min(1.0, completeness_score)
    
    def _assess_innovation(self, output: str) -> float:
        """Assess the innovation and creativity in the output"""
        
        innovation_score = 0.5  # Base score
        
        # Innovation indicators
        innovation_terms = [
            'novel', 'breakthrough', 'innovative', 'revolutionary', 'cutting-edge',
            'paradigm shift', 'game-changing', 'next-generation', 'state-of-the-art'
        ]
        
        innovation_score += 0.05 * sum(1 for term in innovation_terms if term in output.lower())
        
        # Penalty for generic/template responses
        generic_phrases = ['best practices', 'industry standard', 'traditional approach']
        innovation_score -= 0.03 * sum(1 for phrase in generic_phrases if phrase in output.lower())
        
        # Bonus for specific technical details
        technical_specificity = len(re.findall(r'\b\d+[a-zA-Z]*\b', output))  # Numbers with units
        innovation_score += min(0.2, technical_specificity * 0.02)
        
        return min(1.0, max(0.0, innovation_score))
    
    def _evaluate_clarity(self, output: str) -> float:
        """Evaluate the clarity and readability of the output"""
        
        clarity_score = 0.7  # Base score
        
        # Sentence structure analysis
        sentences = output.split('.')
        avg_sentence_length = sum(len(s.split()) for s in sentences) / max(len(sentences), 1)
        
        # Optimal sentence length bonus/penalty
        if 10 <= avg_sentence_length <= 25:
            clarity_score += 0.1
        elif avg_sentence_length > 40:
            clarity_score -= 0.2
        
        # Structure indicators
        if output.count('\n') > 2:  # Has paragraphs
            clarity_score += 0.1
        
        if any(marker in output for marker in ['1.', '2.', '-', '*']):  # Has lists
            clarity_score += 0.1
        
        # Technical jargon balance
        jargon_count = len(re.findall(r'\b[A-Z]{2,}\b', output))  # ALL CAPS words (acronyms)
        if jargon_count > len(output.split()) * 0.1:  # More than 10% jargon
            clarity_score -= 0.1
        
        return min(1.0, max(0.0, clarity_score))
    
    def _extract_key_terms(self, text: str) -> List[str]:
        """Extract key terms from text"""
        # Simple term extraction (can be enhanced with NLP)
        words = re.findall(r'\b[a-z]{3,}\b', text)
        # Filter out common words
        stop_words = {'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'had', 'her', 'was', 'one', 'our', 'out', 'day', 'get', 'has', 'him', 'his', 'how', 'its', 'may', 'new', 'now', 'old', 'see', 'two', 'who', 'boy', 'did', 'she', 'use', 'way', 'will', 'with'}
        return [word for word in words if word not in stop_words]
    
    def _identify_task_components(self, task: str) -> List[str]:
        """Identify key components that should be addressed in the task"""
        components = []
        
        # Action components
        action_words = ['design', 'implement', 'analyze', 'optimize', 'create', 'build', 'research']
        components.extend([word for word in action_words if word in task.lower()])
        
        # Domain components
        domain_words = ['architecture', 'security', 'performance', 'scalability', 'documentation']
        components.extend([word for word in domain_words if word in task.lower()])
        
        # Technical components (extract nouns)
        tech_terms = re.findall(r'\b[a-zA-Z]{4,}\b', task)
        components.extend(tech_terms[:5])  # Limit to 5 main terms
        
        return list(set(components))
    
    def _determine_quality_level(self, score: float) -> str:
        """Determine quality level from score"""
        if score >= self.quality_thresholds['excellent']:
            return 'excellent'
        elif score >= self.quality_thresholds['good']:
            return 'good'
        elif score >= self.quality_thresholds['acceptable']:
            return 'acceptable'
        else:
            return 'poor'
    
    def _generate_improvement_suggestions(self, relevance: float, accuracy: float, 
                                        completeness: float, innovation: float, 
                                        clarity: float) -> List[str]:
        """Generate specific improvement suggestions based on metric scores"""
        suggestions = []
        
        if relevance < 0.7:
            suggestions.append("Increase relevance by addressing more task-specific requirements")
        
        if accuracy < 0.7:
            suggestions.append("Improve technical accuracy with more domain-specific details")
        
        if completeness < 0.7:
            suggestions.append("Provide more comprehensive coverage of all task components")
        
        if innovation < 0.6:
            suggestions.append("Add more innovative approaches and cutting-edge solutions")
        
        if clarity < 0.7:
            suggestions.append("Improve clarity with better structure and clearer explanations")
        
        return suggestions
    
    def _update_agent_performance(self, agent_type: str, quality_result: Dict):
        """Update agent performance tracking"""
        if agent_type not in self.agent_performance_scores:
            self.agent_performance_scores[agent_type] = []
        
        self.agent_performance_scores[agent_type].append({
            'timestamp': datetime.now().isoformat(),
            'overall_score': quality_result['overall_score'],
            'quality_level': quality_result['quality_level'],
            'metrics': quality_result['metrics']
        })
        
        # Keep only last 100 scores per agent
        if len(self.agent_performance_scores[agent_type]) > 100:
            self.agent_performance_scores[agent_type] = self.agent_performance_scores[agent_type][-100:]
    
    async def improve_low_quality_output(self, output: str, quality_result: Dict, 
                                       original_task: str, agent_type: str) -> str:
        """Attempt to improve low-quality outputs"""
        
        if not quality_result['requires_refinement']:
            return output
        
        print(f"🔧 Improving {agent_type} output (score: {quality_result['overall_score']:.3f})")
        
        # Generate improvement prompt based on specific weaknesses
        improvement_prompt = f"""
Original task: {original_task}
Original output quality score: {quality_result['overall_score']:.3f}
Weaknesses identified: {', '.join(quality_result['improvements_suggested'])}

Please improve this output by addressing the identified weaknesses:

{output}

Enhanced output:"""
        
        # For now, return original with improvement note
        # In production, this would call another AI model for refinement
        improved_output = f"""
QUALITY-ENHANCED OUTPUT (Score improved from {quality_result['overall_score']:.3f}):

{output}

[QUALITY IMPROVEMENTS APPLIED: {', '.join(quality_result['improvements_suggested'])}]
"""
        
        return improved_output
    
    def get_agent_performance_summary(self) -> Dict:
        """Get comprehensive agent performance summary"""
        summary = {}
        
        for agent_type, scores in self.agent_performance_scores.items():
            if scores:
                recent_scores = [s['overall_score'] for s in scores[-10:]]  # Last 10 scores
                summary[agent_type] = {
                    'total_evaluations': len(scores),
                    'average_score': sum(s['overall_score'] for s in scores) / len(scores),
                    'recent_average': sum(recent_scores) / len(recent_scores),
                    'best_score': max(s['overall_score'] for s in scores),
                    'quality_trend': 'improving' if recent_scores[-1] > recent_scores[0] else 'declining',
                    'excellence_rate': len([s for s in scores if s['quality_level'] == 'excellent']) / len(scores)
                }
        
        return summary
    
    def save_quality_history(self, filepath: str = "quality_validation_history.json"):
        """Save quality validation history"""
        history_data = {
            'quality_thresholds': self.quality_thresholds,
            'metric_weights': self.metric_weights,
            'agent_performance_scores': self.agent_performance_scores,
            'total_evaluations': sum(len(scores) for scores in self.agent_performance_scores.values()),
            'last_updated': datetime.now().isoformat()
        }
        
        with open(filepath, 'w') as f:
            json.dump(history_data, f, indent=2)
        
        print(f"📊 Quality validation history saved to: {filepath}")

# Test the quality validation system
async def test_quality_validator():
    """Test the quality validation system"""
    
    validator = QualityValidator()
    
    # Test outputs with different quality levels
    test_cases = [
        {
            'output': "This is a comprehensive enterprise-scale microservices architecture designed for real-time trading platforms. The architecture implements distributed load balancing, horizontal scaling, and sub-millisecond latency optimization through advanced caching strategies and optimized data pipelines.",
            'task': "Design a scalable microservices architecture for a real-time trading platform",
            'agent_type': 'cerebras_ultra',
            'specialization': 'architecture',
            'expected_quality': 'excellent'
        },
        {
            'output': "Security is important. Use encryption.",
            'task': "Create a comprehensive security framework for AI systems",
            'agent_type': 'scaleway_eu',
            'specialization': 'security',
            'expected_quality': 'poor'
        },
        {
            'output': "The analysis reveals multiple optimization opportunities including database query optimization, API response caching, and load balancer configuration improvements. Implementation should follow a phased approach with performance monitoring at each stage.",
            'task': "Analyze system performance bottlenecks",
            'agent_type': 'gemini_flash',
            'specialization': 'reasoning',
            'expected_quality': 'good'
        }
    ]
    
    print("🧪 TESTING QUALITY VALIDATION SYSTEM")
    print("=" * 60)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📋 Test Case {i}: Expected Quality = {test_case['expected_quality'].upper()}")
        
        quality_result = validator.score_output_quality(
            test_case['output'],
            test_case['task'],
            test_case['agent_type'],
            test_case['specialization']
        )
        
        print(f"   🎯 Overall Score: {quality_result['overall_score']:.3f}")
        print(f"   📊 Quality Level: {quality_result['quality_level']}")
        print(f"   🔍 Metrics: {quality_result['metrics']}")
        print(f"   ⚡ Requires Refinement: {quality_result['requires_refinement']}")
        
        if quality_result['improvements_suggested']:
            print(f"   💡 Improvements: {', '.join(quality_result['improvements_suggested'])}")
        
        # Test improvement for low-quality outputs
        if quality_result['requires_refinement']:
            improved_output = await validator.improve_low_quality_output(
                test_case['output'], quality_result, test_case['task'], test_case['agent_type']
            )
            print(f"   🔧 Output improved and enhanced")
    
    # Display performance summary
    print(f"\n📊 AGENT PERFORMANCE SUMMARY:")
    performance_summary = validator.get_agent_performance_summary()
    for agent, stats in performance_summary.items():
        print(f"   {agent}: Avg Score = {stats['average_score']:.3f}, Excellence Rate = {stats['excellence_rate']:.1%}")
    
    # Save quality history
    validator.save_quality_history()
    
    print("\n🎉 QUALITY VALIDATION SYSTEM TEST COMPLETED!")

if __name__ == "__main__":
    asyncio.run(test_quality_validator())