from constants.GeneralConstants import AUDIO_RESOURCES_DIR
import os

import sounddevice as sd
import soundfile as sf

def play_audio(file_path):
    data, samplerate = sf.read(file_path, dtype='float32')
    sd.play(data, samplerate)

def play_sound(sound_name):
    sound_path = f"{AUDIO_RESOURCES_DIR}/{sound_name}.wav"
    # Check if the sound file exists
    if not os.path.exists(sound_path):
        print(f"Sound file not found: {sound_path}")
        return
    play_audio(sound_path)

# If this file is run directly, play the default sound
if __name__ == "__main__":
    play_sound("ding")
    sd.wait()  # Wait until sound has finished playing
