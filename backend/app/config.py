"""
Configuration management for VIVARIUM ZERO
Loads settings from environment variables
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # World Settings
    world_width: int = 800
    world_height: int = 600
    initial_population: int = 20
    max_population: int = 500
    
    # Energy Economy
    photosynthesis_rate: float = 0.5
    existence_tax: float = 0.2
    food_energy: float = 20.0
    food_spawn_interval: float = 2.0
    food_spawn_count: int = 3
    
    # Evolution
    mutation_rate: float = 0.01
    reproduction_energy: float = 80.0
    
    # Performance
    target_fps: int = 60
    max_gas_per_tick: int = 50

    # Features
    enable_vm: bool = False
    
    # Database
    snapshot_interval: int = 300
    database_path: str = "./data/vivarium.db"
    
    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
