import asyncio
from googletrans import Translator

async def translate_text(text, target_language):
    translator = Translator()
    translation = await translator.translate(text, dest=target_language)
    translated_text = translation.text
    print("Translated text:", translated_text)
    return translated_text
