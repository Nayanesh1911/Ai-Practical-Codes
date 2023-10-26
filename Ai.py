from tkinter import *
import openai

BG_GRAY = "#808080"
BG_COLOR = "black"
TEXT_COLOR = "white"
BOT_NAME = "Nano"
openai.api_key = "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"

FONT = "Helvetica 14"
FONT_BOLD = "Helvetica 13 bold"

class ChatbotInterface:

    def __init__(self):
        self.window = Tk()
        self._setup_main_window()

    def run(self):
        self.window.mainloop()

    def _setup_main_window(self):
        self.window.title("Nayanesh Assistant")
        self.window.resizable(width=False, height=False)
        self.window.configure(width=470, height=550, bg=BG_COLOR)

        head_label = Label(self.window, bg=BG_COLOR, fg=TEXT_COLOR,
                           text="Welcome",
                           font=FONT_BOLD,
                           pady=10)
        head_label.place(relwidth=1)

        line = Label(self.window, width=450, bg=BG_COLOR)
        line.place(relwidth=1, rely=0.07, relheight=0.012)

        self.text_widget = Text(self.window, width=20, height=2, bg=BG_COLOR, fg=TEXT_COLOR,
                                font=FONT, pady=5, padx=5)
        self.text_widget.place(relheight=0.745, relwidth=1, rely=0.08)
        self.text_widget.configure(cursor="arrow", state="disabled")

        scroll_bar = Scrollbar(self.text_widget)
        scroll_bar.place(relheight=1, relx=0.974)
        scroll_bar.configure(command=self.text_widget.yview)

        bottom_label = Label(self.window, bg=BG_GRAY, height=80)
        bottom_label.place(relwidth=1, rely=0.825)

        self.msg_entry = Entry(bottom_label, bg="#2C3E50", fg=TEXT_COLOR, font=FONT)
        self.msg_entry.place(relwidth=0.74, relheight=0.06, rely=0.008, relx=0.011)
        self.msg_entry.focus()
        self.msg_entry.bind("<Return>", self._on_enter_pressed)

        self.send_button = Button(bottom_label, text="Send", font=FONT_BOLD, width=20, bg=BG_GRAY,
                                  command=lambda: self._on_enter_pressed(None))
        self.send_button.place(relx=0.77, rely=0.008, relheight=0.06, relwidth=0.22)

    def _on_enter_pressed(self, event):
        user_message = self.msg_entry.get()
        self._insert_message(user_message, "You")
        bot_response = self.generate_bot_response(user_message)
        self._insert_message(bot_response, "Chatbot")

    def generate_bot_response(self, user_message):
        try:
            response = openai.Completion.create(
                engine="text-davinci-002",
                prompt=user_message,
                max_tokens=50,
                temperature=0.7
            )
            return response.choices[0].text.strip()
        except Exception as e:
            return str(e)

    def _insert_message(self, msg, sender):
        if not msg:
            return
        self.msg_entry.delete(0, END)
        msg1 = f"{sender}: {msg}\n\n"
        self.text_widget.configure(state="normal")
        self.text_widget.insert(END, msg1)
        self.text_widget.configure(state="disabled")
        self.text_widget.see(END)

if __name__ == "__main__":
    app = ChatbotInterface()
    app.run()
