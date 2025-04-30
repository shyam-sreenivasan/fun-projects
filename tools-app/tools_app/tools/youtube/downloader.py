from yt_dlp import YoutubeDL
import os


def run_download_youtube(upload_folder, video_url, mode, output_basename):
    ydl_opts = {
        'outtmpl': os.path.join(upload_folder, output_basename + '.%(ext)s'),
        'quiet': True,
    }

    if mode == 'audio':
        ydl_opts.update({
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(upload_folder, output_basename + '_audio.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
            }]
        })
    elif mode == 'video':
        ydl_opts['format'] = 'bestvideo+bestaudio/best'
        ydl_opts['merge_output_format'] = "mp4"
    else:  # both: audio and video separately
        ydl_opts['format'] = 'bestvideo+bestaudio/best'
        ydl_opts['merge_output_format'] = "mp4"
        # Will download full video+audio combo; extra audio step below

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

    # If both selected, run separate audio-only download too
    if mode == 'both':
        audio_opts = {
            'outtmpl': os.path.join(upload_folder, output_basename + '_audio.%(ext)s'),
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
            }],
            'quiet': True
        }
        with YoutubeDL(audio_opts) as ydl:
            ydl.download([video_url])
