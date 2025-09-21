import os
from dotenv import load_dotenv
from murf import Murf

load_dotenv()

client = Murf(api_key=os.getenv("MURFAI_API_KEY"))

def generate_audio(fact):
    response = client.text_to_speech.generate(
        text=fact,
        voice_id="en-US-natalie",
        style="Promo",
        pitch=-25,
        rate=25,
    )

    print(response.audio_file)


generate_audio(
    "Did you know? There are more stars in the observable universe than all the grains of sand on every beach on Earth? Let that staggering number sink in! Wild, right? Like, share, and subscribe for more!"
)
