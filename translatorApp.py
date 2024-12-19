import tkinter as tk
from tkinter import ttk, scrolledtext
from googletrans import Translator, LANGUAGES
import threading
import speech_recognition as sr
import pyttsx3
import json
import os
from datetime import datetime

class TranslatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("✨ Universal Translator")
        
        # Configure window size and position
        window_width = 1000
        window_height = 700
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        center_x = int(screen_width/2 - window_width/2)
        center_y = int(screen_height/2 - window_height/2)
        self.root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        
        # Modern color scheme
        self.colors = {
            'bg_primary': "#1C2833",      # Deep Navy
            'bg_secondary': "#2C3E50",    # Dark Blue Gray
            'accent': "#5DADE2",          # Sky Blue
            'accent_2': "#F1C40F",        # Lemon Yellow
            'text_light': "#ECF0F1",      # Light Gray
            'text_dark': "#2C3E50"        # Dark Blue Gray
        }
        
        self.root.configure(bg=self.colors['bg_primary'])
        
        # Initialize translator
        self.translator = Translator(service_urls=['translate.google.com'])
        
        # Style configuration
        self.style = ttk.Style()
        self.style.configure('Custom.TCombobox',
                           background=self.colors['bg_secondary'],
                           fieldbackground=self.colors['bg_secondary'],
                           foreground=self.colors['text_light'],
                           arrowcolor=self.colors['accent_2'])
        
        # Add padding at the top
        top_padding = tk.Frame(root, height=40, bg=self.colors['bg_primary'])
        top_padding.pack(fill=tk.X)

        # Title with modern styling
        title_frame = tk.Frame(root, bg=self.colors['bg_primary'])
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        title = tk.Label(title_frame,
                        text="🌐 Universal Translator 🌐",
                        font=("Montserrat", 32, "bold"),
                        bg=self.colors['bg_primary'],
                        fg=self.colors['accent_2'])
        title.pack()
        
        subtitle = tk.Label(title_frame,
                          text="Breaking Language Barriers",
                          font=("Montserrat", 14),
                          bg=self.colors['bg_primary'],
                          fg=self.colors['accent'])
        subtitle.pack()

        # Container frame
        container = tk.Frame(root, bg=self.colors['bg_primary'], padx=40, pady=20)
        container.pack(fill=tk.BOTH, expand=True)

        # Language selection frame
        lang_frame = tk.Frame(container, bg=self.colors['bg_primary'])
        lang_frame.pack(fill=tk.X, pady=(0, 15))

        # Add source_lang_var initialization
        self.source_lang_var = tk.StringVar(value="Auto-Detect")
        
        # From label and detection
        self.detected_lang_label = tk.Label(lang_frame,
                                          text="Detected Language: Auto",
                                          bg=self.colors['bg_primary'],
                                          fg=self.colors['accent'],
                                          font=("Montserrat", 12))
        self.detected_lang_label.pack(side=tk.LEFT)

        # Swap button with hover effects
        self.swap_btn = tk.Button(lang_frame,
                                text="🔄",
                                command=self.swap_languages,
                                bg=self.colors['bg_secondary'],
                                fg=self.colors['accent_2'],
                                font=("Montserrat", 14),
                                relief=tk.FLAT,
                                borderwidth=0,
                                padx=15,
                                pady=5)
        self.swap_btn.pack(side=tk.LEFT, padx=20)
        self._add_hover_effect(self.swap_btn)

        # To label and combobox
        to_label = tk.Label(lang_frame,
                          text="To:",
                          bg=self.colors['bg_primary'],
                          fg=self.colors['text_light'],
                          font=("Montserrat", 12))
        to_label.pack(side=tk.LEFT, padx=(10, 5))

        self.target_lang_var = tk.StringVar()
        target_combo = ttk.Combobox(lang_frame,
                                  textvariable=self.target_lang_var,
                                  values=sorted(LANGUAGES.values()),
                                  style='Custom.TCombobox',
                                  width=20)
        target_combo.pack(side=tk.LEFT)

        # Text areas frame
        text_frame = tk.Frame(container, bg=self.colors['bg_primary'])
        text_frame.pack(fill=tk.BOTH, expand=True)

        # Text areas with improved wrapping and spacing
        # Source text area
        self.source_text = scrolledtext.ScrolledText(
            text_frame,
            wrap=tk.WORD,  # Ensure word wrapping (not character wrapping)
            width=30,
            height=10,
            font=("Poppins", 13),
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_light'],
            insertbackground=self.colors['text_light'],
            padx=25,        # Increased horizontal padding
            pady=20,        # Increased vertical padding
            relief=tk.FLAT,
            borderwidth=0,
            spacing1=5,     # Space between lines
            spacing2=2,     # Space between paragraphs
            spacing3=5      # Space before paragraphs
        )
        self.source_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        self.source_text.insert("1.0", "\n")  # Top margin
        
        # Target text area
        self.target_text = scrolledtext.ScrolledText(
            text_frame,
            wrap=tk.WORD,  # Ensure word wrapping (not character wrapping)
            width=30,
            height=10,
            font=("Poppins", 13),
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_light'],
            insertbackground=self.colors['text_light'],
            padx=25,        # Increased horizontal padding
            pady=20,        # Increased vertical padding
            relief=tk.FLAT,
            borderwidth=0,
            spacing1=5,     # Space between lines
            spacing2=2,     # Space between paragraphs
            spacing3=5      # Space before paragraphs
        )
        self.target_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.target_text.insert("1.0", "\n")  # Top margin

        # Translate button frame
        btn_frame = tk.Frame(container, bg=self.colors['bg_primary'])
        btn_frame.pack(fill=tk.X, pady=(20, 0))

        # Modern translate button
        self.translate_btn = tk.Button(
            btn_frame,
            text="Translate ✨",
            command=self.translate,
            bg=self.colors['accent'],
            fg=self.colors['text_light'],
            font=("Montserrat", 14, "bold"),
            relief=tk.FLAT,
            borderwidth=0,
            padx=30,
            pady=10
        )
        self.translate_btn.pack()
        self._add_hover_effect(self.translate_btn, is_translate_btn=True)

        # Status label
        self.status_label = tk.Label(
            btn_frame,
            text="Ready to translate",
            bg=self.colors['bg_primary'],
            fg=self.colors['accent'],
            font=("Montserrat", 10)
        )
        self.status_label.pack(pady=(5, 0))

        # Add history and favorites storage
        self.history = []
        self.favorites = set()
        self.load_saved_data()
        
        # Add character count label
        self.char_count_source = tk.Label(
            container,
            text="Characters: 0/5000",
            bg=self.colors['bg_primary'],
            fg=self.colors['text_light'],
            font=("Montserrat", 10)
        )
        self.char_count_source.pack(pady=(5, 0))
        
        # Add loading animation label
        self.loading_label = tk.Label(
            btn_frame,
            text="",
            bg=self.colors['bg_primary'],
            fg=self.colors['accent_2'],
            font=("Montserrat", 12)
        )
        self.loading_label.pack()
        
        # Modify keyboard shortcuts (remove copy shortcut)
        self.root.bind('<Control-Return>', lambda e: self.translate())
        self.root.bind('<Control-l>', lambda e: self.toggle_theme())
        
        # Add theme toggle button
        self.theme_btn = tk.Button(
            title_frame,
            text="🌙",
            command=self.toggle_theme,
            bg=self.colors['bg_primary'],
            fg=self.colors['accent_2'],
            font=("Montserrat", 12),
            relief=tk.FLAT,
            padx=10
        )
        self.theme_btn.pack(side=tk.RIGHT, padx=10)
        
        # Bind text change events for character count
        self.source_text.bind('<KeyRelease>', self.update_char_count)

        # Initialize speech components
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        
        # Add voice control buttons frame
        voice_frame = tk.Frame(container, bg=self.colors['bg_primary'])
        voice_frame.pack(fill=tk.X, pady=5)
        
        # Voice input button
        self.voice_input_btn = tk.Button(
            voice_frame,
            text="🎤 Speak",
            command=self.start_voice_input,
            bg=self.colors['bg_secondary'],
            fg=self.colors['accent_2'],
            font=("Montserrat", 12),
            relief=tk.FLAT,
            padx=15
        )
        self.voice_input_btn.pack(side=tk.LEFT, padx=5)
        
        # Text-to-Speech button
        self.tts_btn = tk.Button(
            voice_frame,
            text="🔊 Listen",
            command=self.speak_translation,
            bg=self.colors['bg_secondary'],
            fg=self.colors['accent_2'],
            font=("Montserrat", 12),
            relief=tk.FLAT,
            padx=15
        )
        self.tts_btn.pack(side=tk.RIGHT, padx=5)

        # Add hover effects to buttons
        for btn in [self.voice_input_btn, self.tts_btn]:
            self._add_hover_effect(btn)

    def _add_hover_effect(self, button, is_translate_btn=False):
        """Add hover effect to buttons"""
        if is_translate_btn:
            button.bind('<Enter>', 
                       lambda e: button.config(
                           bg=self.colors['accent_2'],
                           fg=self.colors['text_dark']))
            button.bind('<Leave>', 
                       lambda e: button.config(
                           bg=self.colors['accent'],
                           fg=self.colors['text_light']))
        else:
            button.bind('<Enter>', 
                       lambda e: button.config(
                           bg=self.colors['accent'],
                           fg=self.colors['text_light']))
            button.bind('<Leave>', 
                       lambda e: button.config(
                           bg=self.colors['bg_secondary'],
                           fg=self.colors['accent_2']))

    def get_language_code(self, language_name):
        """Convert language name to language code"""
        for code, name in LANGUAGES.items():
            if name.lower() == language_name.lower():
                return code
        return None

    def swap_languages(self):
        """Swap source and target languages"""
        if self.source_lang_var.get() != "Auto-Detect":
            source = self.source_lang_var.get()
            target = self.target_lang_var.get()
            self.source_lang_var.set(target)
            self.target_lang_var.set(source)
            
            # Also swap the text
            source_text = self.source_text.get("1.0", tk.END).strip()
            target_text = self.target_text.get("1.0", tk.END).strip()
            self.source_text.delete("1.0", tk.END)
            self.target_text.delete("1.0", tk.END)
            self.source_text.insert("1.0", target_text)
            self.target_text.insert("1.0", source_text)

    def translate(self):
        """Override translate method to add new features"""
        self.translate_btn.config(state=tk.DISABLED)
        self.show_loading_animation()
        self.play_sound("translate")
        
        # Get all text including first line if it contains overflow
        text = self.source_text.get("2.0", tk.END).strip()
        # Check if there's any text in the first line (overflow)
        first_line = self.source_text.get("1.0", "2.0").strip()
        if first_line:
            text = first_line + text
        
        if not text:
            self.status_label.config(text="Please enter some text to translate")
            self.translate_btn.config(state=tk.NORMAL)
            return
        
        # Start translation in a separate thread
        thread = threading.Thread(target=self._translate_thread, args=(text,))
        thread.start()

    def _translate_thread(self, text):
        """Handle the translation process"""
        try:
            source_lang = "auto" if self.source_lang_var.get() == "Auto-Detect" \
                else self.get_language_code(self.source_lang_var.get())
            target_lang = self.get_language_code(self.target_lang_var.get())

            # Perform translation
            result = self.translator.translate(text,
                                            src=source_lang,
                                            dest=target_lang)

            # Update UI in the main thread
            self.root.after(0, self._update_translation_result, result)
            
        except Exception as e:
            self.root.after(0, self._update_error, str(e))
        finally:
            self.root.after(0, self._enable_translate_button)

    def _update_translation_result(self, result):
        """Update the translation result in the UI"""
        self.target_text.delete("1.0", tk.END)
        # Add initial newline for margin
        self.target_text.insert("1.0", "\n")
        # Insert translated text after the margin
        self.target_text.insert("2.0", result.text)
        
        if result.src != 'auto':
            detected_lang = LANGUAGES.get(result.src, 'unknown').title()
            self.status_label.config(text=f"Detected language: {detected_lang}")
        else:
            self.status_label.config(text="Translation complete!")

    def _update_error(self, error_msg):
        """Update error message in the UI"""
        self.status_label.config(text=f"Error: {error_msg}")

    def _enable_translate_button(self):
        """Re-enable the translate button"""
        self.translate_btn.config(state=tk.NORMAL)

    def on_text_change(self, event=None):
        """Handle text changes and maintain the top margin"""
        # Ensure first line is always empty for margin
        first_line = self.source_text.get("1.0", "2.0").strip()
        if not self.source_text.get("1.0", "2.0").startswith("\n"):
            self.source_text.insert("1.0", "\n")
        
        # Get text for language detection
        text = self.source_text.get("1.0", tk.END).strip()
        if text:
            try:
                detected = self.translator.detect(text)
                detected_lang = LANGUAGES.get(detected.lang, 'unknown').title()
                self.detected_lang_label.config(
                    text=f"Detected Language: {detected_lang}"
                )
            except:
                pass

    def load_saved_data(self):
        """Load translation history and favorites"""
        try:
            with open('translator_data.json', 'r') as f:
                data = json.load(f)
                self.history = data.get('history', [])
                self.favorites = set(data.get('favorites', []))
        except FileNotFoundError:
            pass

    def save_data(self):
        """Save translation history and favorites"""
        with open('translator_data.json', 'w') as f:
            json.dump({
                'history': self.history[-10:],  # Keep last 10 translations
                'favorites': list(self.favorites)
            }, f)

    def update_char_count(self, event=None):
        """Update character count label"""
        text = self.source_text.get("1.0", tk.END).strip()
        count = len(text)
        self.char_count_source.config(
            text=f"Characters: {count}/5000",
            fg=self.colors['accent'] if count <= 5000 else "red"
        )

    def toggle_theme(self):
        """Toggle between light and dark theme"""
        if self.colors['bg_primary'] == "#1C2833":  # Dark theme
            self.colors.update({
                'bg_primary': "#FFFFFF",
                'bg_secondary': "#F5F5F5",
                'text_light': "#2C3E50",
                'text_dark': "#1C2833"
            })
            self.theme_btn.config(text="☀️")
        else:  # Light theme
            self.colors.update({
                'bg_primary': "#1C2833",
                'bg_secondary': "#2C3E50",
                'text_light': "#ECF0F1",
                'text_dark': "#2C3E50"
            })
            self.theme_btn.config(text="🌙")
        
        self.apply_theme()

    def apply_theme(self):
        """Apply current theme to all widgets"""
        self.root.configure(bg=self.colors['bg_primary'])
        # Update all widgets with new colors
        # ... (update all widgets with new theme colors)

    def play_sound(self, action):
        """Play sound effects"""
        sounds = {
            'copy': 'sounds/copy.wav',
            'translate': 'sounds/translate.wav',
            'error': 'sounds/error.wav'
        }
        try:
            if os.path.exists(sounds[action]):
                threading.Thread(target=playsound, args=(sounds[action],)).start()
        except:
            pass

    def show_loading_animation(self):
        """Show loading animation during translation"""
        chars = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
        def animate():
            for char in chars:
                if self.translate_btn['state'] == tk.DISABLED:
                    self.loading_label.config(text=f"Translating {char}")
                    self.root.after(100)
                    self.root.update()
                else:
                    self.loading_label.config(text="")
                    break
        threading.Thread(target=animate).start()

    def start_voice_input(self):
        """Handle voice input"""
        self.status_label.config(text="🎤 Listening... Speak now")
        self.voice_input_btn.config(state=tk.DISABLED)
        
        def listen():
            try:
                with sr.Microphone() as source:
                    self.recognizer.adjust_for_ambient_noise(source)
                    audio = self.recognizer.listen(source, timeout=5)
                    text = self.recognizer.recognize_google(audio)
                    
                    # Update UI in main thread
                    self.root.after(0, self._update_voice_input, text)
                    
            except sr.WaitTimeoutError:
                self.root.after(0, self.status_label.config, 
                              {"text": "No speech detected. Please try again."})
            except sr.RequestError:
                self.root.after(0, self.status_label.config, 
                              {"text": "Could not connect to speech service."})
            except Exception as e:
                self.root.after(0, self.status_label.config, 
                              {"text": f"Error: {str(e)}"})
            finally:
                self.root.after(0, self.voice_input_btn.config, {"state": tk.NORMAL})
        
        threading.Thread(target=listen).start()

    def _update_voice_input(self, text):
        """Update the source text with voice input"""
        self.source_text.delete("1.0", tk.END)
        self.source_text.insert("1.0", "\n" + text)
        self.status_label.config(text="✨ Voice input received!")
        self.translate()  # Auto-translate after voice input

    def speak_translation(self):
        """Convert translation to speech"""
        text = self.target_text.get("2.0", tk.END).strip()
        if text:
            self.status_label.config(text="🔊 Playing audio...")
            self.tts_btn.config(state=tk.DISABLED)
            
            def speak():
                try:
                    self.engine.say(text)
                    self.engine.runAndWait()
                    self.root.after(0, self.status_label.config, 
                                  {"text": "Audio playback complete!"})
                except Exception as e:
                    self.root.after(0, self.status_label.config, 
                                  {"text": f"Audio Error: {str(e)}"})
                finally:
                    self.root.after(0, self.tts_btn.config, {"state": tk.NORMAL})
            
            threading.Thread(target=speak).start()

def main():
    root = tk.Tk()
    app = TranslatorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
