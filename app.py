import streamlit as st
from code_reviewer import generate_prompt, review_code_with_groq
import requests

# Page Config
st.set_page_config(page_title="🧠 AI Code Review Agent", page_icon="🛠️", layout="wide")

# Custom CSS for styling
st.markdown("""
    <style>
    .main {
        background: linear-gradient(to right, #fdfbfb, #ebedee);
        font-family: 'Segoe UI', sans-serif;
    }
    h1 {
        background: linear-gradient(to right, #00c6ff, #0072ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3em !important;
        text-align: center;
        margin-bottom: 0.5em;
    }
    .stTextArea textarea {
        
        font-family: 'Fira Code', monospace;
        font-size: 15px;
    }
    .stButton > button {
        background-color: #0072ff;
        color: white;
        font-weight: bold;
        padding: 0.6em 1.2em;
        border-radius: 10px;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #0051c7;
        transform: scale(1.05);
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown("<h1>🤖 AI Code Review Agent</h1>", unsafe_allow_html=True)
st.markdown("### 🚀 Paste your code below and get smart, instant feedback using Groq's LLaMA3 engine.")

# Input Section
review_mode = st.radio("Choose Code Input Mode", ["Paste Code", "GitHub File Link"])

code = ""
if review_mode == "Paste Code":
    code = st.text_area("🧾 Paste your code here", height=300, placeholder="def add(a, b): return a + b")
elif review_mode == "GitHub File Link":
    github_link = st.text_input("🔗 Enter raw GitHub file link")
    if github_link and github_link.startswith("http"):
        try:
            response = requests.get(github_link)
            response.raise_for_status()
            code = response.text
            st.success("✅ Code fetched successfully from GitHub!")
            st.code(code, language="python")
        except Exception as e:
            st.error(f"❌ Failed to fetch code: {e}")

# Language Dropdown
language = st.selectbox("📝 Select the language of your code", ["Python", "JavaScript", "Java", "C++", "Go", "Other"])

# Review Button
if st.button("🔍 Review My Code"):
    if not code.strip():
        st.warning("⚠️ Please paste code or enter a valid GitHub link.")
    else:
        with st.spinner("⏳ Reviewing your code using Groq's LLaMA3..."):
            prompt = generate_prompt(code, language)
            review = review_code_with_groq(prompt)
        st.success("✅ Code Review Completed!")
        st.markdown("### 🧠 AI Review Feedback:")
        st.code(review, language="markdown")
        st.balloons()  # 🎈 celebratory animation
