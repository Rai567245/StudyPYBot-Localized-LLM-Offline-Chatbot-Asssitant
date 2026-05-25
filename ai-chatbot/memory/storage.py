import json
import os
from tkinter import filedialog, messagebox

class ChatStorage:
    def __init__(self, file_path="projects/python-macro-projects/ai-chatbot/data/conversations.json"):
        self.file_path = file_path
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

    def load_history(self):
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, "r") as f:
                    return json.load(f)
            except (json.JSONDecodeError, ValueError):
                return []
        return []

    def get_recent_history(self, limit=3):
        history_data = self.load_history()
        context = ""
        for entry in history_data[-limit:]:
            context += f"User: {entry['user']}\nAssistant: {entry['bot']}\n"
        return context

    def save_chat(self, user_msg, bot_msg):
        history = self.load_history()
        history.append({"user": user_msg, "bot": bot_msg})
        with open(self.file_path, "w") as f:
            json.dump(history, f, indent=4)

    def export_to_txt(self):
        history = self.load_history()
        if not history:
            messagebox.showwarning("Empty", "No history to save.")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt")],
            title="Save Study Guide"
        )

        if file_path:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write("=== StudyPYBot: Python Study Guide ===\n\n")
                for entry in history:
                    f.write(f"Question: {entry['user']}\nAnswer:\n{entry['bot']}\n")
                    f.write("-" * 30 + "\n")
            messagebox.showinfo("Saved", "Study guide exported successfully!")
            
    def save_history(self, history_data):
        """Overwrites the entire conversation file with the provided history list."""
        try:
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(history_data, f, indent=4)
        except Exception as e:
            print(f"Error saving history: {e}")