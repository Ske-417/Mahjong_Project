"""
Tests for Mahjong game
"""

import unittest
from mahjong_tile import Tile, TileType, JihaiType
from mahjong_wall import Wall
from mahjong_hand import Hand
from mahjong_game import MahjongGame, Player


class TestTile(unittest.TestCase):
    """Test Tile class"""
    
    def test_create_number_tile(self):
        """Test creating number tiles"""
        tile = Tile(TileType.MANZU, 5)
        self.assertEqual(tile.tile_type, TileType.MANZU)
        self.assertEqual(tile.value, 5)
        self.assertIsNone(tile.jihai)
    
    def test_create_honor_tile(self):
        """Test creating honor tiles"""
        tile = Tile(TileType.JIHAI, jihai=JihaiType.TON)
        self.assertEqual(tile.tile_type, TileType.JIHAI)
        self.assertIsNone(tile.value)
        self.assertEqual(tile.jihai, JihaiType.TON)
    
    def test_tile_equality(self):
        """Test tile equality"""
        tile1 = Tile(TileType.PINZU, 3)
        tile2 = Tile(TileType.PINZU, 3)
        tile3 = Tile(TileType.PINZU, 4)
        self.assertEqual(tile1, tile2)
        self.assertNotEqual(tile1, tile3)
    
    def test_tile_sorting(self):
        """Test tile sorting"""
        tiles = [
            Tile(TileType.JIHAI, jihai=JihaiType.HAKU),
            Tile(TileType.SOUZU, 5),
            Tile(TileType.MANZU, 1),
            Tile(TileType.PINZU, 9)
        ]
        sorted_tiles = sorted(tiles)
        self.assertEqual(sorted_tiles[0].tile_type, TileType.MANZU)
        self.assertEqual(sorted_tiles[1].tile_type, TileType.PINZU)
        self.assertEqual(sorted_tiles[2].tile_type, TileType.SOUZU)
        self.assertEqual(sorted_tiles[3].tile_type, TileType.JIHAI)
    
    def test_terminal_tiles(self):
        """Test terminal tile detection"""
        tile1 = Tile(TileType.MANZU, 1)
        tile9 = Tile(TileType.MANZU, 9)
        tile5 = Tile(TileType.MANZU, 5)
        
        self.assertTrue(tile1.is_terminal())
        self.assertTrue(tile9.is_terminal())
        self.assertFalse(tile5.is_terminal())
    
    def test_simple_tiles(self):
        """Test simple tile detection"""
        tile2 = Tile(TileType.SOUZU, 2)
        tile8 = Tile(TileType.SOUZU, 8)
        tile1 = Tile(TileType.SOUZU, 1)
        
        self.assertTrue(tile2.is_simple())
        self.assertTrue(tile8.is_simple())
        self.assertFalse(tile1.is_simple())


class TestWall(unittest.TestCase):
    """Test Wall class"""
    
    def test_wall_initialization(self):
        """Test wall has correct number of tiles"""
        wall = Wall(shuffle=False)
        self.assertEqual(wall.remaining_count(), 136)
    
    def test_draw_tile(self):
        """Test drawing tiles"""
        wall = Wall(shuffle=False)
        initial_count = wall.remaining_count()
        tile = wall.draw_tile()
        self.assertIsInstance(tile, Tile)
        self.assertEqual(wall.remaining_count(), initial_count - 1)
    
    def test_draw_multiple_tiles(self):
        """Test drawing multiple tiles"""
        wall = Wall(shuffle=False)
        tiles = wall.draw_tiles(13)
        self.assertEqual(len(tiles), 13)
        self.assertEqual(wall.remaining_count(), 136 - 13)
    
    def test_wall_empty(self):
        """Test wall empty detection"""
        wall = Wall(shuffle=False)
        wall.draw_tiles(136)
        self.assertTrue(wall.is_empty())
        with self.assertRaises(IndexError):
            wall.draw_tile()


