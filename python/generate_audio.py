from dotenv import load_dotenv
from murf import Murf

load_dotenv()

murf_client = Murf(api_key="MURFAI_API_KEY")

def generate_audio(fact):
    response = murf_client.text_to_speech.generate(
        text=f"""Did you know? {fact}""",
        voice_id="en-US-ken",
        style="Conversational",
        pitch=-25,
        rate=25,
    )

    print(response.audio_file)
