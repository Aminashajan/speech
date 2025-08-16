import whisper
import torch
import keyboard
import pyaudio
import wave
import time

# Load Whisper Model
model = whisper.load_model("base")  # Options: "tiny", "base", "small", "medium", "large"

# Define supported languages
LANGUAGES = {
    "English": "en",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Hindi": "hi",
    "Chinese": "zh",
    "Japanese": "ja"
}

paused = False  # Pause flag

def toggle_pause():
    """Toggle pause state when 'P' is pressed."""
    global paused
    paused = not paused
    print("Paused" if paused else "Resumed")

def choose_language():
    """Allow the user to select a language."""
    print("Select a language for real-time captioning:")
    for i, lang in enumerate(LANGUAGES.keys(), start=1):
        print(f"{i}. {lang}")
    
    choice = int(input("Enter the number of your language: ")) - 1
    selected_language = list(LANGUAGES.values())[choice]
    print(f"Selected Language: {list(LANGUAGES.keys())[choice]} ({selected_language})")
    return selected_language

def record_audio(filename="temp_audio.wav", duration=5, rate=16000, channels=1):
    """Records audio from the microphone and saves it as a WAV file."""
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=channels, rate=rate, input=True, frames_per_buffer=1024)
    
    print("Listening... (Press 'P' to pause, 'R' to resume)")
    frames = []

    for _ in range(0, int(rate / 1024 * duration)):
        if paused:
            time.sleep(0.1)  # Pause without blocking the script
            continue
        data = stream.read(1024)
        frames.append(data)
    
    stream.stop_stream()
    stream.close()
    p.terminate()

    # Save recorded audio
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
    wf.setframerate(rate)
    wf.writeframes(b''.join(frames))
    wf.close()

def transcribe_audio(filename, language):
    """Transcribes recorded audio using Whisper."""
    result = model.transcribe(filename, language=language)
    return result["text"]

def real_time_captioning(language_code):
    """Continuously captures and transcribes speech in real time."""
    keyboard.add_hotkey('p', toggle_pause)  # Assign 'P' key to toggle pause

    while True:
        if not paused:
            record_audio()  # Capture short audio clip
            text = transcribe_audio("temp_audio.wav", language_code)
            print(f"Caption ({language_code}): {text}")

if __name__ == "__main__":
    language = choose_language()
    real_time_captioning(language)
