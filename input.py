import threading
import tkinter as tk
import speech_recognition as sr


class input_data:
    
    
    def __init__(self, root, on_input_callback=None):
        self.root = root
        self.on_input_callback = on_input_callback
        self.root.title("Voice & Keyboard Notepad")
        self.root.geometry("500x400")

        # Text window where both typed and spoken text appear
        self.text_area = tk.Text(root, font=("Arial", 14), wrap=tk.WORD)
        self.text_area.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        # Trigger terminal printing whenever you type a key
        self.text_area.bind("<Return>", self.on_enter_pressed)

        # Status label to show when the mic is listening
        self.status_label = tk.Label(
            root, text="Ready (Type above or click Speak)", fg="gray"
        )
        self.status_label.pack(pady=(0, 5))

        # Button to trigger voice recognition
        self.speak_btn = tk.Button(
            root,
            text="🎤 Speak",
            font=("Arial", 12, "bold"),
            command=self.start_listening_thread,
        )
        self.speak_btn.pack(pady=(0, 10))

        self.start_listening_thread()


    def on_enter_pressed(self, event):
        # Grab the entire line where the cursor currently is
        typed_line = self.text_area.get("insert linestart", "insert lineend").strip()
        if typed_line:
            self.handle_command(typed_line, "Typed")

    def start_listening_thread(self):
        self.speak_btn.config(state=tk.DISABLED)
        self.status_label.config(text="Listening... Speak now", fg="red")
        threading.Thread(target=self.recognize_voice, daemon=True).start()

    def recognize_voice(self):
        recognizer = sr.Recognizer()
        recognizer.energy_threshold = 300  # Fixes mic not picking up quiet speech
        recognizer.dynamic_energy_threshold = False

        # If your real mic is index 1 or 2 from the list command, put sr.Microphone(device_index=1)
        with sr.Microphone(device_index=1) as source:
            print("[Status]: Continuous listening active. Speak or type anytime!")
            while True:
                try:
                    self.root.after(0, lambda: self.status_label.config(text="Listening continuously...", fg="red"))
                    audio = recognizer.listen(source, phrase_time_limit=10)
                    
                    self.root.after(0, lambda: self.status_label.config(text="Processing...", fg="blue"))
                    spoken_text = recognizer.recognize_google(audio)
                    # Only activate if the wake word "lewis" is spoken
                    if "lewis" in spoken_text.lower():
                        # Strip the wake word "lewis" (and common mishearings like "louis") out of the command
                        clean_command = (
                            spoken_text.lower()
                            .replace("lewis", "")
                            .replace("louis", "")
                            .strip(" ,.-")
                        )
                        if clean_command:
                            self.handle_command(clean_command, "Voice")
                        else:
                            print("[Wake Word]: Lewis is awake! Say your command.")
                    else:
                        print("[Ignored]: Wake word 'Lewis' not detected.")
                    
                   
                except sr.UnknownValueError:
                    # Print in terminal so you know it heard sound, just couldn't make out words
                    print("[Status]: Heard noise, couldn't understand words.")
                except sr.RequestError as e:
                    print(f"[Error]: Google API unreachable: {e}")
                except Exception as e:
                    print(f"[Mic Error]: {e}")

    def insert_text(self, text):
        self.text_area.insert(tk.INSERT, text)
        self.text_area.see(tk.END)

    def handle_command(self, text, source_type):
        clean_text = text.lower().strip()
        print(f"[{source_type}]: {text}")

        if clean_text == "clear screen":
            self.root.after(0, lambda: self.text_area.delete("1.0", tk.END))
            print("[Command]: Screen cleared")

        elif clean_text == "new line":
            self.root.after(0, self.insert_text, "\n")
            print("[Command]: New line added")

        elif clean_text == "exit app":
            print("[Command]: Closing app...")
            self.root.after(0, self.root.destroy)

        else:
            # Only insert into window if it came from Voice (typing is already in the window)
            if source_type == "Voice":
                self.root.after(0, self.insert_text, text + " ")
            if self.on_input_callback:
                self.on_input_callback(text, source_type)
    

if __name__ == "__main__":
    root = tk.Tk()
    app = input_data(root)
    root.mainloop()
