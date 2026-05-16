import os
import tkinter as tk
from tkinter import scrolledtext
import threading
from ai_agent import EnergyAgent
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.environ["GOOGLE_API_KEY"]
CSV_PATH = "data/energy_data.csv"


class ChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("EnergyData Assistant")
        self.root.geometry("600x500")
        self.agent = EnergyAgent(csv_path=CSV_PATH, api_key=API_KEY)
        self.setup_ui()

    def setup_ui(self):
        self.chat_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, state='disabled', font=("Arial", 11))
        self.chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        input_frame = tk.Frame(self.root)
        input_frame.pack(fill=tk.X, padx=10, pady=(0, 10))

        self.entry_box = tk.Entry(input_frame, font=("Arial", 12))
        self.entry_box.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.entry_box.bind("<Return>", lambda event: self.process_query())

        self.send_btn = tk.Button(input_frame, text="Send", bg="#4CAF50", fg="white", font=("Arial", 11, "bold"),
                                  command=self.process_query)
        self.send_btn.pack(side=tk.RIGHT)

        self.append_to_chat("System", "Welcome! I am your AI energy assistant. Ask me anything about your dataset.\n")

    def process_query(self):
        user_text = self.entry_box.get().strip()
        if not user_text:
            return

        self.entry_box.delete(0, tk.END)

        self.append_to_chat("You", user_text)
        self.append_to_chat("System", "Analyzing data, please wait...")

        self.send_btn.config(state=tk.DISABLED)
        self.entry_box.config(state=tk.DISABLED)

        threading.Thread(target=self.fetch_ai_response, args=(user_text,)).start()

    def fetch_ai_response(self, user_text):
        ai_reply = self.agent.ask(user_text)

        self.root.after(0, self.update_chat_with_response, ai_reply)

    def update_chat_with_response(self, ai_reply):
        self.chat_area.config(state='normal')
        content = self.chat_area.get("1.0", tk.END)
        new_content = content.replace("System: Analyzing data, please wait...\n\n", "")
        self.chat_area.delete("1.0", tk.END)
        self.chat_area.insert(tk.END, new_content)
        self.chat_area.config(state='disabled')

        self.append_to_chat("AI Assistant", ai_reply)

        self.send_btn.config(state=tk.NORMAL)
        self.entry_box.config(state=tk.NORMAL)
        self.entry_box.focus()

    def append_to_chat(self, sender, message):
        """Helper function for nicely formatting text in the chat"""
        self.chat_area.config(state='normal')
        self.chat_area.insert(tk.END, f"{sender}: ", sender)
        self.chat_area.insert(tk.END, f"{message}\n\n")

        self.chat_area.tag_config("You", foreground="blue", font=("Arial", 11, "bold"))
        self.chat_area.tag_config("AI Assistant", foreground="green", font=("Arial", 11, "bold"))
        self.chat_area.tag_config("System", foreground="gray", font=("Arial", 10, "italic"))

        self.chat_area.see(tk.END)
        self.chat_area.config(state='disabled')
