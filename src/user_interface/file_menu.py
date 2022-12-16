import tkinter as tk
from tkinter import filedialog
import os
from glossar.glossar import Glossary

class FileMenu:

    import_file_path: str
    delete_file_path: str

    def update_glossary_entry_ui() -> None:
        root = tk.Tk()
        root.title("Update glossary word")
        
        key_label = tk.Label(master= root, text= "Word to rename:")
        key_label.pack(fill= tk.BOTH)

        key_entry = tk.Entry(master= root, justify= tk.CENTER)
        key_entry.pack(fill= tk.BOTH)

        new_name_label = tk.Label(master= root, text= "New Name:")
        new_name_label.pack(fill= tk.BOTH)
        new_name_entry = tk.Entry(master= root, justify= tk.CENTER)
        new_name_entry.pack(fill= tk.BOTH)

        tk.Button(master= root, 
                  text="Update Glossary", 
                  command= lambda: FileMenu.update_glossary_entry(word= key_entry.get(), new_word= new_name_entry.get())).pack()


    def update_glossary_entry(root: tk.Tk, word: str, new_word: str) -> None:
        Glossary.update_database_word(word= word, new_word= new_word, connection= Glossary.connect_to_glossary_data())


    def update_glossary_explanation_ui() -> None:
        root = tk.Tk()
        root.title("Update glossary explanation")
        
        key_label = tk.Label(master= root, text= "Word to update explanation for:")
        key_label.pack(fill= tk.BOTH)
        key_entry = tk.Entry(master= root, justify= tk.CENTER)
        key_entry.pack(fill= tk.BOTH)

        new_explanation_label = tk.Label(master= root, text= "New Explanation:")
        new_explanation_label.pack(fill= tk.BOTH)
        new_explanation_entry = tk.Entry(master= root, justify= tk.CENTER)
        new_explanation_entry.pack(fill= tk.BOTH)

        tk.Button(master= root, 
                  text="Update Explanation", 
                  command= lambda: FileMenu.update_glossary_explanation(word= key_entry.get(), new_explanation= new_explanation_entry.get())).pack()


    def update_glossary_explanation(word: str, new_explanation: str) -> None:
        Glossary.update_database_explanation(word= word, new_explanation= new_explanation, connection= Glossary.connect_to_glossary_data())


    def insert_new_glossary_entry_ui() -> None:
        root = tk.Tk()
        root.title("Insert new glossary entry")
        
        new_key_label = tk.Label(master= root, text= "New Entry:")
        new_key_label.pack(fill= tk.BOTH)
        new_key_entry = tk.Entry(master= root, justify= tk.CENTER)
        new_key_entry.pack(fill= tk.BOTH)

        new_explanation_label = tk.Label(master= root, text= "Explanation:")
        new_explanation_label.pack(fill= tk.BOTH)
        new_explanation_entry = tk.Entry(master= root, justify= tk.CENTER)
        new_explanation_entry.pack(fill= tk.BOTH)

        tk.Button(master= root, 
                  text="Insert word", 
                  command= lambda: FileMenu.insert_new_glossary_entry(word= new_key_entry.get(), explanation= new_explanation_entry.get())).pack()


    def insert_new_glossary_entry(word: str, explanation: str) -> None:
        Glossary.create_database_entry(connection= Glossary.connect_to_glossary_data(), explanation= explanation, word= word)


    def delete_glossary_entry_ui() -> None:
        root = tk.Tk()
        root.title("Delete glossary entry")
        
        key_to_delete_label = tk.Label(master= root, text= "Word to delete:")
        key_to_delete_label.pack(fill= tk.BOTH)
        key_to_delete_entry = tk.Entry(master= root, justify= tk.CENTER)
        key_to_delete_entry.pack(fill= tk.BOTH)

        tk.Button(master= root, 
                  text="Delete word", 
                  command= lambda: FileMenu.delete_glossary_entry(word= key_to_delete_entry.get())).pack()


    def delete_glossary_entry(word: str) -> None:
        Glossary.delete_database_entry(connection= Glossary.connect_to_glossary_data(), entry_to_delete= word)


    def present_all_entries_ui() -> None:
        root = tk.Tk()
        root.title("All current entries")
        all_entries= Glossary.fetch_all_database_entries(connection= Glossary.connect_to_glossary_data())
        
        display_entries = tk.Text(master= root, width=150)
        display_entries.pack()

        for entry in all_entries:
            word, explanation = entry
            display_entries.insert("1.0", f"{word};{explanation}\n")


    def import_glossary_entries_ui() -> None:
        root = tk.Tk()
        root.title("Select import file")
        
        key_to_delete = tk.Label(master= root, text= "Filepath")
        key_to_delete.pack(fill= tk.BOTH)

        tk.Button(master = root,
                  text= "Select file path",
                  command= FileMenu.get_import_file_path()).pack(fill= tk.BOTH)

    
        tk.Button(master= root, 
                  text="Import data", 
                  command= lambda: Glossary.import_file(FileMenu.import_file_path)).pack(fill= tk.BOTH)


    def get_import_file_path() -> None:

        """Stores the filepath of the import file in the static variable."""

        FileMenu.import_file_path= filedialog.askopenfilename()
    

    def get_import_template_ui() -> None:
        
        """Allows one to download an import template for further imports."""

        Glossary.create_import_template()

    
    def delete_files_via_file_upload_ui() -> None:
        root = tk.Tk()
        root.title("Select import file")
        
        key_to_delete = tk.Label(master= root, text= "Filepath")
        key_to_delete.pack(fill= tk.BOTH)

        tk.Button(master = root,
                  text= "Select file path",
                  command= FileMenu.get_import_file_path()).pack(fill= tk.BOTH)

    
        tk.Button(master= root, 
                  text="Delete entries", 
                  command= lambda: Glossary.delete_entries_via_file_upload(FileMenu.import_file_path)).pack(fill= tk.BOTH)


    def get_delete_file_path() -> None:
        
        """Stores the filepath of the import-deletion file in the static variable."""

        FileMenu.delete_file_path= filedialog.askopenfilename()