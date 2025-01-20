import serial.tools.list_ports
from PyQt6.QtWidgets import QMainWindow, QTextEdit, QVBoxLayout, QWidget, QPushButton, QLabel, QComboBox, QHBoxLayout, QSizePolicy
from PyQt6.QtGui import QPalette, QColor, QFont, QSyntaxHighlighter, QTextCharFormat
from PyQt6.QtCore import Qt
import re

class ArduinoSyntaxHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.highlighting_rules = []

        # Arduino keywords
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor("#d35400"))  # Orange color for keywords
        keywords = [
            "\\bvoid\\b", "\\bint\\b", "\\bboolean\\b", "\\bchar\\b", "\\bunsigned\\b", "\\blong\\b",
            "\\bsetup\\b", "\\bloop\\b", "\\bif\\b", "\\belse\\b", "\\bfor\\b", "\\bwhile\\b", "\\bdo\\b",
            "\\breturn\\b", "\\bbreak\\b", "\\bcontinue\\b", "\\bgoto\\b", "\\bswitch\\b", "\\bcase\\b",
            "\\bdefault\\b", "\\bfloat\\b", "\\bdouble\\b", "\\bbyte\\b", "\\btrue\\b", "\\bfalse\\b"
        ]
        for word in keywords:
            pattern = re.compile(word)
            self.highlighting_rules.append((pattern, keyword_format))

        # Arduino functions
        function_format = QTextCharFormat()
        function_format.setForeground(QColor("#00979c"))  # Teal color for functions
        functions = [
            "\\bdigitalWrite\\b", "\\bdigitalRead\\b", "\\banalogWrite\\b", "\\banalogRead\\b",
            "\\bpinMode\\b", "\\bdelay\\b", "\\bdelayMicroseconds\\b", "\\bmillis\\b", "\\bmicros\\b",
            "\\bSerial\\.begin\\b", "\\bSerial\\.print\\b", "\\bSerial\\.println\\b", "\\bSerial\\.read\\b"
        ]
        for word in functions:
            pattern = re.compile(word)
            self.highlighting_rules.append((pattern, function_format))

        # Numbers
        number_format = QTextCharFormat()
        number_format.setForeground(QColor("#8e44ad"))  # Purple color for numbers
        self.highlighting_rules.append((re.compile("\\b[0-9]+\\b"), number_format))

        # Comments
        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor("#95a5a6"))  # Gray color for comments
        self.highlighting_rules.append((re.compile("//[^\n]*"), comment_format))
        
        # Preprocessor directives
        preprocessor_format = QTextCharFormat()
        preprocessor_format.setForeground(QColor("#16a085"))  # Green color for preprocessor
        self.highlighting_rules.append((re.compile("#[^\n]*"), preprocessor_format))

        # String literals
        string_format = QTextCharFormat()
        string_format.setForeground(QColor("#27ae60"))  # Green color for strings
        self.highlighting_rules.append((re.compile("\".*\""), string_format))

    def highlightBlock(self, text):
        for pattern, format in self.highlighting_rules:
            for match in pattern.finditer(text):
                self.setFormat(match.start(), match.end() - match.start(), format)

class ArduinoIDEEmulator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Arduino IDE Emulator")
        
        # Set initial size
        self.setGeometry(100, 100, 800, 600)
        
        # Set minimum size to ensure usability
        self.setMinimumSize(400, 300)
        
        # Allow resizing
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        # Set window background color to match Arduino IDE
        self.setStyleSheet("""
            QMainWindow {
                background-color: #ffffff;
            }
            QTextEdit {
                background-color: #ffffff;
                color: #000000;
                font-family: Consolas, Monaco, monospace;
                font-size: 13px;
                selection-background-color: #b5d5ff;
            }
            QPushButton {
                background-color: #7cb7f1;
                color: white;
                border: none;
                padding: 5px 15px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #5a9bd5;
            }
            QLabel {
                color: #333333;
            }
            QComboBox {
                background-color: white;
                border: 1px solid #cccccc;
                border-radius: 4px;
                padding: 5px;
            }
        """)

        # Set up the UI
        self.initUI()

    def initUI(self):
        # Main widget
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        # Layout
        layout = QVBoxLayout()

        # Text editor for Arduino code
        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText("Write your Arduino code here...")
        
        # Apply syntax highlighter
        self.highlighter = ArduinoSyntaxHighlighter(self.text_edit.document())
        
        layout.addWidget(self.text_edit)

        # Serial port selection
        port_layout = QHBoxLayout()
        self.port_combo = QComboBox()
        self.refresh_ports()
        port_layout.addWidget(QLabel("Select Port:"))
        port_layout.addWidget(self.port_combo)
        layout.addLayout(port_layout)

        # Buttons
        button_layout = QHBoxLayout()
        verify_button = QPushButton("Verify")
        verify_button.clicked.connect(self.verify_code)
        button_layout.addWidget(verify_button)

        upload_button = QPushButton("Upload")
        upload_button.clicked.connect(self.upload_code)
        button_layout.addWidget(upload_button)

        layout.addLayout(button_layout)

        # Output label
        self.output_label = QLabel("Output:")
        layout.addWidget(self.output_label)

        main_widget.setLayout(layout)

    def refresh_ports(self):
        """Refresh the available serial ports"""
        self.port_combo.clear()
        ports = serial.tools.list_ports.comports()
        for port in ports:
            self.port_combo.addItem(f"{port.device} - {port.description}")

    def verify_code(self):
        """Simulate code verification"""
        code = self.text_edit.toPlainText()
        if code.strip():
            self.output_label.setText("Code verified successfully!")
        else:
            self.output_label.setText("No code to verify.")

    def upload_code(self):
        """Simulate code upload"""
        selected_port = self.port_combo.currentText()
        if selected_port:
            self.output_label.setText(f"Code uploaded to {selected_port.split(' - ')[0]}")
        else:
            self.output_label.setText("No port selected.") 