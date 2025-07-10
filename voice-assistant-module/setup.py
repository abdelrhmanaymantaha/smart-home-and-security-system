from setuptools import setup, find_packages

setup(
    name="Voice Assistant",
    version="1.0",
    description="A simple voice assistant",
    author="Abdelrhman ayman",
    author_email="Abdotha5@gmail.com",
    packages=find_packages(),  # Automatically finds packages
    install_requires=[
        "pandas",  
        "paho-mqtt",
        "pyaudio",
        'pyttsx3',
        'torch',
        'openai-whisper',
        'scikit-learn',
        'joblib',
        'requests',
        "matplotlib",
        "seaborn",
        "sqlalchemy",
    ],
)