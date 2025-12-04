"""
麻雀手牌 (Mahjong Hand)
Represents a player's hand of tiles
"""

from typing import List, Set, Tuple
from collections import Counter
from mahjong_tile import Tile, TileType


class Hand:
    """麻雀手牌 (Player's hand)"""
    
    def __init__(self):
        """Initialize an empty hand"""
        self.tiles: List[Tile] = []
        self.melds: List[List[Tile]] = []  # For pon, chi, kan
    
    def add_tile(self, tile: Tile):
        """Add a tile to the hand"""
        self.tiles.append(tile)
        self.tiles.sort()
    
    def add_tiles(self, tiles: List[Tile]):
        """Add multiple tiles to the hand"""
        self.tiles.extend(tiles)
        self.tiles.sort()
    
    def discard_tile(self, tile: Tile) -> bool:
        """
        Discard a tile from the hand
        
        Args:
            tile: The tile to discard
            
        Returns:
            True if tile was found and discarded, False otherwise
        """
        try:
            self.tiles.remove(tile)
            return True
        except ValueError:
            return False
    
    def get_tile_count(self) -> int:
        """Get the number of tiles in hand (excluding melds)"""
        return len(self.tiles)
    
    def get_total_tile_count(self) -> int:
        """Get total tiles including melds"""
        meld_count = sum(len(meld) for meld in self.melds)
        return len(self.tiles) + meld_count
    
    def __str__(self) -> str:
        """String representation of the hand"""
        return " ".join(str(tile) for tile in self.tiles)
    
    def check_tenpai(self) -> bool:
        """
        Check if hand is in tenpai (ready to win)
        Simple implementation: checks if 1 tile away from complete hand
        """
        # Need 14 tiles for complete hand (or 13 + 1 draw)
        if self.get_tile_count() != 13:
            return False
        
        # Check if adding any possible tile would create a winning hand
        all_possible_tiles = self._get_all_possible_tiles()
        for tile in all_possible_tiles:
            test_hand = Hand()
            test_hand.tiles = self.tiles.copy()
            test_hand.add_tile(tile)
            if test_hand.check_win():
                return True
        return False
    
    def check_win(self) -> bool:
        """
        Check if hand is a winning hand (agari)
        Basic implementation: 4 melds (sets of 3) + 1 pair
        """
        if self.get_tile_count() != 14:
            return False
        
        # Try each tile as the pair
        tile_counts = Counter(self.tiles)
        for pair_tile, count in tile_counts.items():
            if count >= 2:
                # Try this as the pair
                remaining = self.tiles.copy()
                remaining.remove(pair_tile)
                remaining.remove(pair_tile)
                
                if self._check_melds(remaining):
                    return True
        
        return False
    
    def _check_melds(self, tiles: List[Tile]) -> bool:
        """
        Recursively check if tiles can form valid melds
        A meld is either:
        - Pon: 3 identical tiles
        - Chi: 3 consecutive tiles of the same suit
        """
        if not tiles:
            return True
        
        if len(tiles) % 3 != 0:
            return False
        
        tiles = sorted(tiles)
        first_tile = tiles[0]
        
        # Try pon (3 identical tiles)
        if tiles.count(first_tile) >= 3:
            remaining = tiles.copy()
            for _ in range(3):
                remaining.remove(first_tile)
            if self._check_melds(remaining):
                return True
        
        # Try chi (3 consecutive tiles of same suit)
        if first_tile.tile_type != TileType.JIHAI:
            # Look for tile+1 and tile+2
            tile_plus_1 = Tile(first_tile.tile_type, first_tile.value + 1)
            tile_plus_2 = Tile(first_tile.tile_type, first_tile.value + 2)
            
            if (first_tile.value <= 7 and 
                tile_plus_1 in tiles and 
                tile_plus_2 in tiles):
                remaining = tiles.copy()
                remaining.remove(first_tile)
                remaining.remove(tile_plus_1)
                remaining.remove(tile_plus_2)
                if self._check_melds(remaining):
                    return True
        
        return False
    
    def _get_all_possible_tiles(self) -> Set[Tile]:
        """Get set of all possible tile types"""
        tiles = set()
        
        # Number tiles
        for tile_type in [TileType.MANZU, TileType.PINZU, TileType.SOUZU]:
            for value in range(1, 10):
                tiles.add(Tile(tile_type, value))
        
        # Honor tiles
        from mahjong_tile import JihaiType
        for jihai in JihaiType:
            tiles.add(Tile(TileType.JIHAI, jihai=jihai))
        
        return tiles
    
    def get_waiting_tiles(self) -> List[Tile]:
        """
        Get tiles that would complete the hand (machi)
        Returns list of tiles that would create a winning hand
        """
        if self.get_tile_count() != 13:
            return []
        
        waiting = []
        all_possible_tiles = self._get_all_possible_tiles()
        
        for tile in all_possible_tiles:
            test_hand = Hand()
            test_hand.tiles = self.tiles.copy()
            test_hand.add_tile(tile)
            if test_hand.check_win():
                waiting.append(tile)
        
        return waiting
