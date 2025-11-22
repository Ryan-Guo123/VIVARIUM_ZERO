"""
Unit tests for Spatial Grid
"""
import pytest
from app.core.spatial_grid import SpatialGrid
from app.core.entity import Entity


def test_spatial_grid_creation():
    """Test spatial grid initialization"""
    grid = SpatialGrid(cell_size=50)
    
    assert grid.cell_size == 50
    assert len(grid.grid) == 0


def test_insert_and_retrieve():
    """Test inserting objects and retrieving nearby ones"""
    grid = SpatialGrid(cell_size=50)
    
    entity1 = Entity(x=100, y=100)
    entity2 = Entity(x=110, y=110)
    entity3 = Entity(x=500, y=500)
    
    # Insert entities
    grid.insert(entity1, entity1.x, entity1.y)
    grid.insert(entity2, entity2.x, entity2.y)
    grid.insert(entity3, entity3.x, entity3.y)
    
    # Get nearby entities from (100, 100)
    nearby = grid.get_nearby(100, 100)
    
    # Should find entity1 and entity2 (both in same area)
    # but NOT entity3 (far away)
    assert entity1 in nearby
    assert entity2 in nearby
    assert entity3 not in nearby


def test_clear_grid():
    """Test clearing the grid"""
    grid = SpatialGrid(cell_size=50)
    
    entity = Entity(x=100, y=100)
    grid.insert(entity, entity.x, entity.y)
    
    assert len(grid.grid) > 0
    
    grid.clear()
    
    assert len(grid.grid) == 0


def test_update_entities():
    """Test rebuilding grid with entity list"""
    grid = SpatialGrid(cell_size=50)
    
    entities = [
        Entity(x=100, y=100),
        Entity(x=200, y=200),
        Entity(x=300, y=300),
    ]
    
    grid.update_entities(entities)
    
    # Grid should have entries
    assert len(grid.grid) > 0
    
    # Should be able to find nearby entities
    nearby = grid.get_nearby(100, 100)
    assert len(nearby) > 0


def test_cell_boundaries():
    """Test that objects in different cells are separated"""
    grid = SpatialGrid(cell_size=50)
    
    # Create entities in different cells
    entity1 = Entity(x=25, y=25)    # Cell (0, 0)
    entity2 = Entity(x=200, y=200)  # Cell (4, 4)
    
    grid.insert(entity1, entity1.x, entity1.y)
    grid.insert(entity2, entity2.x, entity2.y)
    
    # From cell (0, 0), should not find entity in cell (4, 4)
    nearby = grid.get_nearby(25, 25)
    
    assert entity1 in nearby
    assert entity2 not in nearby
