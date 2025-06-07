import random

suits = ['h', 'd', 'c', 's']

def expand_hand_to_specific_cards(hand_name):
    """
    "AKs" → ["Ah", "Kh"] などに変換
    スートはランダムに決定（重複除去は外部で行う）
    """
    if len(hand_name) == 2:  # ペア
        rank = hand_name[0]
        s1, s2 = random.sample(suits, 2)
        return [rank + s1, rank + s2]
    elif len(hand_name) == 3:
        r1, r2, suited = hand_name[0], hand_name[1], hand_name[2]
        if suited == 's':
            s = random.choice(suits)
            return [r1 + s, r2 + s]
        else:  # offsuit
            s1, s2 = random.sample(suits, 2)
            while s1 == s2:
                s2 = random.choice(suits)
            return [r1 + s1, r2 + s2]
    else:
        raise ValueError("Invalid hand name: " + hand_name)

def format_flop(flop_cards):
    """
    ["7h", "Qd", "Td"] → "7h Qd Td" 形式の文字列へ
    """
    return " ".join(flop_cards)

def format_hand(card1, card2):
    """
    ["Ah", "Kh"] → "AhKh"
    """
    return card1 + card2
