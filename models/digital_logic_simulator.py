from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QComboBox, 
                            QPushButton, QLabel, QGridLayout,
                            QHBoxLayout, QFrame, QTableWidget,
                            QTableWidgetItem, QSizePolicy)
from PyQt6.QtCore import Qt, QPropertyAnimation, QRect, QEasingCurve, QTimer, QSize
from PyQt6.QtGui import QColor, QFont
import os

class DigitalLogicSimulator(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.resize(600, 400)

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        # Title
        title = QLabel("Digital Logic Simulator")
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: #2c3e50;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)

        # Content layout
        content_layout = QHBoxLayout()
        
        # Left side controls
        left_container = QFrame()
        left_container.setMaximumWidth(240)
        controls_layout = QVBoxLayout(left_container)
        
        # Input switches frame
        input_frame = QFrame()
        input_frame.setStyleSheet("background-color: #f5f6fa; border-radius: 8px; padding: 8px;")
        input_layout = QVBoxLayout(input_frame)
        
        switch_label = QLabel("Input Switches:")
        switch_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #2c3e50;")
        input_layout.addWidget(switch_label)
        
        switches_layout = QHBoxLayout()
        self.switches = []
        
        for name in ['A', 'B']:
            switch_container = QVBoxLayout()
            
            label = QLabel(name)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setStyleSheet("font-size: 16px; font-weight: bold; color: #2c3e50;")
            switch_container.addWidget(label)
            
            switch = QPushButton()
            switch.setCheckable(True)
            switch.setFixedSize(40, 40)
            switch.clicked.connect(lambda checked, s=switch: self.handle_switch_click(s))
            switch.setStyleSheet("""
                QPushButton {
                    background-color: #e74c3c;
                    border-radius: 20px;
                    border: 2px solid #c0392b;
                }
                QPushButton:checked {
                    background-color: #2ecc71;
                    border: 2px solid #27ae60;
                }
                QPushButton:hover {
                    background-color: #ff6b6b;
                }
                QPushButton:checked:hover {
                    background-color: #5ef198;
                }
            """)
            
            self.switches.append(switch)
            switch_container.addWidget(switch)
            switches_layout.addLayout(switch_container)
        
        input_layout.addLayout(switches_layout)
        controls_layout.addWidget(input_frame)

        # Gate selector
        gate_frame = QFrame()
        gate_frame.setStyleSheet("background-color: #f5f6fa; border-radius: 8px; padding: 8px;")
        gate_layout = QVBoxLayout(gate_frame)
        
        gate_label = QLabel("Select Logic Gate:")
        gate_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #2c3e50;")
        gate_layout.addWidget(gate_label)
        
        self.gate_selector = QComboBox()
        self.gate_selector.addItems(["AND", "OR", "NAND", "NOR", "XOR"])
        self.gate_selector.setStyleSheet("""
            QComboBox {
                background-color: white;
                border: 2px solid #3498db;
                border-radius: 4px;
                padding: 5px;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 2px solid #3498db;
                border-bottom: 2px solid #3498db;
                width: 8px;
                height: 8px;
                transform: rotate(-45deg);
                margin-right: 8px;
            }
        """)
        self.gate_selector.currentTextChanged.connect(self.handle_gate_change)
        gate_layout.addWidget(self.gate_selector)
        
        controls_layout.addWidget(gate_frame)

        # Output display
        output_frame = QFrame()
        output_frame.setStyleSheet("background-color: #f5f6fa; border-radius: 8px; padding: 8px;")
        output_layout = QVBoxLayout(output_frame)
        
        output_label = QLabel("Output:")
        output_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #2c3e50;")
        output_layout.addWidget(output_label)
        
        self.output_display = QPushButton()
        self.output_display.setEnabled(False)
        self.output_display.setFixedSize(65, 65)
        self.output_display.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                border-radius: 32px;
                border: 3px solid #c0392b;
            }
            QPushButton:checked {
                background-color: #2ecc71;
                border: 3px solid #27ae60;
            }
        """)
        output_layout.addWidget(self.output_display, alignment=Qt.AlignmentFlag.AlignCenter)
        
        controls_layout.addWidget(output_frame)
        content_layout.addWidget(left_container)

        # Truth table frame (60% of width)
        truth_frame = QFrame()
        truth_frame.setStyleSheet("""
            QFrame {
                background-color: #f5f6fa;
                border-radius: 8px;
                padding: 8px;
            }
            QTableWidget {
                background-color: white;
                border: none;
            }
            QHeaderView::section {
                background-color: #34495e;
                color: white;
                padding: 4px;
                border: none;
                font-size: 12px;
                font-weight: bold;
            }
        """)
        
        truth_layout = QVBoxLayout(truth_frame)
        truth_layout.setSpacing(5)
        
        truth_label = QLabel("Truth Table:")
        truth_label.setStyleSheet("font-size: 12px; font-weight: bold; color: #2c3e50;")
        truth_layout.addWidget(truth_label)
        
        self.truth_table = QTableWidget()
        self.truth_table.setColumnCount(3)
        self.truth_table.setRowCount(4)
        self.truth_table.setHorizontalHeaderLabels(['A', 'B', 'Output'])
        self.truth_table.verticalHeader().setVisible(False)
        
        # Harmonized column widths
        for i in range(3):
            self.truth_table.setColumnWidth(i, 50)
        # Harmonized row heights
        for i in range(4):
            self.truth_table.setRowHeight(i, 25)
        
        truth_layout.addWidget(self.truth_table)

        # Add equation label
        self.equation_label = QLabel()
        self.equation_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: bold;
                color: #2c3e50;
                padding: 8px;
                background-color: white;
                border-radius: 4px;
            }
        """)
        self.equation_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        truth_layout.addWidget(self.equation_label)
        
        content_layout.addWidget(truth_frame)
        
        main_layout.addLayout(content_layout)
        self.update_simulation()

    def handle_switch_click(self, switch):
        """Handle switch click with bounce animation"""
        anim = QPropertyAnimation(switch, b"geometry")
        anim.setDuration(100)
        anim.setEasingCurve(QEasingCurve.Type.OutBounce)
        
        start_rect = switch.geometry()
        anim.setKeyValueAt(0, start_rect)
        anim.setKeyValueAt(0.3, QRect(start_rect.x(), start_rect.y() - 5, 
                                     start_rect.width(), start_rect.height()))
        anim.setKeyValueAt(1, start_rect)
        
        # Update simulation immediately after state change
        self.update_simulation()
        anim.start()

    def update_simulation(self):
        """Update all simulation components"""
        # Get current state
        inputs = [switch.isChecked() for switch in self.switches]
        gate = self.gate_selector.currentText()
        
        # Calculate output
        output = self.evaluate_gate(inputs, gate)
        
        # Update output display with animation
        anim = QPropertyAnimation(self.output_display, b"geometry")
        anim.setDuration(100)
        anim.setEasingCurve(QEasingCurve.Type.OutBounce)
        
        start_rect = self.output_display.geometry()
        anim.setKeyValueAt(0, start_rect)
        anim.setKeyValueAt(0.3, QRect(start_rect.x(), start_rect.y() - 5, 
                                     start_rect.width(), start_rect.height()))
        anim.setKeyValueAt(1, start_rect)
        
        # Set the output state
        if output:
            self.output_display.setStyleSheet("""
                QPushButton {
                    background-color: #2ecc71;
                    border-radius: 32px;
                    border: 3px solid #27ae60;
                }
            """)
        else:
            self.output_display.setStyleSheet("""
                QPushButton {
                    background-color: #e74c3c;
                    border-radius: 32px;
                    border: 3px solid #c0392b;
                }
            """)
        
        # Update truth table
        self.update_truth_table()
        
        # Start animation
        anim.start()

    def evaluate_gate(self, inputs, gate_type):
        """Evaluate the logic gate output for 2 inputs"""
        a, b = inputs[0], inputs[1]
        
        if gate_type == "AND":
            return a and b
        elif gate_type == "OR":
            return a or b
        elif gate_type == "NAND":
            return not (a and b)
        elif gate_type == "NOR":
            return not (a or b)
        elif gate_type == "XOR":
            return a != b
        return False

    def update_truth_table(self):
        """Update the truth table based on current gate"""
        gate = self.gate_selector.currentText()
        current_inputs = [switch.isChecked() for switch in self.switches]
        
        for row in range(4):
            a = bool(row & 2)
            b = bool(row & 1)
            
            # Create items
            a_item = QTableWidgetItem('1' if a else '0')
            b_item = QTableWidgetItem('1' if b else '0')
            
            # Calculate output
            output = self.evaluate_gate([a, b], gate)
            output_item = QTableWidgetItem('1' if output else '0')
            
            # Style all items
            for item in [a_item, b_item, output_item]:
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                item.setFont(QFont("Arial", 14, QFont.Weight.Bold))
                item.setBackground(Qt.GlobalColor.white)
            
            # Highlight current input combination
            if a == current_inputs[0] and b == current_inputs[1]:
                a_item.setBackground(Qt.GlobalColor.yellow)
                b_item.setBackground(Qt.GlobalColor.yellow)
                output_item.setBackground(QColor("#e8e8e8"))
            
            self.truth_table.setItem(row, 0, a_item)
            self.truth_table.setItem(row, 1, b_item)
            self.truth_table.setItem(row, 2, output_item)
        
        self.equation_label.setText(f"Output = {gate}(A, B)")

    def handle_gate_change(self):
        """Handle gate selection change"""
        self.update_simulation()
        self.update_equation()

    def update_equation(self):
        """Update the equation based on selected gate"""
        gate = self.gate_selector.currentText()
        equations = {
            "AND": "Output = A • B",
            "OR": "Output = A + B",
            "NAND": "Output = (A • B)'",
            "NOR": "Output = (A + B)'",
            "XOR": "Output = A ⊕ B"
        }
        self.equation_label.setText(equations[gate]) 