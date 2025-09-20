from openai import OpenAI
from moviepy import ImageClip, AudioFileClip
import os
from dotenv import load_dotenv
from murf import Murf

load_dotenv()

# 1. OpenAI API client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
murf_client = Murf(api_key="MURFAI_API_KEY")

# 2. Hardcoded fact
fact = "Honey never spoils. Archaeologists have found pots of honey in ancient Egyptian tombs that are over 3000 years old and still edible."


# 3. Generate Script from Fact
def generate_script(fact):
    prompt = f"""
    Create a short engaging 30-second script for a YouTube short video.
    The script MUST start with the words: "Did you know?"

    Fact: {fact}
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content.strip()


script = generate_script(fact)
print("Generated Script:\n", script)

# 4. Convert Script to Speech


def text_to_speech(script, output_path):
    # Stream TTS to file for efficiency and memory safety
    with client.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts",
        voice="alloy",
        input=script,
    ) as response:
        response.stream_to_file(output_path)
    return output_path


# Prepare output paths
project_root = os.path.dirname(os.path.dirname(__file__))
output_dir = os.path.join(project_root, "output")
os.makedirs(output_dir, exist_ok=True)

audio_file_path = os.path.join(output_dir, "audio.mp3")
audio_file = text_to_speech(script, audio_file_path)

# 5. Create Video (audio + static image)


def create_video(audio_file, output_path):
    # Resolve background image path inside this python package
    bg_image_path = os.path.join(os.path.dirname(__file__), "assets", "bg.jpg")

    # Load audio to get duration
    audio = AudioFileClip(audio_file)
    duration = audio.duration

    # Create an image clip that matches audio duration
    image = ImageClip(bg_image_path).set_duration(duration)

    # Combine image and audio
    final_clip = image.set_audio(audio)

    # Export video
    final_clip.write_videofile(output_path, fps=24)


video_output_path = os.path.join(output_dir, "final.mp4")
create_video(audio_file, video_output_path)
