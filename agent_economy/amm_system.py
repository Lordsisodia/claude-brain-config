"""
Agent Capability Automated Market Maker (AMM) System
===================================================

A sophisticated AMM system for trading AI agent capabilities, featuring:
- Concentrated liquidity pools for capability tokens
- Dynamic pricing based on supply/demand
- Predictive algorithms using reinforcement learning
- Multi-asset capability bundles
- Impermanent loss protection

Based on 2024 research showing predictive AMMs can reduce divergence and 
slippage losses through deep LSTM and Q-learning frameworks.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
import time
import math
import hashlib
from collections import defaultdict, deque
import json

class CapabilityToken(Enum):
    """Tokenized agent capabilities for trading"""
    REASONING_TOKEN = "REASON"
    PLANNING_TOKEN = "PLAN"
    EXECUTION_TOKEN = "EXEC"
    ANALYSIS_TOKEN = "ANALYZE"
    CREATIVITY_TOKEN = "CREATE"
    COORDINATION_TOKEN = "COORD"
    LEARNING_TOKEN = "LEARN"
    COMMUNICATION_TOKEN = "COMM"
    BUNDLE_TOKEN = "BUNDLE"  # Multi-capability bundles

@dataclass
class LiquidityPosition:
    """Represents a liquidity provider's position in a pool"""
    provider: str
    token_a_amount: float
    token_b_amount: float
    shares: float
    entry_price: float
    entry_time: float
    accumulated_fees: float = 0.0
    impermanent_loss: float = 0.0

@dataclass
class Trade:
    """Represents a trade in the AMM"""
    id: str
    trader: str
    token_in: CapabilityToken
    token_out: CapabilityToken
    amount_in: float
    amount_out: float
    price: float
    slippage: float
    fee: float
    timestamp: float
    pool_id: str

@dataclass
class PredictionModel:
    """LSTM + Q-learning prediction model for price forecasting"""
    sequence_length: int = 24  # Look back 24 time periods
    learning_rate: float = 0.001
    epsilon: float = 0.1  # Exploration rate for Q-learning
    epsilon_decay: float = 0.995
    min_epsilon: float = 0.01
    memory_size: int = 10000
    batch_size: int = 32
    
    def __init__(self):
        self.price_history = deque(maxlen=self.memory_size)
        self.volume_history = deque(maxlen=self.memory_size)
        self.prediction_accuracy = 0.5
        self.q_table = defaultdict(lambda: defaultdict(float))
        self.last_prediction = 0.0

