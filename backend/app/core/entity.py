"""
Entity class - represents a living creature in the simulation
Phase 1: Simple entity with hardcoded behavior (random walk)
Phase 2: Will be extended with VM genome execution
"""
import random
import math
from typing import List, Tuple, Optional
from dataclasses import dataclass, field
import uuid

from .vm.interpreter import VMInterpreter
from .vm.genome import seed_wanderer
from ..config import settings

@dataclass
class Entity:
    """A living creature in the VIVARIUM"""
    
    # Identity
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    generation: int = 0
    parent_id: Optional[str] = None
    
    # Physics
    x: float = 0.0
    y: float = 0.0
    vx: float = 0.0
    vy: float = 0.0
    angle: float = 0.0  # in radians
    radius: float = 8.0
    
    # Biology
    energy: float = 50.0
    max_energy: float = 100.0
    age: int = 0  # in ticks
    
    # Phenotype (visual traits)
    color: Tuple[int, int, int] = (200, 200, 200)
    
    # Trail for visualization
    trail: List[Tuple[float, float]] = field(default_factory=list)
    max_trail_length: int = 20

    # Genome (Phase 2)
    genome: List = field(default_factory=list)
    
    def __post_init__(self):
        """Initialize random starting angle"""
        if self.angle == 0.0:
            self.angle = random.uniform(0, 2 * math.pi)
        if settings.enable_vm and not self.genome:
            self.genome = seed_wanderer()
    
    def update_physics(self, dt: float, world_width: int, world_height: int):
        """Update position and handle wall collisions"""
        # Update position
        self.x += self.vx * dt
        self.y += self.vy * dt
        
        # Wall collision with bounce
        if self.x - self.radius < 0:
            self.x = self.radius
            self.vx *= -0.8  # Energy loss on bounce
        elif self.x + self.radius > world_width:
            self.x = world_width - self.radius
            self.vx *= -0.8
        
        if self.y - self.radius < 0:
            self.y = self.radius
            self.vy *= -0.8
        elif self.y + self.radius > world_height:
            self.y = world_height - self.radius
            self.vy *= -0.8
        
        # Update trail
        self.trail.append((self.x, self.y))
        if len(self.trail) > self.max_trail_length:
            self.trail.pop(0)
    
    def update_energy(self, dt: float, photosynthesis: float, existence_tax: float):
        """Update energy based on passive income and costs"""
        self.energy += photosynthesis * dt
        self.energy -= existence_tax * dt
        self.energy = min(self.energy, self.max_energy)
        self.age += 1
    
    def is_alive(self) -> bool:
        """Check if entity is still alive"""
        return self.energy > 0
    
    def can_reproduce(self, threshold: float) -> bool:
        """Check if entity has enough energy to reproduce"""
        return self.energy >= threshold
    
    def simple_behavior(self):
        """Phase 1: Hardcoded random walk behavior"""
        # Random walk with occasional direction changes
        if random.random() < 0.02:  # 2% chance to turn
            self.angle += random.uniform(-math.pi/4, math.pi/4)
        
        # Move forward
        speed = 30.0
        self.vx = math.cos(self.angle) * speed
        self.vy = math.sin(self.angle) * speed

    def execute_genome(self):
        """Phase 2: Execute genome via VM (fallback to simple if empty)"""
        if not self.genome:
            return self.simple_behavior()
        vm = VMInterpreter(max_gas=settings.max_gas_per_tick)
        vm.execute(self, self.genome)
    
    def eat_food(self, food_energy: float):
        """Consume food and gain energy"""
        self.energy += food_energy
        self.energy = min(self.energy, self.max_energy)
    
    def reproduce(self) -> 'Entity':
        """Create offspring with half of parent's energy"""
        # Split energy
        child_energy = self.energy / 2
        self.energy = child_energy
        
        # Create child near parent
        offset = random.uniform(-20, 20)
        child = Entity(
            x=self.x + offset,
            y=self.y + offset,
            energy=child_energy,
            generation=self.generation + 1,
            parent_id=self.id,
            color=self.color  # Phase 1: inherit color
        )
        
        return child
    
    def to_dict(self) -> dict:
        """Serialize to dictionary for JSON transmission"""
        return {
            'id': self.id,
            'x': self.x,
            'y': self.y,
            'angle': self.angle,
            'radius': self.radius,
            'energy': self.energy,
            'max_energy': self.max_energy,
            'age': self.age,
            'generation': self.generation,
            'color': self.color,
            'trail': self.trail[-5:] if self.trail else []  # Send only last 5 points
        }
