import tkinter as tk
from tkinter.scrolledtext import ScrolledText

class ChatWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.wm_title("Chat")

        self.log = ScrolledText(self)
        self.log.bind("<Key>", lambda evt: "break") # Not editable
        self.log.tag_configure('you', foreground='green')
        self.log.tag_configure('peer', foreground='red')
        self.log.pack(side="top", fill="both", expand=True)

        self.send_frame = tk.Frame(self)
        self.send_frame.pack(side="bottom", fill="x")

        self.send_entry = tk.Entry(self.send_frame)
        self.send_entry.bind("<Return>", lambda evt: self.send_message())
        self.send_entry.pack(side="left", fill="x", expand=True)

        self.send_button = tk.Button(self.send_frame)
        self.send_button["text"] = "Send"
        self.send_button["command"] = self.send_message
        self.send_button.pack(side="right")

        self.recv_message("Someone", "test")
        self.recv_message("Someone", "test2")

    def send_message(self):
        message = self.send_entry.get()
        self.send_entry.delete(0, len(message))
        self.log.insert("end", "You> " , "you")
        self.log.insert("end", message + "\n", None)

    def recv_message(self, sender, message):
        self.log.insert("end", sender + "> ", "peer")
        self.log.insert("end", message + "\n")

window = ChatWindow()
window.mainloop()
