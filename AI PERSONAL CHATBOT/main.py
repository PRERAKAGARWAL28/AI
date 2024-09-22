import pvporcupine
import pyaudio
import speech_recognition as sr
import webbrowser
import pyttsx3
import requests
import openai
import os
import numpy as np
import asyncio
import threading
import musicLibrary

# Initialize recognizer, text-to-speech engine, and API keys
recognizer = sr.Recognizer()
engine = pyttsx3.init()
engine.setProperty('rate', 190)  # Adjust to a comfortable speaking speed

newsapi = os.getenv("211b7171620e4461bb03a811df8cd66d", "211b7171620e4461bb03a811df8cd66d")
openai.api_key = os.getenv("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", "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")
porcupine_access_key = "qOmissHGSj3fZE1Z616/YFg/r6flkHzB1t2bP50Wt1Jw7tgfrU20Mw=="  # Your Porcupine access key

def speak(text):
    """Convert text to speech using pyttsx3 for faster performance."""
    engine.say(text)
    engine.runAndWait()

async def ask_openai(question):
    """Query OpenAI API asynchronously and return the response."""
    try:
        completion = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "You are a virtual assistant."},
                      {"role": "user", "content": question}]
        )
        return completion.choices[0].message['content']
    except Exception as e:
        print(f"OpenAI API error: {e}")
        return "I couldn't get an answer from the AI."

def processCommand(command):
    """Process user commands."""
    if "open google" in command.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in command.lower():
        webbrowser.open("https://facebook.com")
    elif "open youtube" in command.lower():
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in command.lower():
        webbrowser.open("https://linkedin.com")
    elif "open portfolio" in command.lower():
        webbrowser.open("https://prerakagarwal28.github.io/MY-portfolio1/")
    elif "open achievements" in command.lower():
        webbrowser.open("https://drive.google.com/file/d/1Wcej1ks_XT5W4u43rBY3UEdnf63KSRDv/view?usp=sharing")
    elif "open my cv" in command.lower():
        webbrowser.open("https://drive.google.com/file/d/1Je8sRK8I_O5pfhvC7JoFN37zyBqaRVU-/view?usp=sharing")
    elif command.lower().startswith("play"):
        song = command.lower().split(" ", 1)[1]  # Get the song name after "play"
        link = musicLibrary.music.get(song, None)
        if link:
            webbrowser.open(link)
        else:
            speak("Sorry, I couldn't find the song.")
    elif "news" in command.lower():
        threading.Thread(target=fetch_news).start()  # Fetch news concurrently
    else:
        # Query OpenAI for general questions
        response = asyncio.run(ask_openai(command))
        speak(response)

def fetch_news():
    """Fetch and speak top news headlines."""
    try:
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}")
        if r.status_code == 200:
            data = r.json()
            articles = data.get('articles', [])
            for article in articles[:5]:  # Read out the top 5 headlines
                title = article.get('title', 'No title available')
                speak(title)
        else:
            speak("Unable to fetch news at the moment.")
    except Exception as e:
        print(f"News fetch error: {e}")
        speak("Error in fetching news.")

def porcupine_wake_word_detection():
    """Use Porcupine to detect the 'Porcupine' wake word."""
    porcupine = None
    pa = None
    audio_stream = None

    try:
        porcupine = pvporcupine.create(access_key=porcupine_access_key, keywords=["computer"])  # Use the "Porcupine" keyword

        pa = pyaudio.PyAudio()

        audio_stream = pa.open(
            rate=porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=porcupine.frame_length)

        print("Listening for the wake word 'Porcupine'...")

        while True:
            pcm = audio_stream.read(porcupine.frame_length, exception_on_overflow=False)
            pcm = np.frombuffer(pcm, dtype=np.int16)

            keyword_index = porcupine.process(pcm)
            if keyword_index >= 0:
                print("Wake word detected!")
                speak("Yes?")

                # Listen for commands after the wake word
                with sr.Microphone() as source:
                    print("Listening for command...")
                    recognizer.adjust_for_ambient_noise(source, duration=1)
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                    try:
                        command = recognizer.recognize_google(audio)
                        print(f"Command recognized: {command}")
                        processCommand(command)
                    except sr.UnknownValueError:
                        print("Could not understand command")
                    except sr.RequestError as e:
                        print(f"Speech recognition error: {e}")
    except Exception as e:
        print(f"Error initializing Porcupine: {e}")
    finally:
        if audio_stream is not None:
            audio_stream.close()
        if pa is not None:
            pa.terminate()
        if porcupine is not None:
            porcupine.delete()

if __name__ == "__main__":
    speak("Hi i am Prerak's Personal Assistant...")
    porcupine_wake_word_detection()  # Start Porcupine for wake word detection
