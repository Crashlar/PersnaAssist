<<<<<<< HEAD
import pyttsx3

class TTSEngine:
    def __init__(self, rate=180, volume=1.0, voice_index=0):
        """
        Initialize TTS engine with given settings
        """
        self.engine = pyttsx3.init()

        # Set speech rate (speed)
        self.engine.setProperty('rate', rate)

        # Set volume (0.0 to 1.0)
        self.engine.setProperty('volume', volume)

        # Set voice (male/female depending on system)
        voices = self.engine.getProperty('voices')
        if voices and len(voices) > voice_index:
            self.engine.setProperty('voice', voices[voice_index].id)

    def speak(self, text: str):
        """
        Convert text to speech and play it
        """
        self.engine.say(text)
        self.engine.runAndWait()

    def stop(self):
        """
        Stop current speech (useful for interruption)
        """
        self.engine.stop()
=======
import asyncio
import pyttsx3

def speak_sync(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

async def text_to_speech(text: str):
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, speak_sync, text)

>>>>>>> 708e1532998f7d2c57644d8f5c60c3d35e78f530