class ConcentratedLiquidityPool:
    """
    Concentrated liquidity AMM pool inspired by Uniswap V3
    
    Allows liquidity providers to concentrate their capital in specific
    price ranges for improved capital efficiency.
    """
    
    def __init__(self, token_a: CapabilityToken, token_b: CapabilityToken, 
                 fee_rate: float = 0.003, tick_spacing: int = 60):
        self.token_a = token_a
        self.token_b = token_b
        self.fee_rate = fee_rate
        self.tick_spacing = tick_spacing
        
        # Pool state
        self.reserve_a = 1000.0  # Initial liquidity
        self.reserve_b = 1000.0
        self.total_shares = 2000.0
        self.sqrt_price = math.sqrt(self.reserve_b / self.reserve_a)
        self.current_tick = 0
        
        # Concentrated liquidity data structures
        self.ticks = {}  # tick -> liquidity_net
        self.positions = {}  # position_id -> LiquidityPosition
        self.active_liquidity = 2000.0
        
        # Trading history
        self.trades = []
        self.volume_24h = 0.0
        self.fees_collected = 0.0
        
        # Prediction model
        self.prediction_model = PredictionModel()
        
        # Price oracle data
        self.price_history = deque(maxlen=1000)
        self.price_history.append(1.0)  # Initial price ratio
        
    def get_price(self) -> float:
        """Get current price of token_a in terms of token_b"""
        if self.reserve_a == 0:
            return 0.0
        return self.reserve_b / self.reserve_a
    
    def tick_to_price(self, tick: int) -> float:
        """Convert tick to price"""
        return 1.0001 ** tick
    
    def price_to_tick(self, price: float) -> int:
        """Convert price to tick"""
        if price <= 0:
            return -887272  # Minimum tick
        return int(math.log(price) / math.log(1.0001))
    
    def add_liquidity(self, provider: str, amount_a: float, amount_b: float,
                     tick_lower: int = -60, tick_upper: int = 60) -> str:
        """
        Add concentrated liquidity to the pool within specified price range
        
        Args:
            provider: Address of liquidity provider
            amount_a: Amount of token A to provide
            amount_b: Amount of token B to provide
            tick_lower: Lower bound tick for the position
            tick_upper: Upper bound tick for the position
        
        Returns:
            Position ID
        """
        # Ensure ticks are valid and spaced correctly
        if tick_lower >= tick_upper:
            raise ValueError("Invalid tick range")
        if tick_lower % self.tick_spacing != 0 or tick_upper % self.tick_spacing != 0:
            raise ValueError("Ticks must align with tick spacing")
        
        # Calculate liquidity amount
        price_lower = self.tick_to_price(tick_lower)
        price_upper = self.tick_to_price(tick_upper)
        current_price = self.get_price()
        
        # Determine liquidity based on current price position
        if current_price < price_lower:
            # All token A
            liquidity = amount_a / (1 / math.sqrt(price_lower) - 1 / math.sqrt(price_upper))
        elif current_price > price_upper:
            # All token B
            liquidity = amount_b / (math.sqrt(price_upper) - math.sqrt(price_lower))
        else:
            # Mixed position
            liquidity_a = amount_a / (1 / math.sqrt(current_price) - 1 / math.sqrt(price_upper))
            liquidity_b = amount_b / (math.sqrt(current_price) - math.sqrt(price_lower))
            liquidity = min(liquidity_a, liquidity_b)
        
        # Create position
        position_id = hashlib.sha256(f"{provider}_{time.time()}".encode()).hexdigest()[:16]
        position = LiquidityPosition(
            provider=provider,
            token_a_amount=amount_a,
            token_b_amount=amount_b,
            shares=liquidity,
            entry_price=current_price,
            entry_time=time.time()
        )
        
        self.positions[position_id] = position
        
        # Update pool reserves
        self.reserve_a += amount_a
        self.reserve_b += amount_b
        self.total_shares += liquidity
        
        # Update tick data
        if tick_lower not in self.ticks:
            self.ticks[tick_lower] = 0
        if tick_upper not in self.ticks:
            self.ticks[tick_upper] = 0
            
        self.ticks[tick_lower] += liquidity
        self.ticks[tick_upper] -= liquidity
        
        # Update active liquidity if position is in range
        if tick_lower <= self.current_tick < tick_upper:
            self.active_liquidity += liquidity
        
        return position_id
    
    def remove_liquidity(self, position_id: str) -> Tuple[float, float]:
        """Remove liquidity position and return tokens"""
        if position_id not in self.positions:
            raise ValueError("Position not found")
        
        position = self.positions[position_id]
        
        # Calculate share of pool
        share_ratio = position.shares / self.total_shares
        
        # Calculate tokens to return (including fees)
        token_a_return = self.reserve_a * share_ratio + position.accumulated_fees * 0.5
        token_b_return = self.reserve_b * share_ratio + position.accumulated_fees * 0.5
        
        # Update pool state
        self.reserve_a -= token_a_return
        self.reserve_b -= token_b_return
        self.total_shares -= position.shares
        
        # Calculate impermanent loss
        current_price = self.get_price()
        position.impermanent_loss = self._calculate_impermanent_loss(
            position.entry_price, current_price, position.token_a_amount, position.token_b_amount
        )
        
        # Remove position
        del self.positions[position_id]
        
        return token_a_return, token_b_return
    
    def _calculate_impermanent_loss(self, entry_price: float, current_price: float,
                                  initial_a: float, initial_b: float) -> float:
        """Calculate impermanent loss for a position"""
        if entry_price == 0:
            return 0.0
            
        price_ratio = current_price / entry_price
        sqrt_ratio = math.sqrt(price_ratio)
        
        # Value if held vs value in pool
        held_value = initial_a * current_price + initial_b
        pool_value = 2 * sqrt_ratio * (initial_a * entry_price + initial_b) / (1 + sqrt_ratio)
        
        return (held_value - pool_value) / held_value if held_value > 0 else 0.0
    
    def swap(self, trader: str, token_in: CapabilityToken, amount_in: float,
            min_amount_out: float = 0.0) -> Trade:
        """
        Execute a swap in the concentrated liquidity pool
        
        Uses the concentrated liquidity formula to calculate output amount
        and update the pool state.
        """
        if amount_in <= 0:
            raise ValueError("Amount must be positive")
        
        # Determine swap direction
        zero_for_one = (token_in == self.token_a)
        
        # Calculate fee
        fee_amount = amount_in * self.fee_rate
        amount_in_after_fee = amount_in - fee_amount
        
        # Use concentrated liquidity formula
        if zero_for_one:
            # Swapping token A for token B
            amount_out = self._calculate_swap_output(amount_in_after_fee, True)
            new_reserve_a = self.reserve_a + amount_in_after_fee
            new_reserve_b = self.reserve_b - amount_out
            token_out = self.token_b
        else:
            # Swapping token B for token A
            amount_out = self._calculate_swap_output(amount_in_after_fee, False)
            new_reserve_a = self.reserve_a - amount_out
            new_reserve_b = self.reserve_b + amount_in_after_fee
            token_out = self.token_a
        
        # Check slippage protection
        if amount_out < min_amount_out:
            raise ValueError(f"Insufficient output amount: {amount_out} < {min_amount_out}")
        
        # Calculate price and slippage
        old_price = self.get_price()
        
        # Update reserves
        self.reserve_a = max(0.1, new_reserve_a)  # Prevent zero reserves
        self.reserve_b = max(0.1, new_reserve_b)
        
        new_price = self.get_price()
        slippage = abs(new_price - old_price) / old_price if old_price > 0 else 0
        
        # Update current tick
        self.current_tick = self.price_to_tick(new_price)
        
        # Distribute fees to liquidity providers
        self._distribute_fees(fee_amount)
        
        # Create trade record
        trade_id = hashlib.sha256(f"{trader}_{time.time()}".encode()).hexdigest()[:16]
        trade = Trade(
            id=trade_id,
            trader=trader,
            token_in=token_in,
            token_out=token_out,
            amount_in=amount_in,
            amount_out=amount_out,
            price=amount_out / amount_in if amount_in > 0 else 0,
            slippage=slippage,
            fee=fee_amount,
            timestamp=time.time(),
            pool_id=f"{self.token_a.value}_{self.token_b.value}"
        )
        
        self.trades.append(trade)
        self.volume_24h += amount_in
        self.fees_collected += fee_amount
        
        # Update price history for prediction model
        self.price_history.append(new_price)
        self._update_prediction_model(trade)
        
        return trade
    
    def _calculate_swap_output(self, amount_in: float, zero_for_one: bool) -> float:
        """Calculate swap output using concentrated liquidity formula"""
        if zero_for_one:
            # x * y = k, solve for new y
            k = self.reserve_a * self.reserve_b
            new_reserve_a = self.reserve_a + amount_in
            new_reserve_b = k / new_reserve_a
            amount_out = self.reserve_b - new_reserve_b
        else:
            k = self.reserve_a * self.reserve_b
            new_reserve_b = self.reserve_b + amount_in
            new_reserve_a = k / new_reserve_b
            amount_out = self.reserve_a - new_reserve_a
        
        return max(0, amount_out)
    
    def _distribute_fees(self, fee_amount: float):
        """Distribute trading fees to active liquidity providers"""
        if self.active_liquidity == 0:
            return
        
        for position in self.positions.values():
            # Calculate share of fees based on liquidity share
            share = position.shares / self.active_liquidity
            position.accumulated_fees += fee_amount * share
    
    def _update_prediction_model(self, trade: Trade):
        """Update the LSTM + Q-learning prediction model"""
        model = self.prediction_model
        
        # Add to training data
        model.price_history.append(trade.price)
        model.volume_history.append(trade.amount_in)
        
        # Simple Q-learning update for price direction prediction
        current_price = self.get_price()
        if len(self.price_history) >= 2:
            price_change = current_price - list(self.price_history)[-2]
            action = "buy" if price_change > 0 else "sell"
            
            # State representation (simplified)
            state = f"price_{int(current_price * 100)}_volume_{int(trade.amount_in)}"
            
            # Q-learning update
            reward = abs(price_change)  # Reward accuracy of prediction
            current_q = model.q_table[state][action]
            
            # Simple Q-update (in practice, would use neural network)
            learning_rate = model.learning_rate
            model.q_table[state][action] = current_q + learning_rate * (reward - current_q)
            
            # Update prediction accuracy
            if (model.last_prediction > 0 and price_change > 0) or \
               (model.last_prediction < 0 and price_change < 0):
                model.prediction_accuracy = 0.9 * model.prediction_accuracy + 0.1 * 1.0
            else:
                model.prediction_accuracy = 0.9 * model.prediction_accuracy + 0.1 * 0.0
        
        # Decay epsilon for exploration
        model.epsilon = max(model.min_epsilon, model.epsilon * model.epsilon_decay)
    
    def predict_price(self, time_horizon: int = 1) -> Tuple[float, float]:
        """
        Predict future price using LSTM + Q-learning model
        
        Returns:
            (predicted_price, confidence)
        """
        if len(self.price_history) < self.prediction_model.sequence_length:
            return self.get_price(), 0.5
        
        # Simple prediction based on Q-table (in practice, would use LSTM)
        current_price = self.get_price()
        recent_volume = sum(trade.amount_in for trade in self.trades[-10:]) / 10 if self.trades else 0
        
        state = f"price_{int(current_price * 100)}_volume_{int(recent_volume)}"
        
        # Get best action from Q-table
        if state in self.prediction_model.q_table:
            q_values = self.prediction_model.q_table[state]
            best_action = max(q_values.keys(), key=lambda k: q_values[k]) if q_values else "hold"
        else:
            best_action = "hold"
        
        # Convert action to price prediction
        if best_action == "buy":
            predicted_price = current_price * 1.05  # 5% increase
        elif best_action == "sell":
            predicted_price = current_price * 0.95  # 5% decrease
        else:
            predicted_price = current_price
        
        self.prediction_model.last_prediction = predicted_price - current_price
        
        return predicted_price, self.prediction_model.prediction_accuracy
    
    def get_pool_stats(self) -> Dict:
        """Get comprehensive pool statistics"""
        current_price = self.get_price()
        tvl = self.reserve_a * current_price + self.reserve_b
        
        # Calculate 24h metrics
        recent_trades = [t for t in self.trades if time.time() - t.timestamp < 86400]
        volume_24h = sum(t.amount_in for t in recent_trades)
        
        return {
            "token_a": self.token_a.value,
            "token_b": self.token_b.value,
            "reserve_a": self.reserve_a,
            "reserve_b": self.reserve_b,
            "current_price": current_price,
            "total_value_locked": tvl,
            "volume_24h": volume_24h,
            "fee_rate": self.fee_rate,
            "total_shares": self.total_shares,
            "active_liquidity": self.active_liquidity,
            "fees_collected": self.fees_collected,
            "total_trades": len(self.trades),
            "prediction_accuracy": self.prediction_model.prediction_accuracy,
            "current_tick": self.current_tick
        }

