from pathlib import Path
import sqlite3 
import re

class Glossary:

    """Main class to manage the glossary entries of complicated words as well as the currently tracked 
    and, since concidered complicated, highlighted words. Manages the database model as well."""
    
    highlighted_words = list()
    table = "glossary_table"
    already_existing_words = set()

 
    def connect_to_glossary_data() -> sqlite3.Connection:

        connection = sqlite3.connect("src/glossar/Glossary.db")
        return connection


    def update_database_word(word: str, new_word: str, connection: sqlite3.Connection) -> None:
        
        """Updates a keyword from the old keyname to the new keyname 'new_word'"""
        
        cursor = connection.cursor()
        
        try:
            cursor.execute(f"""UPDATE {Glossary.table} 
                               SET word == '{new_word}' 
                               WHERE word == '{word}'""")
        finally:
            connection.commit()


    def update_database_explanation(connection: sqlite3.Connection, word: str, new_explanation: str) -> None:
        
        """Updates an existing entry explanation. uses word as key to find the specific entry"""
        
        cursor = connection.cursor()
        
        try:
            cursor.execute(f"""UPDATE {Glossary.table} 
                           SET explanation == '{new_explanation}' 
                           WHERE word == '{word}'""")
        finally:
            connection.commit()


    def create_database_entry(connection: sqlite3.Connection, word: str, explanation: str) -> None:
        
        """Creates a single new database entry with word as key and explanation as definition within the glossary."""
        
        cursor = connection.cursor()

        try:
            cursor.execute(f'''INSERT INTO {Glossary.table} (word, explanation) 
                           VALUES ('{word}', '{explanation}')''')
        finally:
            connection.commit()


    def delete_database_entry(connection: sqlite3.Connection, entry_to_delete: str) -> None:
        
        """Deletes a single database entry according to the entry_to_delete argument passed in which has to be the key value."""
        
        cursor = connection.cursor()

        try:
            cursor.execute(f"""DELETE 
                            FROM {Glossary.table} 
                            WHERE word == '{entry_to_delete}'""")
        finally:
            connection.commit()


    def fetch_all_keys_from_database(connection: sqlite3.Connection) -> list[tuple[str]]:
        
        """Grabs only the word column from the database."""

        cursor = connection.cursor()
        
        try:
            cursor.execute(f"""SELECT word 
                           FROM {Glossary.table}""")
        
        finally:
            connection.commit()
            return cursor.fetchall()
    

    def fetch_all_database_entries(connection: sqlite3.Connection) -> list[tuple[str]]:
        
        """Grabs all database entries from the database for all columns existing in the database."""
        
        cursor = connection.cursor()
        
        try:
            cursor.execute(f"""SELECT * 
                            FROM {Glossary.table}""")
        
        finally:
            connection.commit()
            return cursor.fetchall()


    def fetch_explanation_for_database_entry(connection: sqlite3.Connection, word: str) -> list[str]:
        
        """Grabs a specific explanation for a specific word from database."""
        
        cursor = connection.cursor()
        
        try:
            cursor.execute(f"""SELECT explanation 
                            FROM {Glossary.table} 
                            WHERE word == '{word}'""")
        
        finally:
            connection.commit()
            return cursor.fetchall()

    
    def initialize_table(connection: sqlite3.Connection) -> None:

        """Initial creation of the glossary table."""

        try:
            connection.execute(f"""CREATE TABLE IF NOT EXISTS {Glossary.table}
                                    (word varchar PRIMARY KEY,
                                    explanation varchar)""")
        
        finally:
            connection.commit()


    def get_glossar_keys() -> list[str]:
        
        """
        Returns all words which are stored within the glossary labled as 'difficult to understand'. 
        Returns all those words as a list.
        """

        con = Glossary.connect_to_glossary_data()
        return Glossary.fetch_all_keys_from_database(con)       


    def get_definition(word: str) -> str:
        
        """Grabs a specific definition stored within the database for a word passed in."""

        con = Glossary.connect_to_glossary_data()
        return Glossary.fetch_explanation_for_database_entry(con, word)[0][0]


    def clear_hightlighted_words() -> None:
        
        """Deletes all words stored within the highligted words list."""
        
        Glossary.highlighted_words.clear()


    def is_highlighted(word: str) -> bool:

        """Returns either True if a word is listed in the highlighted words list or False if not."""

        return word in Glossary.highlighted_words


    def track_highlighted_word(word: str) -> None:
        
        """Tracks if a word is already stored within the highlighted words list. List is used to create the buttons later on.
        If statement cares about listing a word only one time within the word list."""

        if Glossary.is_highlighted(word= word):
            pass

        else:
            Glossary.highlighted_words.append(word)
    

    def is_concidered_complicated(word: str) -> bool:
        
        """Checks whether a word is stored within the database. Database covers all words which are considered complicated.
        Returns either True if word is list, or False if word does not exist within the database."""
        
        try:
            word = re.findall("([a-zA-Z0-9]\w+)", word)[0]

        except:
            pass
        
        con = Glossary.connect_to_glossary_data()

        all_current_keys = Glossary.fetch_all_keys_from_database(con)
        for keys in all_current_keys:
            if word in keys:
                return True
        
        
        return False


    def read_import_file(file_path: str) -> list[str]:
        
        """Reads in a file from the path passed in as argument."""

        file_path = Path(file_path)

        if file_path.suffix != ".csv":
            return None

        with open(file_path, "r") as import_file:
            file_content = import_file.readlines()
        
        return file_content


    def write_imported_data_to_database(file_content: list[str]) -> None:

        """Splits the file content elements and calls the create database entry function.
        """

        con = Glossary.connect_to_glossary_data()

        for row in file_content[1:]:
            
            if len(row) <= 1:
                # catches empty row or 1 digit key
                continue

            word, explanation = row.split(";") #splits the csv row into word and explanation
            
            try:
                Glossary.create_database_entry(connection= con,
                                               word= word,
                                               explanation= explanation)
            
            except sqlite3.OperationalError as op_err:
                print(f"Database is currently locked: {op_err}")
            
            except sqlite3.DatabaseError as db_err:
                Glossary.update_database_explanation(connection= con, 
                                                     word= word, 
                                                     new_explanation= explanation)
                
                print(f"Value '{word}' already exists: {db_err}.\n '{word}s' explanation is updated with '{explanation}'")


    def import_file(file_path: str) -> bool:
       
        """Wrapper function to import files into the database. Returns true if the import was succesful"""

        file_content: list[str]

        file_content= Glossary.read_import_file(file_path= file_path)

        if not file_content:
            return False

        Glossary.write_imported_data_to_database(file_content= file_content)
        return True


    def create_import_template() -> None:
        
        """Stores an import template to the users location. This can be used for either upload or deletion."""

        path = "/Users/florianluebke/Desktop/import_template.csv"

        with open(path, "w") as template:
            template.write("word;explanation\n")
            template.write("DHB;Deutscher Handball Bund\n")

    
    def delete_entries_via_file_upload(file_path: str) -> None:
        
        """Reads file content row by row and deletes the entries which are present within the database."""
        
        file_content = Glossary.read_import_file(file_path= file_path)
        con = Glossary.connect_to_glossary_data()
        
        for row in file_content[1:]:
            
            if len(row) <= 1:
                # catches empty row
                continue

            word, explanation = row.split(";")

            try:
                Glossary.delete_database_entry(connection= con, entry_to_delete= word)

            except sqlite3.OperationalError as op_err:
                print(f"Error occured. {word} is maybe not deleted.")
                print(f"Error message: {op_err}")
                
            finally:
                con.commit()