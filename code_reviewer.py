import requests
import os
from dotenv import load_dotenv

load_dotenv()

def generate_prompt(code, language):
    return f"""
You are an expert code reviewer and a senior software engineer with years of experience in reviewing production-grade code.

Please deeply analyze and review the following {language} code.

Your review must include:

1. 🔍 **Line-by-line analysis**: Point out errors, bad practices, and unnecessary code if any.
2. 📦 **Code structure and modularity**: How well-structured is the code? Is it following clean code principles (e.g., SOLID, DRY, KISS)?
3. 🛡️ **Security vulnerabilities**: Mention any known or possible security risks in the code.
4. 🚀 **Performance optimizations**: Are there any better approaches or algorithms that would enhance performance?
5. ✅ **Readability and maintainability**: Suggest improvements for variable naming, comments, and formatting.
6. 💡 **Scalability Suggestions**: If this code were to grow in production, what should be improved?
7. 🧪 **Testability**: Is the code easily testable? Recommend unit or integration tests if needed.
8. 🎯 **Best Practices**: Highlight adherence or violations of industry-standard best practices and language-specific conventions.

Format your response clearly using bullet points, headings, and markdown. Be honest, professional, and constructive.

Code to review:
{code}

"""

def review_code_with_groq(prompt):
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return "❌ GROQ_API_KEY not found in environment."

    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": "You are a helpful code reviewer."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.5
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except requests.exceptions.RequestException as e:
        return f"❌ Error occurred: {e}"