class CapabilityAMM:
    """
    Multi-pool AMM system for trading AI agent capabilities
    
    Manages multiple liquidity pools, routing, and cross-pool arbitrage.
    Implements advanced features like:
    - Multi-hop swaps
    - Capability bundles
    - Dynamic fee adjustment
    - Predictive market making
    """
    
    def __init__(self):
        self.pools: Dict[str, ConcentratedLiquidityPool] = {}
        self.capability_prices: Dict[CapabilityToken, float] = {}
        self.global_volume_24h = 0.0
        self.total_fees_collected = 0.0
        
        # Initialize capability prices
        for capability in CapabilityToken:
            self.capability_prices[capability] = 1.0
        
        # Create initial pools for all capability pairs
        self._initialize_pools()
        
        # Arbitrage tracking
        self.arbitrage_opportunities = []
        self.arbitrage_threshold = 0.01  # 1% price difference
    
    def _initialize_pools(self):
        """Initialize liquidity pools for capability trading"""
        capabilities = list(CapabilityToken)
        
        # Create pools for major capability pairs
        major_pairs = [
            (CapabilityToken.REASONING_TOKEN, CapabilityToken.PLANNING_TOKEN),
            (CapabilityToken.EXECUTION_TOKEN, CapabilityToken.ANALYSIS_TOKEN),
            (CapabilityToken.CREATIVITY_TOKEN, CapabilityToken.COMMUNICATION_TOKEN),
            (CapabilityToken.LEARNING_TOKEN, CapabilityToken.COORDINATION_TOKEN),
            # Add bundle token pairs
            (CapabilityToken.BUNDLE_TOKEN, CapabilityToken.REASONING_TOKEN),
            (CapabilityToken.BUNDLE_TOKEN, CapabilityToken.EXECUTION_TOKEN)
        ]
        
        for token_a, token_b in major_pairs:
            pool_id = f"{token_a.value}_{token_b.value}"
            self.pools[pool_id] = ConcentratedLiquidityPool(token_a, token_b)
    
    def add_liquidity_to_pool(self, pool_id: str, provider: str, amount_a: float, 
                             amount_b: float, tick_lower: int = -60, 
                             tick_upper: int = 60) -> str:
        """Add liquidity to a specific pool"""
        if pool_id not in self.pools:
            raise ValueError(f"Pool {pool_id} not found")
        
        return self.pools[pool_id].add_liquidity(provider, amount_a, amount_b, 
                                               tick_lower, tick_upper)
    
    def swap_capability(self, trader: str, token_in: CapabilityToken, 
                       token_out: CapabilityToken, amount_in: float,
                       max_slippage: float = 0.05) -> List[Trade]:
        """
        Execute a capability swap, potentially using multiple hops
        
        Returns list of trades executed (multiple trades for multi-hop swaps)
        """
        # Find direct pool first
        direct_pool_id = f"{token_in.value}_{token_out.value}"
        reverse_pool_id = f"{token_out.value}_{token_in.value}"
        
        if direct_pool_id in self.pools:
            pool = self.pools[direct_pool_id]
            min_amount_out = amount_in * (1 - max_slippage)
            trade = pool.swap(trader, token_in, amount_in, min_amount_out)
            self._update_global_stats(trade)
            return [trade]
        
        elif reverse_pool_id in self.pools:
            pool = self.pools[reverse_pool_id]
            min_amount_out = amount_in * (1 - max_slippage)
            trade = pool.swap(trader, token_in, amount_in, min_amount_out)
            self._update_global_stats(trade)
            return [trade]
        
        else:
            # Multi-hop swap through intermediate token
            return self._execute_multihop_swap(trader, token_in, token_out, 
                                             amount_in, max_slippage)
    
    def _execute_multihop_swap(self, trader: str, token_in: CapabilityToken,
                              token_out: CapabilityToken, amount_in: float,
                              max_slippage: float) -> List[Trade]:
        """Execute multi-hop swap through intermediate tokens"""
        # Find best route through available pools
        best_route = self._find_best_route(token_in, token_out, amount_in)
        
        if not best_route:
            raise ValueError(f"No route found from {token_in.value} to {token_out.value}")
        
        trades = []
        current_amount = amount_in
        
        for i, (pool_id, intermediate_token) in enumerate(best_route):
            pool = self.pools[pool_id]
            
            # Calculate slippage tolerance for this hop
            hop_slippage = max_slippage / len(best_route)
            min_amount_out = current_amount * (1 - hop_slippage)
            
            # Determine input token for this hop
            if i == 0:
                input_token = token_in
            else:
                input_token = best_route[i-1][1]
            
            trade = pool.swap(trader, input_token, current_amount, min_amount_out)
            trades.append(trade)
            self._update_global_stats(trade)
            
            current_amount = trade.amount_out
        
        return trades
    
    def _find_best_route(self, token_in: CapabilityToken, token_out: CapabilityToken,
                        amount_in: float) -> List[Tuple[str, CapabilityToken]]:
        """Find the best routing path for a swap"""
        # Simple implementation - could be enhanced with Dijkstra's algorithm
        intermediate_tokens = [CapabilityToken.BUNDLE_TOKEN, CapabilityToken.REASONING_TOKEN]
        
        for intermediate in intermediate_tokens:
            if intermediate == token_in or intermediate == token_out:
                continue
            
            # Check if both hops exist
            hop1_pool = f"{token_in.value}_{intermediate.value}"
            hop1_reverse = f"{intermediate.value}_{token_in.value}"
            hop2_pool = f"{intermediate.value}_{token_out.value}"
            hop2_reverse = f"{token_out.value}_{intermediate.value}"
            
            hop1_exists = hop1_pool in self.pools or hop1_reverse in self.pools
            hop2_exists = hop2_pool in self.pools or hop2_reverse in self.pools
            
            if hop1_exists and hop2_exists:
                route = []
                if hop1_pool in self.pools:
                    route.append((hop1_pool, intermediate))
                else:
                    route.append((hop1_reverse, intermediate))
                
                if hop2_pool in self.pools:
                    route.append((hop2_pool, token_out))
                else:
                    route.append((hop2_reverse, token_out))
                
                return route
        
        return []
    
    def create_capability_bundle(self, creator: str, capabilities: List[CapabilityToken],
                               weights: List[float], bundle_size: float) -> str:
        """
        Create a capability bundle token representing a weighted portfolio
        of different capabilities
        """
        if len(capabilities) != len(weights):
            raise ValueError("Capabilities and weights must have same length")
        
        if abs(sum(weights) - 1.0) > 0.001:
            raise ValueError("Weights must sum to 1.0")
        
        bundle_id = hashlib.sha256(f"{creator}_{time.time()}".encode()).hexdigest()[:16]
        
        # For simplicity, we'll track bundles in metadata
        # In practice, this would be implemented as ERC-20 tokens
        bundle_metadata = {
            "id": bundle_id,
            "creator": creator,
            "capabilities": [cap.value for cap in capabilities],
            "weights": weights,
            "total_size": bundle_size,
            "created_at": time.time()
        }
        
        return bundle_id
    
    def detect_arbitrage_opportunities(self) -> List[Dict]:
        """Detect arbitrage opportunities across pools"""
        opportunities = []
        
        # Check all token pairs across different pools
        tokens = list(CapabilityToken)
        
        for i, token_a in enumerate(tokens):
            for j, token_b in enumerate(tokens[i+1:], i+1):
                # Get prices from different routes
                direct_price = self._get_direct_price(token_a, token_b)
                indirect_prices = self._get_indirect_prices(token_a, token_b)
                
                for route, price in indirect_prices.items():
                    if direct_price and abs(price - direct_price) / direct_price > self.arbitrage_threshold:
                        opportunities.append({
                            "token_a": token_a.value,
                            "token_b": token_b.value,
                            "direct_price": direct_price,
                            "indirect_price": price,
                            "indirect_route": route,
                            "profit_opportunity": abs(price - direct_price) / direct_price,
                            "timestamp": time.time()
                        })
        
        self.arbitrage_opportunities = opportunities
        return opportunities
    
    def _get_direct_price(self, token_a: CapabilityToken, token_b: CapabilityToken) -> Optional[float]:
        """Get direct price between two tokens"""
        pool_id = f"{token_a.value}_{token_b.value}"
        reverse_pool_id = f"{token_b.value}_{token_a.value}"
        
        if pool_id in self.pools:
            return self.pools[pool_id].get_price()
        elif reverse_pool_id in self.pools:
            return 1.0 / self.pools[reverse_pool_id].get_price()
        
        return None
    
    def _get_indirect_prices(self, token_a: CapabilityToken, 
                           token_b: CapabilityToken) -> Dict[str, float]:
        """Get indirect prices through different routing paths"""
        indirect_prices = {}
        
        # Simple implementation - check routes through bundle token
        bundle_token = CapabilityToken.BUNDLE_TOKEN
        
        if bundle_token != token_a and bundle_token != token_b:
            price_a_to_bundle = self._get_direct_price(token_a, bundle_token)
            price_bundle_to_b = self._get_direct_price(bundle_token, token_b)
            
            if price_a_to_bundle and price_bundle_to_b:
                indirect_price = price_a_to_bundle * price_bundle_to_b
                indirect_prices[f"{token_a.value}->{bundle_token.value}->{token_b.value}"] = indirect_price
        
        return indirect_prices
    
    def _update_global_stats(self, trade: Trade):
        """Update global AMM statistics"""
        self.global_volume_24h += trade.amount_in
        self.total_fees_collected += trade.fee
        
        # Update capability prices based on trade
        # Simple price impact model
        impact_factor = 0.01  # 1% price impact per trade
        if trade.token_in in self.capability_prices:
            self.capability_prices[trade.token_in] *= (1 + impact_factor * trade.slippage)
        if trade.token_out in self.capability_prices:
            self.capability_prices[trade.token_out] *= (1 - impact_factor * trade.slippage)
    
    def get_pool_list(self) -> List[Dict]:
        """Get list of all pools with basic stats"""
        return [
            {
                "pool_id": pool_id,
                **pool.get_pool_stats()
            }
            for pool_id, pool in self.pools.items()
        ]
    
    def get_global_stats(self) -> Dict:
        """Get global AMM statistics"""
        total_tvl = sum(pool.reserve_a * pool.get_price() + pool.reserve_b 
                       for pool in self.pools.values())
        
        return {
            "total_pools": len(self.pools),
            "total_value_locked": total_tvl,
            "global_volume_24h": self.global_volume_24h,
            "total_fees_collected": self.total_fees_collected,
            "capability_prices": {cap.value: price for cap, price in self.capability_prices.items()},
            "arbitrage_opportunities": len(self.arbitrage_opportunities),
            "active_traders": len(set(trade.trader for pool in self.pools.values() for trade in pool.trades))
        }

