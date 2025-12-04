"""
Automated demo of the Mahjong CLI
Simulates a few turns of gameplay
"""

import sys
from io import StringIO
from mahjong_game import MahjongGame


def demo_cli_game():
    """Demonstrate a simple automated game"""
    print("=" * 80)
    print("麻雀CLI デモ - 自動プレイ".center(80))
    print("Mahjong CLI Demo - Automated Play".center(80))
    print("=" * 80)
    print()
    
    # Create game
    game = MahjongGame(["東家", "南家", "西家", "北家"])
    game.start_game()
    
    print("ゲーム開始！")
    print(f"局: {game.round_wind} {game.round_number}局")
    print(f"牌山残り: {game.wall.remaining_count()}枚")
    print()
    
    # Play a few turns
    for turn in range(8):
        current_player = game.get_current_player()
        print("-" * 80)
        print(f"ターン {turn + 1}: {current_player.name}")
        print("-" * 80)
        
        # Show hand before draw
        print(f"手牌（{current_player.hand.get_tile_count()}枚）: {current_player.hand}")
        
        # Draw
        if game.wall.is_empty():
            print("牌山が空になりました")
            break
            
        drawn_tile = game.draw_phase()
        print(f"ツモ: {drawn_tile}")
        
        # Show hand after draw
        print(f"手牌（{current_player.hand.get_tile_count()}枚）: {current_player.hand}")
        
        # Check for win
        if game.check_win(current_player):
            print(f"\n🎉🎉🎉 {current_player.name} 和了！ 🎉🎉🎉\n")
            break
        
        # Check for tenpai
        if game.check_tenpai(current_player):
            waiting = current_player.hand.get_waiting_tiles()
            print(f"【聴牌】待ち: {' '.join(str(t) for t in waiting)}")
        
        # Discard (automatically discard the first tile)
        tile_to_discard = current_player.hand.tiles[0]
        game.discard_phase(tile_to_discard)
        print(f"打牌: {tile_to_discard}")
        
        # Show discards
        if current_player.discards:
            print(f"捨て牌: {' '.join(str(t) for t in current_player.discards[-3:])}"
                  f"{' ...' if len(current_player.discards) > 3 else ''}")
        
        print()
        
        # Next player
        game.next_player()
    
    print("=" * 80)
    print("デモ終了".center(80))
    print("=" * 80)
    print()
    print("実際のゲームをプレイするには:")
    print("  python mahjong_cli.py")
    print()


if __name__ == "__main__":
    demo_cli_game()
