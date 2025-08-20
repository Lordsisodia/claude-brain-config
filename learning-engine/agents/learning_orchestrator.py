#!/usr/bin/env python3
"""
Learning Orchestrator Agent
Master coordinator for all learning activities across the system
"""

import json
import time
import threading
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
import uuid
import asyncio
from dataclasses import dataclass, asdict
from typing import Dict, List, Any, Optional

@dataclass
class LearningEvent:
    event_id: str
    event_type: str
    source: str
    data: Dict[str, Any]
    timestamp: str
    priority: int = 5  # 1-10, 10 being highest

@dataclass
class LearningPattern:
    pattern_id: str
    pattern_type: str
    confidence: float
    data: Dict[str, Any]
    first_seen: str
    last_updated: str
    frequency: int = 1

@dataclass
class OptimizationSuggestion:
    suggestion_id: str
    target_system: str
    optimization_type: str
    description: str
    expected_benefit: str
    confidence: float
    implementation_complexity: str
    created_at: str

class LearningOrchestrator:
    def __init__(self, learning_home=None):
        self.learning_home = Path(learning_home or Path.home() / ".learning-engine")
        self.orchestrator_id = str(uuid.uuid4())
        self.is_running = False
        
        # Learning state
        self.active_patterns = {}
        self.recent_events = []
        self.optimization_queue = []
        self.agent_registry = {}
        
        # Create directories
        for subdir in ["orchestrator", "events", "patterns", "optimizations", "agents"]:
            (self.learning_home / subdir).mkdir(parents=True, exist_ok=True)
        
        print(f"🧠 Learning Orchestrator initialized")
        print(f"🆔 Orchestrator ID: {self.orchestrator_id}")
        print(f"📂 Learning home: {self.learning_home}")

    async def start_orchestration(self):
        """Start the learning orchestration system"""
        self.is_running = True
        
        print("🚀 Starting Learning Orchestration System...")
        
        # Initialize components
        await self._initialize_knowledge_base()
        await self._register_learning_agents()
        await self._start_pattern_synthesis()
        
        # Start orchestration loops
        tasks = [
            asyncio.create_task(self._event_processing_loop()),
            asyncio.create_task(self._pattern_synthesis_loop()),
            asyncio.create_task(self._optimization_generation_loop()),
            asyncio.create_task(self._agent_coordination_loop()),
            asyncio.create_task(self._performance_monitoring_loop())
        ]
        
        print("✅ Learning Orchestration System active!")
        
        try:
            await asyncio.gather(*tasks)
        except KeyboardInterrupt:
            await self.stop_orchestration()

    async def stop_orchestration(self):
        """Stop orchestration and save state"""
        print("🛑 Stopping Learning Orchestration...")
        self.is_running = False
        await self._save_orchestration_state()
        print("💾 Orchestration state saved!")

    async def _initialize_knowledge_base(self):
        """Initialize the central knowledge base"""
        print("📚 Initializing Knowledge Base...")
        
        knowledge_base = {
            "orchestrator_id": self.orchestrator_id,
            "initialized_at": datetime.now().isoformat(),
            "active_patterns": {},
            "pattern_relationships": {},
            "optimization_history": [],
            "learning_metrics": {
                "patterns_discovered": 0,
                "optimizations_generated": 0,
                "optimizations_applied": 0,
                "learning_efficiency": 0.0
            }
        }
        
        kb_file = self.learning_home / "orchestrator" / "knowledge_base.json"
        with open(kb_file, 'w') as f:
            json.dump(knowledge_base, f, indent=2)
        
        print("✅ Knowledge Base initialized")

    async def _register_learning_agents(self):
        """Register and coordinate learning agents"""
        print("🤖 Registering Learning Agents...")
        
        # Define available learning agents
        learning_agents = {
            "session_observer": {
                "type": "SESSION_OBSERVER",
                "description": "Monitors TMUX brain sessions",
                "status": "available",
                "capabilities": ["session_monitoring", "command_tracking", "window_analysis"]
            },
            "performance_analyzer": {
                "type": "PERFORMANCE_ANALYZER",
                "description": "Analyzes system performance metrics",
                "status": "available",
                "capabilities": ["metric_collection", "bottleneck_detection", "trend_analysis"]
            },
            "pattern_recognizer": {
                "type": "PATTERN_RECOGNIZER",
                "description": "Identifies patterns in user behavior and system usage",
                "status": "available",
                "capabilities": ["pattern_detection", "correlation_analysis", "trend_prediction"]
            },
            "config_optimizer": {
                "type": "CONFIG_OPTIMIZER",
                "description": "Optimizes system configurations based on usage patterns",
                "status": "available",
                "capabilities": ["config_analysis", "optimization_suggestion", "auto_tuning"]
            },
            "predictive_engine": {
                "type": "PREDICTIVE_ENGINE",
                "description": "Predicts future needs and optimizations",
                "status": "available",
                "capabilities": ["need_prediction", "resource_forecasting", "proactive_optimization"]
            }
        }
        
        self.agent_registry = learning_agents
        
        # Save agent registry
        registry_file = self.learning_home / "agents" / "registry.json"
        with open(registry_file, 'w') as f:
            json.dump(learning_agents, f, indent=2)
        
        print(f"✅ Registered {len(learning_agents)} learning agents")

    async def _start_pattern_synthesis(self):
        """Initialize pattern synthesis engine"""
        print("🔄 Starting Pattern Synthesis Engine...")
        
        synthesis_config = {
            "synthesis_interval": 30,  # seconds
            "pattern_correlation_threshold": 0.7,
            "optimization_generation_threshold": 0.8,
            "learning_rate": 0.1,
            "pattern_decay_rate": 0.05
        }
        
        config_file = self.learning_home / "orchestrator" / "synthesis_config.json"
        with open(config_file, 'w') as f:
            json.dump(synthesis_config, f, indent=2)
        
        print("✅ Pattern Synthesis Engine ready")

    async def _event_processing_loop(self):
        """Process incoming learning events"""
        while self.is_running:
            try:
                # Collect events from all sources
                events = await self._collect_learning_events()
                
                for event in events:
                    await self._process_learning_event(event)
                
                # Clean up old events
                await self._cleanup_old_events()
                
            except Exception as e:
                print(f"⚠️ Event processing error: {e}")
            
            await asyncio.sleep(1)

    async def _pattern_synthesis_loop(self):
        """Synthesize patterns from collected events"""
        while self.is_running:
            try:
                # Analyze recent events for patterns
                patterns = await self._synthesize_patterns()
                
                for pattern in patterns:
                    await self._update_pattern_database(pattern)
                
                # Generate pattern relationships
                await self._update_pattern_relationships()
                
            except Exception as e:
                print(f"⚠️ Pattern synthesis error: {e}")
            
            await asyncio.sleep(30)

    async def _optimization_generation_loop(self):
        """Generate optimization suggestions based on patterns"""
        while self.is_running:
            try:
                # Analyze patterns for optimization opportunities
                optimizations = await self._generate_optimizations()
                
                for optimization in optimizations:
                    await self._queue_optimization(optimization)
                
                # Process optimization queue
                await self._process_optimization_queue()
                
            except Exception as e:
                print(f"⚠️ Optimization generation error: {e}")
            
            await asyncio.sleep(60)

    async def _agent_coordination_loop(self):
        """Coordinate learning agents and distribute tasks"""
        while self.is_running:
            try:
                # Check agent status
                await self._update_agent_status()
                
                # Distribute learning tasks
                await self._distribute_learning_tasks()
                
                # Collect agent results
                await self._collect_agent_results()
                
            except Exception as e:
                print(f"⚠️ Agent coordination error: {e}")
            
            await asyncio.sleep(10)

    async def _performance_monitoring_loop(self):
        """Monitor learning system performance"""
        while self.is_running:
            try:
                # Collect performance metrics
                metrics = await self._collect_performance_metrics()
                
                # Update learning efficiency
                await self._update_learning_efficiency(metrics)
                
                # Generate performance reports
                await self._generate_performance_report(metrics)
                
            except Exception as e:
                print(f"⚠️ Performance monitoring error: {e}")
            
            await asyncio.sleep(120)

    async def _collect_learning_events(self):
        """Collect events from all learning sources"""
        events = []
        
        # Collect from session observers
        session_events = await self._collect_session_events()
        events.extend(session_events)
        
        # Collect from TMUX brain monitoring
        tmux_events = await self._collect_tmux_events()
        events.extend(tmux_events)
        
        # Collect from performance monitors
        performance_events = await self._collect_performance_events()
        events.extend(performance_events)
        
        return events

    async def _collect_session_events(self):
        """Collect events from session observers"""
        events = []
        sessions_dir = self.learning_home / "sessions"
        
        if sessions_dir.exists():
            for session_file in sessions_dir.glob("*.jsonl"):
                try:
                    with open(session_file, 'r') as f:
                        lines = f.readlines()
                        # Get recent events (last 10)
                        for line in lines[-10:]:
                            event_data = json.loads(line)
                            event = LearningEvent(
                                event_id=str(uuid.uuid4()),
                                event_type="session_event",
                                source="session_observer",
                                data=event_data,
                                timestamp=datetime.now().isoformat(),
                                priority=6
                            )
                            events.append(event)
                except Exception as e:
                    print(f"⚠️ Error reading session file {session_file}: {e}")
        
        return events

    async def _collect_tmux_events(self):
        """Collect events from TMUX brain monitoring"""
        events = []
        
        try:
            # Check if BRAIN-MAIN session exists
            result = subprocess.run(
                ["tmux", "has-session", "-t", "BRAIN-MAIN"],
                capture_output=True, text=True, timeout=5
            )
            
            if result.returncode == 0:
                # Get session info
                session_info = subprocess.run(
                    ["tmux", "list-windows", "-t", "BRAIN-MAIN", "-F", "#{window_index}:#{window_name}"],
                    capture_output=True, text=True, timeout=5
                )
                
                if session_info.returncode == 0:
                    event = LearningEvent(
                        event_id=str(uuid.uuid4()),
                        event_type="tmux_session_active",
                        source="tmux_monitor",
                        data={"windows": session_info.stdout.strip().split('\n')},
                        timestamp=datetime.now().isoformat(),
                        priority=5
                    )
                    events.append(event)
                    
        except subprocess.TimeoutExpired:
            pass
        except Exception as e:
            print(f"⚠️ TMUX monitoring error: {e}")
        
        return events

    async def _collect_performance_events(self):
        """Collect performance-related events"""
        events = []
        
        # Collect system performance metrics
        try:
            # Memory usage
            import psutil
            memory_percent = psutil.virtual_memory().percent
            cpu_percent = psutil.cpu_percent(interval=1)
            
            event = LearningEvent(
                event_id=str(uuid.uuid4()),
                event_type="system_performance",
                source="performance_monitor",
                data={
                    "memory_percent": memory_percent,
                    "cpu_percent": cpu_percent,
                    "timestamp": datetime.now().isoformat()
                },
                timestamp=datetime.now().isoformat(),
                priority=4
            )
            events.append(event)
            
        except ImportError:
            # psutil not available, skip system metrics
            pass
        except Exception as e:
            print(f"⚠️ Performance monitoring error: {e}")
        
        return events

    async def _process_learning_event(self, event: LearningEvent):
        """Process a single learning event"""
        # Add to recent events
        self.recent_events.append(event)
        
        # Keep only recent events (last 1000)
        if len(self.recent_events) > 1000:
            self.recent_events = self.recent_events[-1000:]
        
        # Log event
        event_file = self.learning_home / "events" / f"events_{datetime.now().strftime('%Y%m%d')}.jsonl"
        with open(event_file, 'a') as f:
            f.write(json.dumps(asdict(event)) + '\n')

    async def _synthesize_patterns(self):
        """Synthesize patterns from recent events"""
        patterns = []
        
        if len(self.recent_events) < 10:
            return patterns
        
        # Pattern 1: Command frequency patterns
        command_patterns = self._analyze_command_patterns()
        if command_patterns:
            pattern = LearningPattern(
                pattern_id=str(uuid.uuid4()),
                pattern_type="command_frequency",
                confidence=0.8,
                data=command_patterns,
                first_seen=datetime.now().isoformat(),
                last_updated=datetime.now().isoformat()
            )
            patterns.append(pattern)
        
        # Pattern 2: Session activity patterns
        activity_patterns = self._analyze_activity_patterns()
        if activity_patterns:
            pattern = LearningPattern(
                pattern_id=str(uuid.uuid4()),
                pattern_type="activity_rhythm",
                confidence=0.7,
                data=activity_patterns,
                first_seen=datetime.now().isoformat(),
                last_updated=datetime.now().isoformat()
            )
            patterns.append(pattern)
        
        # Pattern 3: Performance correlation patterns
        performance_patterns = self._analyze_performance_patterns()
        if performance_patterns:
            pattern = LearningPattern(
                pattern_id=str(uuid.uuid4()),
                pattern_type="performance_correlation",
                confidence=0.9,
                data=performance_patterns,
                first_seen=datetime.now().isoformat(),
                last_updated=datetime.now().isoformat()
            )
            patterns.append(pattern)
        
        return patterns

    def _analyze_command_patterns(self):
        """Analyze command execution patterns"""
        command_events = [e for e in self.recent_events if e.event_type == "session_event"]
        
        if not command_events:
            return None
        
        command_counts = {}
        for event in command_events:
            if 'command' in event.data.get('data', {}):
                cmd = event.data['data']['command']
                command_counts[cmd] = command_counts.get(cmd, 0) + 1
        
        if command_counts:
            return {
                "most_frequent_commands": sorted(command_counts.items(), key=lambda x: x[1], reverse=True)[:10],
                "total_commands": sum(command_counts.values()),
                "unique_commands": len(command_counts)
            }
        
        return None

    def _analyze_activity_patterns(self):
        """Analyze activity rhythm patterns"""
        if len(self.recent_events) < 5:
            return None
        
        # Analyze event timing
        timestamps = [datetime.fromisoformat(e.timestamp.replace('Z', '+00:00')) for e in self.recent_events]
        intervals = []
        
        for i in range(1, len(timestamps)):
            interval = (timestamps[i] - timestamps[i-1]).total_seconds()
            intervals.append(interval)
        
        if intervals:
            avg_interval = sum(intervals) / len(intervals)
            return {
                "average_activity_interval": avg_interval,
                "activity_burst_detected": any(interval < 1 for interval in intervals),
                "total_events": len(self.recent_events)
            }
        
        return None

    def _analyze_performance_patterns(self):
        """Analyze performance correlation patterns"""
        perf_events = [e for e in self.recent_events if e.event_type == "system_performance"]
        
        if len(perf_events) < 3:
            return None
        
        memory_values = [e.data['memory_percent'] for e in perf_events]
        cpu_values = [e.data['cpu_percent'] for e in perf_events]
        
        avg_memory = sum(memory_values) / len(memory_values)
        avg_cpu = sum(cpu_values) / len(cpu_values)
        
        return {
            "average_memory_usage": avg_memory,
            "average_cpu_usage": avg_cpu,
            "performance_stable": max(memory_values) - min(memory_values) < 20,
            "sample_count": len(perf_events)
        }

    async def _update_pattern_database(self, pattern: LearningPattern):
        """Update the pattern database with new patterns"""
        patterns_file = self.learning_home / "patterns" / f"patterns_{datetime.now().strftime('%Y%m%d')}.json"
        
        # Load existing patterns
        patterns_data = {}
        if patterns_file.exists():
            with open(patterns_file, 'r') as f:
                patterns_data = json.load(f)
        
        # Add new pattern
        patterns_data[pattern.pattern_id] = asdict(pattern)
        
        # Save updated patterns
        with open(patterns_file, 'w') as f:
            json.dump(patterns_data, f, indent=2)

    async def _generate_optimizations(self):
        """Generate optimization suggestions based on patterns"""
        optimizations = []
        
        # Load recent patterns
        patterns_dir = self.learning_home / "patterns"
        if not patterns_dir.exists():
            return optimizations
        
        for pattern_file in patterns_dir.glob("patterns_*.json"):
            try:
                with open(pattern_file, 'r') as f:
                    patterns_data = json.load(f)
                
                for pattern_id, pattern_data in patterns_data.items():
                    if pattern_data['confidence'] > 0.8:
                        optimization = self._generate_optimization_from_pattern(pattern_data)
                        if optimization:
                            optimizations.append(optimization)
                            
            except Exception as e:
                print(f"⚠️ Error processing pattern file {pattern_file}: {e}")
        
        return optimizations

    def _generate_optimization_from_pattern(self, pattern_data):
        """Generate an optimization suggestion from a pattern"""
        pattern_type = pattern_data['pattern_type']
        
        if pattern_type == "command_frequency":
            # Suggest command aliases or shortcuts
            commands = pattern_data['data'].get('most_frequent_commands', [])
            if commands and len(commands) > 0:
                most_frequent = commands[0][0]
                return OptimizationSuggestion(
                    suggestion_id=str(uuid.uuid4()),
                    target_system="shell_configuration",
                    optimization_type="alias_creation",
                    description=f"Create alias for frequently used command: {most_frequent}",
                    expected_benefit="Reduce typing time and increase efficiency",
                    confidence=0.8,
                    implementation_complexity="low",
                    created_at=datetime.now().isoformat()
                )
        
        elif pattern_type == "performance_correlation":
            # Suggest performance optimizations
            data = pattern_data['data']
            if data.get('average_memory_usage', 0) > 80:
                return OptimizationSuggestion(
                    suggestion_id=str(uuid.uuid4()),
                    target_system="system_resources",
                    optimization_type="memory_optimization",
                    description="High memory usage detected - suggest memory cleanup or optimization",
                    expected_benefit="Improved system responsiveness",
                    confidence=0.9,
                    implementation_complexity="medium",
                    created_at=datetime.now().isoformat()
                )
        
        return None

    async def _queue_optimization(self, optimization: OptimizationSuggestion):
        """Add optimization to processing queue"""
        self.optimization_queue.append(optimization)
        
        # Log optimization
        opt_file = self.learning_home / "optimizations" / f"queue_{datetime.now().strftime('%Y%m%d')}.jsonl"
        with open(opt_file, 'a') as f:
            f.write(json.dumps(asdict(optimization)) + '\n')

    async def _process_optimization_queue(self):
        """Process queued optimizations"""
        if not self.optimization_queue:
            return
        
        # Process high-confidence, low-complexity optimizations automatically
        auto_apply = []
        for opt in self.optimization_queue:
            if opt.confidence > 0.9 and opt.implementation_complexity == "low":
                auto_apply.append(opt)
        
        for opt in auto_apply:
            await self._apply_optimization(opt)
            self.optimization_queue.remove(opt)

    async def _apply_optimization(self, optimization: OptimizationSuggestion):
        """Apply an optimization suggestion"""
        print(f"🚀 Applying optimization: {optimization.description}")
        
        # Implementation would depend on optimization type
        # For now, just log that it was applied
        applied_file = self.learning_home / "optimizations" / f"applied_{datetime.now().strftime('%Y%m%d')}.jsonl"
        with open(applied_file, 'a') as f:
            applied_data = asdict(optimization)
            applied_data['applied_at'] = datetime.now().isoformat()
            f.write(json.dumps(applied_data) + '\n')

    async def _cleanup_old_events(self):
        """Clean up old events and data"""
        cutoff_time = datetime.now() - timedelta(hours=24)
        
        # Remove old events from memory
        self.recent_events = [
            e for e in self.recent_events 
            if datetime.fromisoformat(e.timestamp.replace('Z', '+00:00')) > cutoff_time
        ]

    async def _update_agent_status(self):
        """Update status of learning agents"""
        # This would check if agents are running and healthy
        pass

    async def _distribute_learning_tasks(self):
        """Distribute learning tasks to agents"""
        # This would assign specific learning tasks to specialized agents
        pass

    async def _collect_agent_results(self):
        """Collect results from learning agents"""
        # This would gather results from distributed learning agents
        pass

    async def _collect_performance_metrics(self):
        """Collect learning system performance metrics"""
        return {
            "events_processed": len(self.recent_events),
            "patterns_active": len(self.active_patterns),
            "optimizations_queued": len(self.optimization_queue),
            "timestamp": datetime.now().isoformat()
        }

    async def _update_learning_efficiency(self, metrics):
        """Update learning efficiency metrics"""
        # Calculate and update learning efficiency based on metrics
        pass

    async def _generate_performance_report(self, metrics):
        """Generate performance report"""
        report_file = self.learning_home / "orchestrator" / f"performance_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
        with open(report_file, 'w') as f:
            json.dump(metrics, f, indent=2)

    async def _update_pattern_relationships(self):
        """Update relationships between patterns"""
        # This would analyze correlations between different patterns
        pass

    async def _save_orchestration_state(self):
        """Save current orchestration state"""
        state = {
            "orchestrator_id": self.orchestrator_id,
            "shutdown_time": datetime.now().isoformat(),
            "final_metrics": {
                "events_processed": len(self.recent_events),
                "patterns_discovered": len(self.active_patterns),
                "optimizations_generated": len(self.optimization_queue)
            }
        }
        
        state_file = self.learning_home / "orchestrator" / f"state_{self.orchestrator_id}.json"
        with open(state_file, 'w') as f:
            json.dump(state, f, indent=2)


async def main():
    orchestrator = LearningOrchestrator()
    
    try:
        await orchestrator.start_orchestration()
    except KeyboardInterrupt:
        await orchestrator.stop_orchestration()


if __name__ == "__main__":
    asyncio.run(main())