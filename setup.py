from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="persnaassist",  
    version="0.1.0",

    author="Mukesh Kumar",
    author_email="mukeshkumar.in25@gmail.com",

    description="Real-time AI Voice Assistant with low latency (STT + LLM + TTS)",
    long_description=long_description,
    long_description_content_type="text/markdown",

    url="https://github.com/Crashlar/PersnaAssist",  

    license="MIT",

    packages=find_packages(),
    # package_dir={"": "src"},

    install_requires=[
        "numpy",
        "sounddevice",
        "pyaudio",
        "faster-whisper",
        "openai",
        "pyttsx3",
        "sqlalchemy",
        "pydantic",
        "python-dotenv",
    ],

    entry_points={
        "console_scripts": [
            "persnaassist=app:main"
        ]
    },

    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],

    keywords="voice assistant, ai assistant, speech to text, text to speech, llm",

    python_requires=">=3.9",
    include_package_data=True,
)