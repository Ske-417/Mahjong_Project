"""
麻雀牌 (Mahjong Tile) classes
Represents the tiles used in Japanese Mahjong (Riichi Mahjong)
"""

from enum import Enum
from typing import Optional


class TileType(Enum):
    """牌の種類 (Tile types)"""
    MANZU = "萬子"  # Characters (man)
    PINZU = "筒子"  # Dots (pin)
    SOUZU = "索子"  # Bamboo (sou)
    JIHAI = "字牌"  # Honor tiles


class JihaiType(Enum):
    """字牌の種類 (Honor tile types)"""
    TON = "東"    # East
    NAN = "南"    # South
    SHA = "西"    # West
    PEI = "北"    # North
    HAKU = "白"   # White dragon
    HATSU = "發"  # Green dragon
    CHUN = "中"   # Red dragon


class Tile:
    """麻雀牌 (Mahjong tile)"""
    
    def __init__(self, tile_type: TileType, value: Optional[int] = None, 
                 jihai: Optional[JihaiType] = None):
        """
        Initialize a Mahjong tile
        
        Args:
            tile_type: Type of the tile (manzu, pinzu, souzu, or jihai)
            value: Value for number tiles (1-9), None for honor tiles
            jihai: Type of honor tile if tile_type is JIHAI
        """
        self.tile_type = tile_type
        self.value = value
        self.jihai = jihai
        
        # Validation
        if tile_type != TileType.JIHAI:
            if value is None or value < 1 or value > 9:
                raise ValueError(f"Number tiles must have value 1-9, got {value}")
            if jihai is not None:
                raise ValueError("Number tiles cannot have jihai type")
        else:
            if jihai is None:
                raise ValueError("Honor tiles must have jihai type")
            if value is not None:
                raise ValueError("Honor tiles cannot have numeric value")
    
    def __str__(self) -> str:
        """String representation of the tile"""
        if self.tile_type == TileType.JIHAI:
            return self.jihai.value
        else:
            return f"{self.value}{self.tile_type.value[0]}"
    
    def __repr__(self) -> str:
        """Detailed representation of the tile"""
        if self.tile_type == TileType.JIHAI:
            return f"Tile({self.tile_type.name}, {self.jihai.name})"
        else:
            return f"Tile({self.tile_type.name}, {self.value})"
    
    def __eq__(self, other) -> bool:
        """Check if two tiles are equal"""
        if not isinstance(other, Tile):
            return False
        return (self.tile_type == other.tile_type and 
                self.value == other.value and 
                self.jihai == other.jihai)
    
    def __hash__(self) -> int:
        """Hash function for using tiles in sets/dicts"""
        return hash((self.tile_type, self.value, self.jihai))
    
    def __lt__(self, other) -> bool:
        """Less than comparison for sorting"""
        if not isinstance(other, Tile):
            return NotImplemented
        
        # Sort order: manzu, pinzu, souzu, jihai
        type_order = [TileType.MANZU, TileType.PINZU, TileType.SOUZU, TileType.JIHAI]
        if self.tile_type != other.tile_type:
            return type_order.index(self.tile_type) < type_order.index(other.tile_type)
        
        if self.tile_type != TileType.JIHAI:
            return self.value < other.value
        else:
            jihai_order = [JihaiType.TON, JihaiType.NAN, JihaiType.SHA, JihaiType.PEI,
                          JihaiType.HAKU, JihaiType.HATSU, JihaiType.CHUN]
            return jihai_order.index(self.jihai) < jihai_order.index(other.jihai)
    
    def is_terminal(self) -> bool:
        """Check if tile is a terminal (1 or 9)"""
        return self.tile_type != TileType.JIHAI and self.value in [1, 9]
    
    def is_honor(self) -> bool:
        """Check if tile is an honor tile"""
        return self.tile_type == TileType.JIHAI
    
    def is_terminal_or_honor(self) -> bool:
        """Check if tile is terminal or honor (yaochuuhai)"""
        return self.is_terminal() or self.is_honor()
    
    def is_simple(self) -> bool:
        """Check if tile is a simple tile (2-8)"""
        return self.tile_type != TileType.JIHAI and 2 <= self.value <= 8
