from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QGridLayout, 
                            QLabel, QFrame, QPushButton, QHBoxLayout,
                            QComboBox, QDialog, QTextEdit, QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
import pyperclip

ARDUINO_CODE = """
// Basic Arduino connection test code
void setup() {
  Serial.begin(115200);
  pinMode(13, OUTPUT);
}

void loop() {
  if (Serial.available() > 0) {
    char command = Serial.read();
    if (command == '1') {
      digitalWrite(13, HIGH);
    }
    else if (command == '0') {
      digitalWrite(13, LOW);
    }
  }
}
"""

class ArduinoInstructionsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent, Qt.WindowType.Dialog)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.setWindowFlags(Qt.WindowType.Dialog | 
                          Qt.WindowType.WindowStaysOnTopHint)
        self.setWindowTitle("Arduino Setup Instructions")
        self.setup_ui()
        
        if parent:
            parent_geo = parent.geometry()
            self.move(parent_geo.center() - self.rect().center())
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Instructions
        instructions = QLabel(
            "Arduino Connection Test Setup:\n\n"
            "1. Open Arduino IDE\n"
            "2. Click the Copy Code button below\n"
            "3. Paste it into Arduino IDE\n"
            "4. Upload to your Arduino\n"
            "5. Close Arduino IDE\n"
            "6. Use the Quick Access toolbar to connect\n"
            "7. Test the connection by controlling the LED"
        )
        instructions.setStyleSheet("font-weight: bold;")
        layout.addWidget(instructions)
        
        # Code display
        self.code_edit = QTextEdit()
        self.code_edit.setPlainText(ARDUINO_CODE)
        self.code_edit.setReadOnly(True)
        font = QFont("Courier New", 10)
        self.code_edit.setFont(font)
        layout.addWidget(self.code_edit)
        
        # Buttons layout
        button_layout = QHBoxLayout()
        
        # Copy button
        copy_btn = QPushButton("Copy Code")
        copy_btn.clicked.connect(self.copy_code)
        button_layout.addWidget(copy_btn)
        
        # Close button
        close_btn = QPushButton("I have uploaded the code")
        close_btn.clicked.connect(self.accept)
        button_layout.addWidget(close_btn)
        
        layout.addLayout(button_layout)
        
        self.setMinimumWidth(500)
        self.setMinimumHeight(400)

    def copy_code(self):
        """Copy the Arduino code to clipboard"""
        pyperclip.copy(ARDUINO_CODE)
        QMessageBox.information(self, "Success", "Code copied to clipboard!")

class ArduinoTest(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.show_instructions()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("Arduino Connection Test")
        title.setStyleSheet("""
            QLabel {
                color: #2c3e50;
                font-size: 16px;
                font-weight: bold;
                margin: 10px 0;
            }
        """)
        layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Instructions Button
        instructions_layout = QHBoxLayout()
        instructions_btn = QPushButton("Show Arduino Instructions")
        instructions_btn.setStyleSheet("""
            QPushButton {
                background-color: #f8f9fa;
                border: 1px solid #ddd;
                padding: 5px 15px;
                border-radius: 4px;
                color: #444;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #e9ecef;
                border-color: #bbb;
            }
        """)
        instructions_btn.clicked.connect(self.show_instructions)
        instructions_layout.addWidget(instructions_btn)
        instructions_layout.addStretch()
        layout.addLayout(instructions_layout)
        
        # Test Frame
        test_frame = QFrame()
        test_frame.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border: 2px solid #ddd;
                border-radius: 10px;
                padding: 15px;
            }
        """)
        test_layout = QVBoxLayout(test_frame)
        
        # Connection Test Section
        test_title = QLabel("Built-in LED Control Test")
        test_title.setStyleSheet("""
            QLabel {
                color: #2c3e50;
                font-size: 14px;
                font-weight: bold;
                margin-bottom: 10px;
            }
        """)
        test_layout.addWidget(test_title)
        
        # LED Button
        self.led_btn = QPushButton("Turn LED On")
        self.led_btn.setCheckable(True)
        self.led_btn.setMinimumHeight(40)
        self.led_btn.clicked.connect(self.toggle_led)
        self.led_btn.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 5px;
                font-weight: bold;
                font-size: 13px;
                min-width: 150px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
            QPushButton:pressed {
                background-color: #1e7e34;
            }
            QPushButton:checked {
                background-color: #dc3545;
            }
            QPushButton:checked:hover {
                background-color: #c82333;
            }
        """)
        test_layout.addWidget(self.led_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Status Label
        self.status_label = QLabel("Test the connection by toggling the LED")
        self.status_label.setStyleSheet("""
            QLabel {
                color: #666;
                font-size: 12px;
                margin-top: 10px;
            }
        """)
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        test_layout.addWidget(self.status_label)
        
        layout.addWidget(test_frame)
        
        # Add stretch to keep widgets at the top
        layout.addStretch()

    def show_instructions(self):
        """Show Arduino setup instructions"""
        dialog = ArduinoInstructionsDialog(self)
        current_pos = self.pos()
        dialog.exec()
        self.move(current_pos)

    def toggle_led(self, checked):
        """Toggle LED to test connection"""
        main_window = self.window()
        if hasattr(main_window, 'serial_connection') and main_window.serial_connection:
            try:
                if checked:
                    main_window.serial_connection.write(b'1')
                    self.led_btn.setText("Turn LED Off")
                    self.status_label.setText("LED is ON - Connection working!")
                    self.status_label.setStyleSheet("""
                        QLabel {
                            color: #28a745;
                            font-size: 12px;
                            font-weight: bold;
                            margin-top: 10px;
                        }
                    """)
                else:
                    main_window.serial_connection.write(b'0')
                    self.led_btn.setText("Turn LED On")
                    self.status_label.setText("LED is OFF - Connection working!")
                    self.status_label.setStyleSheet("""
                        QLabel {
                            color: #666;
                            font-size: 12px;
                            margin-top: 10px;
                        }
                    """)
            except Exception as e:
                QMessageBox.critical(self, "Connection Error", 
                                   f"Failed to communicate with Arduino: {str(e)}")
                self.led_btn.setChecked(False)
                self.led_btn.setText("Turn LED On")
                self.status_label.setText("Connection Error!")
                self.status_label.setStyleSheet("""
                    QLabel {
                        color: #dc3545;
                        font-size: 12px;
                        font-weight: bold;
                        margin-top: 10px;
                    }
                """)
        else:
            QMessageBox.warning(self, "Not Connected", 
                              "Please connect to Arduino using the Quick Access toolbar first!")
            self.led_btn.setChecked(False) 