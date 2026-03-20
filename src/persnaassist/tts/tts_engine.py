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