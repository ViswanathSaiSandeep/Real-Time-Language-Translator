import asyncio
from googletrans import Translator
from stt import speech_to_text

async def translate_text(text):
    translator = Translator() 
    choices = {
        '1': 'es',
        '2': 'fr',
        '3': 'zh-cn',
        '4': 'hi',
        '5': 'te'
    }
    print("Choose the language to be translated")
    print("1. Spanish")
    print("2. French")
    print("3. Chinese")
    print("4. Hindi")
    print("5. Telugu")
    choice = input("Enter your choice: ")

    if choice not in choices:
        print("Invalid choice. Please select a valid option.")
        return None

    target_language = choices[choice]
    translation = await translator.translate(text, dest=target_language)
    translated_text = translation.text
    print("Translated text:", translated_text)
    return translated_text

if __name__ == "__main__":
    print("Choose the mode for translation:")
    print("1. Text to Text")
    print("2. Speech to Text")
    mode = input("Enter your choice: ")

    if mode == '1':
        text = input("Enter the text to be translated: ")
        asyncio.run(translate_text(text))
    elif mode == '2':
        text = speech_to_text()
        if text:
            asyncio.run(translate_text(text))
        else:
            print("No speech detected.")
