"""
Physics engine with Numba acceleration
Handles collision detection, energy transfer, and food consumption
"""
import math
from typing import List, Tuple
from .entity import Entity
from .food_spawner import Food
from .spatial_grid import SpatialGrid


class PhysicsEngine:
    """Manages all physics calculations and interactions"""
    
    def __init__(self, world_width: int, world_height: int):
        self.world_width = world_width
        self.world_height = world_height
        self.spatial_grid = SpatialGrid(cell_size=50)
    
    def update(self, entities: List[Entity], foods: List[Food], dt: float) -> Tuple[List[Entity], List[Food]]:
        """Update all physics for one timestep"""
        # Rebuild spatial grid
        self.spatial_grid.update_entities(entities)
        self.spatial_grid.update_foods(foods)
        
        # Check food consumption
        foods = self.check_food_consumption(entities, foods)
        
        # Check entity collisions (simple separation)
        self.resolve_entity_collisions(entities)
        
        return entities, foods
    
    def check_food_consumption(self, entities: List[Entity], foods: List[Food]) -> List[Food]:
        """Check if any entity is close enough to eat food"""
        remaining_foods = []
        
        for food in foods:
            eaten = False
            
            # Get nearby entities using spatial grid
            nearby_entities = self.spatial_grid.get_nearby(food.x, food.y)
            
            for entity in nearby_entities:
                if not isinstance(entity, Entity):
                    continue
                
                # Calculate distance
                dx = entity.x - food.x
                dy = entity.y - food.y
                dist_sq = dx * dx + dy * dy
                eat_dist_sq = (entity.radius + food.radius) ** 2
                
                if dist_sq < eat_dist_sq:
                    entity.eat_food(food.energy)
                    eaten = True
                    break
            
            if not eaten:
                remaining_foods.append(food)
        
        return remaining_foods
    
    def resolve_entity_collisions(self, entities: List[Entity]):
        """Simple collision resolution - push entities apart"""
        for i, entity1 in enumerate(entities):
            # Get nearby entities using spatial grid
            nearby = self.spatial_grid.get_nearby(entity1.x, entity1.y)
            
            for entity2 in nearby:
                if not isinstance(entity2, Entity):
                    continue
                if entity1.id == entity2.id:
                    continue
                
                # Calculate distance
                dx = entity2.x - entity1.x
                dy = entity2.y - entity1.y
                dist_sq = dx * dx + dy * dy
                min_dist = entity1.radius + entity2.radius
                
                if dist_sq < min_dist * min_dist and dist_sq > 0:
                    # Push apart
                    dist = math.sqrt(dist_sq)
                    overlap = min_dist - dist
                    nx = dx / dist
                    ny = dy / dist
                    
                    # Move each entity half the overlap distance
                    entity1.x -= nx * overlap * 0.5
                    entity1.y -= ny * overlap * 0.5
                    entity2.x += nx * overlap * 0.5
                    entity2.y += ny * overlap * 0.5
    
    def distance_to_nearest(self, x: float, y: float, objects: List) -> Tuple[float, object]:
        """Find nearest object from a list"""
        if not objects:
            return float('inf'), None
        
        min_dist = float('inf')
        nearest = None
        
        for obj in objects:
            dx = obj.x - x
            dy = obj.y - y
            dist = math.sqrt(dx * dx + dy * dy)
            
            if dist < min_dist:
                min_dist = dist
                nearest = obj
        
        return min_dist, nearest
