"""
麻雀ゲーム (Mahjong Game)
Main game logic for Mahjong
"""

from typing import List, Optional
from mahjong_tile import Tile
from mahjong_wall import Wall
from mahjong_hand import Hand


class Player:
    """麻雀プレイヤー (Mahjong player)"""
    
    def __init__(self, name: str):
        """
        Initialize a player
        
        Args:
            name: Player's name
        """
        self.name = name
        self.hand = Hand()
        self.discards: List[Tile] = []
        self.score = 25000  # Starting score in standard rules
    
    def draw_tile(self, tile: Tile):
        """Draw a tile from the wall"""
        self.hand.add_tile(tile)
    
    def discard_tile(self, tile: Tile) -> bool:
        """
        Discard a tile
        
        Args:
            tile: The tile to discard
            
        Returns:
            True if successful, False otherwise
        """
        if self.hand.discard_tile(tile):
            self.discards.append(tile)
            return True
        return False
    
    def __str__(self) -> str:
        return f"{self.name} (Score: {self.score})"


class MahjongGame:
    """麻雀ゲーム (Mahjong game)"""
    
    def __init__(self, player_names: List[str]):
        """
        Initialize a Mahjong game
        
        Args:
            player_names: List of player names (must be 4 players)
        """
        if len(player_names) != 4:
            raise ValueError("Mahjong requires exactly 4 players")
        
        self.players = [Player(name) for name in player_names]
        self.wall = Wall()
        self.current_player_index = 0
        self.round_number = 1
        self.round_wind = "東"  # East round
        self.game_over = False
    
    def deal_initial_tiles(self):
        """Deal 13 tiles to each player"""
        for player in self.players:
            tiles = self.wall.draw_tiles(13)
            player.hand.add_tiles(tiles)
    
    def get_current_player(self) -> Player:
        """Get the current player"""
        return self.players[self.current_player_index]
    
    def next_player(self):
        """Move to the next player"""
        self.current_player_index = (self.current_player_index + 1) % 4
    
    def draw_phase(self) -> Tile:
        """
        Current player draws a tile
        
        Returns:
            The tile drawn
        """
        if self.wall.is_empty():
            self.game_over = True
            raise IndexError("Wall is empty - game is a draw")
        
        tile = self.wall.draw_tile()
        self.get_current_player().draw_tile(tile)
        return tile
    
    def discard_phase(self, tile: Tile) -> bool:
        """
        Current player discards a tile
        
        Args:
            tile: The tile to discard
            
        Returns:
            True if successful, False otherwise
        """
        return self.get_current_player().discard_tile(tile)
    
    def check_win(self, player: Player) -> bool:
        """
        Check if a player has won
        
        Args:
            player: The player to check
            
        Returns:
            True if player has won, False otherwise
        """
        return player.hand.check_win()
    
    def check_tenpai(self, player: Player) -> bool:
        """
        Check if a player is in tenpai (ready to win)
        
        Args:
            player: The player to check
            
        Returns:
            True if player is in tenpai, False otherwise
        """
        return player.hand.check_tenpai()
    
    def get_game_state(self) -> dict:
        """
        Get current game state
        
        Returns:
            Dictionary with game state information
        """
        return {
            "round": self.round_number,
            "round_wind": self.round_wind,
            "current_player": self.get_current_player().name,
            "wall_remaining": self.wall.remaining_count(),
            "players": [
                {
                    "name": p.name,
                    "score": p.score,
                    "hand_size": p.hand.get_tile_count(),
                    "discards": len(p.discards)
                }
                for p in self.players
            ]
        }
    
    def start_game(self):
        """Start a new game"""
        self.wall = Wall()
        self.current_player_index = 0
        self.game_over = False
        self.deal_initial_tiles()
