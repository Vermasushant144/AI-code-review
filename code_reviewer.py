import requests
import os
from dotenv import load_dotenv

load_dotenv()

def generate_prompt(code, language):
    return f"""
You are an expert code reviewer and senior developer.

Review the following {language} code and provide:
1. Code quality feedback
2. Potential bugs or security issues
3. Suggestions for improvements
4. Performance optimizations (if any)

Code:
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
