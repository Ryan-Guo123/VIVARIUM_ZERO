"""
World - The main simulation container
Manages the entire simulation state and update loop
"""
import random
import time
from typing import List, Dict
from .entity import Entity
from .food_spawner import FoodSpawner, Food
from .physics import PhysicsEngine
from ..config import settings


class World:
    """The VIVARIUM world - contains all entities and manages simulation"""
    
    def __init__(self):
        self.width = settings.world_width
        self.height = settings.world_height
        
        # Simulation state
        self.entities: List[Entity] = []
        self.foods: List[Food] = []
        self.generation = 0
        self.tick = 0
        self.paused = False
        self.step_mode = False  # For single-step debugging
        
        # Systems
        self.physics = PhysicsEngine(self.width, self.height)
        self.food_spawner = FoodSpawner(
            world_width=self.width,
            world_height=self.height,
            spawn_interval=settings.food_spawn_interval,
            spawn_count=settings.food_spawn_count,
            food_energy=settings.food_energy
        )
        
        # Performance tracking
        self.last_update_time = time.time()
        self.dt = 1.0 / settings.target_fps
        
        # Initialize world
        self._spawn_initial_population()
    
    def _spawn_initial_population(self):
        """Create initial population of entities"""
        for i in range(settings.initial_population):
            entity = Entity(
                x=random.uniform(50, self.width - 50),
                y=random.uniform(50, self.height - 50),
                energy=random.uniform(40, 60),
                color=self._get_random_color()
            )
            self.entities.append(entity)
        
        # Spawn some initial food
        self.foods = self.food_spawner.spawn_food()
    
    def _get_random_color(self) -> tuple:
        """Generate random creature color"""
        colors = [
            (255, 100, 100),  # Red
            (100, 100, 255),  # Blue
            (255, 255, 100),  # Yellow
            (255, 150, 255),  # Pink
            (100, 255, 255),  # Cyan
        ]
        return random.choice(colors)
    
    def update(self):
        """Main simulation update loop"""
        if self.paused and not self.step_mode:
            return
        
        # Reset step mode after one update
        if self.step_mode:
            self.step_mode = False
            self.paused = True
        
        # Update entities
        alive_entities = []
        new_entities = []
        
        for entity in self.entities:
            # Phase 1/2: Choose behavior by feature flag
            if settings.enable_vm:
                entity.execute_genome()
            else:
                entity.simple_behavior()
            
            # Update physics
            entity.update_physics(self.dt, self.width, self.height)
            
            # Update energy (photosynthesis and existence tax)
            entity.update_energy(
                self.dt,
                settings.photosynthesis_rate,
                settings.existence_tax
            )
            
            # Check reproduction
            if entity.can_reproduce(settings.reproduction_energy):
                child = entity.reproduce()
                new_entities.append(child)
            
            # Check if alive
            if entity.is_alive():
                alive_entities.append(entity)
            else:
                # Entity died - create food from corpse
                corpse_food = Food(
                    id=f"corpse_{entity.id[:8]}",
                    x=entity.x,
                    y=entity.y,
                    energy=10.0,  # Corpse provides some energy
                    color=(150, 75, 0)  # Brown for corpses
                )
                self.foods.append(corpse_food)
        
        # Add new offspring
        alive_entities.extend(new_entities)
        
        # Apply population cap
        if len(alive_entities) > settings.max_population:
            # Kill random entities if over capacity (environmental pressure)
            alive_entities = random.sample(alive_entities, settings.max_population)
        
        self.entities = alive_entities
        
        # Update physics (collision detection, food consumption)
        self.entities, self.foods = self.physics.update(self.entities, self.foods, self.dt)
        
        # Spawn new food
        self.foods = self.food_spawner.update(self.dt, self.foods)
        
        # Update counters
        self.tick += 1
        if len(self.entities) > 0:
            max_gen = max(e.generation for e in self.entities)
            if max_gen > self.generation:
                self.generation = max_gen
    
    def get_state(self) -> Dict:
        """Get current world state for transmission to clients"""
        return {
            'tick': self.tick,
            'generation': self.generation,
            'population': len(self.entities),
            'food_count': len(self.foods),
            'paused': self.paused,
            'entities': [e.to_dict() for e in self.entities],
            'foods': [f.to_dict() for f in self.foods],
            'world_width': self.width,
            'world_height': self.height,
        }
    
    def get_statistics(self) -> Dict:
        """Get simulation statistics"""
        if not self.entities:
            return {
                'population': 0,
                'avg_energy': 0,
                'avg_age': 0,
                'generation': self.generation
            }
        
        return {
            'population': len(self.entities),
            'avg_energy': sum(e.energy for e in self.entities) / len(self.entities),
            'avg_age': sum(e.age for e in self.entities) / len(self.entities),
            'generation': self.generation,
            'food_count': len(self.foods)
        }
    
    def pause(self):
        """Pause simulation"""
        self.paused = True
    
    def resume(self):
        """Resume simulation"""
        self.paused = False
        self.step_mode = False
    
    def step(self):
        """Execute single simulation step"""
        self.step_mode = True
        self.paused = False
    
    def reset(self):
        """Reset world to initial state"""
        self.entities.clear()
        self.foods.clear()
        self.tick = 0
        self.generation = 0
        self._spawn_initial_population()
