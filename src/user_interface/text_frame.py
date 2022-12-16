import tkinter as tk
import re
from glossar.glossar import Glossary
from settings.settings import HIGHLIGHTED_WORD_COLORS, SPECIAL_SIGNS, REGEX_PATTERN_CONNECTED_WORDS, REGEX_PATTERN_SPORTRESULT_DATE, REGEX_PATTERN_FILTER_WORD
from text_manager.text_manager import TextManager
class TextFrame(tk.Frame):

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self.text = tk.Text(master= self)
        self.text.pack(fill= tk.BOTH)
        self.text.tag_config("highlighted", **HIGHLIGHTED_WORD_COLORS)
        self.text.insert("1.0", "Der DFB-Verein ist super. 02.02.2021 Er handelt immer vorausschauend. Das nennt man Prävention. Es steht 1:0. Das BIP ist dabei egal.")


    def text_is_emptry(self, text: str) -> bool:
        return len(text) == 0


    def process_text(self) -> None:

        """Grabs the current text stored within the Text widget. 
        Splits the words at the whitespace and processes the text
        word by word. Evaluates every word if it is concidered complicated
        or not."""

        self.glossary_entries = Glossary.get_glossar_keys()

        raw_text = self.text.get("1.0", tk.END).split()

        self.text.delete("1.0", tk.END)

        for word in raw_text:

            if TextManager.is_number_or_sport_result(word= word, regex_pattern= REGEX_PATTERN_SPORTRESULT_DATE):    
                # does not split up the date, soccer result or whatever
                self.update_presented_text(word)

            elif TextManager.is_connected_word(word= word, regex_pattern= REGEX_PATTERN_CONNECTED_WORDS):
                # special case for compositions like dfb-haus etc.
                # splits the composition

                for word in TextManager.filter_word(word= word, regex_pattern= REGEX_PATTERN_FILTER_WORD):
                    self.update_presented_text(word)

            else:       
                # normal case 
                self.update_presented_text(word)
            

    def update_presented_text(self, word: str) -> None:
            
            """Inserts the words word by word. Takes care if it is 
            concidered complicated. If true, highlights the word, otherwise just inserts them"""

            # if word.isnumeric():
            if TextManager.is_numeric_word(word= word):
                # checks if the word passed in is something like a date or a sports result or something. 
                # inserts the result in its original format.
                self.handle_special_signs(word= word, highlight_word= False)

            elif TextManager.word_in_character_list(word= word, character_list= SPECIAL_SIGNS):
            # elif self.is_special_character(word):
                self.text.insert(tk.END, f"{word} ")

            # case it is a complicated word, since it is listed in the glossary.
            elif Glossary.is_concidered_complicated(word):
       
                word = self.handle_special_signs(word= word, highlight_word= True)
                self.track_highlighted_words(word)

            else:
                # case its a non-complicated word, not listed in glossary.
                self.text.insert(tk.END, f"{word} ")


    def handle_special_signs(self, word: str, highlight_word: bool = False) -> str:
        
        """Handles the special signs after a word or number."""

        if word.endswith(SPECIAL_SIGNS):

            # splits the special sign into the suffix variable
            suffix = word[len(word) - 1]

            # regex to get rid of special signs and grab the word
            word = TextManager.filter_word(word= word, regex_pattern= REGEX_PATTERN_FILTER_WORD)[0]

            # composition of  word and suffix to restore the original text.
            self.highlight_word(word= word, highlight_word= highlight_word)
            
            # special sign is separated, to avoid highlighting the special sign.
            self.text.insert(tk.END, f"{suffix} ")


        else:
            # word is not followed by a special sign
            self.highlight_word(word= word, highlight_word= highlight_word)
                       
            # whitespace is separated, to avoid highlighting the whitespace.
            self.text.insert(tk.END, f" ")
        
        return word


    def highlight_word(self, word: str, highlight_word: bool) -> None:
        
        """Highlights a word within the text widget if considered complicated word."""

        if highlight_word:
                self.text.insert(tk.END, f"{word}", "highlighted")
        else:
            self.text.insert(tk.END, f"{word}")


    def track_highlighted_words(self, word: str) -> None:
        
        """Tracks the complicated words detected within a list. 
        Does not allow for duplicates, therefore uses a set."""

        Glossary.track_highlighted_word(word= word)

