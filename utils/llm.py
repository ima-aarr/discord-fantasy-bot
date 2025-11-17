import os
import openai

openai.api_key = os.environ.get("OPENAI_API_KEY")

def generate_text(prompt, max_tokens=150):
    if not openai.api_key:
        return "[LLM未設定] " + prompt
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role":"user","content":prompt}],
        max_tokens=max_tokens
    )
    return response.choices[0].message.content.strip()
