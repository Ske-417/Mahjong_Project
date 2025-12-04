"""
麻雀ゲームのデモ (Mahjong Game Demo)
Demonstrates basic functionality of the Mahjong game
"""

from mahjong_tile import Tile, TileType, JihaiType
from mahjong_wall import Wall
from mahjong_hand import Hand
from mahjong_game import MahjongGame


def demo_tiles():
    """Demonstrate tile creation and properties"""
    print("=" * 60)
    print("牌のデモ (Tile Demo)")
    print("=" * 60)
    
    # Create various tiles
    tiles = [
        Tile(TileType.MANZU, 1),
        Tile(TileType.PINZU, 5),
        Tile(TileType.SOUZU, 9),
        Tile(TileType.JIHAI, jihai=JihaiType.TON),
        Tile(TileType.JIHAI, jihai=JihaiType.HAKU),
    ]
    
    print("\n作成した牌:")
    for tile in tiles:
        print(f"  {tile} - Terminal: {tile.is_terminal()}, "
              f"Honor: {tile.is_honor()}, Simple: {tile.is_simple()}")
    
    print("\nソート後:")
    sorted_tiles = sorted(tiles)
    print(f"  {' '.join(str(t) for t in sorted_tiles)}")


def demo_wall():
    """Demonstrate wall functionality"""
    print("\n" + "=" * 60)
    print("牌山のデモ (Wall Demo)")
    print("=" * 60)
    
    wall = Wall(shuffle=False)
    print(f"\n牌山の初期枚数: {wall.remaining_count()}枚")
    
    # Draw some tiles
    drawn = wall.draw_tiles(5)
    print(f"\n5枚引いた: {' '.join(str(t) for t in drawn)}")
    print(f"残り枚数: {wall.remaining_count()}枚")


def demo_hand():
    """Demonstrate hand functionality"""
    print("\n" + "=" * 60)
    print("手牌のデモ (Hand Demo)")
    print("=" * 60)
    
    hand = Hand()
    
    # Add a simple winning hand
    print("\n和了形の手牌を作成:")
    # 111 222 333 m, 456 p, 77 s
    for _ in range(3):
        hand.add_tile(Tile(TileType.MANZU, 1))
    for _ in range(3):
        hand.add_tile(Tile(TileType.MANZU, 2))
    for _ in range(3):
        hand.add_tile(Tile(TileType.MANZU, 3))
    for val in [4, 5, 6]:
        hand.add_tile(Tile(TileType.PINZU, val))
    for _ in range(2):
        hand.add_tile(Tile(TileType.SOUZU, 7))
    
    print(f"手牌: {hand}")
    print(f"枚数: {hand.get_tile_count()}")
    print(f"和了: {hand.check_win()}")
    
    # Demonstrate tenpai
    print("\n聴牌形の手牌を作成:")
    hand2 = Hand()
    # Remove one tile to make it tenpai
    for _ in range(3):
        hand2.add_tile(Tile(TileType.MANZU, 1))
    for _ in range(3):
        hand2.add_tile(Tile(TileType.MANZU, 2))
    for _ in range(3):
        hand2.add_tile(Tile(TileType.MANZU, 3))
    for val in [4, 5, 6]:
        hand2.add_tile(Tile(TileType.PINZU, val))
    hand2.add_tile(Tile(TileType.SOUZU, 7))  # Only 1 instead of pair
    
    print(f"手牌: {hand2}")
    print(f"聴牌: {hand2.check_tenpai()}")
    waiting = hand2.get_waiting_tiles()
    if waiting:
        print(f"待ち牌: {' '.join(str(t) for t in waiting)}")


def demo_game():
    """Demonstrate game functionality"""
    print("\n" + "=" * 60)
    print("ゲームのデモ (Game Demo)")
    print("=" * 60)
    
    # Create a game
    game = MahjongGame(["東家", "南家", "西家", "北家"])
    game.start_game()
    
    print("\nゲーム開始")
    state = game.get_game_state()
    
    print(f"\n局: {state['round_wind']} {state['round']}局")
    print(f"牌山残り: {state['wall_remaining']}枚")
    
    print("\nプレイヤー:")
    for player_info in state['players']:
        print(f"  {player_info['name']}: {player_info['score']}点 "
              f"(手牌{player_info['hand_size']}枚)")
    
    # Show first player's hand
    first_player = game.get_current_player()
    print(f"\n{first_player.name}の手牌:")
    print(f"  {first_player.hand}")


def main():
    """Run all demos"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + "麻雀ゲーム デモンストレーション".center(58) + "║")
    print("║" + "Mahjong Game Demonstration".center(58) + "║")
    print("╚" + "=" * 58 + "╝")
    
    demo_tiles()
    demo_wall()
    demo_hand()
    demo_game()
    
    print("\n" + "=" * 60)
    print("デモ終了 (Demo Complete)")
    print("=" * 60)
    print("\nゲームをプレイするには: python mahjong_cli.py")
    print("テストを実行するには: python test_mahjong.py")
    print()


if __name__ == "__main__":
    main()
