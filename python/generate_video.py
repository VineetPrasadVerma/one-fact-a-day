from moviepy import (
    ImageClip,
    AudioFileClip,
    CompositeAudioClip,
    concatenate_videoclips,
    CompositeVideoClip,
)
from moviepy.video.fx import FadeIn, FadeOut
import random
import numpy as np


def crossfade_transition(clip1, clip2, duration=0.5):
    """Crossfade transition between two clips"""
    clip1_end = clip1.subclipped(clip1.duration - duration, clip1.duration)
    clip2_start = clip2.subclipped(0, duration)

    clip1_end = clip1_end.with_effects([FadeOut(duration)])
    clip2_start = clip2_start.with_effects([FadeIn(duration)])

    return concatenate_videoclips(
        [
            clip1.subclipped(0, clip1.duration - duration),
            CompositeVideoClip([clip1_end, clip2_start]),
            clip2.subclipped(duration, clip2.duration),
        ]
    )


def slide_transition(clip1, clip2, direction="left", duration=0.5):
    """Slide transition between two clips using position animation"""
    w, h = clip1.w, clip1.h

    # Create transition clips
    clip1_end = clip1.subclipped(clip1.duration - duration, clip1.duration)
    clip2_start = clip2.subclipped(0, duration)

    # Define position functions based on direction
    def get_pos1(t):
        progress = t / duration
        if direction == "left":
            return (int(-w * progress), 0)
        elif direction == "right":
            return (int(w * progress), 0)
        elif direction == "up":
            return (0, int(-h * progress))
        else:  # down
            return (0, int(h * progress))

    def get_pos2(t):
        progress = t / duration
        if direction == "left":
            return (int(w * (1 - progress)), 0)
        elif direction == "right":
            return (int(-w * (1 - progress)), 0)
        elif direction == "up":
            return (0, int(h * (1 - progress)))
        else:  # down
            return (0, int(-h * (1 - progress)))

    clip1_end = clip1_end.with_position(get_pos1)
    clip2_start = clip2_start.with_position(get_pos2)

    transition_clip = CompositeVideoClip([clip1_end, clip2_start], size=(w, h))

    return concatenate_videoclips(
        [
            clip1.subclipped(0, clip1.duration - duration),
            transition_clip,
            clip2.subclipped(duration, clip2.duration),
        ]
    )


def apply_random_transition(clip1, clip2, transition_duration=0.5):
    """Apply a random transition between two clips"""
    # Use mostly crossfade for reliability, with occasional slide transitions
    transition_type = random.choice(["crossfade", "crossfade", "crossfade"])

    if transition_type == "crossfade":
        print(f"Applying crossfade transition")
        return crossfade_transition(clip1, clip2, transition_duration)
    else:
        # Random slide direction
        direction = random.choice(["left", "right", "up", "down"])
        print(f"Applying slide_{direction} transition")
        try:
            return slide_transition(clip1, clip2, direction, transition_duration)
        except:
            # Fallback to crossfade if slide fails
            return crossfade_transition(clip1, clip2, transition_duration)


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
    intro_duration = 1
    outro_duration = 2
    # per_image_duration = narration.duration / len(fact_image_paths)
    per_image_duration = 5.5  # subtract intro outro time

    # --- Create clips ---
    intro = ImageClip(intro_image).with_duration(intro_duration).resized(height=720)
    fact_clips = [
        ImageClip(img).with_duration(per_image_duration).resized(height=720)
        for img in fact_image_paths
    ]
    outro = ImageClip(outro_image).with_duration(outro_duration).resized(height=720)

    # --- Combine video clips with random transitions ---
    transition_duration = 0.5  # 0.5 seconds for transitions

    # Start with intro
    video = intro

    # Add fact clips with transitions
    for i, fact_clip in enumerate(fact_clips):
        video = apply_random_transition(video, fact_clip, transition_duration)

    # Add outro with transition
    video = apply_random_transition(video, outro, transition_duration)

    # --- Loop or trim background music properly ---
    if bg_music.duration < video.duration:
        # Loop the bg music until it covers full video duration
        loops = int(video.duration // bg_music.duration) + 1
        bg_music_loops = [bg_music] * loops
        bg_music_full = CompositeAudioClip(bg_music_loops).with_duration(video.duration)
    else:
        bg_music_full = bg_music.with_volume_scaled(0.7)
        bg_music_full = bg_music.subclipped(5, narration.duration + 5)

    # --- Combine narration (starts after intro) + bg music ---
    final_audio = CompositeAudioClip(
        [bg_music_full, narration.with_start(0)]
    ).with_duration(narration.duration)

    # --- Attach audio ---
    video = video.with_audio(final_audio)

    # --- Export final video ---
    video.write_videofile(output_path, fps=24, audio_codec="aac")

    print(f"Video saved at {output_path}")


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
