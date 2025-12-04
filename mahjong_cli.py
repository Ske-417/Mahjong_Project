"""
麻雀CLI (Mahjong Command Line Interface)
Simple command-line interface to play Mahjong
"""

import sys
from mahjong_game import MahjongGame, Player
from mahjong_tile import Tile


def print_separator():
    """Print a separator line"""
    print("=" * 80)


def print_game_state(game: MahjongGame):
    """Print current game state"""
    print_separator()
    state = game.get_game_state()
    print(f"【{state['round_wind']} {state['round']}局】 牌山残り: {state['wall_remaining']}枚")
    print(f"現在のプレイヤー: {state['current_player']}")
    print_separator()
    
    for player_info in state['players']:
        print(f"{player_info['name']}: {player_info['score']}点 "
              f"(手牌{player_info['hand_size']}枚, 捨て牌{player_info['discards']}枚)")
    print_separator()


def print_hand(player: Player):
    """Print a player's hand"""
    print(f"\n{player.name}の手牌:")
    print(f"  {player.hand}")
    print(f"  ({player.hand.get_tile_count()}枚)")


def print_discards(player: Player):
    """Print a player's discards"""
    if player.discards:
        print(f"\n捨て牌: {' '.join(str(tile) for tile in player.discards)}")


def get_tile_choice(player: Player) -> Tile:
    """
    Get player's choice of tile to discard
    
    Args:
        player: The player choosing
        
    Returns:
        The chosen tile
    """
    tiles = player.hand.tiles
    
    print("\n牌を選んでください:")
    for i, tile in enumerate(tiles):
        print(f"  {i + 1}: {tile}")
    
    while True:
        try:
            choice = input(f"\n番号を入力 (1-{len(tiles)}): ").strip()
            if not choice:
                continue
            
            index = int(choice) - 1
            if 0 <= index < len(tiles):
                return tiles[index]
            else:
                print(f"1から{len(tiles)}の間で入力してください")
        except ValueError:
            print("数字を入力してください")
        except KeyboardInterrupt:
            print("\n\nゲームを終了します")
            sys.exit(0)


def play_turn(game: MahjongGame):
    """Play one turn"""
    current_player = game.get_current_player()
    
    print(f"\n{'='*80}")
    print(f"{current_player.name}のターン")
    print(f"{'='*80}")
    
    # Draw phase
    try:
        drawn_tile = game.draw_phase()
        print(f"\n引いた牌: {drawn_tile}")
    except IndexError as e:
        print(f"\n{e}")
        return False
    
    # Show hand
    print_hand(current_player)
    
    # Check for win
    if game.check_win(current_player):
        print(f"\n🎉 {current_player.name}の和了！ 🎉")
        print_hand(current_player)
        return False
    
    # Check for tenpai
    if game.check_tenpai(current_player):
        waiting_tiles = current_player.hand.get_waiting_tiles()
        print(f"\n【聴牌】待ち牌: {' '.join(str(tile) for tile in waiting_tiles)}")
    
    # Discard phase
    tile_to_discard = get_tile_choice(current_player)
    game.discard_phase(tile_to_discard)
    print(f"\n捨てた牌: {tile_to_discard}")
    
    # Show discards
    print_discards(current_player)
    
    # Move to next player
    game.next_player()
    
    return True


def main():
    """Main function to run the Mahjong game"""
    print("=" * 80)
    print("麻雀ゲーム (Mahjong Game)".center(80))
    print("=" * 80)
    
    # Get player names
    print("\nプレイヤー名を入力してください (4人)")
    player_names = []
    
    for i in range(4):
        while True:
            name = input(f"プレイヤー{i + 1}の名前: ").strip()
            if name:
                player_names.append(name)
                break
            else:
                print("名前を入力してください")
    
    # Initialize game
    game = MahjongGame(player_names)
    game.start_game()
    
    print("\nゲームを開始します！")
    print_game_state(game)
    
    # Game loop
    turn_count = 0
    max_turns = 200  # Prevent infinite loops
    
    while not game.game_over and turn_count < max_turns:
        turn_count += 1
        
        if not play_turn(game):
            break
        
        # Show game state every 4 turns
        if turn_count % 4 == 0:
            print_game_state(game)
    
    # Game end
    print("\n" + "=" * 80)
    print("ゲーム終了".center(80))
    print("=" * 80)
    
    # Show final scores
    print("\n最終スコア:")
    for player in game.players:
        print(f"  {player.name}: {player.score}点")
    
    print("\nご利用ありがとうございました！")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nゲームを終了します")
        sys.exit(0)
