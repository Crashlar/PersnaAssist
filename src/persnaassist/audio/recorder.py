import sounddevice as sd
import numpy as np

class AudioRecorder:
    def __init__(self, sample_rate=16000, channels=1, chunk_size=1024):
        self.sample_rate = sample_rate
        self.channels = channels
        self.chunk_size = chunk_size

    def record_chunk(self):
        """
        Record a small chunk of audio (low latency)
        """
        audio = sd.rec(
            frames=self.chunk_size,
            samplerate=self.sample_rate,
            channels=self.channels,
            dtype="int16"
        )
        sd.wait()
        return audio

    def record_seconds(self, duration=3):
        """
        Record full audio for given seconds (not real-time)
        """
        audio = sd.rec(
            int(duration * self.sample_rate),
            samplerate=self.sample_rate,
            channels=self.channels,
            dtype="int16"
        )
        sd.wait()
        return audio

    def stream_audio(self):
        """
        Generator for continuous audio stream (BEST for real-time)
        """
        with sd.InputStream(
            samplerate=self.sample_rate,
            channels=self.channels,
            blocksize=self.chunk_size,
            dtype="int16"
        ) as stream:
            while True:
                audio_chunk, _ = stream.read(self.chunk_size)
                yield audio_chunk