import numpy as np
import sounddevice as sd
import soundfile as sf
import threading
from collections import deque
from datetime import datetime

from constants.GeneralConstants import TEMP_AUDIO_DIR

class AudioBuffer:
    def __init__(self, sample_rate=16000, channels=1, buffer_seconds=60, chunk_size=1024):
        """
        Rolling audio buffer that keeps the last `buffer_seconds` of audio.

        :param sample_rate: Sampling rate in Hz
        :param channels: Number of channels (1 = mono)
        :param buffer_seconds: How many seconds of audio to keep
        :param chunk_size: Number of samples per chunk callback
        """
        self.sample_rate = sample_rate
        self.channels = channels
        self.buffer_seconds = buffer_seconds
        self.chunk_size = chunk_size

        # Max number of chunks in deque
        self.max_chunks = (self.sample_rate * self.buffer_seconds) // self.chunk_size

        # Deque stores chunks of audio
        self.buffer = deque(maxlen=self.max_chunks)

        self._stream = None
        self._lock = threading.Lock()

    def _callback(self, indata, frames, time, status):
        if status:
            print("Audio status:", status)
        # Flatten in case of multiple channels
        chunk = indata.copy().reshape(-1)
        with self._lock:
            self.buffer.append(chunk)

    def start(self):
        """Start recording in a background thread."""
        self._stream = sd.InputStream(
            samplerate=self.sample_rate,
            channels=self.channels,
            blocksize=self.chunk_size,
            callback=self._callback
        )
        self._stream.start()
        print("Audio buffer started...")

    def stop(self):
        """Stop recording."""
        if self._stream:
            self._stream.stop()
            self._stream.close()
            self._stream = None
            print("Audio buffer stopped.")

    def get_buffer(self):
        """Return the last `buffer_seconds` audio as a NumPy array (float32)."""
        with self._lock:
            if len(self.buffer) == 0:
                return np.zeros(self.chunk_size, dtype=np.float32)
            return np.concatenate(list(self.buffer))

    def snapshot_to_wav(self, filename=None):
        """Save the current buffer to a WAV file."""
        audio = self.get_buffer()
        if filename is None:
            # Default filename with timestamp
            filename = datetime.now().strftime("snapshot_%Y%m%d_%H%M%S.wav")
        
        # Make sure to use the temp audio directory
        full_path = f"{TEMP_AUDIO_DIR}/{filename}"
        sf.write(full_path, audio, samplerate=self.sample_rate)

        print(f"Snapshot saved to {full_path}")
        return full_path

# ============================
# Demo usage
# ============================
if __name__ == "__main__":
    import time
    buffer_seconds = 10
    audio_buffer = AudioBuffer(buffer_seconds=buffer_seconds)
    audio_buffer.start()

    try:
        while True:
            cmd = input(f"Press ENTER to save last {buffer_seconds}s to WAV, Ctrl+C to quit: ")
            audio_buffer.snapshot_to_wav()
    except KeyboardInterrupt:
        audio_buffer.stop()