class TestHand(unittest.TestCase):
    """Test Hand class"""
    
    def test_add_tile(self):
        """Test adding tiles to hand"""
        hand = Hand()
        tile = Tile(TileType.MANZU, 5)
        hand.add_tile(tile)
        self.assertEqual(hand.get_tile_count(), 1)
        self.assertIn(tile, hand.tiles)
    
    def test_discard_tile(self):
        """Test discarding tiles"""
        hand = Hand()
        tile = Tile(TileType.PINZU, 7)
        hand.add_tile(tile)
        result = hand.discard_tile(tile)
        self.assertTrue(result)
        self.assertEqual(hand.get_tile_count(), 0)
    
    def test_check_win_simple(self):
        """Test simple winning hand detection"""
        hand = Hand()
        
        # Create a simple winning hand: 111 222 333 444 55
        for _ in range(3):
            hand.add_tile(Tile(TileType.MANZU, 1))
        for _ in range(3):
            hand.add_tile(Tile(TileType.MANZU, 2))
        for _ in range(3):
            hand.add_tile(Tile(TileType.MANZU, 3))
        for _ in range(3):
            hand.add_tile(Tile(TileType.MANZU, 4))
        for _ in range(2):
            hand.add_tile(Tile(TileType.MANZU, 5))
        
        self.assertTrue(hand.check_win())
    
    def test_check_win_with_sequences(self):
        """Test winning hand with sequences"""
        hand = Hand()
        
        # Create hand with sequences: 123 456 789 m + 11 p
        for value in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
            hand.add_tile(Tile(TileType.MANZU, value))
        for value in [4, 5, 6]:
            hand.add_tile(Tile(TileType.MANZU, value))
        for _ in range(2):
            hand.add_tile(Tile(TileType.PINZU, 1))
        
        self.assertTrue(hand.check_win())


class TestPlayer(unittest.TestCase):
    """Test Player class"""
    
    def test_create_player(self):
        """Test creating a player"""
        player = Player("Test Player")
        self.assertEqual(player.name, "Test Player")
        self.assertEqual(player.score, 25000)
        self.assertEqual(player.hand.get_tile_count(), 0)
    
    def test_draw_and_discard(self):
        """Test drawing and discarding tiles"""
        player = Player("Test")
        tile = Tile(TileType.SOUZU, 3)
        player.draw_tile(tile)
        self.assertEqual(player.hand.get_tile_count(), 1)
        
        player.discard_tile(tile)
        self.assertEqual(player.hand.get_tile_count(), 0)
        self.assertEqual(len(player.discards), 1)


class TestMahjongGame(unittest.TestCase):
    """Test MahjongGame class"""
    
    def test_create_game(self):
        """Test creating a game"""
        game = MahjongGame(["Player1", "Player2", "Player3", "Player4"])
        self.assertEqual(len(game.players), 4)
        self.assertEqual(game.wall.remaining_count(), 136)
    
    def test_deal_initial_tiles(self):
        """Test dealing initial tiles"""
        game = MahjongGame(["P1", "P2", "P3", "P4"])
        game.deal_initial_tiles()
        
        for player in game.players:
            self.assertEqual(player.hand.get_tile_count(), 13)
        
        # 4 players * 13 tiles = 52 tiles dealt
        self.assertEqual(game.wall.remaining_count(), 136 - 52)
    
    def test_turn_progression(self):
        """Test turn progression"""
        game = MahjongGame(["P1", "P2", "P3", "P4"])
        
        self.assertEqual(game.current_player_index, 0)
        game.next_player()
        self.assertEqual(game.current_player_index, 1)
        game.next_player()
        self.assertEqual(game.current_player_index, 2)
        game.next_player()
        self.assertEqual(game.current_player_index, 3)
        game.next_player()
        self.assertEqual(game.current_player_index, 0)  # Back to first player
    
    def test_game_requires_4_players(self):
        """Test that game requires exactly 4 players"""
        with self.assertRaises(ValueError):
            MahjongGame(["P1", "P2", "P3"])


if __name__ == "__main__":
    unittest.main()
