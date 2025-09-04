import streamlit as st
import pandas as pd
import random
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Lucky for Life 추천기", layout="wide")
st.title("🎯 Lucky for Life 자동 추천기")

# ==================== CSV 업로드 ====================
uploaded_file = st.file_uploader("CSV 파일 업로드", type="csv")
data = None

if uploaded_file is not None:
    try:
        data = pd.read_csv(uploaded_file)
        st.success("데이터 로드 완료!")
    except Exception as e:
        st.error(f"파일 읽는 중 오류 발생: {e}")

# ==================== 추천 번호 생성 ====================
def generate_numbers(data, style='hot'):
    all_nums = data[['Num1','Num2','Num3','Num4','Num5']].values.flatten()
    num_counts = pd.Series(all_nums).value_counts()
    hot_nums = num_counts.sort_values(ascending=False).index.tolist()[:10]
    cold_nums = num_counts.sort_values().index.tolist()[:10]
    
    if style == 'hot':
        nums = random.sample(hot_nums, 5)
    elif style == 'balanced':
        nums = random.sample(hot_nums, 3) + random.sample(cold_nums, 2)
    elif style == 'cold':
        nums = random.sample(cold_nums, 5)
    else:
        nums = random.sample(range(1,50), 5)
    
    lucky_ball = random.randint(1,20)
    return sorted(nums), lucky_ball

# ==================== 히트맵 ====================
def plot_heatmap(data):
    all_nums = data[['Num1','Num2','Num3','Num4','Num5']].values.flatten()
    num_counts = pd.Series(all_nums).value_counts().sort_index()
    
    fig, ax = plt.subplots(figsize=(12,5))
    sns.barplot(x=num_counts.index, y=num_counts.values, palette="viridis", ax=ax)
    ax.set_title("Number Frequency Heatmap")
    ax.set_xlabel("Numbers")
    ax.set_ylabel("Frequency")
    st.pyplot(fig)

    lucky_counts = data['LuckyBall'].value_counts().sort_index()
    fig2, ax2 = plt.subplots(figsize=(12,3))
    sns.barplot(x=lucky_counts.index, y=lucky_counts.values, palette="magma", ax=ax2)
    ax2.set_title("Lucky Ball Frequency")
    ax2.set_xlabel("Lucky Ball")
    ax2.set_ylabel("Frequency")
    st.pyplot(fig2)

# ==================== UI ====================
if data is not None:
    if st.button("🎲 추천 번호 생성"):
        styles = ['hot', 'balanced', 'cold', 'hot', 'balanced']
        st.subheader("추천 번호 5세트")
        for i, style in enumerate(styles, 1):
            nums, lucky = generate_numbers(data, style)
            st.write(f"{i}️⃣ {nums} + Lucky Ball ({lucky}) -> 스타일: {style}")

    if st.button("📊 히트맵 보기"):
        plot_heatmap(data)
