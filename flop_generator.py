from itertools import combinations
from utils import get_card_ranks, get_card_suits

RANKS = "23456789TJQKA"
SUITS = "hdcs"

def generate_flops_for_type(hero_hand: str, flop_type: str):
    """
    指定ハンドとフロップタイプに合致するフロップ候補を全通り返す
    例: hero_hand="8h7h", flop_type="1ヒット+同スート2枚"
    """
    used = set(hero_hand)
    h1, h2 = hero_hand[:2], hero_hand[2:]

    flops = []

    # パターンごとに条件分岐
    if flop_type == "1ヒット+同スート2枚":
        rank_hit = h1[0] if h1[0] in RANKS else h2[0]
        suit = h1[1] if h1[1] == h2[1] else None
        if suit is None:
            return []

        for r2 in RANKS:
            for r3 in RANKS:
                flop = [(rank_hit + suit), (r2 + suit), (r3 + next(s for s in SUITS if s != suit))]
                if len(set(flop + [h1, h2])) == 5:  # 重複カードなし
                    flops.append(flop)

    elif flop_type == "ノーヒット":
        exclude_ranks = [h1[0], h2[0]]
        for r1, r2, r3 in combinations(RANKS, 3):
            if any(r in exclude_ranks for r in (r1, r2, r3)):
                continue
            for s1 in SUITS:
                for s2 in SUITS:
                    for s3 in SUITS:
                        flop = [r1 + s1, r2 + s2, r3 + s3]
                        if len(set(flop + [h1, h2])) == 5:
                            flops.append(flop)

    # 他のタイプも今後追加可
    return flops
