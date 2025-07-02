import os
from pydub import AudioSegment

def merge_audios_in_folder(input_folder, output_path="merged_audio.mp3"):
    # Supported audio formats
    supported_exts = ('.mp3', '.wav', '.ogg', '.flac', '.aac', '.m4a')

    # List and sort files for consistent order
    audio_files = sorted([
        f for f in os.listdir(input_folder)
        if f.lower().endswith(supported_exts)
    ])

    if not audio_files:
        print("No supported audio files found in the folder.")
        return

    print(f"Found {len(audio_files)} files. Merging...")

    # Initialize with the first audio file
    combined = AudioSegment.from_file(os.path.join(input_folder, audio_files[0]))

    # Append the rest
    for filename in audio_files[1:]:
        filepath = os.path.join(input_folder, filename)
        next_audio = AudioSegment.from_file(filepath)
        combined += next_audio

    # Export merged audio
    combined.export(output_path, format="mp3")
    print(f"Merged audio saved to {output_path}")

# Example usage:
if __name__ == "__main__":
    merge_audios_in_folder("/home/shyam/Downloads/kidambi-slokas", "merged_output.mp3")
