import streamlit as st
import random
from calculate_winrate_detailed_v2 import simulate_winrate_for_flop_type
from feature_extractor import extract_flop_features
from preflop_winrate_dict import preflop_winrates
from utils import expand_hand_to_specific_cards, format_flop

# ==== UI構成 ====
st.title("ShiftFlop 勝率変動ランキング")
st.write("プリフロップからフロップでどのように勝率が変化するかを分析します。")

# --- ハンド選択 ---
hand_options = list(preflop_winrates.keys())
hero_hand_name = st.selectbox("ヒーローのハンドを選択", hand_options)

# --- フロップタイプ選択 ---
flop_type = st.selectbox("フロップタイプを選択", [
    "High Card Rainbow",
    "Paired Board",
    "Suited Two Tone",
    "Connected Low",
    "1 Hit + 2 Flush Draw",
    "No Hit",
    "Straight Possible"
])

# --- 試行回数 ---
num_trials = st.selectbox("モンテカルロ試行回数", [1000, 10000, 50000, 100000])

# --- 実行ボタン ---
if st.button("ShiftFlop を実行"):
    with st.spinner("計算中..."):
        hero_cards = expand_hand_to_specific_cards(hero_hand_name)
        results = simulate_winrate_for_flop_type(
            hero_cards, flop_type, num_trials=num_trials, sample_per_trial=10
        )

        preflop_wr = preflop_winrates[hero_hand_name]

        # 勝率差の大きい順にソート
        results_sorted = sorted(results, key=lambda x: abs(x["winrate"] - preflop_wr), reverse=True)[:10]

        st.subheader("勝率変動ランキング（トップ10）")
        for item in results_sorted:
            flop_str = format_flop(item["flop"])
            shift = round(item["winrate"] - preflop_wr, 2)
            feature = extract_flop_features("".join(hero_cards), item["flop"])
            st.markdown(f"""
                <div class='report'>
                <b>Flop:</b> {flop_str}  
                <b>Winrate:</b> {item["winrate"]:.1f}%  
                <b>Shift:</b> {shift:+.2f}%  
                <b>Features:</b> {feature}
                </div>
            """, unsafe_allow_html=True)
