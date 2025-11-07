# import os
# from dotenv import load_dotenv
# from murf import Murf
# import requests
# from datetime import date

# load_dotenv()

# client = Murf(api_key=os.getenv("MURFAI_API_KEY"))

# output_path = f"""/Users/vineetverma/Desktop/Learnings/one-fact-a-day/python/assets/voice"""

# def generate_audio(fact):
#     response = client.text_to_speech.generate(
#         text=fact,
#         voice_id="en-US-ken",
#         style="Conversational",
#         pitch=0,
#         rate=25,
#         format='MP3',
#         audio_duration=15
#     )

#     return response.audio_file

# def download_audio(audio_url):
#     # Murf returns an audio file link (URL)
#     print(f"Audio file URL: {audio_url}")

#     # Download audio
#     audio_response = requests.get(audio_url)
#     if audio_response.status_code == 200:
#         with open(f'{output_path}/{date.today()}.mp3', "wb") as f:
#             f.write(audio_response.content)
#         print(f"Audio saved")
#     else:
#         print(f"Failed to download audio: {audio_response.status_code}")


# download_audio(generate_audio(
#     f"""Did you know?
#     There are more stars in the observable universe than all the grains of sand on every beach on Earth? Let that staggering number sink in! Wild, right?
#     Like, share, and subscribe for more!
#     """
# ))

import os
import json
import base64
from datetime import date
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs.types.voice_settings import VoiceSettings

load_dotenv()

output_path = (
    f"""/Users/vineetverma/Desktop/Learnings/one-fact-a-day/python/assets/voice"""
)

client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))

character_start_times_seconds = [];
character_end_times_seconds = [];
characters = [];

def generate_audio(text):
    return client.text_to_speech.convert_with_timestamps(
        text=text,
        voice_id="Xb7hH8MSUJpSbSDYk0k2",
        model_id="eleven_multilingual_v2",
        output_format="mp3_44100_128",
        voice_settings={
            "speed": 1.05,
            "stability": 0.45,
            "style": 0.25,
            "similarity_boost": 0.75,
            "use_speaker_boost": True,
        },
    )


def download_audio(audio_resp):
    # Access the audio_base_64 attribute from the response object
    audio_base_64 = audio_resp.audio_base_64
    characters = audio_resp.alignment.characters
    character_start_times_seconds = audio_resp.alignment.character_start_times_seconds
    character_end_times_seconds = audio_resp.alignment.character_end_times_seconds
    audio_bytes = base64.b64decode(audio_base_64)
    output_file = os.path.join(output_path, f"{date.today()}.mp3")
    
    with open(output_file, 'wb') as f:
        f.write(audio_bytes)
    print(f"Characters {characters}")
    print(f"Character start time seconds {character_start_times_seconds}")
    print(f"Character end time seconds {character_end_times_seconds}")
    print(f"Audio file saved to {output_file}")


download_audio(generate_audio(
    f"""Did you know? That big, fluffy cloud drifting overhead actually weighs over a million pounds? Yep! A single cumulus cloud holds enough water to be heavier than an entire herd of elephants. Seriously, imagine that immense weight silently floating by! Mind-blowing, right? Like, share, and subscribe for more!
    """
))
