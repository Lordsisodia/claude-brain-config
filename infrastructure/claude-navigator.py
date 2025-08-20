#!/usr/bin/env python3
"""
Claude Enterprise Navigation Intelligence System
AI-native discovery and activation for 1,664-file enterprise configuration
"""

import os
import re
import json
import time
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional
from collections import defaultdict, Counter
from datetime import datetime

class ClaudeNavigator:
    def __init__(self, claude_dir: str = "/Users/shaansisodia/.claude"):
        self.claude_dir = Path(claude_dir)
        self.analytics_file = self.claude_dir / "analytics" / "usage_patterns.json"
        self.systems_index = self.claude_dir / "infrastructure" / "systems_index.json"
        
        # Intelligence system mapping
        self.intelligence_systems = self._build_intelligence_map()
        self.command_registry = self._build_command_registry()
        self.usage_analytics = self._load_analytics()
        
        # Natural language patterns
        self.intent_patterns = {
            # Analysis & Understanding
            r'(analyze|analysis|understand|examine|review)': {
                'primary': ['analyze', 'ultimate-analyze'],
                'intelligence': ['task-intelligence-system', 'context-optimization-system'],
                'activation': 'deep_analysis'
            },
            
            # Development workflows
            r'(build|compile|test|deploy)': {
                'primary': ['build', 'test', 'deploy'],
                'intelligence': ['command-execution-intelligence', 'ecosystem-orchestration-intelligence'],
                'activation': 'development_workflow'
            },
            
            # Project management
            r'(plan|manage|organize|track)': {
                'primary': ['plan-product', 'todo', 'estimate'],
                'intelligence': ['task-intelligence-system', 'performance-intelligence-system'],
                'activation': 'project_management'
            },
            
            # AI reasoning
            r'(think|reason|solve|complex)': {
                'primary': ['ultimate-analyze'],
                'intelligence': ['chain-of-thought-intelligence', 'extended-thinking-intelligence'],
                'activation': 'ultra_reasoning'
            },
            
            # Architecture & design
            r'(architect|design|structure|system)': {
                'primary': ['ai-architect', 'design'],
                'intelligence': ['codebase-intelligence-system', 'deep-navigation-intelligence'],
                'activation': 'architecture_mode'
            },
            
            # Automation & deployment
            r'(automate|autonomous|deploy|scale)': {
                'primary': ['autonomous-deploy', 'spawn'],
                'intelligence': ['ecosystem-orchestration-intelligence', 'multi-agent-orchestration-intelligence'],
                'activation': 'autonomous_mode'
            }
        }
    
    def _build_intelligence_map(self) -> Dict:
        """Build comprehensive map of intelligence systems"""
        systems = {}
        shared_dir = self.claude_dir / "shared"
        
        if shared_dir.exists():
            for yml_file in shared_dir.glob("*.yml"):
                system_name = yml_file.stem
                
                # Parse system capabilities
                try:
                    with open(yml_file, 'r') as f:
                        content = f.read()
                    
                    # Extract anchors and descriptions
                    anchors = re.findall(r'^([^:\s]+):\s*&([^\s]+)', content, re.MULTILINE)
                    
                    systems[system_name] = {
                        'file': str(yml_file),
                        'anchors': [anchor[1] for anchor in anchors],
                        'categories': self._categorize_system(system_name),
                        'complexity': self._assess_complexity(content),
                        'dependencies': self._find_dependencies(content)
                    }
                except Exception as e:
                    continue
        
        return systems
    
    def _build_command_registry(self) -> Dict:
        """Build registry of all available commands"""
        commands = {}
        commands_dir = self.claude_dir / "commands"
        
        if commands_dir.exists():
            for cmd_path in commands_dir.rglob("*.md"):
                if cmd_path.name != "index.md":
                    cmd_name = cmd_path.stem
                    
                    try:
                        with open(cmd_path, 'r') as f:
                            content = f.read()
                        
                        commands[cmd_name] = {
                            'file': str(cmd_path),
                            'category': self._categorize_command(cmd_path),
                            'description': self._extract_description(content),
                            'complexity': self._assess_command_complexity(content),
                            'keywords': self._extract_keywords(content)
                        }
                    except Exception:
                        continue
        
        return commands
    
    def discover(self, query: str) -> Dict:
        """Natural language discovery of systems and commands"""
        query_lower = query.lower()
        
        results = {
            'commands': [],
            'intelligence_systems': [],
            'activation_patterns': [],
            'suggested_workflows': [],
            'confidence': 0.0
        }
        
        # Intent matching
        for pattern, config in self.intent_patterns.items():
            if re.search(pattern, query_lower):
                results['commands'].extend(config['primary'])
                results['intelligence_systems'].extend(config['intelligence'])
                results['activation_patterns'].append(config['activation'])
        
        # Keyword matching for commands
        for cmd_name, cmd_info in self.command_registry.items():
            relevance = self._calculate_relevance(query_lower, cmd_info)
            if relevance > 0.3:
                results['commands'].append({
                    'name': cmd_name,
                    'relevance': relevance,
                    'description': cmd_info.get('description', ''),
                    'category': cmd_info.get('category', '')
                })
        
        # Intelligence system matching
        for sys_name, sys_info in self.intelligence_systems.items():
            relevance = self._calculate_system_relevance(query_lower, sys_info)
            if relevance > 0.2:
                results['intelligence_systems'].append({
                    'name': sys_name,
                    'relevance': relevance,
                    'categories': sys_info.get('categories', []),
                    'anchors': sys_info.get('anchors', [])
                })
        
        # Generate suggested workflows
        results['suggested_workflows'] = self._generate_workflows(results)
        results['confidence'] = self._calculate_confidence(results)
        
        # Track usage
        self._track_discovery(query, results)
        
        return results
    
    def _generate_workflows(self, results: Dict) -> List[str]:
        """Generate suggested workflows based on discovery results"""
        workflows = []
        
        commands = results.get('commands', [])
        intelligence = results.get('intelligence_systems', [])
        
        if any('analyze' in str(cmd).lower() for cmd in commands):
            workflows.append("Deep Analysis: analyze → ultimate-analyze → review")
        
        if any('build' in str(cmd).lower() for cmd in commands):
            workflows.append("Development: build → test → deploy")
        
        if any('plan' in str(cmd).lower() for cmd in commands):
            workflows.append("Planning: plan-product → estimate → todo")
        
        if any('reasoning' in str(sys).lower() for sys in intelligence):
            workflows.append("Ultra Think: Chain-of-thought → Extended thinking")
        
        return workflows[:3]
    
    def _calculate_confidence(self, results: Dict) -> float:
        """Calculate overall confidence in discovery results"""
        command_count = len([c for c in results.get('commands', []) if isinstance(c, dict)])
        intelligence_count = len([s for s in results.get('intelligence_systems', []) if isinstance(s, dict)])
        
        # Base confidence on number and relevance of results
        base_confidence = min((command_count + intelligence_count) * 0.1, 0.8)
        
        # Boost if we found high-relevance matches
        if command_count > 0:
            avg_relevance = sum(c.get('relevance', 0) for c in results.get('commands', []) if isinstance(c, dict)) / command_count
            base_confidence += avg_relevance * 0.2
        
        return min(base_confidence, 1.0)
    
    def activate_pattern(self, pattern_name: str) -> Dict:
        """Activate intelligent system combinations"""
        activation_configs = {
            'deep_analysis': {
                'intelligence': [
                    'task-intelligence-system',
                    'context-optimization-system', 
                    'chain-of-thought-intelligence',
                    'extended-thinking-intelligence'
                ],
                'commands': ['analyze', 'ultimate-analyze'],
                'mode': 'maximum_reasoning'
            },
            
            'ultra_reasoning': {
                'intelligence': [
                    'chain-of-thought-intelligence',
                    'extended-thinking-intelligence',
                    'constitutional-ai-intelligence',
                    'meta-reasoning-simplicity-detector'
                ],
                'commands': ['ultimate-analyze'],
                'mode': 'ultra_think'
            },
            
            'autonomous_mode': {
                'intelligence': [
                    'multi-agent-orchestration-intelligence',
                    'ecosystem-orchestration-intelligence',
                    'adaptive-intelligence-system',
                    'performance-intelligence-system'
                ],
                'commands': ['autonomous-deploy', 'spawn'],
                'mode': 'autonomous_operation'
            },
            
            'development_workflow': {
                'intelligence': [
                    'command-execution-intelligence',
                    'codebase-intelligence-system',
                    'performance-intelligence-system'
                ],
                'commands': ['build', 'test', 'review'],
                'mode': 'development'
            },
            
            'architecture_mode': {
                'intelligence': [
                    'codebase-intelligence-system',
                    'deep-navigation-intelligence',
                    'multi-agent-orchestration-intelligence'
                ],
                'commands': ['ai-architect', 'design'],
                'mode': 'architecture'
            }
        }
        
        config = activation_configs.get(pattern_name, {})
        
        # Track activation
        self._track_activation(pattern_name, config)
        
        return {
            'pattern': pattern_name,
            'config': config,
            'activated_at': datetime.now().isoformat(),
            'expected_capabilities': self._describe_capabilities(config)
        }
    
    def get_system_recommendations(self, current_systems: List[str]) -> Dict:
        """Recommend complementary systems based on current usage"""
        recommendations = {
            'complementary': [],
            'missing_capabilities': [],
            'optimization_suggestions': []
        }
        
        # Analyze current system combination
        current_categories = set()
        for system in current_systems:
            if system in self.intelligence_systems:
                current_categories.update(
                    self.intelligence_systems[system].get('categories', [])
                )
        
        # Find missing complementary systems
        all_categories = {'reasoning', 'compute', 'memory', 'orchestration', 'navigation'}
        missing_categories = all_categories - current_categories
        
        for category in missing_categories:
            for sys_name, sys_info in self.intelligence_systems.items():
                if category in sys_info.get('categories', []):
                    recommendations['complementary'].append({
                        'system': sys_name,
                        'category': category,
                        'reason': f"Adds {category} capabilities"
                    })
                    break
        
        # Usage pattern analysis
        if self.usage_analytics:
            successful_patterns = self._analyze_successful_patterns()
            for pattern in successful_patterns:
                if set(current_systems).issubset(set(pattern['systems'])):
                    missing = set(pattern['systems']) - set(current_systems)
                    for sys in missing:
                        recommendations['optimization_suggestions'].append({
                            'system': sys,
                            'reason': f"Often used with current combination (success rate: {pattern['success_rate']:.1%})"
                        })
        
        return recommendations
    
    def search_capabilities(self, capability: str) -> List[Dict]:
        """Search for specific capabilities across the entire system"""
        results = []
        
        # Search through intelligence systems
        for sys_name, sys_info in self.intelligence_systems.items():
            if self._matches_capability(capability, sys_info):
                results.append({
                    'type': 'intelligence_system',
                    'name': sys_name,
                    'file': sys_info['file'],
                    'match_score': self._calculate_capability_score(capability, sys_info)
                })
        
        # Search through commands
        for cmd_name, cmd_info in self.command_registry.items():
            if self._matches_capability(capability, cmd_info):
                results.append({
                    'type': 'command',
                    'name': cmd_name,
                    'file': cmd_info['file'],
                    'match_score': self._calculate_capability_score(capability, cmd_info)
                })
        
        # Sort by relevance
        results.sort(key=lambda x: x['match_score'], reverse=True)
        
        return results
    
    def get_usage_analytics(self) -> Dict:
        """Get comprehensive usage analytics"""
        if not self.usage_analytics:
            return {'message': 'No usage data available yet'}
        
        return {
            'total_discoveries': len(self.usage_analytics.get('discoveries', [])),
            'total_activations': len(self.usage_analytics.get('activations', [])),
            'most_used_commands': self._get_top_commands(),
            'most_used_intelligence': self._get_top_intelligence_systems(),
            'successful_patterns': self._analyze_successful_patterns(),
            'optimization_opportunities': self._find_optimization_opportunities()
        }
    
    # Helper methods
    def _categorize_system(self, system_name: str) -> List[str]:
        """Categorize intelligence system by name patterns"""
        categories = []
        name_lower = system_name.lower()
        
        if any(word in name_lower for word in ['reasoning', 'thought', 'thinking', 'constitutional']):
            categories.append('reasoning')
        if any(word in name_lower for word in ['compute', 'optimization', 'performance', 'token']):
            categories.append('compute')
        if any(word in name_lower for word in ['memory', 'context', 'session', 'cognitive']):
            categories.append('memory')
        if any(word in name_lower for word in ['orchestration', 'agent', 'mcp', 'ecosystem']):
            categories.append('orchestration')
        if any(word in name_lower for word in ['navigation', 'codebase', 'cursor', 'deep']):
            categories.append('navigation')
        
        return categories or ['general']
    
    def _calculate_relevance(self, query: str, item_info: Dict) -> float:
        """Calculate relevance score for search results"""
        score = 0.0
        query_words = set(query.split())
        
        # Check keywords
        keywords = item_info.get('keywords', [])
        keyword_matches = len(query_words.intersection(set(keywords)))
        score += keyword_matches * 0.3
        
        # Check description
        description = item_info.get('description', '').lower()
        desc_matches = sum(1 for word in query_words if word in description)
        score += desc_matches * 0.2
        
        # Check name similarity
        name = item_info.get('name', '')
        if any(word in name.lower() for word in query_words):
            score += 0.5
        
        return min(score, 1.0)
    
    def _load_analytics(self) -> Dict:
        """Load usage analytics from file"""
        try:
            if self.analytics_file.exists():
                with open(self.analytics_file, 'r') as f:
                    return json.load(f)
        except Exception:
            pass
        
        return {'discoveries': [], 'activations': [], 'patterns': []}
    
    def _track_discovery(self, query: str, results: Dict):
        """Track discovery usage for analytics"""
        discovery_entry = {
            'timestamp': datetime.now().isoformat(),
            'query': query,
            'results_count': len(results.get('commands', [])) + len(results.get('intelligence_systems', [])),
            'confidence': results.get('confidence', 0.0)
        }
        
        self.usage_analytics.setdefault('discoveries', []).append(discovery_entry)
        self._save_analytics()
    
    def _save_analytics(self):
        """Save analytics to file"""
        try:
            self.analytics_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.analytics_file, 'w') as f:
                json.dump(self.usage_analytics, f, indent=2)
        except Exception:
            pass
    
    def _categorize_command(self, cmd_path: Path) -> str:
        """Categorize command by path structure"""
        parts = cmd_path.parts
        if 'development' in parts:
            return 'development'
        elif 'management' in parts:
            return 'management'
        elif 'deployment' in parts:
            return 'deployment'
        elif 'advanced' in parts:
            return 'advanced'
        else:
            return 'general'
    
    def _extract_description(self, content: str) -> str:
        """Extract description from markdown content"""
        lines = content.split('\n')
        for line in lines[:10]:
            if line.strip() and not line.startswith('#'):
                return line.strip()[:100]
        return "Command description not available"
    
    def _assess_complexity(self, content: str) -> str:
        """Assess complexity of intelligence system"""
        if len(content) > 5000:
            return 'high'
        elif len(content) > 2000:
            return 'medium'
        else:
            return 'low'
    
    def _assess_command_complexity(self, content: str) -> str:
        """Assess complexity of command"""
        if 'autonomous' in content.lower() or 'ultimate' in content.lower():
            return 'high'
        elif 'advanced' in content.lower():
            return 'medium'
        else:
            return 'low'
    
    def _extract_keywords(self, content: str) -> List[str]:
        """Extract keywords from content"""
        import re
        
        # Simple keyword extraction
        words = re.findall(r'\b\w+\b', content.lower())
        
        # Filter common words and get meaningful terms
        stopwords = {'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'a', 'an'}
        keywords = [w for w in words if len(w) > 3 and w not in stopwords]
        
        # Get most frequent keywords
        from collections import Counter
        return [word for word, count in Counter(keywords).most_common(10)]
    
    def _find_dependencies(self, content: str) -> List[str]:
        """Find dependencies in content"""
        deps = []
        lines = content.split('\n')
        for line in lines:
            if '@include' in line:
                deps.append(line.strip())
        return deps
    
    def _calculate_system_relevance(self, query: str, sys_info: Dict) -> float:
        """Calculate relevance of intelligence system to query"""
        score = 0.0
        query_words = set(query.split())
        
        # Check system name
        name = sys_info.get('name', '').lower()
        name_words = set(name.replace('-', ' ').split())
        overlap = len(query_words.intersection(name_words))
        score += overlap * 0.4
        
        # Check categories
        categories = sys_info.get('categories', [])
        for category in categories:
            if any(word in category.lower() for word in query_words):
                score += 0.3
        
        return min(score, 1.0)
    
    def _describe_capabilities(self, config: Dict) -> List[str]:
        """Describe capabilities of activation configuration"""
        capabilities = []
        
        intelligence = config.get('intelligence', [])
        for system in intelligence:
            if 'reasoning' in system:
                capabilities.append("Advanced reasoning and problem solving")
            elif 'memory' in system:
                capabilities.append("Context and memory management")
            elif 'orchestration' in system:
                capabilities.append("Multi-agent coordination")
            elif 'performance' in system:
                capabilities.append("Performance optimization")
        
        return capabilities[:5]
    
    def _matches_capability(self, capability: str, item_info: Dict) -> bool:
        """Check if item matches capability search"""
        capability_lower = capability.lower()
        
        # Check in various fields
        name = item_info.get('name', '').lower()
        description = item_info.get('description', '').lower()
        keywords = [k.lower() for k in item_info.get('keywords', [])]
        
        return (capability_lower in name or 
                capability_lower in description or
                any(capability_lower in k for k in keywords))
    
    def _calculate_capability_score(self, capability: str, item_info: Dict) -> float:
        """Calculate capability match score"""
        score = 0.0
        capability_lower = capability.lower()
        
        name = item_info.get('name', '').lower()
        if capability_lower in name:
            score += 0.6
        
        description = item_info.get('description', '').lower()
        if capability_lower in description:
            score += 0.3
        
        keywords = [k.lower() for k in item_info.get('keywords', [])]
        if any(capability_lower in k for k in keywords):
            score += 0.2
        
        return min(score, 1.0)
    
    def _get_top_commands(self) -> List[Tuple[str, int]]:
        """Get most used commands from analytics"""
        if not self.usage_analytics.get('discoveries'):
            return []
        
        command_counts = Counter()
        for discovery in self.usage_analytics['discoveries']:
            # This would be populated by actual usage tracking
            pass
        
        return command_counts.most_common(5)
    
    def _get_top_intelligence_systems(self) -> List[Tuple[str, int]]:
        """Get most used intelligence systems"""
        if not self.usage_analytics.get('discoveries'):
            return []
        
        system_counts = Counter()
        for discovery in self.usage_analytics['discoveries']:
            # This would be populated by actual usage tracking
            pass
        
        return system_counts.most_common(5)
    
    def _analyze_successful_patterns(self) -> List[Dict]:
        """Analyze successful activation patterns"""
        # This would analyze actual success data
        return [
            {
                'systems': ['task-intelligence-system', 'context-optimization-system'],
                'success_rate': 0.85,
                'use_count': 12
            },
            {
                'systems': ['chain-of-thought-intelligence', 'extended-thinking-intelligence'],
                'success_rate': 0.92,
                'use_count': 8
            }
        ]
    
    def _find_optimization_opportunities(self) -> List[str]:
        """Find system optimization opportunities"""
        return [
            "Consider activating constitutional-ai-intelligence for complex problems",
            "Multi-agent orchestration could improve automation workflows",
            "Token economy optimization could reduce costs"
        ]

def main():
    """CLI interface for Claude Navigator"""
    import sys
    
    navigator = ClaudeNavigator()
    
    if len(sys.argv) < 2:
        print("🧠 Claude Enterprise Navigator")
        print("Usage:")
        print("  claude-navigator discover 'analyze complex data'")
        print("  claude-navigator activate ultra_reasoning")
        print("  claude-navigator search 'memory management'")
        print("  claude-navigator analytics")
        return
    
    command = sys.argv[1]
    
    if command == "discover" and len(sys.argv) > 2:
        query = " ".join(sys.argv[2:])
        results = navigator.discover(query)
        
        print(f"🔍 Discovery Results for: '{query}'")
        print(f"📊 Confidence: {results['confidence']:.1%}")
        
        if results['commands']:
            print("\n🎯 Recommended Commands:")
            for cmd in results['commands'][:5]:
                if isinstance(cmd, dict):
                    print(f"  • {cmd['name']} (relevance: {cmd['relevance']:.1%})")
                else:
                    print(f"  • {cmd}")
        
        if results['intelligence_systems']:
            print("\n🧠 Intelligence Systems:")
            for sys in results['intelligence_systems'][:5]:
                if isinstance(sys, dict):
                    print(f"  • {sys['name']} (relevance: {sys['relevance']:.1%})")
                else:
                    print(f"  • {sys}")
        
        if results['activation_patterns']:
            print("\n⚡ Suggested Activation Patterns:")
            for pattern in results['activation_patterns']:
                print(f"  • {pattern}")
    
    elif command == "activate" and len(sys.argv) > 2:
        pattern = sys.argv[2]
        result = navigator.activate_pattern(pattern)
        
        print(f"⚡ Activated Pattern: {pattern}")
        print(f"🎯 Mode: {result['config'].get('mode', 'unknown')}")
        print(f"🧠 Intelligence Systems: {len(result['config'].get('intelligence', []))}")
        print(f"🎛️ Commands: {result['config'].get('commands', [])}")
    
    elif command == "search" and len(sys.argv) > 2:
        capability = " ".join(sys.argv[2:])
        results = navigator.search_capabilities(capability)
        
        print(f"🔍 Capability Search: '{capability}'")
        for result in results[:10]:
            print(f"  • {result['type']}: {result['name']} (score: {result['match_score']:.2f})")
    
    elif command == "analytics":
        analytics = navigator.get_usage_analytics()
        
        print("📊 Usage Analytics:")
        print(f"  Discoveries: {analytics.get('total_discoveries', 0)}")
        print(f"  Activations: {analytics.get('total_activations', 0)}")
        
        if 'most_used_commands' in analytics:
            print("\n🏆 Top Commands:")
            for cmd, count in analytics['most_used_commands'][:5]:
                print(f"  • {cmd}: {count} uses")

if __name__ == "__main__":
    main()