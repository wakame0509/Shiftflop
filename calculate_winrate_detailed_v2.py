import eval7
import random

def evaluate_hand(hand, board):
    full_hand = hand + board
    eval_hand = eval7.Hand(eval7.Card(full_hand[0]), eval7.Card(full_hand[1]))
    eval_board = [eval7.Card(c) for c in board]
    return eval_hand.evaluate(eval_board)

def simulate_winrate_vs_range(hero_hand, board, opponent_range, iterations=1000):
    """
    自分のハンドとボードに対して、25%レンジの相手と対戦したときの勝率を推定
    """
    wins, ties = 0, 0
    deck = [eval7.Card(rank + suit) for rank in '23456789TJQKA' for suit in 'cdhs']
    used_cards = set(hero_hand + board)

    for card in used_cards:
        deck.remove(eval7.Card(card))

    for _ in range(iterations):
        random.shuffle(deck)
        sampled_opponent = random.choice(opponent_range)
        opp_hand = [eval7.Card(sampled_opponent[0]), eval7.Card(sampled_opponent[1])]

        if opp_hand[0] in used_cards or opp_hand[1] in used_cards:
            continue

        remaining = deck.copy()
        if len(board) == 3:
            sample_board = board + [str(remaining[0]), str(remaining[1])]
        elif len(board) == 4:
            sample_board = board + [str(remaining[0])]
        else:
            sample_board = board

        hero_val = evaluate_hand(hero_hand, sample_board)
        opp_val = evaluate_hand(sampled_opponent, sample_board)

        if hero_val > opp_val:
            wins += 1
        elif hero_val == opp_val:
            ties += 1

    total = wins + ties + (iterations - wins - ties)
    return (wins + ties / 2) / total if total > 0 else 0.0

def simulate_winrate_for_flop_type(hero_hand, flop_list, opponent_range, iterations=1000):
    """
    指定フロップタイプのフロップ全通りのうちランダムに抽出し、平均的な勝率を出す
    """
    winrates = []
    for _ in range(iterations):
        flop = random.choice(flop_list)
        winrate = simulate_winrate_vs_range(hero_hand, flop, opponent_range, iterations=1)
        winrates.append(winrate)
    return sum(winrates) / len(winrates)

def simulate_shift_turn(hero_hand, flop, turn_candidates, opponent_range, iterations=1000):
    """
    ターンに指定カードが落ちた場合の勝率を計算（1枚ずつ数え上げ）
    """
    results = {}
    for turn_card in turn_candidates:
        if turn_card in flop or turn_card in hero_hand:
            continue
        board = flop + [turn_card]
        winrate = simulate_winrate_vs_range(hero_hand, board, opponent_range, iterations)
        results[turn_card] = round(winrate * 100, 2)
    return results
