import tkinter as tk
from glossar.glossar import Glossary
from settings.settings import BUTTON_FRAME_SETTINGS, MAIN_BUTTON_FRAME_SETTINGS
from user_interface.text_frame import TextFrame
from user_interface.button_frame import ButtonFrame
from user_interface.main_button_frame import MainButtonFrame


class MainWindow(tk.Tk):


    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self.label = tk.Label(master= self, 
                              text= "Please enter your text below. After clicking the 'Scan text' button,\nthe programm will scan the whole text and highlight complicated words",
                              justify=tk.LEFT)
        self.label.grid(column= 0, row= 0)

        self.scan_button = tk.Button(master= self, text= "Scan text", command= lambda: self.highlight_text())
        self.scan_button.grid(column= 0, row= 1, sticky="WE")

        self.quit_button = tk.Button(master= self, text= "Quit", command= lambda: quit())
        self.quit_button.grid(column= 1, row= 1, sticky="WE")

    
    def set_text_frame(self, text_frame: TextFrame) -> None:
        self.text_frame = text_frame
        self.text_frame.grid(column= 0, row= 2, columnspan= 2, sticky="NSWE")
        self.set_entry_widget()


    def set_entry_widget(self) -> None:
        self.text = self.text_frame.text


    def highlight_text(self) -> None:
        
        """Scans the text from the entry widget. Puts up buttons for every word which is listed within the glossary."""

        try:
            self.destroy_main_button_frame()
        
        except:
            pass
        
        self.text_frame.process_text()
        self.create_explanatory_buttons()
        self.clear_highlighted_words()


    def destroy_main_button_frame(self) -> None:
        
        """DEstroys the main button frame which carries all the buttons of the complicated words which allow 
        one to bring up the glossary definition of these words."""
        
        self.main_button_frame.destroy()


    def clear_highlighted_words(self) -> None:

        """Clears the list of the glossary class which tracks the complicated and highlighted words within the text."""

        Glossary.clear_hightlighted_words()

    
    def create_explanatory_buttons(self) -> None:
        
        """Creates the buttons which allow one to get the glossary definition of a specific complicated word."""

        self.main_button_frame = MainButtonFrame(master= self, **MAIN_BUTTON_FRAME_SETTINGS) 
        self.main_button_frame.grid(column= 2, 
                                    row= 0,
                                    rowspan= 3, 
                                    sticky="N")

        for highlighted_word in Glossary.highlighted_words:
            ButtonFrame(master= self.main_button_frame ,button_text= highlighted_word,
                        **BUTTON_FRAME_SETTINGS).pack(fill=tk.X)
    