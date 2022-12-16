import tkinter as tk
from user_interface.text_frame import TextFrame
from user_interface.main_window import MainWindow
from user_interface.file_menu import FileMenu

if __name__ == "__main__":

    root = MainWindow()
    root.set_text_frame(TextFrame(master= root))
    root.title("Text analyzer - do you understand?")

    menu = tk.Menu(master= root)
    root.config(menu= menu)
    filemenu = tk.Menu(menu)
    menu.add_cascade(label="Manage glossary", menu= filemenu)
    filemenu.add_command(label="Insert new glossary entry", command= lambda: FileMenu.insert_new_glossary_entry_ui())
    filemenu.add_command(label="Import glossary data", command= lambda: FileMenu.import_glossary_entries_ui())
    filemenu.add_command(label="Download import template", command= lambda: FileMenu.get_import_template_ui())
    filemenu.add_separator()
    filemenu.add_command(label="Update glossary word", command= lambda: FileMenu.update_glossary_entry_ui())
    filemenu.add_command(label="Update word-related explanation", command= lambda: FileMenu.update_glossary_explanation_ui())
    filemenu.add_command(label="Show all glossary entries", command= lambda: FileMenu.present_all_entries_ui())
    filemenu.add_separator()
    filemenu.add_command(label="Delete single glossary entry", command= lambda: FileMenu.delete_glossary_entry_ui())
    filemenu.add_command(label="Delete glossary files via file upload", command= lambda: FileMenu.delete_files_via_file_upload_ui())
    
    root.mainloop()
