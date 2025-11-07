import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def generate_script():
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"""
                    I am going to send this prompt to ElevenLabs to generate audio, so write the fact in a way that sounds natural and human when spoken aloud.

                    Create a short, engaging script that lasts around 15 seconds when spoken for a YouTube Short video. 
                    The script MUST start with the exact words: 'Did you know?' 
                    and MUST end with the exact words: 'Like, share, and subscribe for more!' 

                    Requirements:
                    - Use a real, verifiable fact. 
                    - Make it surprising, conversational, and emotionally engaging (not academic). 
                    - Add sensory or vivid words that make it sound alive when spoken. 
                    - Keep language simple, friendly, and natural — as if someone is talking to a general audience. 
                    - Avoid long or complex sentences — use short, punchy lines that flow naturally when read aloud.
                    - Ensure the total spoken length is approximately 15 seconds.

                    Return ONLY the script text, nothing else.
                  """,
    )
    print(response.text)


generate_script()
