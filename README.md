# NoteTaking App
The NoteTakingApp is a desktop application for managing and editing notes, built using PyQt6 and SQLite. The application allows users to create, view, edit, and manage notes in a user-friendly interface. Below are the key features and functionalities:
![image](https://github.com/user-attachments/assets/845d0778-18e8-4e40-9424-4fbbf5bb7298)

## User Interface
Main Window: The main window is structured with a sidebar and a content area. The sidebar displays a list of notes, while the content area shows the details of the currently selected note.
Sidebar: Contains a QListWidget for displaying note titles. Users can create new notes, edit existing ones, or delete them. The sidebar also includes context menus for additional actions.
Note Input Area: Consists of a QLineEdit for entering the note title and a QTextEdit for the note's content. This area allows users to add or edit note content.

## Functionalities
![image](https://github.com/user-attachments/assets/425b60f8-1a0a-4816-856f-f403d35218d0)

Creating Notes: Users can create new notes by entering a title and content, which are then added to both the sidebar and the internal dictionary.
Editing Notes: Users can select a note from the sidebar to edit its title and content. The changes are reflected in both the sidebar and the internal dictionary.
Deleting Notes: Notes can be deleted from the sidebar and the internal dictionary.
Saving and Loading Notes: Notes are saved to an SQLite database (notes.db). Upon starting the app, existing notes are loaded from this database. Users can also save notes to text files and import text files to create new notes.
Clipboard Operations: Users can copy, cut, and paste notes using a clipboard feature. The app handles copying and pasting of note content, including generating unique names for pasted notes.

## Menu Bar
![image](https://github.com/user-attachments/assets/353bf889-27f8-4192-ae38-467b1ad21cfa)

File Menu: Includes options to create new notes, open existing text files, save notes, and exit the application.
Edit Menu: Provides undo functionality.
Undo and Redo: The application supports undo and redo operations for actions such as adding, deleting, and editing notes. The undo and redo stacks keep track of these actions.
View Menu: Allows users to view or hide the sidebar.
View and Hide Sidebar: Users can toggle the visibility of the sidebar through the application menu.

## Context Menus
![image](https://github.com/user-attachments/assets/e6845a66-b099-44de-ac1e-d5d8131e22a7)

Sidebar Context Menu: Provides additional actions such as creating new notes, editing, deleting, copying, pasting, and cutting notes. This menu appears when right-clicking on a note in the sidebar.

## Data Storage
SQLite Database: Notes are stored in an SQLite database to persist data between application sessions.

## Creating Executable
Uses PyInstaller (pip install pyinstaller) to convert the python PyQt6 application into a standalone executable (pyinstaller --name NoteTakingApp --onefile --windowed note_taking_app.py)
