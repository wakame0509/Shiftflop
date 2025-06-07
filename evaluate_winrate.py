import random
import eval7

def evaluate_vs_range(hero_hand: str, board: list, opponent_range: list, trials: int = 100):
    """
    ヒーローのハンドとフロップに対して、相手レンジと勝率を評価
    board: ["7h", "Qd", "Td"] のような3枚
    opponent_range: [["Ah", "Kh"], ["Ad", "Kd"], ...]
    trials: 1ハンドにつき何試行するか（軽量化用）

    return: 勝率（勝ち＋引き分け/2）の平均（0〜1）
    """
    hero_cards = [eval7.Card(card) for card in [hero_hand[:2], hero_hand[2:]]]
    board_cards = [eval7.Card(card) for card in board]
    used_cards = set(hero_cards + board_cards)

    win = 0
    tie = 0
    total = 0

    for opp_hand in opponent_range:
        opp_cards = [eval7.Card(c) for c in opp_hand]
        if any(c in used_cards for c in opp_cards):
            continue  # 使用済カードとの重複回避

        for _ in range(trials):
            deck = [card for card in eval7.Deck() if card not in used_cards and card not in opp_cards]
            random.shuffle(deck)
            needed = 5 - len(board_cards)
            draw = deck[:needed]
            full_board = board_cards + draw

            hero = eval7.Hand(hero_cards, full_board)
            opp = eval7.Hand(opp_cards, full_board)
            res = hero.evaluate() - opp.evaluate()

            if res > 0:
                win += 1
            elif res == 0:
                tie += 1
            total += 1

    return (win + tie / 2) / total if total else 0.0
