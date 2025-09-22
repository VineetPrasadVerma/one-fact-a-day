# import os
# from dotenv import load_dotenv
# from murf import Murf

# load_dotenv()

# client = Murf(api_key=os.getenv("MURFAI_API_KEY"))

# def generate_audio(fact):
#     response = client.text_to_speech.generate(
#         text=fact,
#         voice_id="en-US-natalie",
#         style="Promo",
#         pitch=-25,
#         rate=0,
#     )

#     print(response.audio_file)


# generate_audio(
#     f"""Did you know?
#     There are more stars in the observable universe than all the grains of sand on every beach on Earth? Let that staggering number sink in! Wild, right?
#     Like, share, and subscribe for more!
#     """
# )

import os
from datetime import date
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs import play

load_dotenv()

output_path = f"""/Users/vineetverma/Desktop/Learnings/one-fact-a-day/python/assets/voice"""

client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))

audio = client.text_to_speech.convert(
    text="Did you know? There are more stars in the observable universe than all the grains of sand on every beach on Earth? Let that staggering number sink in! Wild, right?... Like, share, and subscribe for more!",
    # voice_id="nPczCjzI2devNBz1zQrb", default,
    voice_id="zgqefOY5FPQ3bB7OZTVR",
    model_id="eleven_multilingual_v2",
    output_format="mp3_44100_128",
)

# Save audio file
with open(f"{output_path}/{date.today()}.mp3", "wb") as f:
    for chunk in audio:
        f.write(chunk)

# Play the audio
with open("did_you_know.mp3", "rb") as f:
    play(f.read())
