import streamlit as st
import pandas as pd
import openai

# 최신 방식: 클라이언트 객체 생성
client = openai.OpenAI(api_key=st.secrets["openai"]["api_key"])

# 데이터 불러오기
faq_df = pd.read_csv("faq_data.csv")

# Streamlit UI
st.title("고객센터 FAQ 챗봇")
question = st.text_input("무엇을 도와드릴까요?")

if question:
    matched_answer = faq_df.iloc[0]["answer"]
    for i, row in faq_df.iterrows():
        if any(word in question for word in row["question"].split()):
            matched_answer = row["answer"]
            break

    prompt = f"""다음 고객 질문에 대해, 문서를 참고해 3줄 이내로 자연스럽게 답변해줘:
    질문: {question}
    문서 내용: {matched_answer}
    """

    # 최신 API 호출 방식
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )

    st.markdown("### 🤖 답변")
    st.write(response.choices[0].message.content)
