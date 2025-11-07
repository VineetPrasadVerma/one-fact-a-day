from moviepy import (
    ImageClip,
    AudioFileClip,
    CompositeAudioClip,
    concatenate_videoclips,
    CompositeVideoClip,
    TextClip,
)
from moviepy.video.fx import FadeIn, FadeOut
import random
import numpy as np
import re
import os

# Font path for macOS system fonts
FONT_PATH = "/System/Library/Fonts/Helvetica.ttc"
# Fallback to system default if Helvetica not found
if not os.path.exists(FONT_PATH):
    FONT_PATH = "/System/Library/Fonts/HelveticaNeue.ttc"


# For captions
# Characters ['D', 'i', 'd', ' ', 'y', 'o', 'u', ' ', 'k', 'n', 'o', 'w', '?', ' ', 'T', 'h', 'a', 't', ' ', 'b', 'i', 'g', ',', ' ', 'f', 'l', 'u', 'f', 'f', 'y', ' ', 'c', 'l', 'o', 'u', 'd', ' ', 'd', 'r', 'i', 'f', 't', 'i', 'n', 'g', ' ', 'o', 'v', 'e', 'r', 'h', 'e', 'a', 'd', ' ', 'a', 'c', 't', 'u', 'a', 'l', 'l', 'y', ' ', 'w', 'e', 'i', 'g', 'h', 's', ' ', 'o', 'v', 'e', 'r', ' ', 'a', ' ', 'm', 'i', 'l', 'l', 'i', 'o', 'n', ' ', 'p', 'o', 'u', 'n', 'd', 's', '?', ' ', 'Y', 'e', 'p', '!', ' ', 'A', ' ', 's', 'i', 'n', 'g', 'l', 'e', ' ', 'c', 'u', 'm', 'u', 'l', 'u', 's', ' ', 'c', 'l', 'o', 'u', 'd', ' ', 'h', 'o', 'l', 'd', 's', ' ', 'e', 'n', 'o', 'u', 'g', 'h', ' ', 'w', 'a', 't', 'e', 'r', ' ', 't', 'o', ' ', 'b', 'e', ' ', 'h', 'e', 'a', 'v', 'i', 'e', 'r', ' ', 't', 'h', 'a', 'n', ' ', 'a', 'n', ' ', 'e', 'n', 't', 'i', 'r', 'e', ' ', 'h', 'e', 'r', 'd', ' ', 'o', 'f', ' ', 'e', 'l', 'e', 'p', 'h', 'a', 'n', 't', 's', '.', ' ', 'S', 'e', 'r', 'i', 'o', 'u', 's', 'l', 'y', ',', ' ', 'i', 'm', 'a', 'g', 'i', 'n', 'e', ' ', 't', 'h', 'a', 't', ' ', 'i', 'm', 'm', 'e', 'n', 's', 'e', ' ', 'w', 'e', 'i', 'g', 'h', 't', ' ', 's', 'i', 'l', 'e', 'n', 't', 'l', 'y', ' ', 'f', 'l', 'o', 'a', 't', 'i', 'n', 'g', ' ', 'b', 'y', '!', ' ', 'M', 'i', 'n', 'd', '-', 'b', 'l', 'o', 'w', 'i', 'n', 'g', ',', ' ', 'r', 'i', 'g', 'h', 't', '?', ' ', 'L', 'i', 'k', 'e', ',', ' ', 's', 'h', 'a', 'r', 'e', ',', ' ', 'a', 'n', 'd', ' ', 's', 'u', 'b', 's', 'c', 'r', 'i', 'b', 'e', ' ', 'f', 'o', 'r', ' ', 'm', 'o', 'r', 'e', '!', '\n', ' ', ' ', ' ', ' ']
# Character start time seconds [0.0, 0.116, 0.174, 0.221, 0.267, 0.29, 0.325, 0.348, 0.395, 0.441, 0.488, 0.557, 0.639, 0.836, 1.103, 1.149, 1.231, 1.277, 1.312, 1.405, 1.486, 1.602, 1.672, 1.718, 1.776, 1.858, 1.927, 1.974, 2.02, 2.101, 2.171, 2.241, 2.287, 2.357, 2.45, 2.508, 2.554, 2.601, 2.647, 2.694, 2.74, 2.798, 2.856, 2.902, 2.926, 2.949, 3.007, 3.042, 3.1, 3.146, 3.204, 3.251, 3.297, 3.344, 3.39, 3.437, 3.495, 3.541, 3.587, 3.634, 3.68, 3.715, 3.762, 3.796, 3.855, 3.889, 3.971, 3.994, 4.017, 4.063, 4.11, 4.168, 4.226, 4.284, 4.331, 4.365, 4.435, 4.458, 4.54, 4.586, 4.644, 4.69, 4.737, 4.783, 4.841, 4.876, 4.946, 5.004, 5.12, 5.178, 5.236, 5.294, 5.41, 5.526, 5.642, 5.735, 5.851, 5.968, 6.107, 6.525, 6.606, 6.722, 6.78, 6.861, 6.896, 6.989, 7.059, 7.105, 7.198, 7.314, 7.454, 7.546, 7.616, 7.697, 7.767, 7.825, 7.883, 7.93, 7.999, 8.092, 8.162, 8.231, 8.29, 8.336, 8.417, 8.464, 8.522, 8.568, 8.626, 8.661, 8.719, 8.754, 8.789, 8.824, 8.858, 8.905, 8.951, 9.044, 9.114, 9.16, 9.195, 9.242, 9.265, 9.288, 9.358, 9.392, 9.462, 9.52, 9.578, 9.636, 9.683, 9.741, 9.81, 9.88, 9.903, 9.961, 9.985, 10.019, 10.066, 10.101, 10.147, 10.182, 10.217, 10.275, 10.321, 10.391, 10.53, 10.693, 10.762, 10.797, 10.855, 10.902, 10.983, 11.053, 11.099, 11.146, 11.18, 11.204, 11.262, 11.308, 11.355, 11.413, 11.459, 11.517, 11.587, 11.633, 11.691, 11.784, 11.981, 12.399, 12.481, 12.597, 12.666, 12.713, 12.759, 12.794, 12.864, 12.945, 13.061, 13.177, 13.34, 13.456, 13.537, 13.63, 13.7, 13.746, 13.793, 13.827, 13.862, 13.886, 13.92, 13.955, 14.002, 14.06, 14.095, 14.164, 14.234, 14.292, 14.35, 14.408, 14.454, 14.501, 14.547, 14.617, 14.652, 14.675, 14.721, 14.779, 14.837, 14.907, 15.046, 15.104, 15.162, 15.185, 15.232, 15.29, 15.325, 15.383, 15.429, 15.487, 15.534, 15.592, 15.65, 15.719, 15.743, 15.766, 15.836, 15.894, 16.161, 16.3, 16.567, 16.648, 16.764, 16.822, 16.857, 16.915, 16.962, 17.02, 17.078, 17.124, 17.182, 17.217, 17.24, 17.287, 17.31, 17.38, 17.461, 17.496, 17.542, 17.635, 17.716, 17.809, 17.891, 18.007, 18.065, 18.181, 18.216, 18.274, 18.343, 18.436, 18.552, 18.622, 18.68, 18.715, 18.738, 18.808, 18.866, 18.901, 18.959, 19.005, 19.063, 19.144, 19.226, 19.342, 19.423, 19.504, 19.562, 19.609, 19.644, 19.69, 19.737, 19.771, 19.818, 19.864, 19.98, 20.038, 20.154, 20.201, 20.201, 20.201, 20.201, 20.201]
# Character end time seconds [0.116, 0.174, 0.221, 0.267, 0.29, 0.325, 0.348, 0.395, 0.441, 0.488, 0.557, 0.639, 0.836, 1.103, 1.149, 1.231, 1.277, 1.312, 1.405, 1.486, 1.602, 1.672, 1.718, 1.776, 1.858, 1.927, 1.974, 2.02, 2.101, 2.171, 2.241, 2.287, 2.357, 2.45, 2.508, 2.554, 2.601, 2.647, 2.694, 2.74, 2.798, 2.856, 2.902, 2.926, 2.949, 3.007, 3.042, 3.1, 3.146, 3.204, 3.251, 3.297, 3.344, 3.39, 3.437, 3.495, 3.541, 3.587, 3.634, 3.68, 3.715, 3.762, 3.796, 3.855, 3.889, 3.971, 3.994, 4.017, 4.063, 4.11, 4.168, 4.226, 4.284, 4.331, 4.365, 4.435, 4.458, 4.54, 4.586, 4.644, 4.69, 4.737, 4.783, 4.841, 4.876, 4.946, 5.004, 5.12, 5.178, 5.236, 5.294, 5.41, 5.526, 5.642, 5.735, 5.851, 5.968, 6.107, 6.525, 6.606, 6.722, 6.78, 6.861, 6.896, 6.989, 7.059, 7.105, 7.198, 7.314, 7.454, 7.546, 7.616, 7.697, 7.767, 7.825, 7.883, 7.93, 7.999, 8.092, 8.162, 8.231, 8.29, 8.336, 8.417, 8.464, 8.522, 8.568, 8.626, 8.661, 8.719, 8.754, 8.789, 8.824, 8.858, 8.905, 8.951, 9.044, 9.114, 9.16, 9.195, 9.242, 9.265, 9.288, 9.358, 9.392, 9.462, 9.52, 9.578, 9.636, 9.683, 9.741, 9.81, 9.88, 9.903, 9.961, 9.985, 10.019, 10.066, 10.101, 10.147, 10.182, 10.217, 10.275, 10.321, 10.391, 10.53, 10.693, 10.762, 10.797, 10.855, 10.902, 10.983, 11.053, 11.099, 11.146, 11.18, 11.204, 11.262, 11.308, 11.355, 11.413, 11.459, 11.517, 11.587, 11.633, 11.691, 11.784, 11.981, 12.399, 12.481, 12.597, 12.666, 12.713, 12.759, 12.794, 12.864, 12.945, 13.061, 13.177, 13.34, 13.456, 13.537, 13.63, 13.7, 13.746, 13.793, 13.827, 13.862, 13.886, 13.92, 13.955, 14.002, 14.06, 14.095, 14.164, 14.234, 14.292, 14.35, 14.408, 14.454, 14.501, 14.547, 14.617, 14.652, 14.675, 14.721, 14.779, 14.837, 14.907, 15.046, 15.104, 15.162, 15.185, 15.232, 15.29, 15.325, 15.383, 15.429, 15.487, 15.534, 15.592, 15.65, 15.719, 15.743, 15.766, 15.836, 15.894, 16.161, 16.3, 16.567, 16.648, 16.764, 16.822, 16.857, 16.915, 16.962, 17.02, 17.078, 17.124, 17.182, 17.217, 17.24, 17.287, 17.31, 17.38, 17.461, 17.496, 17.542, 17.635, 17.716, 17.809, 17.891, 18.007, 18.065, 18.181, 18.216, 18.274, 18.343, 18.436, 18.552, 18.622, 18.68, 18.715, 18.738, 18.808, 18.866, 18.901, 18.959, 19.005, 19.063, 19.144, 19.226, 19.342, 19.423, 19.504, 19.562, 19.609, 19.644, 19.69, 19.737, 19.771, 19.818, 19.864, 19.98, 20.038, 20.154, 20.201, 20.201, 20.201, 20.201, 20.201, 20.387]

