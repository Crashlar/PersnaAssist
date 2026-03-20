import sounddevice as sd
import numpy as np
import wave

class AudioPlayer:
    def __init__(self, sample_rate=16000):
        self.sample_rate = sample_rate

    def play_array(self, audio: np.ndarray):
        """
        Play audio from numpy array
        """
        sd.play(audio, self.sample_rate)
        sd.wait()

    def play_wav(self, file_path: str):
        """
        Play audio from WAV file
        """
        with wave.open(file_path, 'rb') as wf:
            sample_rate = wf.getframerate()
            frames = wf.readframes(wf.getnframes())

            audio = np.frombuffer(frames, dtype=np.int16)

            sd.play(audio, sample_rate)
            sd.wait()

    def play_stream(self, audio_generator):
        """
        Play streaming audio (advanced use)
        """
        for chunk in audio_generator:
            sd.play(chunk, self.sample_rate)
            sd.wait()