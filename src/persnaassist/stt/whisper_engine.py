<<<<<<< HEAD
from faster_whisper import WhisperModel
import numpy as np

class WhisperEngine:
    def __init__(self, model_size="base", device="cpu", compute_type="int8"):
        """
        Initialize Whisper model

        model_size: tiny, base, small, medium, large
        device: cpu or cuda
        compute_type: int8 (fast), float16 (gpu)
        """
        self.model = WhisperModel(
            model_size,
            device=device,
            compute_type=compute_type
        )

    def transcribe(self, audio, sample_rate=16000) -> str:

    # Convert to float32
        if audio.dtype == "int16":
            audio = audio.astype("float32") / 32768.0

        # Convert shape (48000,1) → (48000,)
        if len(audio.shape) > 1:
            audio = audio.squeeze()

        #  NORMALIZE (IMPORTANT)
        max_val = np.max(np.abs(audio))
        if max_val > 0:
            audio = audio / max_val

        segments, _ = self.model.transcribe(
            audio,
            language="en",
            beam_size=1
        )

        text = ""
        for segment in segments:
            text += segment.text + " "

        return text.strip()

    def transcribe_file(self, file_path: str) -> str:
        """
        Convert audio file to text
        """
        segments, _ = self.model.transcribe(file_path)

        text = ""
        for segment in segments:
            text += segment.text + " "

        return text.strip()
=======
import speech_recognition as sr

def speech_to_text_from_mic():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Speak now...")
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return "Could not understand audio"
    except sr.RequestError as e:
        return f"Error: {e}"

>>>>>>> 708e1532998f7d2c57644d8f5c60c3d35e78f530
