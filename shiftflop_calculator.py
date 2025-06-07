import random
from collections import defaultdict
from evaluate_winrate import evaluate_vs_range  # 勝率評価関数
from preflop_winrate_dict import preflop_winrates
from opponent_hands_25_range import opponent_hands
from flop_generator import generate_flops_for_type
from feature_extractor import extract_flop_features

def run_shiftflop_analysis(hero_hand: str, flop_type: str, num_trials: int = 1000, sample_size: int = 10):
    """
    プリフロップ → フロップの勝率変動を特徴量付きで返す
    """
    all_flops = generate_flops_for_type(hero_hand, flop_type)
    if len(all_flops) < sample_size:
        raise ValueError("フロップ候補数が少なすぎます")

    preflop_winrate = preflop_winrates.get(hero_hand, None)
    if preflop_winrate is None:
        raise ValueError("指定ハンドのプリフロップ勝率が辞書に存在しません")

    result_table = defaultdict(lambda: {"count": 0, "total_delta": 0.0, "feature": None})

    for _ in range(num_trials):
        sampled_flops = random.sample(all_flops, sample_size)
        for flop in sampled_flops:
            winrate = evaluate_vs_range(hero_hand, flop, opponent_hands)
            delta = winrate - preflop_winrate
            feature = extract_flop_features(hero_hand, flop)
            key = tuple(flop)

            result_table[key]["count"] += 1
            result_table[key]["total_delta"] += delta
            result_table[key]["feature"] = feature

    # 結果を加工してリスト形式に
    summary = []
    for flop, stats in result_table.items():
        avg_delta = stats["total_delta"] / stats["count"]
        summary.append({
            "flop": flop,
            "winrate_shift": round(avg_delta * 100, 2),
            "feature": stats["feature"]
        })

    # 勝率差でソート
    summary.sort(key=lambda x: x["winrate_shift"], reverse=True)
    return summary
