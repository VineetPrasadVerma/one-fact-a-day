from moviepy import ImageClip, AudioFileClip, CompositeAudioClip, concatenate_videoclips

def create_fact_video(
    fact_audio_path,
    fact_image_paths,
    bg_music_path,
    intro_image,
    outro_image,
    output_path="./final_fact_video.mp4",
):
    # --- Load assets ---
    narration = AudioFileClip(fact_audio_path)
    bg_music = AudioFileClip(bg_music_path)

    # --- Durations ---
    intro_duration = 2
    outro_duration = 2
    per_image_duration = narration.duration / len(fact_image_paths)

    # --- Create clips ---
    intro = ImageClip(intro_image).with_duration(intro_duration).resized(height=720)
    fact_clips = [
        ImageClip(img).with_duration(per_image_duration).resized(height=720)
        for img in fact_image_paths
    ]
    outro = ImageClip(outro_image).with_duration(outro_duration).resized(height=720)

    # --- Combine video clips ---
    video = concatenate_videoclips([intro, *fact_clips, outro], method="compose")

    # --- Loop or trim background music properly ---
    if bg_music.duration < video.duration:
        # Loop the bg music until it covers full video duration
        loops = int(video.duration // bg_music.duration) + 1
        bg_music_loops = [bg_music] * loops
        bg_music_full = CompositeAudioClip(bg_music_loops).with_duration(video.duration)
    else:
        bg_music_full = bg_music.subclipped(0, video.duration)

    # --- Combine narration (starts after intro) + bg music ---
    final_audio = CompositeAudioClip([
        bg_music_full,
        narration.with_start(intro_duration)
    ]).with_duration(video.duration)

    # --- Attach audio ---
    video = video.with_audio(final_audio)

    # --- Export final video ---
    video.write_videofile(output_path, fps=24, audio_codec="aac")

    print(f"✅ Video saved at {output_path}")


# --- Example usage ---
if __name__ == "__main__":
    create_fact_video(
        fact_audio_path="./python/assets/voice/2025-09-24.mp3",
        fact_image_paths=[
            "./python/assets/images/fact_image_1.png",
            "./python/assets/images/fact_image_2.png",
        ],
        bg_music_path="./python/assets/background_music/bg_1.mp3",
        intro_image="./python/assets/static_images/intro.png",
        outro_image="./python/assets/static_images/outro.png",
        output_path="./python/assets/video/fact_video.mp4",
    )