import streamlit as st
from code_reviewer import generate_prompt, review_code_with_groq

st.set_page_config(page_title="AI Code Reviewer", layout="wide")
st.title("🤖 AI Code Review Agent (Streamlit + Groq)")

st.markdown("Paste your code below and get an instant AI-powered code review.")

code = st.text_area("🧾 Paste your code here", height=300, placeholder="def add(a, b): return a + b")

language = st.selectbox("📝 Select the language of your code", ["Python", "JavaScript", "Java", "C++", "Go", "Other"])

if st.button("🚀 Review My Code"):
    if not code.strip():
        st.warning("Please paste your code before clicking review.")
    else:
        with st.spinner("Reviewing your code using Groq's LLaMA3..."):
            prompt = generate_prompt(code, language)
            review = review_code_with_groq(prompt)
        st.success("✅ Code Review Completed")
        st.markdown("### 🧠 Review Feedback:")
        st.code(review, language="markdown")
