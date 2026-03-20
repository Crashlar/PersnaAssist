import asyncio
import pyttsx3

def speak_sync(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

async def text_to_speech(text: str):
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, speak_sync, text)