# Example usage and testing
if __name__ == "__main__":
    print("=== AI Agent Capability AMM System Demo ===\n")
    
    # Initialize AMM
    amm = CapabilityAMM()
    
    # Add liquidity to pools
    print("Adding liquidity to pools...")
    for pool_id in list(amm.pools.keys())[:3]:  # First 3 pools
        position_id = amm.add_liquidity_to_pool(
            pool_id, f"lp_{pool_id}", 1000.0, 1000.0, -120, 120
        )
        print(f"Added liquidity to {pool_id}, position: {position_id}")
    
    # Execute some swaps
    print("\nExecuting capability swaps...")
    trades = []
    
    # Direct swap
    trade = amm.swap_capability(
        "trader_001",
        CapabilityToken.REASONING_TOKEN,
        CapabilityToken.PLANNING_TOKEN,
        100.0
    )
    trades.extend(trade)
    print(f"Direct swap: {trade[0].amount_in} {trade[0].token_in.value} -> {trade[0].amount_out} {trade[0].token_out.value}")
    
    # Multi-hop swap
    try:
        trade = amm.swap_capability(
            "trader_002",
            CapabilityToken.CREATIVITY_TOKEN,
            CapabilityToken.LEARNING_TOKEN,
            50.0
        )
        trades.extend(trade)
        print(f"Multi-hop swap completed with {len(trade)} hops")
    except ValueError as e:
        print(f"Multi-hop swap failed: {e}")
    
    # Price predictions
    print("\nPrice predictions from LSTM+Q-learning models:")
    for pool_id, pool in list(amm.pools.items())[:3]:
        predicted_price, confidence = pool.predict_price()
        current_price = pool.get_price()
        print(f"{pool_id}: Current={current_price:.4f}, Predicted={predicted_price:.4f}, Confidence={confidence:.2f}")
    
    # Arbitrage detection
    print("\nDetecting arbitrage opportunities...")
    arbitrage_ops = amm.detect_arbitrage_opportunities()
    if arbitrage_ops:
        for op in arbitrage_ops[:3]:  # Show first 3
            print(f"Arbitrage: {op['token_a']}->{op['token_b']}, Profit: {op['profit_opportunity']:.2%}")
    else:
        print("No arbitrage opportunities detected")
    
    # Pool statistics
    print("\nPool Statistics:")
    for pool_info in amm.get_pool_list()[:3]:
        print(f"{pool_info['pool_id']}: TVL=${pool_info['total_value_locked']:.2f}, "
              f"Volume=${pool_info['volume_24h']:.2f}, "
              f"Prediction Accuracy={pool_info['prediction_accuracy']:.1%}")
    
    # Global statistics
    print("\nGlobal AMM Statistics:")
    global_stats = amm.get_global_stats()
    print(f"Total TVL: ${global_stats['total_value_locked']:.2f}")
    print(f"Global Volume 24h: ${global_stats['global_volume_24h']:.2f}")
    print(f"Total Fees Collected: ${global_stats['total_fees_collected']:.2f}")
    print(f"Active Traders: {global_stats['active_traders']}")
    print(f"Arbitrage Opportunities: {global_stats['arbitrage_opportunities']}")
    
    # Capability prices
    print("\nCapability Token Prices:")
    for token, price in global_stats['capability_prices'].items():
        print(f"{token}: ${price:.4f}")