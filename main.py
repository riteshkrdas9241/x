import tkinter as tk
from input import input_data
from memory import MemoryRecorder
from skills.websearch import search_google, search_youtube, open_website
import os, sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


# Import skills from your separate files in skills/
from skills.websearch import search_google, search_youtube
from skills.systemtools import tell_time, tell_date, open_app


class AssistantMain:

    def __init__(self):
        print("[Main]: Booting Memory Recorder...")
        self.recorder = MemoryRecorder()

        # Map trigger phrases to functions from your external skill files
        # (Order matters: put more specific phrases like "youtube" before general ones like "search")
        self.skills = [
            ("open youtube", open_website),
            ("open steamrip", open_website),   # <-- MUST be ABOVE ("open ", open_app)!
            ("open fmhy", open_website),
            ("youtube", search_youtube),
            ("play ", search_youtube),
            ("search", search_google),
            ("google", search_google),
            ("what time", tell_time),
            ("current time", tell_time),
            ("what date", tell_date),
            ("today's date", tell_date),
            ("open ", open_app),               # <-- General "open " comes AFTER specific websites
            ("launch ", open_app),
        ]


    def process_pipeline(self, text, source):
        """
        Central workflow for every voice or typed input:
        1. Save into daily tasks/ or chats/ via recorder.py
        2. Check if any external file in skills/ should execute an action
        """
        # Step 1: Record memory
        self.recorder.record_input(text, source)

        # Step 2: Execute matching skill
        lower_text = text.lower().strip()
        for trigger, skill_function in self.skills:
            if trigger in lower_text:
                skill_function(text)
                break


if __name__ == "__main__":
    assistant = AssistantMain()

    print("[Main]: Opening Voice & Keyboard Window...")
    root = tk.Tk()
    app = input_data(root, on_input_callback=assistant.process_pipeline)
    root.mainloop()
