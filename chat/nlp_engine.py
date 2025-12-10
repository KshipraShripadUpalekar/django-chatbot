import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def ai_response(user_message):
    if not os.getenv("OPENAI_API_KEY"):
        return "⚠ API key missing. Please set OPENAI_API_KEY environment variable."

    try:
        chat_completion = client.chat.completions.create(
            model="gpt-4.1-mini",   # can change to gpt-4.1, gpt-3.5, etc.
            messages=[
                {"role": "system", "content": "You are a friendly helpful chatbot. Reply naturally."},
                {"role": "user", "content": user_message}
            ]
        )

        return chat_completion.choices[0].message.content

    except Exception as e:
        print("AI Error:", e)
        return "Sorry, I could not reach the AI server 😢 Try again later."
