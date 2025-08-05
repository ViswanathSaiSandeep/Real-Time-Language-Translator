import speech_recognition as sr

def speech_to_text():
    recognizer = sr.Recognizer()
    recognizer.energy_threshold = 300
    recognizer.dynamic_energy_threshold = True
    recognizer.pause_threshold = 0.4 
    recognizer.operation_timeout = 5

    with sr.Microphone() as source:
        print("Calibrating mic...")
        recognizer.adjust_for_ambient_noise(source, duration=0.2)
        while True:
            print("Listening...")
            try:
                audio = recognizer.listen(source, timeout=2, phrase_time_limit=5)
            except sr.WaitTimeoutError:
                print("No speech detected. Listening again...")
                continue
            try:
                print("Recognizing...")
                text = recognizer.recognize_google(audio, language='en-US')
                print("You said:", text)
                return text
            except sr.UnknownValueError:
                print("Could not understand audio.")
            except sr.RequestError as e:
                print(f"API error: {e}")
            return None

if __name__ == "__main__":
    speech_to_text()