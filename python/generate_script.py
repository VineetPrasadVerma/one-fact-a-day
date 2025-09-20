# from openai import OpenAI
# import os
# from dotenv import load_dotenv

# load_dotenv()

# # 1. OpenAI API client
# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# def generate_script(fact):
#     prompt = f"""
#     Create a short engaging 30-second script for a YouTube short video.
#     The script MUST start with the words: "Did you know?"

#     Fact: {fact}
#     """
#     response = client.chat.completions.create(
#         model="gpt-4o-mini",
#         messages=[{"role": "user", "content": prompt}],
#     )
#     return response.choices[0].message.content.strip()

from google import genai

client = genai.Client()

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="How does AI work?"
)
print(response.text)