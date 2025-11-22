"""
Food spawner - generates food particles in the world
"""
import random
from dataclasses import dataclass
from typing import Tuple
import uuid


@dataclass
class Food:
    """Food particle that creatures can eat"""
    
    id: str
    x: float
    y: float
    energy: float = 20.0
    radius: float = 5.0
    color: Tuple[int, int, int] = (50, 255, 50)  # Green
    
    def to_dict(self) -> dict:
        """Serialize to dictionary"""
        return {
            'id': self.id,
            'x': self.x,
            'y': self.y,
            'radius': self.radius,
            'color': self.color
        }


class FoodSpawner:
    """Manages food generation in the world"""
    
    def __init__(self, world_width: int, world_height: int, 
                 spawn_interval: float, spawn_count: int, food_energy: float):
        self.world_width = world_width
        self.world_height = world_height
        self.spawn_interval = spawn_interval
        self.spawn_count = spawn_count
        self.food_energy = food_energy
        self.time_since_spawn = 0.0
    
    def update(self, dt: float, foods: list) -> list:
        """Update spawner and generate new food if needed"""
        self.time_since_spawn += dt
        
        if self.time_since_spawn >= self.spawn_interval:
            self.time_since_spawn = 0.0
            new_foods = self.spawn_food()
            foods.extend(new_foods)
        
        return foods
    
    def spawn_food(self) -> list:
        """Generate new food particles at random positions"""
        foods = []
        for _ in range(self.spawn_count):
            food = Food(
                id=str(uuid.uuid4()),
                x=random.uniform(20, self.world_width - 20),
                y=random.uniform(20, self.world_height - 20),
                energy=self.food_energy
            )
            foods.append(food)
        return foods
