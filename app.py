from stt import speech_to_text
from translate import translate_text
from tts import text_to_speech
import asyncio
import time

def real_time_language_translator():
    print("------------------------------------------------")
    print("- Welcome to the Real-Time Language Translator -")
    print("------------------------------------------------")
    print("Choose the mode:")
    print("1. Speech to Text")
    print("2. Text to Text")
    print("3. Text to Speech")
    print("4. Exit")
    mode = input("Enter the mode number: ")
    choices = {
        '1': 'zh-cn',
        '2': 'es',
        '3': 'fr',
        '4': 'te',
        '5': 'hi'
    }
    print("Choose the language to be translated:")
    print("1. Chinese")
    print("2. Spanish") 
    print("3. French")
    print("4. Telugu")
    print("5. Hindi")
    choice = input("Enter the language number: ")
    target_language = choices[choice]
    print("Selected ", target_language, " as the target language.")
    if mode == '1':
        text = speech_to_text()
        asyncio.run(translate_text(text, target_language))
        time.sleep(1)
        real_time_language_translator()
    elif mode == '2':
        text = input("Enter the text to translate: ")
        asyncio.run(translate_text(text, target_language))
        time.sleep(1)
        real_time_language_translator()
    elif mode == '3':
        text = input("Enter the text to translate: ")
        translated_text = asyncio.run(translate_text(text, target_language))
        text_to_speech(translated_text, language=target_language)
        time.sleep(1)
        real_time_language_translator()
    elif mode == '4':
        print("Exiting the program.")
        exit()
    else:
        print("Invalid choice. Please try again.")
        real_time_language_translator()

if __name__ == "__main__":
    real_time_language_translator()