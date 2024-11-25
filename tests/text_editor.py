from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTextEdit, QPushButton, QHBoxLayout, QFileDialog
)
from PyQt6.QtCore import Qt


class TextEditorWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initializeUI()

    def initializeUI(self):
        """Set up the Text Editor UI."""
        # Main layout
        layout = QVBoxLayout(self)

        # Text area
        self.text_area = QTextEdit()
        layout.addWidget(self.text_area)

        # Buttons layout
        button_layout = QHBoxLayout()

        # Add Copy button
        copy_button = QPushButton("Copy")
        copy_button.clicked.connect(self.copyText)
        button_layout.addWidget(copy_button)

        # Add Paste button
        paste_button = QPushButton("Paste")
        paste_button.clicked.connect(self.pasteText)
        button_layout.addWidget(paste_button)

        # Add Cut button
        cut_button = QPushButton("Cut")
        cut_button.clicked.connect(self.cutText)
        button_layout.addWidget(cut_button)

        # Add Save button
        save_button = QPushButton("Save File")
        save_button.clicked.connect(self.saveText)
        button_layout.addWidget(save_button)

        # Add button layout to the main layout
        layout.addLayout(button_layout)
        self.setLayout(layout)

    def copyText(self):
        """Copy selected text to the clipboard."""
        cursor = self.text_area.textCursor()
        if cursor.hasSelection():
            self.text_area.copy()

    def pasteText(self):
        """Paste text from the clipboard into the text area."""
        self.text_area.paste()

    def cutText(self):
        """Cut selected text to the clipboard."""
        cursor = self.text_area.textCursor()
        if cursor.hasSelection():
            self.text_area.cut()

    def saveText(self):
        """Save text from the editor to a file."""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save File",
            "",
            "Text Files (*.txt);;All Files (*)",
        )
        if file_path:  # If a file path is selected
            with open(file_path, "w") as file:
                file.write(self.text_area.toPlainText())
