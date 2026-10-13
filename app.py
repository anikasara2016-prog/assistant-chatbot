
import os
import threading
import tkinter as tk
from tkinter import messagebox, scrolledtext

from dotenv import load_dotenv
from groq import Groq

# Load API settings from .env beside this file
load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"))

API_KEY = os.getenv("GROQ_API_KEY", "").strip()
MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")

SYSTEM_PROMPT = """
You are Assistant AI, a helpful and honest assistant.
Reply in the user's language, including Bangla when appropriate.
Help with programming, AI/ML, education and general questions.
Use clear explanations and examples.
Never invent facts. Admit uncertainty when necessary.
"""

BG = "#10131C"
PANEL = "#191E2B"
INPUT_BG = "#242B3B"
FG = "#F1F4FA"
MUTED = "#A5AEC0"
BLUE = "#6C8CFF"
GREEN = "#25C9A5"


class AssistantChatbot:
    def __init__(self, root):
        self.root = root
        self.root.title("Assistant AI")
        self.root.geometry("900x700")
        self.root.minsize(600, 450)
        self.root.configure(bg=BG)

        self.client = Groq(api_key=API_KEY) if API_KEY else None
        self.messages = []
        self.busy = False

        # GRID LAYOUT: input stays in its own bottom row
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(2, weight=1)

        self.build_ui()

        self.add_message(
            "Assistant AI",
            "হ্যালো! 👋\n\n"
            "আমি Assistant AI। বাংলায় অথবা English-এ প্রশ্ন করো।\n"
            "Python, AI/ML, পড়াশোনা এবং সাধারণ বিষয়ে সাহায্য করতে পারি।",
        )

        if self.client:
            self.set_status("Ready • Ask me anything")
        else:
            self.set_status("API key missing")
            self.add_message(
                "System",
                "Project-এর .env ফাইলে GROQ_API_KEY যোগ করো।",
            )

    def build_ui(self):
        # Header: row 0
        header = tk.Frame(self.root, bg=PANEL, padx=18, pady=12)
        header.grid(row=0, column=0, sticky="ew")
        header.grid_columnconfigure(0, weight=1)

        tk.Label(
            header,
            text="🤖 Assistant AI",
            font=("Segoe UI", 19, "bold"),
            bg=PANEL,
            fg=FG,
        ).grid(row=0, column=0, sticky="w")

        tk.Button(
            header,
            text="New Chat",
            command=self.clear_chat,
            bg="#30394D",
            fg=FG,
            activebackground="#414D66",
            activeforeground=FG,
            relief="flat",
            padx=12,
            pady=7,
            cursor="hand2",
        ).grid(row=0, column=1, sticky="e")

        # Status: row 1
        self.status = tk.Label(
            self.root,
            text="Connecting...",
            bg=BG,
            fg=MUTED,
            font=("Segoe UI", 9),
            anchor="w",
            padx=18,
            pady=6,
        )
        self.status.grid(row=1, column=0, sticky="ew")

        # Chat history: expandable row 2
        chat_frame = tk.Frame(self.root, bg=BG)
        chat_frame.grid(
            row=2, column=0, sticky="nsew", padx=10, pady=4
        )
        chat_frame.grid_rowconfigure(0, weight=1)
        chat_frame.grid_columnconfigure(0, weight=1)

        self.chat = scrolledtext.ScrolledText(
            chat_frame,
            wrap=tk.WORD,
            font=("Segoe UI", 11),
            bg=BG,
            fg=FG,
            insertbackground=FG,
            relief="flat",
            borderwidth=0,
            padx=14,
            pady=10,
            state="disabled",
        )
        self.chat.grid(row=0, column=0, sticky="nsew")

        self.chat.tag_configure(
            "user_name",
            foreground=BLUE,
            font=("Segoe UI", 11, "bold"),
            spacing1=8,
        )
        self.chat.tag_configure(
            "bot_name",
            foreground=GREEN,
            font=("Segoe UI", 11, "bold"),
            spacing1=8,
        )
        self.chat.tag_configure(
            "system_name",
            foreground="#FF7979",
            font=("Segoe UI", 10, "bold"),
        )
        self.chat.tag_configure(
            "body",
            foreground=FG,
            lmargin1=8,
            lmargin2=8,
            spacing3=10,
        )

        # Input footer: fixed row 3
        footer = tk.Frame(
            self.root,
            bg=PANEL,
            padx=12,
            pady=10,
        )
        footer.grid(row=3, column=0, sticky="ew")
        footer.grid_columnconfigure(0, weight=1)

        self.entry = tk.Text(
            footer,
            height=3,
            wrap=tk.WORD,
            font=("Segoe UI", 11),
            bg=INPUT_BG,
            fg=FG,
            insertbackground=FG,
            selectbackground="#3C4E75",
            relief="flat",
            borderwidth=0,
            padx=10,
            pady=9,
        )
        self.entry.grid(
            row=0, column=0, sticky="ew", padx=(0, 10)
        )
        self.entry.bind("<Return>", self.on_enter)

        self.send_button = tk.Button(
            footer,
            text="Send ➤",
            command=self.send_message,
            font=("Segoe UI", 10, "bold"),
            bg=BLUE,
            fg="white",
            activebackground="#5879E8",
            activeforeground="white",
            relief="flat",
            padx=16,
            pady=10,
            cursor="hand2",
        )
        self.send_button.grid(row=0, column=1, sticky="ns")

        # Footer note: row 4
        tk.Label(
            self.root,
            text="AI can make mistakes. Verify important information.",
            bg=BG,
            fg=MUTED,
            font=("Segoe UI", 8),
            pady=4,
        ).grid(row=4, column=0, sticky="ew")

        self.entry.focus_set()

    def set_status(self, text):
        self.status.config(text=text)

    def add_message(self, sender, text):
        self.chat.configure(state="normal")

        if sender == "You":
            tag = "user_name"
        elif sender == "Assistant AI":
            tag = "bot_name"
        else:
            tag = "system_name"

        self.chat.insert(tk.END, sender + "\n", tag)
        self.chat.insert(tk.END, text + "\n\n", "body")
        self.chat.configure(state="disabled")
        self.chat.see(tk.END)

    def on_enter(self, event):
        # Shift+Enter inserts a newline
        if event.state & 0x0001:
            return None

        self.send_message()
        return "break"

    def send_message(self):
        if self.busy:
            return

        prompt = self.entry.get("1.0", "end-1c").strip()
        if not prompt:
            self.entry.focus_set()
            return

        if not self.client:
            messagebox.showerror(
                "API Key Missing",
                "Project-এর .env ফাইলে GROQ_API_KEY যোগ করো।",
            )
            return

        self.entry.delete("1.0", tk.END)
        self.add_message("You", prompt)

        self.messages.append({"role": "user", "content": prompt})
        request_messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            *self.messages,
        ]

        self.busy = True
        self.send_button.config(state="disabled")
        self.set_status("Thinking... Please wait")

        threading.Thread(
            target=self.fetch_answer,
            args=(request_messages,),
            daemon=True,
        ).start()

    def fetch_answer(self, request_messages):
        try:
            response = self.client.chat.completions.create(
                model=MODEL,
                messages=request_messages,
                temperature=0.5,
                max_completion_tokens=2048,
            )

            answer = response.choices[0].message.content
            if not answer:
                answer = "কোনো উত্তর পাওয়া যায়নি। আবার চেষ্টা করো।"

            self.root.after(
                0, self.finish_answer, answer, None
            )

        except Exception as exc:
            self.root.after(
                0, self.finish_answer, None, str(exc)
            )

    def finish_answer(self, answer, error):
        self.busy = False
        self.send_button.config(state="normal")

        if error:
            if self.messages and self.messages[-1]["role"] == "user":
                self.messages.pop()

            if "401" in error:
                message = "API key invalid। .env ফাইল পরীক্ষা করো।"
            elif "429" in error:
                message = "API quota বা rate limit শেষ। পরে চেষ্টা করো।"
            elif "404" in error:
                message = (
                    f"Model পাওয়া যায়নি: {MODEL}\n"
                    "Groq Console-এ available model পরীক্ষা করো।"
                )
            else:
                message = f"API error:\n{error[:600]}"

            self.add_message("System", message)
            self.set_status("Request failed")
            self.entry.focus_set()
            return

        self.messages.append(
            {"role": "assistant", "content": answer}
        )
        self.add_message("Assistant AI", answer)
        self.set_status("Ready • Ask me anything")
        self.entry.focus_set()

    def clear_chat(self):
        if self.busy:
            messagebox.showinfo(
                "Please wait",
                "উত্তর তৈরি হওয়া পর্যন্ত অপেক্ষা করো।",
            )
            return

        self.messages.clear()
        self.chat.configure(state="normal")
        self.chat.delete("1.0", tk.END)
        self.chat.configure(state="disabled")

        self.add_message(
            "Assistant AI",
            "নতুন chat শুরু হয়েছে। কী জানতে চাও?",
        )
        self.set_status("New conversation")
        self.entry.focus_set()


if __name__ == "__main__":
    root = tk.Tk()
    app = AssistantChatbot(root)
    root.mainloop()
