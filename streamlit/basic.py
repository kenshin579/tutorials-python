import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

st.write("Hello, world!")

st.write("1. 데이터프레임 보여주기")
chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])
chart_data.to_csv("chart_data.csv", index=False)
st.line_chart(chart_data)


st.write("2. 표 보여주기")
st.write(pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40],
}))

st.write("3. 그래프 그리기")
# dataframe의 크기가 클 경우 알아서 슬라이드 바가 나타난다
df = pd.DataFrame(np.random.randn(50, 20), columns=("col %d" % i for i in range(20)))

# st.dataframe(df)  # Same as st.write(df)

# 인덱스 행을 없애주면 테이블이 더 깔끔해진다
st.dataframe(df, hide_index = True)  # Same as st.write(df)

# 차트보여주기

st.write("4. 차트 보여주기")
st.bar_chart(df)  # 막대그래프
st.line_chart(df)  # 꺾은선그래프

st.write("5. pylot으로 차트 그리기")
# pylot으로 직접 차트를 만들어 사용 - 이 부분은 렌더링이 안됨
arr = np.random.normal(1, 1, size=100)
fig, ax = plt.subplots()
ax.hist(arr, bins=20)

st.pyplot(fig)