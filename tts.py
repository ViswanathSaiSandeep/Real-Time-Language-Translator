from gtts import gTTS
import pygame
import time
import os

def text_to_speech(text, language="en"):
    if not text:
        print("No text provided for TTS.")
        return

    try:
        filename = "output.mp3"
        tts = gTTS(text=text, lang=language)
        tts.save(filename)

        pygame.mixer.init()
        pygame.mixer.music.load(filename)
        time.sleep(0.3)
        pygame.mixer.music.play()
        
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)

        pygame.mixer.quit()
        os.remove(filename)

    except Exception as e:
        print("Error in TTS:", e)