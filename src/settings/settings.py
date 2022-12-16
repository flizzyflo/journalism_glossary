
import string

## UI Settings
BUTTON_FRAME_SETTINGS = {"borderwidth": 1, 
                         "relief": 'groove',
                        }

MAIN_BUTTON_FRAME_SETTINGS = {"borderwidth": 2, 
                              "relief": 'groove',
                             }

## Text widget highlighting colors
HIGHLIGHTED_WORD_COLORS = {"foreground": "black", "background": "yellow"}

## Special sign container
SPECIAL_SIGNS = tuple(sign for sign in string.punctuation)

## Regex patterns
REGEX_PATTERN_SPORTRESULT_DATE = "([0-9]+[:, ;, .][0-9]+([:,;,.][0-9]+)?)"
REGEX_PATTERN_CONNECTED_WORDS = "([a-zA-Z0-9]\w+)"
REGEX_PATTERN_FILTER_WORD = "([a-zA-Z0-9]\w+)"

