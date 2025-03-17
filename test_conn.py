import os

import openai
from openai import OpenAI

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

try:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Hello"}]
    )
    print("API Connection Successful!")
except Exception as e:
    print(f"API Error: {str(e)}")