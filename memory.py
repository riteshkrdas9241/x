import json
import os
import re
from datetime import datetime
import tkinter as tk
from input import input_data

TASKS_DIR = "tasks"
CHATS_DIR = "chats"

TASK_KEYWORDS = (
    "task", "remind", "todo", "to do", "need to", "have to",
    "must", "finish", "complete", "submit", "buy", "call",
    "schedule", "meeting", "deadline", "work on"
)

FILLER_WORDS = {
    "um", "uh", "like", "you know", "basically", "actually",
    "literally", "just", "maybe", "kind of", "sort of", "i think", "so"
}


class MemoryRecorder:

    def __init__(self):
        os.makedirs(TASKS_DIR, exist_ok=True)
        os.makedirs(CHATS_DIR, exist_ok=True)

    def get_daily_files(self):
        """Returns today's two permanent file paths: (tasks_path, chats_path)."""
        today_str = datetime.now().strftime("%Y-%m-%d")
        tasks_path = os.path.join(TASKS_DIR, f"{today_str}_tasks.json")
        chats_path = os.path.join(CHATS_DIR, f"{today_str}_chats.json")
        return tasks_path, chats_path

    def load_json(self, filepath):
        if not os.path.exists(filepath):
            return []
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []

    def save_json(self, filepath, data):
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def is_task(self, text):
        lower_text = text.lower()
        return any(keyword in lower_text for keyword in TASK_KEYWORDS)

    def summarize_chat(self, text):
        """Summarizes casual talk/notes so chats stay compact for interaction modeling."""
        cleaned = text.strip()
        for filler in FILLER_WORDS:
            cleaned = re.sub(rf"\b{re.escape(filler)}\b", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"\s+", " ", cleaned).strip(" ,.-")
        if len(cleaned) > 80:
            cleaned = cleaned[:77].rstrip() + "..."
        return cleaned if cleaned else text.strip()

    def record_input(self, text, source):
        now = datetime.now()
        tasks_file, chats_file = self.get_daily_files()

        if self.is_task(text):
            # 1. Store exact task permanently in today's tasks file (for Work Pattern Recognition)
            tasks = self.load_json(tasks_file)
            entry = {
                "id": len(tasks) + 1,
                "time": now.strftime("%H:%M:%S"),
                "day": now.strftime("%A"),
                "hour": now.hour,
                "how": source,  # "Voice" or "Typed"
                "exact_task": text.strip(),
                "status": "pending"
            }
            tasks.append(entry)
            self.save_json(tasks_file, tasks)
            print(f"[Work Memory -> {tasks_file}]: {entry['exact_task']}")

        else:
            # 2. Store summarized chat permanently in today's chats file (for Human Interaction Building)
            chats = self.load_json(chats_file)
            entry = {
                "id": len(chats) + 1,
                "time": now.strftime("%H:%M:%S"),
                "day": now.strftime("%A"),
                "hour": now.hour,
                "how": source,  # "Voice" or "Typed"
                "summary": self.summarize_chat(text)
            }
            chats.append(entry)
            self.save_json(chats_file, chats)
            print(f"[Chat Memory -> {chats_file}]: {entry['summary']}")


if __name__ == "__main__":
    recorder = MemoryRecorder()
    root = tk.Tk()
    app = input_data(root, on_input_callback=recorder.record_input)
    root.mainloop()
