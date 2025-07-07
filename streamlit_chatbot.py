import streamlit as st
import pandas as pd
import openai

# ① OpenAI API 키 입력 (꼭 본인 키로 바꿔주세요!)
openai.api_key = "YOUR_API_KEY"

# ② FAQ CSV 파일 불러오기
faq_df = pd.read_csv("faq_data.csv")  # ← 여기에서 불러옵니다!

# ③ Streamlit UI 구성
st.title("고객센터 FAQ 챗봇")
user_question = st.text_input("무엇을 도와드릴까요?")

# ④ 질문이 입력되었을 때 동작
if user_question:
    # ⑤ 간단한 키워드 기반 문서 검색 (가장 유사한 문서 1개 찾기)
    matched_answer = None
    for idx, row in faq_df.iterrows():
        if any(keyword in user_question for keyword in row["question"].split()):
            matched_answer = row["answer"]
            break
    if not matched_answer:
        matched_answer = "죄송합니다. 정확한 답변을 찾지 못했습니다. 고객센터로 문의해 주세요."

    # ⑥ GPT에게 응답 문장 정리 요청
    prompt = f"""다음과 같은 고객의 질문에 대해 문서를 참고하여 3줄 이내로 정리해서 응답해줘.
    질문: "{user_question}"
    문서 내용: "{matched_answer}"
    """

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # 또는 gpt-4
        messages=[{"role": "user", "content": prompt}]
    )

    # ⑦ 출력
    st.markdown("### 🤖 챗봇 응답:")
    st.write(response["choices"][0]["message"]["content"])
