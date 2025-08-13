
import os
from moviepy import VideoFileClip, AudioFileClip, concatenate_videoclips, concatenate_audioclips # type: ignore
import uuid

def parse_time_to_seconds(time_str):
    """Convert HH:MM:SS to seconds."""
    parts = list(map(int, time_str.strip().split(":")))
    while len(parts) < 3:
        parts.insert(0, 0)  # pad to HH:MM:SS
    h, m, s = parts
    return h * 3600 + m * 60 + s

def trim_media_file(input_path, start_times, end_times, output_folder):
    mime_type = input_path.lower()
    is_audio = mime_type.endswith((".mp3", ".wav", ".m4a", ".aac"))

    start_seconds = [parse_time_to_seconds(t) for t in start_times]
    end_seconds = [parse_time_to_seconds(t) for t in end_times]

    output_ext = ".mp3" if is_audio else ".mp4"
    output_filename = f"trimmed_{uuid.uuid4().hex}{output_ext}"
    output_path = os.path.join(output_folder, output_filename)

    try:
        if is_audio:
            clip = AudioFileClip(input_path)
            segments = [clip.subclipped(s, e) for s, e in zip(start_seconds, end_seconds)]
            final_clip = concatenate_audioclips(segments)
            final_clip.write_audiofile(output_path)
        else:
            clip = VideoFileClip(input_path)
            segments = [clip.subclipped(s, e) for s, e in zip(start_seconds, end_seconds)]
            final_clip = concatenate_videoclips(segments)
            final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")

        clip.close()
        final_clip.close()
        return output_path
    except Exception as e:
        print(f"[ERROR] Failed to trim media: {e}")
        return None