"""
Configuration management for Autonomous Strategy Evolution Framework.
Centralized configuration with environment variable support.
"""

import os
from dataclasses import dataclass
from typing import Dict, List, Optional
from enum import Enum
import logging
from dotenv import load_dotenv

load_dotenv()

class MarketCondition(Enum):
    """Market regime classifications"""
    TRENDING_BULL = "trending_bull"
    TRENDING_BEAR = "trending_bear"
    RANGING = "ranging"
    VOLATILE = "volatile"
    LOW_VOLATILITY = "low_volatility"

class RiskLevel(Enum):
    """Risk tolerance levels"""
    CONSERVATIVE = 0.1
    MODERATE = 0.3
    AGGRESSIVE = 0.5

@dataclass
class ExchangeConfig:
    """Exchange-specific configuration"""
    name: str
    api_key: str = ""
    api_secret: str = ""
    sandbox_mode: bool = True
    rate_limit: int = 1000

@dataclass
class StrategyConfig:
    """Strategy generation parameters"""
    max_strategies_per_generation: int = 50
    min_performance_threshold: float = 0.15  # 15% minimum Sharpe ratio
    max_drawdown_limit: float = 0.25  # 25% max drawdown
    lookback_periods: List[int] = None
    
    def __post_init__(self):
        if self.lookback_periods is None:
            self.lookback_periods = [50, 100, 200]

@dataclass
class EvolutionConfig:
    """Evolution algorithm parameters"""
    population_size: int = 100
    mutation_rate: float = 0.1
    crossover_rate: float = 0.7
    elitism_count: int = 5
    max_generations: int = 100
    performance_metric: str = "sharpe_ratio"

class Config:
    """Main configuration class"""
    
    def __init__(self):
        # Firebase configuration
        self.firebase_credentials_path = os.getenv("FIREBASE_CREDENTIALS_PATH", "./service_account.json")
        self.firestore_collections = {
            "strategies": "trading_strategies",
            "performance": "strategy_performance",
            "market_data": "market_conditions",
            "execution_logs": "execution_logs"
        }
        
        # Trading configuration
        self.default_pair = os.getenv("DEFAULT_PAIR", "BTC/USDT")
        self.timeframes = ["1h", "4h", "1d"]
        self.initial_capital = float(os.getenv("INITIAL_CAPITAL", 10000.0))
        
        # Exchange configuration
        self.exchange = ExchangeConfig(
            name=os.getenv("EXCHANGE_NAME", "binance"),
            api_key=os.getenv("EXCHANGE_API_KEY", ""),
            api_secret=os.getenv("EXCHANGE_API_SECRET", ""),
            sandbox_mode=os.getenv("SANDBOX_MODE", "true").lower() == "true"
        )
        
        # Strategy configuration
        self.strategy = StrategyConfig()
        
        # Evolution configuration
        self.evolution = EvolutionConfig()
        
        # Risk management
        self.risk_level = RiskLevel.MODERATE
        self.max_position_size = 0.1  # 10% of capital per position
        self.stop_loss_range = (0.02, 0.05)  # 2-5% stop loss
        self.take_profit_range = (0.03, 0.08)  # 3-8% take profit
        
        # Logging configuration
        self.log_level = getattr(logging, os.getenv("LOG_LEVEL", "INFO"))
        self.log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        
    def validate(self) -> bool:
        """Validate configuration"""
        if not os.path.exists(self.firebase_credentials_path):
            logging.error(f"Firebase credentials not found at {self.firebase_credentials_path}")
            return False
        
        if self.initial_capital <= 0:
            logging.error(f"Initial capital must be positive: {self.initial_capital}")
            return False
            
        return True

# Global configuration instance
config = Config()