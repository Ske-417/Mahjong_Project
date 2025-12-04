"""
麻雀山 (Mahjong Wall/Deck)
Manages the collection of all tiles in the game
"""

import random
from typing import List
from mahjong_tile import Tile, TileType, JihaiType


class Wall:
    """麻雀山 (Wall) - The collection of all tiles in the game"""
    
    def __init__(self, shuffle: bool = True):
        """
        Initialize the wall with all 136 tiles
        
        Args:
            shuffle: Whether to shuffle the tiles (default True)
        """
        self.tiles: List[Tile] = []
        self._initialize_tiles()
        if shuffle:
            self.shuffle()
    
    def _initialize_tiles(self):
        """Create all 136 tiles (4 of each type)"""
        # Number tiles: Manzu, Pinzu, Souzu (1-9 each, 4 copies)
        for tile_type in [TileType.MANZU, TileType.PINZU, TileType.SOUZU]:
            for value in range(1, 10):
                for _ in range(4):  # 4 copies of each tile
                    self.tiles.append(Tile(tile_type, value))
        
        # Honor tiles: 7 types, 4 copies each
        for jihai in JihaiType:
            for _ in range(4):
                self.tiles.append(Tile(TileType.JIHAI, jihai=jihai))
    
    def shuffle(self):
        """Shuffle the tiles"""
        random.shuffle(self.tiles)
    
    def draw_tile(self) -> Tile:
        """
        Draw a tile from the wall
        
        Returns:
            A tile from the wall
            
        Raises:
            IndexError: If the wall is empty
        """
        if not self.tiles:
            raise IndexError("Wall is empty")
        return self.tiles.pop()
    
    def draw_tiles(self, count: int) -> List[Tile]:
        """
        Draw multiple tiles from the wall
        
        Args:
            count: Number of tiles to draw
            
        Returns:
            List of tiles drawn
            
        Raises:
            ValueError: If count exceeds available tiles
        """
        if count > len(self.tiles):
            raise ValueError(f"Cannot draw {count} tiles, only {len(self.tiles)} available")
        
        drawn = []
        for _ in range(count):
            drawn.append(self.draw_tile())
        return drawn
    
    def remaining_count(self) -> int:
        """Get the number of remaining tiles in the wall"""
        return len(self.tiles)
    
    def is_empty(self) -> bool:
        """Check if the wall is empty"""
        return len(self.tiles) == 0
