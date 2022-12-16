import tkinter as tk
from tkinter import messagebox

from glossar.glossar import Glossary

class ButtonFrame(tk.Frame):

    def __init__(self, button_text: str, **kwargs) -> None:
        super().__init__(**kwargs)

        self.button = tk.Button(self, text= button_text, command= lambda: self.present_word_definition(button_text))
        self.button.pack(fill= tk.BOTH)


    def present_word_definition(self, word: str) -> None:

        """Presents the presentation for the single word. Pop up window appears by clicking the specific button.
        Contains the explanation stored within the glossary database."""

        root = tk.Tk()
        root.title(f"Explanation for '{word}'")
        tk.Label(master = root, text= f"Hinterlegte Defintion für '{word}':").pack(fill= tk.BOTH)
        text_widget = tk.Text(master= root, height= 10, width= 55)
        text_widget.pack(fill= tk.BOTH)
        text = f"{Glossary.get_definition(word)}"
        text_widget.insert("1.0", text)

