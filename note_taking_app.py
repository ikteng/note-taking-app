import sys
import sqlite3
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QListWidget, QPushButton, QLineEdit, QTextEdit, QMenu, QDialog, QAbstractItemView, QListWidgetItem, QFileDialog, QMessageBox, QSplitter
from PyQt6.QtCore import Qt

class NoteTakingApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.notes = {}
        self.sidebar_enabled = False  # Flag to track if the sidebar is enabled
        self.undo_stack = []  # Stack to store actions for undo
        self.redo_stack = []  # Stack to store actions for redo
        self.clipboard = None  # Initialize clipboard attribute

        self.setWindowTitle("Note Taking App")
        self.setGeometry(500, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.main_layout = QHBoxLayout(self.central_widget)

        # Create top menu
        self.menu_bar = self.menuBar()
        self.menu_bar.setStyleSheet("background-color: #B0FFAD;")

        # Create a horizontal layout for the menu bar items
        self.menu_layout = QHBoxLayout()

        # File menu
        self.file_menu = self.menu_bar.addMenu("&File")

        # Actions for the file menu
        self.new_action = QAction("&New", self)
        self.new_action.triggered.connect(self.add_note)
        self.new_action.setShortcut("Ctrl+N")
        self.file_menu.addAction(self.new_action)

        self.open_action = QAction("&Open", self)
        self.open_action.triggered.connect(self.open_file)
        self.open_action.setShortcut("Ctrl+O")
        self.file_menu.addAction(self.open_action)

        self.save_action = QAction("&Save", self)
        self.save_action.triggered.connect(self.save_note)
        self.save_action.setShortcut("Ctrl+S")
        self.file_menu.addAction(self.save_action)

        self.file_menu.addSeparator()

        self.exit_action = QAction("&Exit", self)
        self.exit_action.triggered.connect(self.close)
        self.exit_action.setShortcut("Ctrl+Q")
        self.file_menu.addAction(self.exit_action)

       # Edit Menu
        self.edit_menu = self.menu_bar.addMenu("&Edit")

        # Add undo action
        self.undo_action = QAction("&Undo", self)
        self.undo_action.triggered.connect(self.undo)
        self.undo_action.setShortcut("Ctrl+Z")
        self.edit_menu.addAction(self.undo_action)

        # View Menu
        self.view_menu = self.menu_bar.addMenu("&View")

        self.view_side_menu_action = QAction("&View Side Menu", self)
        self.view_side_menu_action.triggered.connect(self.view_side_menu)
        self.view_menu.addAction(self.view_side_menu_action)

        self.hide_side_menu_action = QAction("&Hide Side Menu", self)
        self.hide_side_menu_action.triggered.connect(self.hide_side_menu)
        self.view_menu.addAction(self.hide_side_menu_action)

        # Layout for sidebar
        self.sidebar_widget = QWidget()
        self.sidebar_layout = QVBoxLayout(self.sidebar_widget)

        self.sidebar = QListWidget()
        self.sidebar.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.sidebar.customContextMenuRequested.connect(self.show_sidebar_menu)
        self.sidebar.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.sidebar.setDragDropMode(QAbstractItemView.DragDropMode.InternalMove)
        self.sidebar.setMovement(QListWidget.Movement.Free)
        self.sidebar.itemDoubleClicked.connect(self.edit_note)

        self.add_note_button = QPushButton("Create New Note")
        self.add_note_button.clicked.connect(self.add_note)
        self.add_note_button.setStyleSheet("background-color: #CEFFC9;")
        self.add_note_button.setMaximumSize(200, 100)

        self.sidebar_layout.addWidget(self.add_note_button)
        self.sidebar_layout.addWidget(self.sidebar)
        self.sidebar.setStyleSheet("background-color: #FFFFFF;")
        self.sidebar.setMaximumSize(200, 800)

        self.sidebar.setStyleSheet(
            """
            QListWidget::item:hover{
                background-color: #CEFFC9;  /* Change the color to your desired hover color */
            }

             QListWidget::item:selected{
                color: black;
                background-color: #B0FFAD;;  /* Change the color to your desired hover color */
            }
            """
        )

        # Layout for note input area
        self.notes_input_widget = QWidget()
        self.notes_input_layout = QVBoxLayout(self.notes_input_widget)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter Note's Name")
        self.name_input.setStyleSheet("background-color: #FFFFFF;")
        self.name_input.setEnabled(False)
        self.name_input.setVisible(False)

        self.content_input = QTextEdit()
        self.content_input.setStyleSheet("background-color: #FFFFFF;")
        self.content_input.setEnabled(False)  # Disable content input initially
        self.content_input.setVisible(False)
        self.content_input.textChanged.connect(self.update_note_content)  # Connect textChanged signal

        self.notes_input_layout.addWidget(self.name_input)
        self.notes_input_layout.addWidget(self.content_input)

        self.main_layout.addWidget(self.sidebar_widget)
        self.main_layout.addWidget(self.notes_input_widget)

        # Set minimum size for name input
        self.name_input.setMinimumSize(550, 30)  # Adjust the width and height as needed

        # Set minimum size for content input
        self.content_input.setMinimumSize(550, 200)

        # Reduce the layout margins and spacing

        # Create a splitter to manage the layout
        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        self.splitter.addWidget(self.sidebar_widget)
        self.splitter.addWidget(self.notes_input_widget)
        
        # Set the central widget to the splitter
        self.setCentralWidget(self.splitter)
        
        self.load_notes()

        # Create actions for shortcuts
        self.new_action = QAction("New", self)
        self.new_action.triggered.connect(self.add_note)
        self.new_action.setShortcut("Ctrl+N")

        self.edit_action = QAction("Edit", self)
        self.edit_action.triggered.connect(self.edit_note)
        self.edit_action.setShortcut("Ctrl+E")

        self.delete_action = QAction("Delete", self)
        self.delete_action.triggered.connect(self.delete_note)
        self.delete_action.setShortcut("DELETE")

        self.copy_action = QAction("Copy", self)
        self.copy_action.triggered.connect(self.copy_note)
        self.copy_action.setShortcut("Ctrl+C")

        self.paste_action = QAction("Paste", self)
        self.paste_action.triggered.connect(self.paste_note)
        self.paste_action.setShortcut("Ctrl+V")

        self.cut_action = QAction("Cut", self)
        self.cut_action.triggered.connect(self.cut_note)
        self.cut_action.setShortcut("Ctrl+X")
        self.open_action.setShortcutVisibleInContextMenu(True)

        # Add actions to the sidebar menu
        self.add_menu_actions()

        # Connect signals for name and content input fields
        self.name_input.editingFinished.connect(self.update_note_name)
    
    def update_note_name(self):
        current_item = self.sidebar.currentItem()
        if current_item:
            old_name = current_item.text()
            new_name = self.name_input.text()
            if new_name and new_name != old_name:
                self.notes[new_name] = self.notes.pop(old_name, '')  # Update dictionary
                current_item.setText(new_name)  # Update sidebar item

    def update_note_content(self):
        current_item = self.sidebar.currentItem()
        if current_item:
            name = current_item.text()
            content = self.content_input.toPlainText()
            self.notes[name] = content  # Update dictionary
            old_content = content
            self.undo_stack.append(('edit', name, old_content))
    
    def add_note(self):
        if not self.sidebar_enabled:
            untitled_note = "Untitled Note"
            self.sidebar.addItem(untitled_note)
            return

        name = self.name_input.text()
        content = self.content_input.toPlainText()
        if name and content:
            self.notes[name] = content  # Add note to the dictionary
            self.sidebar.addItem(name)  # Add note to the sidebar
            self.name_input.clear()
            self.content_input.clear()
            self.name_input.setEnabled(False)  # Disable name input after adding the note
            self.content_input.setEnabled(False)  # Disable content input after adding the note
            self.name_input.setVisible(False)
            self.content_input.setVisible(False)
            self.sidebar_enabled = False  # Reset sidebar flag

            self.undo_stack.append(('add', name, content))

    def edit_note(self):
        item = self.sidebar.currentItem()
        if item:
            name = item.text()
            content = self.notes.get(name, "")
            # Fill up the name_input and content_input fields with the selected note's content
            self.name_input.setText(name)
            self.content_input.setPlainText(content)
            self.name_input.setEnabled(True)
            self.content_input.setEnabled(True)
            self.name_input.setVisible(True)
            self.content_input.setVisible(True)

    def delete_note(self):
        item = self.sidebar.currentItem()
        if item:
            name = item.text()
            if name in self.notes:  # Check if the note exists in the dictionary
                content = self.notes.pop(name)  # Remove note from the dictionary and get its content
                self.sidebar.takeItem(self.sidebar.currentRow())
                self.undo_stack.append(('delete', name, content))

    def load_notes(self):
        conn = sqlite3.connect('notes.db')
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS notes
                        (name TEXT, content TEXT)''')
        conn.commit()

        cursor.execute("SELECT * FROM notes")
        rows = cursor.fetchall()
        for row in rows:
            name, content = row
            self.notes[name] = content  # Add note to the dictionary
            self.sidebar.addItem(name)

    def save_notes(self):
        conn = sqlite3.connect('notes.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM notes")
        for name, content in self.notes.items():
            cursor.execute("INSERT INTO notes VALUES (?, ?)", (name, content))
        conn.commit()

    def save_note(self):
        current_item = self.sidebar.currentItem()
        if current_item:
            name = current_item.text()
            content = self.notes.get(name, "")
            file_path, _ = QFileDialog.getSaveFileName(self, "Save Note As", "", "Text Files (*.txt)")
            if file_path:
                with open(file_path, 'w') as file:
                    file.write(content)
                QMessageBox.information(self, "Note Saved", "The note has been successfully saved as a text file.")

    def add_menu_actions(self):
        # Add copy, paste, and cut actions
        self.sidebar.addAction(self.new_action)
        self.sidebar.addAction(self.delete_action)
        self.sidebar.addAction(self.edit_action)
        self.sidebar.addAction(self.cut_action)
        self.sidebar.addAction(self.copy_action)
        self.sidebar.addAction(self.paste_action)

    def show_sidebar_menu(self, pos):
        menu = QMenu()

        new_action = QAction("New", self)
        new_action.setShortcut("Ctrl+N")
        new_action.triggered.connect(self.add_note)
        menu.addAction(new_action)

        edit_action = QAction("Edit", self)
        edit_action.setShortcut("Ctrl+E")
        edit_action.triggered.connect(self.edit_note)
        menu.addAction(edit_action)

        delete_action = QAction("Delete", self)
        delete_action.setShortcut("DELETE")
        delete_action.triggered.connect(self.delete_note)
        menu.addAction(delete_action)

        menu.addSeparator()

        copy_action = QAction("Copy", self)
        copy_action.setShortcut("Ctrl+C")
        copy_action.triggered.connect(self.copy_note)
        menu.addAction(copy_action)

        paste_action = QAction("Paste", self)
        paste_action.setShortcut("Ctrl+V")
        paste_action.triggered.connect(self.paste_note)
        menu.addAction(paste_action)

        cut_action = QAction("Cut", self)
        cut_action.setShortcut("Ctrl+X")
        cut_action.triggered.connect(self.cut_note)
        menu.addAction(cut_action)

        menu.exec(self.sidebar.mapToGlobal(pos))

    def copy_note(self):
        item = self.sidebar.currentItem()
        if item:
            name = item.text()
            content = self.notes.get(name, "")
            self.clipboard = (name, content)
            # Add copy operation to the undo stack
            self.undo_stack.append(('copy', name, content))

    def paste_note(self):
        if hasattr(self, 'clipboard'):
            copied_note_name, copied_note_content = self.clipboard
            if copied_note_name not in [self.sidebar.item(i).text() for i in range(self.sidebar.count())]:
                unique_name = copied_note_name
            else:
                unique_name = self.generate_unique_name(copied_note_name)
            self.sidebar.addItem(unique_name)
            self.notes[unique_name] = copied_note_content  # Add the copied note to the notes dictionary with an empty content
            self.undo_stack.append(('paste', unique_name))
    
    def generate_unique_name(self, name):
        counter = 1
        unique_name = name
        while unique_name in self.notes:
            unique_name = f"{name} ({counter})"
            counter += 1
        return unique_name

    def cut_note(self):
        item = self.sidebar.currentItem()
        if item:
            name = item.text()
            content = self.notes.get(name, "")
            self.clipboard = (name, content)
            self.sidebar.takeItem(self.sidebar.currentRow())
            self.undo_stack.append(('cut', name, content))

    def undo(self):
        if self.undo_stack:
            action = self.undo_stack.pop()
            if action[0] == 'add':
                name, content = action[1:]
                del self.notes[name]  # Remove the added note
                self.sidebar.takeItem(self.sidebar.count() - 1)  # Remove the last added item from the sidebar
            elif action[0] == 'delete':
                name, content = action[1:]
                self.notes[name] = content  # Restore the deleted note
                self.sidebar.addItem(name)  # Add the deleted note back to the sidebar
            elif action[0] == 'edit':
                name, old_content = action[1:]
                self.notes[name] = old_content  # Restore the previous content

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Import Text File", "", "Text Files (*.txt)")
        if file_path:
            try:
                with open(file_path, 'r') as file:
                    content = file.read()
                    if content:
                        file_name = file_path.split('/')[-1]  # Extract file name from path
                        self.name_input.setText(file_name)  # Set the name input field
                        self.content_input.setPlainText(content)  # Set the content input field
                        self.name_input.setEnabled(True)
                        self.content_input.setEnabled(True)
                        self.name_input.setVisible(True)
                        self.content_input.setVisible(True)
                        self.notes[file_name] = content
                        self.sidebar.addItem(file_name) 
            except Exception as e:
                QMessageBox.critical(self, "Error", f"An error occurred while importing the text file: {str(e)}")

    def view_side_menu(self):
        # Define the method to show the sidebar
        self.sidebar_widget.show()

    def hide_side_menu(self):
        # Define the method to hide the sidebar
        self.sidebar_widget.hide()

    def closeEvent(self, event):
        self.save_notes()
        event.accept()

    def name_changed(self):
        # Update the name in the sidebar when the name input changes
        item = self.sidebar.currentItem()
        if item:
            new_name = self.name_input.text()
            item.setText(new_name)

def main():
    app = QApplication(sys.argv)
    window = NoteTakingApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()