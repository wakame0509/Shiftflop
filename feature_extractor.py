def extract_flop_features(hero_hand, flop):
    """
    指定ハンド＋フロップから、特徴量（セット、オーバーカードなど）を抽出する
    """
    ranks = '23456789TJQKA'
    rank_to_value = {r: i for i, r in enumerate(ranks)}
    
    h1, h2 = hero_hand[:2], hero_hand[2:]
    h1_rank, h1_suit = h1[0], h1[1]
    h2_rank, h2_suit = h2[0], h2[1]
    flop_ranks = [card[0] for card in flop]
    flop_suits = [card[1] for card in flop]

    feature_set = []

    # ワンペア・ツーペア・セット
    matches = flop_ranks.count(h1_rank) + flop_ranks.count(h2_rank)
    if matches == 2:
        feature_set.append("Two Pair")
    elif matches == 1:
        feature_set.append("One Pair")
    elif h1_rank == h2_rank and flop_ranks.count(h1_rank) == 1:
        feature_set.append("Set")
    elif h1_rank == h2_rank and flop_ranks.count(h1_rank) >= 2:
        feature_set.append("Quads")

    # オーバーカード判定（フロップの最大 > ハンド最大）
    max_flop = max(rank_to_value[r] for r in flop_ranks)
    max_hand = max(rank_to_value[h1_rank], rank_to_value[h2_rank])
    if max_flop > max_hand:
        feature_set.append("Overcard on board")

    # フラッシュドロー（同スート4枚）
    suits = [h1_suit, h2_suit] + flop_suits
    for s in 'hdcs':
        if suits.count(s) == 4:
            feature_set.append("Flush Draw")

    # ストレートドロー（ハンド＋フロップで連続したランクが4つ）
    all_ranks = set([h1_rank, h2_rank] + flop_ranks)
    indices = [rank_to_value[r] for r in all_ranks]
    indices.sort()
    for i in range(len(indices) - 3):
        if indices[i+3] - indices[i] == 3:
            feature_set.append("Straight Draw")
            break

    if not feature_set:
        feature_set.append("None")

    return ", ".join(feature_set)