def crossfade_transition(clip1, clip2, duration=0.5):
    """Crossfade transition with manual frame blending for both fade in and fade out"""
    # Extract transition segments
    clip1_end = clip1.subclipped(clip1.duration - duration, clip1.duration)
    clip2_start = clip2.subclipped(0, duration)
    
    # clip1_end = clip1_end.with_effects([FadeOut(duration)])
    # clip2_start = clip2_start.with_effects([FadeIn(duration)])
    
    # Set duration
    clip1_end = clip1_end.with_duration(duration)
    clip2_start = clip2_start.with_duration(duration)
    
    # Manual frame blending ensures both fade in and fade out work correctly
    def make_blended_frame(t):
        """Manually blend frames with smooth opacity transitions"""
        # Calculate progress (0.0 to 1.0)
        progress = t / duration if duration > 0 else 1.0
        
        # Get frames from both clips
        frame1 = clip1_end.get_frame(t)
        frame2 = clip2_start.get_frame(t)
        
        # Calculate opacity values - both fade smoothly and equally
        opacity1 = 1.0 - progress  # Fade out: starts at 1.0, ends at 0.0
        opacity2 = progress        # Fade in: starts at 0.0, ends at 1.0
        
        # Blend frames manually (both are visible throughout)
        blended = (frame1.astype(np.float32) * opacity1 + 
                  frame2.astype(np.float32) * opacity2).astype(np.uint8)
        return blended
    
    # Create a custom clip that blends frames
    from moviepy.video.VideoClip import VideoClip
    
    class BlendedTransitionClip(VideoClip):
        def __init__(self):
            VideoClip.__init__(self)
            self.duration = duration
            self.size = clip1.size
            
        def get_frame(self, t):
            return make_blended_frame(t)
    
    transition = BlendedTransitionClip()

    # return concatenate_videoclips(
    #     [
    #         clip1.subclipped(0, clip1.duration - duration),
    #         CompositeVideoClip([clip1_end, clip2_start]),
    #         clip2.subclipped(duration, clip2.duration),
    #     ]
    # )
    
    return concatenate_videoclips(
        [
            clip1.subclipped(0, clip1.duration - duration),
            transition,
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


def create_captions(script_text, audio_duration, video_size, start_time=0):
    """
    Create animated word-by-word captions for the video
    
    Args:
        script_text: The text to display as captions
        audio_duration: Duration of the audio in seconds
        video_size: Tuple of (width, height) of the video
        start_time: When captions should start (default 0)
    
    Returns:
        List of TextClip objects with timing
    """
    # Split text into words
    words = re.findall(r'\S+', script_text)
    
    # Calculate duration per word
    words_per_second = len(words) / audio_duration
    duration_per_word = audio_duration / len(words)
    
    caption_clips = []
    
    # Group words into phrases (3-4 words at a time for better readability)
    words_per_phrase = 3
    
    for i in range(0, len(words), words_per_phrase):
        phrase = ' '.join(words[i:i + words_per_phrase])
        phrase_start = start_time + (i * duration_per_word)
        phrase_duration = min(words_per_phrase * duration_per_word, audio_duration - (i * duration_per_word))
        
        # Create text clip with styling (using system Helvetica font)
        txt_clip = (
            TextClip(
                text=phrase,
                font=FONT_PATH,
                font_size=30,
                color='white',
                stroke_color='black',
                stroke_width=3,
                method='caption',
                size=(video_size[0] - 100, None),  # Leave margin
                text_align='center'
            )
            .with_position(('center', 'bottom'))
            .with_start(phrase_start)
            .with_duration(phrase_duration)
        )
        
        caption_clips.append(txt_clip)
    
    return caption_clips


def create_word_captions(script_text, audio_duration, video_size, start_time=0):
    """
    Create word-by-word captions (TikTok/Reels style) with yellow highlight effect
    
    Args:
        script_text: The text to display as captions
        audio_duration: Duration of the audio in seconds
        video_size: Tuple of (width, height) of the video
        start_time: When captions should start (default 0)
    
    Returns:
        List of TextClip objects with timing
    """
    # Split text into words
    words = re.findall(r'\S+', script_text)
    
    # Calculate duration per word
    duration_per_word = audio_duration / len(words)
    
    caption_clips = []
    
    for i, word in enumerate(words):
        word_start = start_time + (i * duration_per_word)
        
        # Create text clip with yellow/gold styling for emphasis (using system Helvetica font)
        txt_clip = (
            TextClip(
                text=word.upper(),
                font=FONT_PATH,
                font_size=70,
                color='yellow',
                stroke_color='black',
                stroke_width=4,
            )
            .with_position(('center', int(video_size[1] * 0.75)))  # Position in lower third
            .with_start(word_start)
            .with_duration(duration_per_word * 1.2)  # Slight overlap for smooth transition
            .with_effects([FadeIn(0.1), FadeOut(0.1)])
        )
        
        caption_clips.append(txt_clip)
    
    return caption_clips


def create_fact_video(
    fact_audio_path,
    fact_image_paths,
    bg_music_path,
    intro_image,
    outro_image,
    script_text=None,
    caption_style="word",  # "word" or "phrase" or None
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

    # --- Add captions if script_text is provided ---
    if script_text and caption_style:
        print(f"Adding {caption_style} captions...")
        
        # Get video dimensions
        video_size = (video.w, video.h)
        
        # Create caption clips based on style
        if caption_style == "word":
            caption_clips = create_word_captions(
                script_text, 
                narration.duration, 
                video_size, 
                start_time=0  # Captions start with narration
            )
        elif caption_style == "phrase":
            caption_clips = create_captions(
                script_text, 
                narration.duration, 
                video_size, 
                start_time=0
            )
        else:
            caption_clips = []
        
        # Overlay captions on video
        if caption_clips:
            video = CompositeVideoClip([video] + caption_clips)
            print(f"Added {len(caption_clips)} caption clips")

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
    script_text="""Did you know?
    There are more stars in the observable universe than all the grains of sand on every beach on Earth? Let that staggering number sink in! Wild, right?
    Like, share, and subscribe for more!""",
    caption_style="phrase",  # Use "word" for TikTok-style, "phrase" for phrase-by-phrase, or None for no captions
    output_path="./python/assets/video/fact_video.mp4",
)
