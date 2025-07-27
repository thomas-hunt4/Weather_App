import customtkinter as ctk


class ToplevelWindow(ctk.CTkToplevel):
    """Alert popup window"""
    
    def __init__(self, parent):
        super().__init__(parent)
        self.geometry("600x600")
        self.title()
        self.attributes("-topmost", True) # makes window stick to front

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        label = ctk.CTkLabel(self, text="ALERT!!")
        label.grid(row=0, column=0, pady=(5,5), padx=10)

        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)