from googletrans import Translator, LANGUAGES

def translate_text(text, target_language, source_language='auto'):
    translator = Translator()
    try:
        translation = translator.translate(text, src=source_language, dest=target_language)

        detected_lang_name = LANGUAGES.get(translation.src, "Unknown").capitalize()
        
        print(f"Detected: {detected_lang_name} ({translation.src})")
        print("Translated text:", translation.text)

        return translation.text, detected_lang_name
        
    except Exception as e:
        print("Translation error:", e)
        return "", "Error"