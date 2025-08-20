"""
Agent Economic System - Token Economics & Bonding Curves
=======================================================

A comprehensive implementation of token economics for AI agent marketplaces,
featuring bonding curves, dynamic pricing, and economic incentive alignment.

Based on 2024-2025 research into agent economic models and DeFi mechanisms.
"""

import math
import numpy as np
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
import time
import hashlib
from collections import defaultdict

class AgentCapability(Enum):
    """Types of capabilities agents can offer in the marketplace"""
    REASONING = "reasoning"
    PLANNING = "planning"
    EXECUTION = "execution"
    ANALYSIS = "analysis"
    CREATIVITY = "creativity"
    COORDINATION = "coordination"
    LEARNING = "learning"
    COMMUNICATION = "communication"

class AgentPerformanceMetric(Enum):
    """Performance metrics for agent evaluation"""
    SUCCESS_RATE = "success_rate"
    LATENCY = "latency"
    ACCURACY = "accuracy"
    RESOURCE_EFFICIENCY = "resource_efficiency"
    REPUTATION_SCORE = "reputation_score"
    COMPLETION_TIME = "completion_time"

@dataclass
class Agent:
    """Represents an AI agent in the economic system"""
    id: str
    capabilities: List[AgentCapability]
    token_balance: float = 1000.0  # Starting balance
    stake: float = 0.0
    reputation_score: float = 1.0
    performance_metrics: Dict[AgentPerformanceMetric, float] = field(default_factory=dict)
    compute_credits: float = 100.0
    created_at: float = field(default_factory=time.time)
    last_active: float = field(default_factory=time.time)
    
    def __post_init__(self):
        """Initialize default performance metrics"""
        if not self.performance_metrics:
            self.performance_metrics = {
                AgentPerformanceMetric.SUCCESS_RATE: 0.5,
                AgentPerformanceMetric.LATENCY: 1.0,
                AgentPerformanceMetric.ACCURACY: 0.5,
                AgentPerformanceMetric.RESOURCE_EFFICIENCY: 0.5,
                AgentPerformanceMetric.REPUTATION_SCORE: 1.0,
                AgentPerformanceMetric.COMPLETION_TIME: 1.0
            }

class BondingCurve:
    """
    Implements various bonding curve models for dynamic token pricing
    
    Based on 2024 research showing bonding curves create predictable pricing
    models that encourage early investment and help stabilize token prices.
    """
    
    def __init__(self, curve_type: str = "linear", base_price: float = 0.001, 
                 slope: float = 0.0001, reserve_ratio: float = 0.1):
        self.curve_type = curve_type
        self.base_price = base_price
        self.slope = slope
        self.reserve_ratio = reserve_ratio  # For bancor curves
        
    def calculate_price(self, total_supply: float) -> float:
        """Calculate token price based on current supply using bonding curve"""
        if self.curve_type == "linear":
            return self.base_price + (self.slope * total_supply)
        
        elif self.curve_type == "exponential":
            return self.base_price * math.exp(self.slope * total_supply)
        
        elif self.curve_type == "logarithmic":
            return self.base_price * math.log(1 + self.slope * total_supply)
        
        elif self.curve_type == "polynomial":
            return self.base_price + (self.slope * total_supply ** 2)
        
        elif self.curve_type == "bancor":
            # Bancor formula: price = reserve_balance / (supply * reserve_ratio)
            return self.base_price / (total_supply * self.reserve_ratio + 1)
        
        else:
            raise ValueError(f"Unknown curve type: {self.curve_type}")
    
    def calculate_tokens_for_eth(self, eth_amount: float, current_supply: float) -> float:
        """Calculate how many tokens can be purchased with given ETH amount"""
        if self.curve_type == "linear":
            # Solve: eth = integral of (base_price + slope * x) dx from current_supply to current_supply + tokens
            # eth = base_price * tokens + slope * (tokens^2 / 2 + current_supply * tokens)
            # Rearranging: slope/2 * tokens^2 + (base_price + slope * current_supply) * tokens - eth = 0
            
            a = self.slope / 2
            b = self.base_price + self.slope * current_supply
            c = -eth_amount
            
            if a == 0:  # Linear case where slope is 0
                return eth_amount / self.base_price
            
            discriminant = b**2 - 4*a*c
            if discriminant < 0:
                return 0
            
            return (-b + math.sqrt(discriminant)) / (2 * a)
        
        # For other curve types, use numerical approximation
        tokens = 0
        step_size = 0.1
        total_cost = 0
        
        while total_cost < eth_amount and step_size > 0.001:
            price = self.calculate_price(current_supply + tokens)
            if total_cost + price * step_size <= eth_amount:
                total_cost += price * step_size
                tokens += step_size
            else:
                step_size /= 10
        
        return tokens

