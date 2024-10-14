import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

token = os.getenv("GITHUB_TOKEN")
endpoint = "https://models.inference.ai.azure.com"
model_name = "gpt-4o-mini"

# Read the data from an environment variable
assistant_data = os.getenv("ASSISTANT_DATA", "You are a helpful assistant.")

# Prompt the user for input
user_input = input("Please enter your question: ")

client = OpenAI(
    base_url=endpoint,
    api_key=token,
)

response = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": assistant_data,
        },
        {
            "role": "user",
            "content": user_input,
        },
    ],
    temperature=1.0,
    top_p=1.0,
    max_tokens=1000,
    model=model_name,
)

print(response.choices[0].message.content)
