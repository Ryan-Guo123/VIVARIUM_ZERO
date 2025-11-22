"""
Spatial grid for efficient collision detection
Uses grid-based spatial partitioning to reduce collision checks from O(N²) to O(N)
"""
from typing import Dict, List, Tuple, Set
from collections import defaultdict


class SpatialGrid:
    """Grid-based spatial partitioning for fast neighbor queries"""
    
    def __init__(self, cell_size: int = 50):
        self.cell_size = cell_size
        self.grid: Dict[Tuple[int, int], List] = defaultdict(list)
    
    def clear(self):
        """Clear all grid cells"""
        self.grid.clear()
    
    def _get_cell(self, x: float, y: float) -> Tuple[int, int]:
        """Convert world coordinates to grid cell coordinates"""
        return (int(x // self.cell_size), int(y // self.cell_size))
    
    def insert(self, obj, x: float, y: float):
        """Insert an object at given position"""
        cell = self._get_cell(x, y)
        self.grid[cell].append(obj)
    
    def get_nearby(self, x: float, y: float, radius: float = 0) -> List:
        """Get all objects in nearby cells (including diagonals)"""
        cell_x, cell_y = self._get_cell(x, y)
        
        # Check 3x3 grid around the cell
        nearby = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                cell = (cell_x + dx, cell_y + dy)
                if cell in self.grid:
                    nearby.extend(self.grid[cell])
        
        return nearby
    
    def update_entities(self, entities: List):
        """Rebuild grid with current entity positions"""
        self.clear()
        for entity in entities:
            self.insert(entity, entity.x, entity.y)
    
    def update_foods(self, foods: List):
        """Add foods to grid"""
        for food in foods:
            self.insert(food, food.x, food.y)
