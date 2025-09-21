import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_script():
  response = client.models.generate_content(
      model="gemini-2.5-flash",
      contents="Create a short, engaging script (15 seconds when spoken) for a YouTube Short video. The script MUST start with the exact words: 'Did you know?'Requirements: -Use a real, verifiable fact. -Make it surprising, and conversational (not academic).  - Add emotional or sensory words to make it engaging. -End with a punchy closing line that invites viewers to like, share, and subscribe. - Keep language simple and natural, as if speaking to a general audience. Return ONLY the script text, nothing else.",
  )
  print(response.text)
  
generate_script()
