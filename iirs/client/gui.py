import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText

class ChatLogWidget(ttk.Frame):
    def __init__(self, parent, server_connection):
        super().__init__(parent)
        self.server_connection = server_connection

        self.log_text = tk.Text(self)
        #self.log_text['borderwidth'] = 0
        #self.log_text['background'] = self['background']
        self.log_text.bind("<Key>", lambda evt: "break") # Not editable
        self.log_text.tag_configure('you', foreground='green')
        self.log_text.tag_configure('peer', foreground='red')
        self.log_text.pack(side="left", fill="both", expand=True)

        self.log_scroll = ttk.Scrollbar(self)
        self.log_scroll['command'] = self.log_text.yview
        self.log_text['yscrollcommand'] = self.log_scroll.set
        self.log_scroll.pack(side="right", fill="y")

    def append_message(self, sender, tag, message):
        self.log_text.insert("end", sender + "> ", tag)
        self.log_text.insert("end", message + "\n", None)
        self.log_text.yview_moveto(1.)


class SendWidget(ttk.Frame):
    def __init__(self, send_clbk, parent, server_connection):
        super().__init__(parent)
        self.server_connection = server_connection

        self.send_clbk = send_clbk

        self.send_entry = ttk.Entry(self)
        self.send_entry.bind("<Return>", self.handle_send_evt)
        self.send_entry.pack(side="left", fill="x", expand=True)

        self.send_button = ttk.Button(self)
        self.send_button["text"] = "Send"
        self.send_button["command"] = self.handle_send_evt
        self.send_button.pack(side="right")

    def handle_send_evt(self, evt=None):
        message = self.send_entry.get()
        self.send_entry.delete(0, len(message))
        response = self.server_connection.send_message(message)
        self.send_clbk(message)
        self.master.recv_message("Server", response)


class ChatWindow(tk.Tk):
    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            # need to close sockets, do cleanup
            self.destroy()

    def __init__(self, server_connection):
        super().__init__()

        self.server_connection = server_connection

        self.wm_title("Chat")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        style = ttk.Style()
        style.theme_use('clam')

        self.log = ChatLogWidget(self, server_connection)
        self.log.pack(side="top", fill="both", expand=True)

        self.send_frame = SendWidget(self.send_message, self, server_connection)
        self.send_frame.pack(side="bottom", fill="x")

        # self.recv_message("Someone", "test")
        # self.recv_message("Someone", "test2")

    def send_message(self, message):
        self.log.append_message("You", "you", message)

    def recv_message(self, sender, message):
        self.log.append_message(sender, "peer", message)


# window = ChatWindow()
# window.mainloop()