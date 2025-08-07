from googletrans import Translator

def translate_text(text, target_language):
    translator = Translator()
    try:
        translation = translator.translate(text, dest=target_language)
        translated_text = translation.text
        print("Translated text:", translated_text)
        return translated_text
    except Exception as e:
        print("Translation error:", e)
        return ""