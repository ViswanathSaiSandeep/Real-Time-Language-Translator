import customtkinter as ctk
import threading
from PIL import Image, ImageTk
from stt import speech_to_text
from translate import translate_text
from tts import text_to_speech

class TranslatorApp(ctk.CTk):
    #text to text
    def translate_gui(self):
        if self.target_language_var.get() == "Choose the Language":
            self.output_text.delete("1.0", "end")
            self.output_text.insert("1.0", "Please select a target language.")
            return
        text_to_translate=self.input_text.get("1.0", "end-1c")
        if not text_to_translate.strip():
            self.output_text.delete("1.0", "end")
            self.output_text.insert("1.0", "Please enter the text to translate.")
            return
        target_lang_code = self.language_options[self.target_language_var.get()]

        def run_translation():
            translated_text = translate_text(text_to_translate, target_lang_code)
            self.output_text.delete("1.0", "end")
            self.output_text.insert("1.0", translated_text)
        threading.Thread(target=run_translation, daemon=True).start()

    #speech to text
    def record_and_translate(self):
        self.input_text.delete("1.0", "end")
        self.input_text.insert("1.0", "Listening...")
        self.update()
        def run_stt():
            recognised_text = speech_to_text()
            self.input_text.delete("1.0", "end")
            if recognised_text:
                self.input_text.insert("1.0", recognised_text)
                self.translate_gui()
            else:
                self.input_text.insert("1.0", "Could not understand, Try speaking again")
        threading.Thread(target=run_stt, daemon=True).start()

    #text-to-speech
    def speak_translation(self):
        text_to_speak = self.output_text.get("1.0", "end-1c")
        if not text_to_speak.strip() or "Please enter text" in text_to_speak:
            return
        target_lang_code = self.language_options[self.target_language_var.get()]
        def run_tts():
            text_to_speech(text_to_speak, language=target_lang_code)
        threading.Thread(target=run_tts, daemon=True).start()

    #speech to speech
    def record_and_speak(self):
        self.input_text.delete("1.0", "end")
        self.input_text.insert("1.0", "Listening...")
        self.update()
        def run_stt_tts():
            recognized_text = speech_to_text()
            self.input_text.delete("1.0", "end")
            if recognized_text:
                self.input_text.insert("1.0", recognized_text)
                target_lang_code = self.language_options[self.target_language_var.get()]
                translated_text = translate_text(recognized_text, target_lang_code)
                self.output_text.delete("1.0", "end")
                self.output_text.insert("1.0", translated_text)
                if translated_text:
                    text_to_speech(translated_text, language=target_lang_code)
            else:
                self.input_text.insert("1.0", "Could not understand audio. Please try again.")

        threading.Thread(target=run_stt_tts, daemon=True).start()
    
    #exit app
    def exit_app(self):
        self.destroy()
    
    def clear_all_text(self):
        self.input_text.delete("1.0", "end")
        self.output_text.delete("1.0", "end")

    #swap language code
    #swap language code
    def swap_languages(self):
        input_content = self.input_text.get("1.0", "end-1c")
        output_content = self.output_text.get("1.0", "end-1c")
        
        # Swap language labels
        source_lang_name = self.source_language_var.get()
        target_lang_name = self.target_language_var.get()

        self.source_language_var.set(target_lang_name)
        self.target_language_var.set(source_lang_name)

        # Update language labels above textboxes
        self.input_lang_label.configure(text=target_lang_name)
        self.output_lang_label.configure(text=source_lang_name)
        
        # Swap text content
        self.input_text.delete("1.0", "end")
        self.input_text.insert("1.0", output_content)

        self.output_text.delete("1.0", "end")
        self.output_text.insert("1.0", input_content)

    #update language label
    def update_output_lang_label(self, language_name):
        self.output_lang_label.configure(text=language_name)

    #update input language label
    def update_input_lang_label(self, language_name):
        self.input_lang_label.configure(text=language_name)

    #main class
    def __init__(self):
        super().__init__()

        # window
        self.title("Real Time Language Translator")
        self.geometry("1000x700")
        self.minsize(900, 620) 
        self.configure(fg_color="#1B212B")
        self.iconbitmap("app_logo.ico")

        # PRAMAHA Logo
        pramaha_logo_image = Image.open("pramaha_logo.png") # Make sure the file is in PNG format
        pramaha_logo = ctk.CTkImage(light_image=pramaha_logo_image, dark_image=pramaha_logo_image, size=(200, 50))
        self.pramaha_logo_label = ctk.CTkLabel(self, image=pramaha_logo, text="")
        self.pramaha_logo_label.place(x=15, y=16)

        #title
        self.title_label = ctk.CTkLabel(
            self,
            text="PRAMAHA TRANSLATE",
            font=ctk.CTkFont(family="Poppins",size=25, weight="bold"),
            text_color="#ffffff"
        )
        self.title_label.pack(pady=25)

        #main frame
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.pack(fill = "x", expand=True, padx=15, pady=10)
        self.main_frame.grid_columnconfigure((0,2), weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)

        # language options
        self.language_options = {
            "Spanish": "es", "French": "fr", "German": "de", "Chinese": "zh-cn", "Japanese": "ja", "Hindi": "hi", "Telugu": "te", "English": "en-US"
        }

        # source language dropdown menu
        self.source_lang_label_title = ctk.CTkLabel(self.main_frame, text="Source Language", font=ctk.CTkFont(family="Poppins", size=16, weight="bold"), text_color="#ffffff")
        self.source_lang_label_title.grid(row=0, column=0, pady=(0,5), sticky="s")
        self.source_language_var = ctk.StringVar(value="English")
        self.source_language_menu = ctk.CTkOptionMenu(
            self.main_frame,
            values=list(self.language_options.keys()),
            variable=self.source_language_var,
            command=self.update_input_lang_label,
            fg_color="#121318",
            button_color="#121318",
            button_hover_color="#2A2B30",
            dropdown_fg_color="#121318",
            text_color="#ffffff",
            font=ctk.CTkFont(family="Poppins", size=17),
            anchor="center",
            height=50,
            corner_radius=25
        )
        self.source_language_menu.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 10))

        # target language dropdown menu
        self.target_lang_label_title = ctk.CTkLabel(self.main_frame, text="Target Language", font=ctk.CTkFont(family="Poppins", size=16, weight="bold"), text_color="#ffffff")
        self.target_lang_label_title.grid(row=0, column=2, pady=(0,5), sticky="s")
        self.target_language_var = ctk.StringVar(value="Choose the Language")
        self.target_language_menu = ctk.CTkOptionMenu(
            self.main_frame,
            values=list(self.language_options.keys()),
            variable=self.target_language_var,
            command=self.update_output_lang_label,
            fg_color="#121318",
            button_color="#121318",
            button_hover_color="#2A2B30",
            dropdown_fg_color="#121318",
            text_color="#ffffff",
            font=ctk.CTkFont(family="Poppins", size=17),
            anchor="center",
            height=50,
            corner_radius=25
        )
        self.target_language_menu.grid(row=1, column=2, sticky="ew", padx=10, pady=(0, 10))

        #input box
        self.input_frame = ctk.CTkFrame(self.main_frame, fg_color="#121318", corner_radius=25)
        self.input_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)
        self.input_frame.grid_rowconfigure(1, weight=1)
        self.input_frame.grid_columnconfigure(0, weight=1)

        self.input_lang_label = ctk.CTkLabel(self.input_frame, text="English", font=ctk.CTkFont(family="Poppins Light", size=16), text_color="#b4b4dd", anchor="center")
        self.input_lang_label.grid(row=0, column=0, padx=10, pady=(10, 5))

        self.input_text = ctk.CTkTextbox(self.input_frame, wrap="word", fg_color="transparent", text_color="#ffffff", font=ctk.CTkFont(family="Poppins", size=15, weight="bold"), border_width=0)
        self.input_text.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")
        self.input_text.insert("1.0", "Enter the text to translate!")

         # Output Text Box
        self.output_frame = ctk.CTkFrame(self.main_frame, fg_color="#121318", corner_radius=25)
        self.output_frame.grid(row=2, column=2, sticky="nsew", padx=10, pady=10)
        self.output_frame.grid_rowconfigure(1, weight=1)
        self.output_frame.grid_columnconfigure(0, weight=1)

        self.output_lang_label = ctk.CTkLabel(self.output_frame, text="Choose the Language", font=ctk.CTkFont(family="Poppins Light", size=16), text_color="#b4b4dd", anchor="center")
        self.output_lang_label.grid(row=0, column=0, padx=10, pady=(10, 5))

        self.output_text = ctk.CTkTextbox(self.output_frame, wrap="word", fg_color="transparent", text_color="#ffffff", font=ctk.CTkFont(family="Poppins", size=15, weight="bold"), border_width=0)
        self.output_text.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")
        self.output_text.insert("1.0", "Translated Text will appear here!")

        #swap button
        swap_icon_image = Image.open("swap_icon.png")
        swap_icon = ctk.CTkImage(light_image=swap_icon_image, dark_image=swap_icon_image, size=(40, 40))
        self.swap_button = ctk.CTkButton(self.main_frame, image=swap_icon, text="", width=40, height=40, command=self.swap_languages, fg_color="transparent", hover_color="#000015")
        self.swap_button.grid(row=2, column=1, padx=10)

        self.options_label = ctk.CTkLabel(
            self,
            text="Select the Mode",
            font=ctk.CTkFont(family="Poppins", size=18, weight="bold"),
            text_color="#ffffff"
        )
        self.options_label.pack(pady=(20, 5))

        #button frame for action-buttons
        self.button_frame=ctk.CTkFrame(self, fg_color="transparent")
        self.button_frame.pack(fill="x", padx=15, pady=10)
        self.button_frame.grid_columnconfigure((0, 1, 2, 3, 4, 5), weight=1)

        self.translate_button=ctk.CTkButton(self.button_frame, text="Translate", command=self.translate_gui, height=50, font=ctk.CTkFont(family="Poppins", size=14, weight="bold"), corner_radius=20, fg_color="#121318", hover_color="#6868D8", width=105)
        self.translate_button.grid(row=0, column=0, padx=10, pady=(0,15), sticky="ew")

        self.record_button=ctk.CTkButton(self.button_frame, text="Speech to Text", command=self.record_and_translate, height=50, font=ctk.CTkFont(family="Poppins", size=14, weight="bold"), corner_radius=20, fg_color="#121318", hover_color="#6868D8")
        self.record_button.grid(row=0, column=1, padx=5, pady=(0,15), sticky="ew")

        self.speak_button=ctk.CTkButton(self.button_frame, text="Text to Speech", command=self.speak_translation, height=50, font=ctk.CTkFont(family="Poppins", size=14, weight="bold"), corner_radius=20, fg_color="#121318", hover_color="#6868D8")
        self.speak_button.grid(row=0, column=2, padx=5, pady=(0,15), sticky="ew")

        self.trans_button=ctk.CTkButton(self.button_frame, text="Speech to Speech", command=self.record_and_speak, height=50, font=ctk.CTkFont(family="Poppins", size=14, weight="bold"), corner_radius=20, fg_color="#121318", hover_color="#6868D8")
        self.trans_button.grid(row=0, column=3, padx=5, pady=(0,15), sticky="ew")

        self.clear_button=ctk.CTkButton(self.button_frame, text="Clear Text", command=self.clear_all_text, height=50, font=ctk.CTkFont(family="Poppins", size=14, weight="bold"), corner_radius=20, fg_color="#121318", hover_color="#CB8F4A", width=105)
        self.clear_button.grid(row=0, column=4, padx=5, pady=(0,15), sticky="ew")

        self.exit_button=ctk.CTkButton(self.button_frame, text="Exit", command=self.exit_app, height=50, font=ctk.CTkFont(family="Poppins", size=14, weight="bold"), corner_radius=20, fg_color="#121318", hover_color="#D95555", width=75)
        self.exit_button.grid(row=0, column=5, padx=5, pady=(0,15), sticky="ew")
        

if __name__ == "__main__":
    app = TranslatorApp()
    app.mainloop()