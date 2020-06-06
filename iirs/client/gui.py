import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText

class ChatLogWidget(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

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
        #Temp
        self.log_text.insert("end", sender + "> ", tag)
        self.log_text.insert("end", message + "\n", None)
        self.log_text.yview_moveto(1.)


class SendWidget(ttk.Frame):
    def __init__(self, send_clbk, parent):
        super().__init__(parent)

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
        self.send_clbk(message)


class ChatWindow(tk.Tk):
    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to terminate this chat?"):
            # need to close sockets, do cleanup
            self.destroy()

    def __init__(self, chat_session):
        super().__init__()

        self.chat_session = chat_session

        self.wm_title("Chat")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        style = ttk.Style()
        style.theme_use('clam')

        self.after(1, self.fetch_messages)

        self.log = ChatLogWidget(self)
        self.log.pack(side="top", fill="both", expand=True)

        self.send_frame = SendWidget(self.send_message, self)
        self.send_frame.pack(side="bottom", fill="x")

    def fetch_messages(self):
        self.after(1, self.fetch_messages)

        # Check if any messages have been recieved
        messages = self.chat_session.recv_messages()
        for message in messages:
            peer_message = message.body
            self.recv_message(message.src, peer_message.message)

    def send_message(self, message):
        self.chat_session.send_message(message)
        self.log.append_message("You", "you", message)

    def recv_message(self, sender, message):
        # [TEMP] Self.chat_session.sender temp solution
        self.log.append_message(self.chat_session.peer_name, "peer", message)


"""GUI implementation of register and login TODO if time"""
# class RegisterWidget(ttk.Frame):
#     def __init__(self, register_clbk, parent):
#         super().__init__(parent)
#         self.register_clbk = register_clbk
#         self.register_button = tk.Button(parent, text="Register", command=handle_register_event)
#         self.register_button.pack(side="top", fill="both", expand=True)
#
#     def handle_register_event(self):
#         pass
#
#
# class LoginPage(tk.Tk):
#
#     def __init__(self):
#         super().__init__()
#
#         self.wm_title("Home")
#
#         style = ttk.Style()
#         style.theme_use('clam')
#
#         self.register = RegisterWidget(self.register_user, self)
#         self.register.pack(side="top", fill="both", expand=True)
#
#         self.login = LoginWidget(self.login_user, self)
#         self.login.pack(side="bottom", fill="x")
#
#     def register_user(self):
#         pass
#
#     def login_user(self):
#         pass