class AgentTokenEconomics:
    """
    Core token economics system for agent marketplace
    
    Implements dynamic pricing, reputation-based rewards, and economic
    incentive alignment based on 2024-2025 research findings.
    """
    
    def __init__(self, initial_supply: float = 1000000.0):
        self.total_supply = initial_supply
        self.circulating_supply = initial_supply * 0.3  # 30% initially circulating
        self.bonding_curve = BondingCurve(curve_type="polynomial", base_price=0.001, slope=0.000001)
        self.agents: Dict[str, Agent] = {}
        self.transaction_history: List[Dict] = []
        self.capability_markets: Dict[AgentCapability, Dict] = {}
        self.governance_proposals: List[Dict] = []
        
        # Economic parameters
        self.inflation_rate = 0.05  # 5% annual inflation for rewarding productive agents
        self.burn_rate = 0.02  # 2% of transaction fees burned
        self.staking_reward_rate = 0.08  # 8% annual staking rewards
        self.reputation_bonus_multiplier = 2.0
        
        # Initialize capability markets
        for capability in AgentCapability:
            self.capability_markets[capability] = {
                "total_value_locked": 0.0,
                "average_price": 1.0,
                "volume_24h": 0.0,
                "providers": [],
                "demand_score": 1.0
            }
    
    def register_agent(self, agent_id: str, capabilities: List[AgentCapability], 
                      initial_stake: float = 0.0) -> Agent:
        """Register a new agent in the economic system"""
        agent = Agent(
            id=agent_id,
            capabilities=capabilities,
            stake=initial_stake
        )
        
        # Deduct stake from circulating supply
        if initial_stake > 0:
            self.circulating_supply -= initial_stake
        
        self.agents[agent_id] = agent
        
        # Add agent to relevant capability markets
        for capability in capabilities:
            self.capability_markets[capability]["providers"].append(agent_id)
        
        self._record_transaction({
            "type": "agent_registration",
            "agent_id": agent_id,
            "stake": initial_stake,
            "timestamp": time.time()
        })
        
        return agent
    
    def calculate_agent_value(self, agent_id: str) -> float:
        """
        Calculate the economic value of an agent based on performance,
        reputation, and market demand for their capabilities
        """
        if agent_id not in self.agents:
            return 0.0
        
        agent = self.agents[agent_id]
        base_value = agent.token_balance + agent.stake
        
        # Performance multiplier (0.1 to 5.0 based on metrics)
        performance_score = np.mean(list(agent.performance_metrics.values()))
        performance_multiplier = 0.1 + (performance_score * 4.9)
        
        # Reputation multiplier (0.5 to 3.0 based on reputation score)
        reputation_multiplier = 0.5 + (agent.reputation_score * 2.5)
        
        # Market demand multiplier for agent's capabilities
        demand_multiplier = 1.0
        for capability in agent.capabilities:
            market = self.capability_markets[capability]
            demand_multiplier += market["demand_score"] * 0.2
        
        # Activity multiplier (agents that haven't been active get penalized)
        time_since_activity = time.time() - agent.last_active
        activity_multiplier = max(0.1, 1.0 - (time_since_activity / (30 * 24 * 3600)))  # Decay over 30 days
        
        return base_value * performance_multiplier * reputation_multiplier * demand_multiplier * activity_multiplier
    
    def purchase_tokens(self, agent_id: str, eth_amount: float) -> float:
        """Allow agent to purchase tokens using bonding curve pricing"""
        if agent_id not in self.agents:
            raise ValueError(f"Agent {agent_id} not registered")
        
        tokens_received = self.bonding_curve.calculate_tokens_for_eth(eth_amount, self.circulating_supply)
        
        # Update supply and agent balance
        self.circulating_supply += tokens_received
        self.agents[agent_id].token_balance += tokens_received
        
        self._record_transaction({
            "type": "token_purchase",
            "agent_id": agent_id,
            "eth_amount": eth_amount,
            "tokens_received": tokens_received,
            "price": eth_amount / tokens_received if tokens_received > 0 else 0,
            "timestamp": time.time()
        })
        
        return tokens_received
    
    def stake_tokens(self, agent_id: str, amount: float) -> bool:
        """Allow agent to stake tokens for governance and rewards"""
        if agent_id not in self.agents:
            return False
        
        agent = self.agents[agent_id]
        if agent.token_balance < amount:
            return False
        
        agent.token_balance -= amount
        agent.stake += amount
        
        self._record_transaction({
            "type": "stake",
            "agent_id": agent_id,
            "amount": amount,
            "timestamp": time.time()
        })
        
        return True
    
    def unstake_tokens(self, agent_id: str, amount: float) -> bool:
        """Allow agent to unstake tokens (with potential slashing penalties)"""
        if agent_id not in self.agents:
            return False
        
        agent = self.agents[agent_id]
        if agent.stake < amount:
            return False
        
        # Apply slashing if agent has poor performance
        if agent.reputation_score < 0.5:
            slashing_penalty = amount * (0.5 - agent.reputation_score)
            amount -= slashing_penalty
            self._burn_tokens(slashing_penalty)
        
        agent.stake -= amount
        agent.token_balance += amount
        
        self._record_transaction({
            "type": "unstake",
            "agent_id": agent_id,
            "amount": amount,
            "timestamp": time.time()
        })
        
        return True
    
    def reward_performance(self, agent_id: str, performance_metrics: Dict[AgentPerformanceMetric, float]) -> float:
        """
        Reward agents based on performance metrics and economic contribution
        
        Implements natural selection through economic pressure - high-performing
        agents receive more rewards and accumulate resources.
        """
        if agent_id not in self.agents:
            return 0.0
        
        agent = self.agents[agent_id]
        
        # Update performance metrics with exponential moving average
        alpha = 0.3  # Learning rate for metric updates
        for metric, value in performance_metrics.items():
            if metric in agent.performance_metrics:
                agent.performance_metrics[metric] = (
                    alpha * value + (1 - alpha) * agent.performance_metrics[metric]
                )
            else:
                agent.performance_metrics[metric] = value
        
        # Calculate reward based on performance improvement and absolute performance
        performance_score = np.mean(list(agent.performance_metrics.values()))
        base_reward = performance_score * 10.0  # Base reward proportional to performance
        
        # Reputation bonus for trusted agents
        reputation_bonus = agent.reputation_score * self.reputation_bonus_multiplier
        
        # Stake bonus for committed agents
        stake_bonus = min(agent.stake * 0.001, 5.0)  # Cap stake bonus at 5 tokens
        
        total_reward = base_reward + reputation_bonus + stake_bonus
        
        # Mint new tokens as rewards (controlled inflation)
        self._mint_tokens(total_reward)
        agent.token_balance += total_reward
        agent.last_active = time.time()
        
        # Update reputation based on performance
        if performance_score > 0.7:
            agent.reputation_score = min(3.0, agent.reputation_score * 1.1)
        elif performance_score < 0.3:
            agent.reputation_score = max(0.1, agent.reputation_score * 0.9)
        
        self._record_transaction({
            "type": "performance_reward",
            "agent_id": agent_id,
            "reward": total_reward,
            "performance_score": performance_score,
            "timestamp": time.time()
        })
        
        return total_reward
    
    def charge_for_service(self, provider_id: str, consumer_id: str, 
                          capability: AgentCapability, amount: float) -> bool:
        """Charge for agent services and handle payment"""
        if provider_id not in self.agents or consumer_id not in self.agents:
            return False
        
        provider = self.agents[provider_id]
        consumer = self.agents[consumer_id]
        
        if consumer.token_balance < amount:
            return False
        
        # Calculate fees
        platform_fee = amount * 0.05  # 5% platform fee
        net_payment = amount - platform_fee
        
        # Transfer tokens
        consumer.token_balance -= amount
        provider.token_balance += net_payment
        
        # Burn a portion of platform fee
        burned_amount = platform_fee * self.burn_rate
        self._burn_tokens(burned_amount)
        
        # Update market data
        market = self.capability_markets[capability]
        market["volume_24h"] += amount
        market["total_value_locked"] += net_payment
        
        self._record_transaction({
            "type": "service_payment",
            "provider_id": provider_id,
            "consumer_id": consumer_id,
            "capability": capability.value,
            "amount": amount,
            "platform_fee": platform_fee,
            "timestamp": time.time()
        })
        
        return True
    
    def calculate_capability_price(self, capability: AgentCapability) -> float:
        """Calculate dynamic pricing for capabilities based on supply and demand"""
        market = self.capability_markets[capability]
        
        # Base price influenced by total value locked and demand
        base_price = market["total_value_locked"] / max(len(market["providers"]), 1)
        demand_multiplier = market["demand_score"]
        
        return base_price * demand_multiplier
    
    def update_market_demand(self, capability: AgentCapability, demand_change: float):
        """Update market demand scores based on usage patterns"""
        market = self.capability_markets[capability]
        market["demand_score"] = max(0.1, market["demand_score"] + demand_change)
    
    def get_agent_rankings(self) -> List[Tuple[str, float]]:
        """Get agent rankings by total economic value"""
        rankings = []
        for agent_id in self.agents:
            value = self.calculate_agent_value(agent_id)
            rankings.append((agent_id, value))
        
        return sorted(rankings, key=lambda x: x[1], reverse=True)
    
    def simulate_bankruptcy(self) -> List[str]:
        """
        Simulate bankruptcy for agents with insufficient resources
        
        Implements natural selection - agents that can't sustain themselves
        economically are removed from the system.
        """
        bankrupt_agents = []
        bankruptcy_threshold = 10.0  # Minimum tokens needed to survive
        
        for agent_id, agent in list(self.agents.items()):
            total_resources = agent.token_balance + agent.stake + agent.compute_credits
            
            if total_resources < bankruptcy_threshold and agent.reputation_score < 0.3:
                # Agent goes bankrupt
                bankrupt_agents.append(agent_id)
                
                # Remove from capability markets
                for capability in agent.capabilities:
                    if agent_id in self.capability_markets[capability]["providers"]:
                        self.capability_markets[capability]["providers"].remove(agent_id)
                
                # Burn remaining tokens
                self._burn_tokens(agent.token_balance + agent.stake)
                
                # Remove agent
                del self.agents[agent_id]
                
                self._record_transaction({
                    "type": "bankruptcy",
                    "agent_id": agent_id,
                    "timestamp": time.time()
                })
        
        return bankrupt_agents
    
    def _mint_tokens(self, amount: float):
        """Mint new tokens (controlled inflation for rewards)"""
        self.total_supply += amount
        self.circulating_supply += amount
    
    def _burn_tokens(self, amount: float):
        """Burn tokens to control inflation"""
        self.circulating_supply = max(0, self.circulating_supply - amount)
        self.total_supply = max(0, self.total_supply - amount)
    
    def _record_transaction(self, transaction: Dict):
        """Record transaction in history"""
        transaction["id"] = hashlib.sha256(str(transaction).encode()).hexdigest()[:16]
        self.transaction_history.append(transaction)
    
    def get_market_stats(self) -> Dict:
        """Get comprehensive market statistics"""
        return {
            "total_supply": self.total_supply,
            "circulating_supply": self.circulating_supply,
            "current_price": self.bonding_curve.calculate_price(self.circulating_supply),
            "total_agents": len(self.agents),
            "capability_markets": self.capability_markets,
            "total_transactions": len(self.transaction_history),
            "agent_rankings": self.get_agent_rankings()[:10]  # Top 10 agents
        }

