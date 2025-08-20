#!/usr/bin/env python3
"""
TMUX Session Learning Observer
Monitors TMUX brain sessions and extracts learning patterns
"""

import json
import time
import subprocess
import threading
import argparse
import uuid
from datetime import datetime
from pathlib import Path
import re

class TMUXSessionObserver:
    def __init__(self, session_name="BRAIN-MAIN", learning_home=None):
        self.session_name = session_name
        self.learning_home = Path(learning_home or Path.home() / ".learning-engine")
        self.session_id = str(uuid.uuid4())
        self.is_running = False
        
        # Create necessary directories
        self.learning_home.mkdir(exist_ok=True)
        (self.learning_home / "sessions").mkdir(exist_ok=True)
        (self.learning_home / "patterns").mkdir(exist_ok=True)
        (self.learning_home / "raw").mkdir(exist_ok=True)
        
        # Session log file
        self.session_log = self.learning_home / "sessions" / f"{self.session_id}.jsonl"
        
        print(f"🧠 TMUX Session Observer initialized for session: {session_name}")
        print(f"📝 Session ID: {self.session_id}")
        print(f"📂 Learning home: {self.learning_home}")

    def start_observation(self):
        """Start observing the TMUX session"""
        self.is_running = True
        
        # Start monitoring threads
        threads = [
            threading.Thread(target=self._monitor_windows, daemon=True),
            threading.Thread(target=self._monitor_commands, daemon=True),
            threading.Thread(target=self._monitor_performance, daemon=True),
            threading.Thread(target=self._extract_patterns, daemon=True)
        ]
        
        for thread in threads:
            thread.start()
            
        print(f"✅ Started observing session: {self.session_name}")
        
        try:
            while self.is_running:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop_observation()

    def stop_observation(self):
        """Stop observing and save final patterns"""
        print("🛑 Stopping observation...")
        self.is_running = False
        self._save_session_summary()
        print("💾 Session patterns saved!")

    def _monitor_windows(self):
        """Monitor window creation, switching, and activity"""
        last_windows = set()
        
        while self.is_running:
            try:
                # Get current windows
                result = subprocess.run(
                    ["tmux", "list-windows", "-t", self.session_name, "-F", "#{window_index}:#{window_name}:#{window_active}"],
                    capture_output=True, text=True, timeout=5
                )
                
                if result.returncode == 0:
                    current_windows = set(result.stdout.strip().split('\n'))
                    
                    # Detect new windows
                    new_windows = current_windows - last_windows
                    if new_windows:
                        for window in new_windows:
                            if window:  # Skip empty lines
                                self._log_event("window_created", {
                                    "window": window,
                                    "timestamp": datetime.now().isoformat()
                                })
                    
                    # Detect active window changes
                    active_windows = [w for w in current_windows if w.endswith(':1')]
                    for active_window in active_windows:
                        self._log_event("window_active", {
                            "window": active_window,
                            "timestamp": datetime.now().isoformat()
                        })
                    
                    last_windows = current_windows
                    
            except (subprocess.TimeoutExpired, subprocess.CalledProcessError) as e:
                if self.is_running:  # Only log if we're still supposed to be running
                    print(f"⚠️ Window monitoring error: {e}")
            
            time.sleep(2)

    def _monitor_commands(self):
        """Monitor command execution and patterns"""
        while self.is_running:
            try:
                # Capture recent command history from all windows
                result = subprocess.run(
                    ["tmux", "list-windows", "-t", self.session_name, "-F", "#{window_index}"],
                    capture_output=True, text=True, timeout=5
                )
                
                if result.returncode == 0:
                    window_indices = result.stdout.strip().split('\n')
                    
                    for window_index in window_indices:
                        if window_index:
                            # Capture pane content for command pattern analysis
                            pane_result = subprocess.run(
                                ["tmux", "capture-pane", "-t", f"{self.session_name}:{window_index}", "-p"],
                                capture_output=True, text=True, timeout=5
                            )
                            
                            if pane_result.returncode == 0:
                                content = pane_result.stdout
                                commands = self._extract_commands_from_content(content)
                                
                                for command in commands:
                                    self._log_event("command_executed", {
                                        "window": window_index,
                                        "command": command,
                                        "timestamp": datetime.now().isoformat()
                                    })
                            
            except (subprocess.TimeoutExpired, subprocess.CalledProcessError) as e:
                if self.is_running:
                    print(f"⚠️ Command monitoring error: {e}")
            
            time.sleep(5)

    def _monitor_performance(self):
        """Monitor performance metrics and cognitive modes"""
        while self.is_running:
            try:
                # Get session information
                result = subprocess.run(
                    ["tmux", "display-message", "-t", self.session_name, "-p", "#{session_windows}:#{session_created}"],
                    capture_output=True, text=True, timeout=5
                )
                
                if result.returncode == 0:
                    session_info = result.stdout.strip().split(':')
                    if len(session_info) >= 2:
                        self._log_event("performance_metric", {
                            "window_count": int(session_info[0]),
                            "session_created": session_info[1],
                            "timestamp": datetime.now().isoformat(),
                            "uptime_minutes": self._calculate_uptime()
                        })
                        
            except (subprocess.TimeoutExpired, subprocess.CalledProcessError) as e:
                if self.is_running:
                    print(f"⚠️ Performance monitoring error: {e}")
            
            time.sleep(10)

    def _extract_patterns(self):
        """Extract learning patterns from observed data"""
        pattern_extraction_interval = 30  # seconds
        
        while self.is_running:
            try:
                # Read recent events from session log
                if self.session_log.exists():
                    with open(self.session_log, 'r') as f:
                        events = [json.loads(line) for line in f.readlines()[-100:]]
                    
                    # Extract patterns
                    patterns = self._analyze_event_patterns(events)
                    
                    # Save patterns
                    pattern_file = self.learning_home / "patterns" / f"session_{self.session_id}_{int(time.time())}.json"
                    with open(pattern_file, 'w') as f:
                        json.dump(patterns, f, indent=2)
                        
            except Exception as e:
                if self.is_running:
                    print(f"⚠️ Pattern extraction error: {e}")
            
            time.sleep(pattern_extraction_interval)

    def _extract_commands_from_content(self, content):
        """Extract command patterns from pane content"""
        commands = []
        lines = content.split('\n')
        
        # Look for command patterns (basic implementation)
        command_patterns = [
            r'^\$ (.+)$',  # Shell commands
            r'^> (.+)$',   # Some CLI tools
            r'^>>> (.+)$', # Python REPL
            r'claude-code (.+)',  # Claude Code commands
            r'tmux (.+)',  # TMUX commands
        ]
        
        for line in lines[-20:]:  # Check last 20 lines
            for pattern in command_patterns:
                match = re.search(pattern, line.strip())
                if match:
                    commands.append(match.group(1))
                    
        return commands

    def _analyze_event_patterns(self, events):
        """Analyze events to extract meaningful patterns"""
        patterns = {
            "window_creation_frequency": 0,
            "command_patterns": {},
            "active_window_switches": 0,
            "peak_activity_periods": [],
            "cognitive_mode_indicators": [],
            "performance_trends": {}
        }
        
        # Count window creations
        window_creations = [e for e in events if e.get('event_type') == 'window_created']
        patterns["window_creation_frequency"] = len(window_creations)
        
        # Analyze command patterns
        commands = [e for e in events if e.get('event_type') == 'command_executed']
        command_counts = {}
        for cmd_event in commands:
            cmd = cmd_event.get('data', {}).get('command', '')
            if cmd:
                command_counts[cmd] = command_counts.get(cmd, 0) + 1
        patterns["command_patterns"] = command_counts
        
        # Count window switches
        window_switches = [e for e in events if e.get('event_type') == 'window_active']
        patterns["active_window_switches"] = len(window_switches)
        
        # Detect cognitive mode patterns
        for event in events:
            if 'cognitive' in str(event).lower() or 'think' in str(event).lower():
                patterns["cognitive_mode_indicators"].append(event)
        
        return patterns

    def _calculate_uptime(self):
        """Calculate session uptime in minutes"""
        try:
            result = subprocess.run(
                ["tmux", "display-message", "-t", self.session_name, "-p", "#{session_created}"],
                capture_output=True, text=True
            )
            if result.returncode == 0:
                created_timestamp = int(result.stdout.strip())
                uptime_seconds = time.time() - created_timestamp
                return int(uptime_seconds / 60)
        except:
            pass
        return 0

    def _log_event(self, event_type, data):
        """Log an event to the session log"""
        event = {
            "session_id": self.session_id,
            "event_type": event_type,
            "data": data,
            "timestamp": datetime.now().isoformat()
        }
        
        with open(self.session_log, 'a') as f:
            f.write(json.dumps(event) + '\n')

    def _save_session_summary(self):
        """Save final session summary and patterns"""
        if not self.session_log.exists():
            return
            
        with open(self.session_log, 'r') as f:
            events = [json.loads(line) for line in f.readlines()]
        
        summary = {
            "session_id": self.session_id,
            "session_name": self.session_name,
            "total_events": len(events),
            "duration_minutes": self._calculate_uptime(),
            "final_patterns": self._analyze_event_patterns(events),
            "end_time": datetime.now().isoformat()
        }
        
        summary_file = self.learning_home / "sessions" / f"summary_{self.session_id}.json"
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)
        
        print(f"📊 Session summary saved: {summary_file}")


def main():
    parser = argparse.ArgumentParser(description="TMUX Session Learning Observer")
    parser.add_argument("--session", "-s", default="BRAIN-MAIN", help="TMUX session name to observe")
    parser.add_argument("--learning-home", "-l", help="Learning engine home directory")
    parser.add_argument("--attach-to", "-a", help="Attach to existing session")
    
    args = parser.parse_args()
    
    session_name = args.attach_to or args.session
    observer = TMUXSessionObserver(session_name, args.learning_home)
    
    try:
        observer.start_observation()
    except KeyboardInterrupt:
        observer.stop_observation()


if __name__ == "__main__":
    main()