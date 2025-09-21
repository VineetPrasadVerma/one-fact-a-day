from pydub import AudioSegment

# Load narration (your generated audio)
voice = AudioSegment.from_file("python/assets/background_music/stars_vs_sand.wav")

# Load background music (royalty-free mp3/wav)
music = AudioSegment.from_file("calm_on_the_flip.mp3")

# Reduce background music volume
music = music - 15  # lower volume by 15 dB (tweak as needed)

# Loop/extend music if it's shorter than narration
if len(music) < len(voice):
    times = int(len(voice) / len(music)) + 1
    music = music * times

# Trim music to match voice length
music = music[:len(voice)]

# Overlay narration on top of background music
final_audio = music.overlay(voice)

# Export final audio
final_audio.export("final_with_music.wav", format="mp3")