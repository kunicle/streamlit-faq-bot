import streamlit as st
import pandas as pd
import openai

# OpenAI 클라이언트 설정 (최신 방식)
client = openai.OpenAI(api_key=st.secrets["openai"]["api_key"])

# FAQ 문서 불러오기
faq_df = pd.read_csv("faq_data.csv")

# Streamlit UI
st.title("고객센터 FAQ 챗봇")
question = st.text_input("무엇을 도와드릴까요?")

if question:
    matched_answer = None

    # 🔍 FAQ 문서에서 관련 있는 질문 찾기 (단순 키워드 포함)
    for i, row in faq_df.iterrows():
        if any(word in question for word in row["question"].split()):
            matched_answer = row["answer"]
            break

    # ❗ 관련 문서가 없을 경우: 경고 출력
    if not matched_answer:
        st.warning("죄송합니다. 해당 질문은 등록된 FAQ 범위 밖입니다.\n환불, 배송, 쿠폰, 주문 등 고객센터 관련 문의만 응답 가능합니다.")
    else:
        # ✅ 관련된 문서를 기반으로 GPT 응답 생성
        prompt = f"""다음 고객 질문에 대해, 문서를 참고하여 3줄 이내로 자연스럽게 답변해줘:
        질문: {question}
        문서 내용: {matched_answer}
        """

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )

        st.markdown("### 🤖 답변")
        st.write(response.choices[0].message.content)
