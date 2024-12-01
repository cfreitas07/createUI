from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLineEdit, QGridLayout
from PyQt6.QtCore import Qt
import math

class CalculatorWindow(QWidget):
    # Class variable to store the last state
    _last_state = ""

    def __init__(self):
        super().__init__()
        self.initializeUI()
        
        # Restore the last state if it exists
        if self._last_state:
            self.display.setText(self._last_state)

    def initializeUI(self):
        """Set up the calculator UI."""
        layout = QVBoxLayout(self)

        # Display for calculator
        self.display = QLineEdit()
        self.display.setReadOnly(False)  # Allow keyboard input
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.display.setPlaceholderText("0")
        self.display.setStyleSheet("font-size: 24px; padding: 10px;")
        layout.addWidget(self.display)

        # Calculator buttons
        button_layout = QGridLayout()
        buttons = [
            ('7', 0, 0), ('8', 0, 1), ('9', 0, 2), ('/', 0, 3),
            ('4', 1, 0), ('5', 1, 1), ('6', 1, 2), ('*', 1, 3),
            ('1', 2, 0), ('2', 2, 1), ('3', 2, 2), ('-', 2, 3),
            ('0', 3, 0), ('.', 3, 1), ('=', 3, 2), ('+', 3, 3),
            ('(', 4, 0), (')', 4, 1), ('√', 4, 2), ('^', 4, 3),
            ('sin', 5, 0), ('cos', 5, 1), ('tan', 5, 2), ('DEL', 5, 3),
            ('CE', 6, 0),  # Clear Entry
        ]

        # Add buttons to the grid layout
        for text, row, col in buttons:
            button = QPushButton(text)
            button.setStyleSheet("font-size: 18px; padding: 10px;")
            button.clicked.connect(lambda checked, t=text: self.onButtonClick(t))
            button_layout.addWidget(button, row, col)

        layout.addLayout(button_layout)

        # Set the main layout
        self.setLayout(layout)

    def onButtonClick(self, button_text):
        """Handle button clicks."""
        current_text = self.display.text()

        if button_text == '=':
            try:
                # Safely evaluate the input
                result = self.safeEval(current_text)
                self.display.setText(str(result))
                # Save the result as the last state
                CalculatorWindow._last_state = str(result)
            except Exception:
                self.display.setText("Error")
                CalculatorWindow._last_state = "Error"
        elif button_text == 'CE':
            self.display.clear()  # Clear everything
            CalculatorWindow._last_state = ""
        elif button_text == 'DEL':
            new_text = current_text[:-1]
            self.display.setText(new_text)
            CalculatorWindow._last_state = new_text
        elif button_text == '√':
            try:
                # Compute square root
                result = math.sqrt(float(current_text))
                self.display.setText(str(result))
                CalculatorWindow._last_state = str(result)
            except Exception:
                self.display.setText("Error")
                CalculatorWindow._last_state = "Error"
        elif button_text in ['sin', 'cos', 'tan']:
            try:
                angle = math.radians(float(current_text))  # Convert degrees to radians
                if button_text == 'sin':
                    result = math.sin(angle)
                elif button_text == 'cos':
                    result = math.cos(angle)
                elif button_text == 'tan':
                    result = math.tan(angle)
                self.display.setText(str(result))
                CalculatorWindow._last_state = str(result)
            except Exception:
                self.display.setText("Error")
                CalculatorWindow._last_state = "Error"
        else:
            new_text = current_text + button_text
            self.display.setText(new_text)
            CalculatorWindow._last_state = new_text

    def safeEval(self, expression):
        """Safely evaluate mathematical expressions."""
        # Replace common math operators with their Python equivalents
        expression = expression.replace('^', '**')  # Power operator
        return eval(expression, {"__builtins__": None}, math.__dict__)

    def keyPressEvent(self, event):
        """Handle keyboard input."""
        key = event.key()
        if key in (Qt.Key.Key_Enter, Qt.Key.Key_Return):
            self.onButtonClick('=')
        elif key == Qt.Key.Key_Backspace:
            self.onButtonClick('DEL')
        elif key == Qt.Key.Key_Escape:
            self.onButtonClick('CE')
        else:
            # Add the typed character to the display
            self.display.setText(self.display.text() + event.text())