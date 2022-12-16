import tkinter as tk

class MainButtonFrame(tk.Frame):

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self.label = tk.Label(master= self, text= "Click buttons below to get the explanation for the specific word:")
        self.label.pack()