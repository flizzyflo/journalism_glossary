
import re

class TextManager:

    """Main static class to handle text and evaluate the text with the help of regular expressions."""


    def word_in_character_list(word: str, character_list: list[str]) -> bool:
        
        """Checks whether the word itself is a special sign or not."""

        return word in character_list

    
    def is_number_or_sport_result(word: str, regex_pattern: str = "([0-9]+[:, ;, .][0-9]+([:,;,.][0-9]+)?)") -> bool:
        
        """Checks whether the word is a number, date or other numeric value with special sign"""

        return re.findall(regex_pattern, word) != []

    
    def is_connected_word(word: str, regex_pattern: str = "([a-zA-Z0-9]\w+)") -> bool:
        
        """Checks if the word is a composition like DFB-Haus or something like that."""

        return len(re.findall(regex_pattern, word)) > 1


    def filter_word(word: str, regex_pattern: str = "([a-zA-Z0-9]\w+)") -> list[str]:

        """Returns a filtered word out of the input word. Eliminates all special signs"""

        return re.findall(regex_pattern, word)
    
    def is_numeric_word(word: str) -> bool:
        
        """Checks whether a given input value is a numeric string or not."""

        return word.isnumeric()
    