# Example usage and testing
if __name__ == "__main__":
    # Initialize the economic system
    economy = AgentTokenEconomics()
    
    # Register some agents
    agents = [
        economy.register_agent("agent_001", [AgentCapability.REASONING, AgentCapability.ANALYSIS], 100.0),
        economy.register_agent("agent_002", [AgentCapability.PLANNING, AgentCapability.EXECUTION], 50.0),
        economy.register_agent("agent_003", [AgentCapability.CREATIVITY, AgentCapability.COMMUNICATION], 200.0),
        economy.register_agent("agent_004", [AgentCapability.LEARNING, AgentCapability.COORDINATION], 75.0)
    ]
    
    print("=== AI Agent Economic System Demo ===\n")
    
    # Show initial market stats
    print("Initial Market Stats:")
    stats = economy.get_market_stats()
    print(f"Total Supply: {stats['total_supply']:,.0f}")
    print(f"Current Price: {stats['current_price']:.6f} ETH")
    print(f"Total Agents: {stats['total_agents']}")
    
    # Simulate some economic activity
    print("\n=== Simulating Economic Activity ===")
    
    # Agents purchase tokens
    for i, agent in enumerate(agents):
        eth_amount = 1.0 + i * 0.5
        tokens = economy.purchase_tokens(agent.id, eth_amount)
        print(f"{agent.id} purchased {tokens:.2f} tokens for {eth_amount} ETH")
    
    # Simulate performance and rewards
    print("\n=== Performance-Based Rewards ===")
    performance_data = [
        {"agent_001": {AgentPerformanceMetric.SUCCESS_RATE: 0.9, AgentPerformanceMetric.ACCURACY: 0.85}},
        {"agent_002": {AgentPerformanceMetric.SUCCESS_RATE: 0.7, AgentPerformanceMetric.LATENCY: 0.6}},
        {"agent_003": {AgentPerformanceMetric.SUCCESS_RATE: 0.95, AgentPerformanceMetric.CREATIVITY: 0.9}},
        {"agent_004": {AgentPerformanceMetric.SUCCESS_RATE: 0.3, AgentPerformanceMetric.ACCURACY: 0.4}}
    ]
    
    for perf in performance_data:
        for agent_id, metrics in perf.items():
            reward = economy.reward_performance(agent_id, metrics)
            print(f"{agent_id} received {reward:.2f} tokens as performance reward")
    
    # Show agent rankings
    print("\n=== Agent Rankings by Economic Value ===")
    rankings = economy.get_agent_rankings()
    for i, (agent_id, value) in enumerate(rankings, 1):
        agent = economy.agents[agent_id]
        print(f"{i}. {agent_id}: {value:.2f} total value (reputation: {agent.reputation_score:.2f})")
    
    # Simulate bankruptcy
    print("\n=== Natural Selection: Bankruptcy Simulation ===")
    bankrupt = economy.simulate_bankruptcy()
    if bankrupt:
        print(f"Agents went bankrupt: {bankrupt}")
    else:
        print("No agents went bankrupt this cycle")
    
    # Final market stats
    print("\n=== Final Market Stats ===")
    final_stats = economy.get_market_stats()
    print(f"Total Supply: {final_stats['total_supply']:,.0f}")
    print(f"Current Price: {final_stats['current_price']:.6f} ETH")
    print(f"Surviving Agents: {final_stats['total_agents']}")
    print(f"Total Transactions: {final_stats['total_transactions']}")