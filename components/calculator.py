from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QGridLayout, QPushButton, QLineEdit
import math
import random

class CalculatorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calculator")
        self.setGeometry(100, 100, 500, 400)
        
        # Initialize memory and state variables
        self.memory = 0
        self.current_value = 0
        self.new_number = True
        self.last_operation = None
        self.scientific_mode = False  # For 2nd button functionality

        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Create display
        self.display = QLineEdit('0')
        self.display.setReadOnly(True)
        self.display.setStyleSheet("""
            QLineEdit {
                background-color: #333333;
                color: white;
                padding: 20px;
                font-size: 36px;
                border: none;
                margin-bottom: 1px;
                qproperty-alignment: 'AlignRight';
            }
        """)
        layout.addWidget(self.display)

        # Create button grid
        button_grid = QGridLayout()
        button_grid.setSpacing(1)

        # Button layout (text, row, column, colspan)
        buttons = [
            [('(', 0, 0), (')', 0, 1), ('mc', 0, 2), ('m+', 0, 3), ('m-', 0, 4), ('mr', 0, 5), ('AC', 0, 6), ('±', 0, 7), ('%', 0, 8), ('÷', 0, 9)],
            [('2ⁿᵈ', 1, 0), ('x²', 1, 1), ('x³', 1, 2), ('xʸ', 1, 3), ('eˣ', 1, 4), ('10ˣ', 1, 5), ('7', 1, 6), ('8', 1, 7), ('9', 1, 8), ('×', 1, 9)],
            [('¹/x', 2, 0), ('²√x', 2, 1), ('³√x', 2, 2), ('ʸ√x', 2, 3), ('ln', 2, 4), ('log₁₀', 2, 5), ('4', 2, 6), ('5', 2, 7), ('6', 2, 8), ('−', 2, 9)],
            [('x!', 3, 0), ('sin', 3, 1), ('cos', 3, 2), ('tan', 3, 3), ('e', 3, 4), ('EE', 3, 5), ('1', 3, 6), ('2', 3, 7), ('3', 3, 8), ('+', 3, 9)],
            [('Rad', 4, 0), ('sinh', 4, 1), ('cosh', 4, 2), ('tanh', 4, 3), ('π', 4, 4), ('Rand', 4, 5), ('0', 4, 6, 2), ('.', 4, 8), ('=', 4, 9)]
        ]

        # Button styles
        number_style = """
            QPushButton {
                background-color: #4a4a4a;
                color: white;
                padding: 15px;
                font-size: 16px;
                border: 1px solid #333333;
                border-radius: 0px;
            }
            QPushButton:pressed {
                background-color: #636363;
            }
        """

        function_style = """
            QPushButton {
                background-color: #3a3a3a;
                color: white;
                padding: 15px;
                font-size: 16px;
                border: 1px solid #333333;
                border-radius: 0px;
            }
            QPushButton:pressed {
                background-color: #535353;
            }
        """

        operator_style = """
            QPushButton {
                background-color: #ff9500;
                color: white;
                padding: 15px;
                font-size: 16px;
                border: 1px solid #333333;
                border-radius: 0px;
            }
            QPushButton:pressed {
                background-color: #ffaa33;
            }
        """

        # Add buttons to grid
        for row in buttons:
            for button in row:
                text = button[0]
                r = button[1]
                c = button[2]
                colspan = button[3] if len(button) > 3 else 1
                
                btn = QPushButton(text)
                btn.clicked.connect(self.on_button_click)
                
                # Apply appropriate style
                if text in ['÷', '×', '−', '+', '=']:
                    btn.setStyleSheet(operator_style)
                elif text.isdigit() or text == '.':
                    btn.setStyleSheet(number_style)
                else:
                    btn.setStyleSheet(function_style)
                
                button_grid.addWidget(btn, r, c, 1, colspan)

        layout.addLayout(button_grid)

    def on_button_click(self):
        button = self.sender()
        button_text = button.text()
        current = self.display.text()

        try:
            # Number buttons
            if button_text.isdigit() or button_text == '.':
                if self.new_number:
                    self.display.setText(button_text)
                    self.new_number = False
                else:
                    self.display.setText(current + button_text)
                return

            # Memory operations
            if button_text == 'mc':
                self.memory = 0
            elif button_text == 'm+':
                self.memory += float(current)
            elif button_text == 'm-':
                self.memory -= float(current)
            elif button_text == 'mr':
                self.display.setText(str(self.memory))
                self.new_number = True

            # Clear and modify operations
            elif button_text == 'AC':
                self.display.setText('0')
                self.new_number = True
                self.current_value = 0
                self.last_operation = None
            elif button_text == '±':
                self.display.setText(str(-float(current)))
            elif button_text == '%':
                self.display.setText(str(float(current) / 100))

            # Constants
            elif button_text == 'π':
                self.display.setText(str(math.pi))
                self.new_number = True
            elif button_text == 'e':
                self.display.setText(str(math.e))
                self.new_number = True
            elif button_text == 'Rand':
                self.display.setText(str(random.random()))
                self.new_number = True

            # Scientific operations
            elif button_text == 'x²':
                self.display.setText(str(float(current) ** 2))
                self.new_number = True
            elif button_text == 'x³':
                self.display.setText(str(float(current) ** 3))
                self.new_number = True
            elif button_text == '²√x':
                self.display.setText(str(math.sqrt(float(current))))
                self.new_number = True
            elif button_text == '³√x':
                self.display.setText(str(math.pow(float(current), 1/3)))
                self.new_number = True
            elif button_text == 'sin':
                self.display.setText(str(math.sin(float(current))))
                self.new_number = True
            elif button_text == 'cos':
                self.display.setText(str(math.cos(float(current))))
                self.new_number = True
            elif button_text == 'tan':
                self.display.setText(str(math.tan(float(current))))
                self.new_number = True
            elif button_text == 'ln':
                self.display.setText(str(math.log(float(current))))
                self.new_number = True
            elif button_text == 'log₁₀':
                self.display.setText(str(math.log10(float(current))))
                self.new_number = True
            elif button_text == '¹/x':
                self.display.setText(str(1 / float(current)))
                self.new_number = True
            elif button_text == 'x!':
                n = int(float(current))
                self.display.setText(str(math.factorial(n)))
                self.new_number = True

            # Basic operations
            elif button_text in ['÷', '×', '−', '+']:
                self.current_value = float(current)
                self.last_operation = button_text
                self.new_number = True
            
            # Equals
            elif button_text == '=':
                if self.last_operation:
                    second_value = float(current)
                    if self.last_operation == '÷':
                        result = self.current_value / second_value
                    elif self.last_operation == '×':
                        result = self.current_value * second_value
                    elif self.last_operation == '−':
                        result = self.current_value - second_value
                    elif self.last_operation == '+':
                        result = self.current_value + second_value
                    
                    self.display.setText(str(result))
                    self.current_value = result
                    self.new_number = True
                    self.last_operation = None

        except Exception as e:
            self.display.setText('Error')
            self.new_number = True