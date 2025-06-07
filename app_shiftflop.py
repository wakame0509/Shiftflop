import streamlit as st
from calculate_winrate_detailed_v2 import simulate_winrate_for_flop_type
from hand_list import all_starting_hands  # 169通りのハンド
from flop_type_generator import generate_candidate_flops
import random

st.title("ShiftFlop - フロップによる勝率変動")

# 自分のハンド選択（169通り）
hand = st.selectbox("自分のハンドを選択", all_starting_hands)

# フロップタイプの選択
flop_type = st.selectbox("フロップタイプを選択", [
    "High card rainbow",
    "Low connected rainbow",
    "Paired board",
    "Two-tone board",
    "Monotone board",
    "Ace-high dry",
    "Broadway coordinated"
])

# モンテカルロ試行回数の選択（1回あたりのフロップサンプル数）
sample_count = st.selectbox("フロップのサンプル数（モンテカルロ的に抽出）", [10, 20, 30, 40, 50])

# 開始ボタン
if st.button("計算開始"):
    with st.spinner("計算中..."):
        # 指定されたフロップタイプに対して候補を全生成
        candidate_flops = generate_candidate_flops(hand, flop_type)

        # ランダムにN個抽出
        if len(candidate_flops) < sample_count:
            st.warning("候補が少ないため全てのフロップを使用します")
            selected_flops = candidate_flops
        else:
            selected_flops = random.sample(candidate_flops, sample_count)

        # 各フロップに対して勝率を計算し、差分を平均
        deltas = []
        for flop in selected_flops:
            delta = simulate_winrate_for_flop_type(hand, flop)
            deltas.append(delta)

        avg_delta = sum(deltas) / len(deltas)
        sign = "+" if avg_delta >= 0 else ""
        st.success(f"平均的な勝率の変動: {sign}{avg_delta:.2f}%（{sample_count}サンプル平均）")
