"""
Unit tests for Entity class
"""
import pytest
from app.core.entity import Entity


def test_entity_creation():
    """Test basic entity creation"""
    entity = Entity(x=100, y=100, energy=50)
    
    assert entity.x == 100
    assert entity.y == 100
    assert entity.energy == 50
    assert entity.is_alive() is True
    assert entity.id is not None


def test_entity_energy_update():
    """Test energy updates (photosynthesis and existence tax)"""
    entity = Entity(energy=50)
    
    # Update with photosynthesis and existence tax
    entity.update_energy(dt=1.0, photosynthesis=0.5, existence_tax=0.2)
    
    # Should gain +0.5 - 0.2 = +0.3 per second
    assert entity.energy == pytest.approx(50.3)


def test_entity_death():
    """Test entity death when energy reaches 0"""
    entity = Entity(energy=1.0)
    
    # Drain energy
    entity.update_energy(dt=10.0, photosynthesis=0.0, existence_tax=0.2)
    
    assert entity.energy <= 0
    assert entity.is_alive() is False


def test_entity_food_consumption():
    """Test eating food"""
    entity = Entity(energy=50)
    
    entity.eat_food(20)
    
    assert entity.energy == 70


def test_entity_reproduction():
    """Test reproduction splits energy"""
    parent = Entity(energy=100)
    
    child = parent.reproduce()
    
    assert parent.energy == 50
    assert child.energy == 50
    assert child.generation == parent.generation + 1
    assert child.parent_id == parent.id


def test_entity_wall_collision():
    """Test wall collision and bounce"""
    entity = Entity(x=10, y=10, vx=50, vy=0)
    entity.radius = 8
    
    # Update physics - should hit left wall
    entity.update_physics(dt=1.0, world_width=800, world_height=600)
    
    # Should be pushed back and velocity reversed
    assert entity.x >= entity.radius
    assert entity.vx < 0  # Reversed


def test_entity_can_reproduce():
    """Test reproduction threshold"""
    entity = Entity(energy=79)
    assert entity.can_reproduce(80) is False
    
    entity.energy = 80
    assert entity.can_reproduce(80) is True
    
    entity.energy = 100
    assert entity.can_reproduce(80) is True


def test_entity_to_dict():
    """Test serialization to dictionary"""
    entity = Entity(x=100, y=200, energy=50)
    
    data = entity.to_dict()
    
    assert 'id' in data
    assert 'x' in data
    assert 'y' in data
    assert 'energy' in data
    assert data['x'] == 100
    assert data['y'] == 200
