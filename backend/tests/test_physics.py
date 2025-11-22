"""
Unit tests for Physics Engine
"""
import pytest
from app.core.entity import Entity
from app.core.food_spawner import Food
from app.core.physics import PhysicsEngine


def test_physics_engine_creation():
    """Test physics engine initialization"""
    physics = PhysicsEngine(world_width=800, world_height=600)
    
    assert physics.world_width == 800
    assert physics.world_height == 600
    assert physics.spatial_grid is not None


def test_food_consumption():
    """Test entity eating food when close enough"""
    physics = PhysicsEngine(800, 600)
    
    entity = Entity(x=100, y=100, energy=50)
    food = Food(id="food1", x=105, y=105, energy=20)
    
    entities = [entity]
    foods = [food]
    
    # Update physics
    entities, remaining_foods = physics.update(entities, foods, dt=0.016)
    
    # Food should be eaten
    assert len(remaining_foods) == 0
    assert entity.energy == 70


def test_food_not_consumed_when_far():
    """Test food is not eaten when entity is too far"""
    physics = PhysicsEngine(800, 600)
    
    entity = Entity(x=100, y=100, energy=50)
    food = Food(id="food1", x=200, y=200, energy=20)
    
    entities = [entity]
    foods = [food]
    
    # Update physics
    entities, remaining_foods = physics.update(entities, foods, dt=0.016)
    
    # Food should remain
    assert len(remaining_foods) == 1
    assert entity.energy == 50


def test_entity_collision_resolution():
    """Test entities push apart when colliding"""
    physics = PhysicsEngine(800, 600)
    
    # Create two entities very close together
    entity1 = Entity(x=100, y=100, radius=8)
    entity2 = Entity(x=102, y=100, radius=8)
    
    initial_distance = abs(entity2.x - entity1.x)
    
    entities = [entity1, entity2]
    
    # Update physics multiple times
    for _ in range(5):
        entities, _ = physics.update(entities, [], dt=0.016)
    
    # Entities should be pushed apart
    final_distance = abs(entity2.x - entity1.x)
    assert final_distance > initial_distance


def test_distance_to_nearest():
    """Test finding nearest object"""
    physics = PhysicsEngine(800, 600)
    
    foods = [
        Food(id="f1", x=100, y=100, energy=20),
        Food(id="f2", x=200, y=200, energy=20),
        Food(id="f3", x=50, y=50, energy=20),
    ]
    
    # From origin, f3 should be nearest
    dist, nearest = physics.distance_to_nearest(0, 0, foods)
    
    assert nearest is not None
    assert nearest.id == "f3"
    assert dist < 100
