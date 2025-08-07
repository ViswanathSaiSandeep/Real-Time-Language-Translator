from stt import speech_to_text
from translate import translate_text
from tts import text_to_speech
import time
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
def save_translation(mode, language, input, output):
    with open("translated_text.txt", "a", encoding="utf-8") as f:
        f.write("----- Translation Session -----\n")
        f.write(f"Mode     : {mode}\n")
        f.write(f"Language : {language}\n")
        f.write(f"Input    : {input}\n")
        f.write(f"Output   : {output}\n")
        f.write("-------------------------------\n\n")
def real_time_language_translator():
    while True:
        clear_screen()
        print("------------------------------------------------")
        print("- Welcome to the Real-Time Language Translator -")
        print("------------------------------------------------")
        print("Choose the mode:")
        print("1. Speech to Text")
        print("2. Text to Text")
        print("3. Text to Speech")
        print("4. Speech to Speech")
        print("5. Exit")
        mode_input = input("Enter the mode number: ")
        if mode_input not in ['1', '2', '3', '4', '5']:
            print("Invalid mode number. Please try again.")
            time.sleep(1)
            continue
        if mode_input == '5':
            print("Exiting the program.")
            break
        clear_screen()
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
        if choice not in ['1', '2', '3', '4', '5']:
            print("Invalid language selection. Please enter a valid number.")
            time.sleep(1.5)
            continue
        target_language = choices[choice]
        print("Selected ", target_language, " as the target language.")
        clear_screen()
        if mode_input == '1':
            mode = "Speech to Text"
            text = speech_to_text()
            result = translate_text(text, target_language)
            save_translation(mode, target_language, text, result)
            real_time_language_translator()
        elif mode_input == '2':
            mode = "Text to Text"
            text = input("Enter the text to translate: ")
            result = translate_text(text, target_language)
            save_translation(mode, target_language, text, result)
            time.sleep(1)
            real_time_language_translator()
        elif mode_input == '3':
            mode = "Text to Speech"
            text = input("Enter the text to translate: ")
            translated_text = translate_text(text, target_language)
            text_to_speech(translated_text, language=target_language)
            save_translation(mode, target_language, text, result)
            time.sleep(1)
            real_time_language_translator()
        elif mode_input == '4':
            mode = "Speech to Speech"
            text = speech_to_text()
            translated_text = translate_text(text, target_language)
            text_to_speech(translated_text, language=target_language)
            save_translation(mode, target_language, text, result)
            time.sleep(1)
            real_time_language_translator()

if __name__ == "__main__":
    real_time_language_translator()