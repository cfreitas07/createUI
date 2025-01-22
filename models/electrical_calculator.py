from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QLabel, QLineEdit, QPushButton, QComboBox, QFrame,
                            QTabWidget, QGridLayout)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QDoubleValidator
import math

class ElectricalCalculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Electrical Engineering Calculator")
        self.setGeometry(100, 100, 800, 600)

        # Create main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)

        # Title
        title = QLabel("Electrical Engineering Calculator")
        title.setStyleSheet("font-size: 24px; font-weight: bold; margin: 10px; color: black;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Create tab widget
        tab_widget = QTabWidget()
        tab_widget.setStyleSheet("""
            QTabWidget {
                background-color: #f0f0f0;
                color: black;
            }
            QTabBar::tab {
                background-color: #e0e0e0;
                color: black;
                padding: 8px 20px;
                margin: 2px;
            }
            QTabBar::tab:selected {
                background-color: #f0f0f0;
                border-bottom: none;
            }
        """)

        # Add tabs
        tab_widget.addTab(self.create_ohms_law_tab(), "Ohm's Law")
        tab_widget.addTab(self.create_power_tab(), "Power Calculator")
        tab_widget.addTab(self.create_capacitor_tab(), "Capacitor Calculator")
        tab_widget.addTab(self.create_inductor_tab(), "Inductor Calculator")
        tab_widget.addTab(self.create_resonance_tab(), "Resonance Calculator")
        
        layout.addWidget(tab_widget)

    def create_base_frame(self):
        """Create a base frame with common styling"""
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background-color: #f0f0f0;
                border-radius: 10px;
                padding: 20px;
            }
            QLabel {
                font-size: 16px;
                color: black;
            }
            QLineEdit {
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 4px;
                font-size: 14px;
                color: black;
                background-color: white;
            }
            QPushButton {
                padding: 8px 15px;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        return frame

    def create_ohms_law_tab(self):
        """Create Ohm's Law calculator tab"""
        frame = self.create_base_frame()
        layout = QVBoxLayout(frame)

        # Add formula display
        formula_label = QLabel("V = I × R")
        formula_label.setStyleSheet("font-size: 20px; font-weight: bold; margin: 20px; color: black;")
        formula_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(formula_label)

        # Input fields
        grid = QGridLayout()
        
        self.voltage_input = QLineEdit()
        self.voltage_input.setValidator(QDoubleValidator())
        grid.addWidget(QLabel("Voltage (V):"), 0, 0)
        grid.addWidget(self.voltage_input, 0, 1)

        self.current_input = QLineEdit()
        self.current_input.setValidator(QDoubleValidator())
        grid.addWidget(QLabel("Current (A):"), 1, 0)
        grid.addWidget(self.current_input, 1, 1)

        self.resistance_input = QLineEdit()
        self.resistance_input.setValidator(QDoubleValidator())
        grid.addWidget(QLabel("Resistance (Ω):"), 2, 0)
        grid.addWidget(self.resistance_input, 2, 1)

        layout.addLayout(grid)

        # Calculate button
        calc_button = QPushButton("Calculate")
        calc_button.clicked.connect(self.calculate_ohms_law)
        layout.addWidget(calc_button)

        # Results
        self.ohms_result = QLabel("")
        self.ohms_result.setStyleSheet("font-size: 16px; margin-top: 10px; color: black;")
        self.ohms_result.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.ohms_result)

        return frame

    def create_power_tab(self):
        """Create Power calculator tab"""
        frame = self.create_base_frame()
        layout = QVBoxLayout(frame)

        formula_label = QLabel("P = V × I = I²R = V²/R")
        formula_label.setStyleSheet("font-size: 20px; font-weight: bold; margin: 20px; color: black;")
        formula_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(formula_label)

        grid = QGridLayout()
        
        self.power_voltage = QLineEdit()
        self.power_voltage.setValidator(QDoubleValidator())
        grid.addWidget(QLabel("Voltage (V):"), 0, 0)
        grid.addWidget(self.power_voltage, 0, 1)

        self.power_current = QLineEdit()
        self.power_current.setValidator(QDoubleValidator())
        grid.addWidget(QLabel("Current (A):"), 1, 0)
        grid.addWidget(self.power_current, 1, 1)

        self.power_resistance = QLineEdit()
        self.power_resistance.setValidator(QDoubleValidator())
        grid.addWidget(QLabel("Resistance (Ω):"), 2, 0)
        grid.addWidget(self.power_resistance, 2, 1)

        layout.addLayout(grid)

        calc_button = QPushButton("Calculate Power")
        calc_button.clicked.connect(self.calculate_power)
        layout.addWidget(calc_button)

        self.power_result = QLabel("")
        self.power_result.setStyleSheet("font-size: 16px; margin-top: 10px; color: black;")
        self.power_result.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.power_result)

        return frame

    def create_capacitor_tab(self):
        """Create Capacitor calculator tab"""
        frame = self.create_base_frame()
        layout = QVBoxLayout(frame)

        formula_label = QLabel("Xc = 1/(2πfC)")
        formula_label.setStyleSheet("font-size: 20px; font-weight: bold; margin: 20px; color: black;")
        formula_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(formula_label)

        grid = QGridLayout()
        
        self.capacitance = QLineEdit()
        self.capacitance.setValidator(QDoubleValidator())
        grid.addWidget(QLabel("Capacitance (F):"), 0, 0)
        grid.addWidget(self.capacitance, 0, 1)

        self.cap_frequency = QLineEdit()
        self.cap_frequency.setValidator(QDoubleValidator())
        grid.addWidget(QLabel("Frequency (Hz):"), 1, 0)
        grid.addWidget(self.cap_frequency, 1, 1)

        layout.addLayout(grid)

        calc_button = QPushButton("Calculate Reactance")
        calc_button.clicked.connect(self.calculate_capacitive_reactance)
        layout.addWidget(calc_button)

        self.capacitor_result = QLabel("")
        self.capacitor_result.setStyleSheet("font-size: 16px; margin-top: 10px; color: black;")
        self.capacitor_result.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.capacitor_result)

        return frame

    def create_inductor_tab(self):
        """Create Inductor calculator tab"""
        frame = self.create_base_frame()
        layout = QVBoxLayout(frame)

        formula_label = QLabel("XL = 2πfL")
        formula_label.setStyleSheet("font-size: 20px; font-weight: bold; margin: 20px; color: black;")
        formula_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(formula_label)

        grid = QGridLayout()
        
        self.inductance = QLineEdit()
        self.inductance.setValidator(QDoubleValidator())
        grid.addWidget(QLabel("Inductance (H):"), 0, 0)
        grid.addWidget(self.inductance, 0, 1)

        self.ind_frequency = QLineEdit()
        self.ind_frequency.setValidator(QDoubleValidator())
        grid.addWidget(QLabel("Frequency (Hz):"), 1, 0)
        grid.addWidget(self.ind_frequency, 1, 1)

        layout.addLayout(grid)

        calc_button = QPushButton("Calculate Reactance")
        calc_button.clicked.connect(self.calculate_inductive_reactance)
        layout.addWidget(calc_button)

        self.inductor_result = QLabel("")
        self.inductor_result.setStyleSheet("font-size: 16px; margin-top: 10px; color: black;")
        self.inductor_result.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.inductor_result)

        return frame

    def create_resonance_tab(self):
        """Create Resonance calculator tab"""
        frame = self.create_base_frame()
        layout = QVBoxLayout(frame)

        formula_label = QLabel("fr = 1/(2π√(LC))")
        formula_label.setStyleSheet("font-size: 20px; font-weight: bold; margin: 20px; color: black;")
        formula_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(formula_label)

        grid = QGridLayout()
        
        self.res_inductance = QLineEdit()
        self.res_inductance.setValidator(QDoubleValidator())
        grid.addWidget(QLabel("Inductance (H):"), 0, 0)
        grid.addWidget(self.res_inductance, 0, 1)

        self.res_capacitance = QLineEdit()
        self.res_capacitance.setValidator(QDoubleValidator())
        grid.addWidget(QLabel("Capacitance (F):"), 1, 0)
        grid.addWidget(self.res_capacitance, 1, 1)

        layout.addLayout(grid)

        calc_button = QPushButton("Calculate Resonant Frequency")
        calc_button.clicked.connect(self.calculate_resonance)
        layout.addWidget(calc_button)

        self.resonance_result = QLabel("")
        self.resonance_result.setStyleSheet("font-size: 16px; margin-top: 10px; color: black;")
        self.resonance_result.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.resonance_result)

        return frame

    def calculate_ohms_law(self):
        try:
            v = self.voltage_input.text()
            i = self.current_input.text()
            r = self.resistance_input.text()

            if v and i and not r:
                resistance = float(v) / float(i)
                self.resistance_input.setText(f"{resistance:.2f}")
                self.ohms_result.setText(f"Calculated Resistance: {resistance:.2f} Ω")
            elif v and r and not i:
                current = float(v) / float(r)
                self.current_input.setText(f"{current:.2f}")
                self.ohms_result.setText(f"Calculated Current: {current:.2f} A")
            elif i and r and not v:
                voltage = float(i) * float(r)
                self.voltage_input.setText(f"{voltage:.2f}")
                self.ohms_result.setText(f"Calculated Voltage: {voltage:.2f} V")
            else:
                self.ohms_result.setText("Please provide exactly two values")
        except Exception as e:
            self.ohms_result.setText(f"Error: {str(e)}")

    def calculate_power(self):
        try:
            v = self.power_voltage.text()
            i = self.power_current.text()
            r = self.power_resistance.text()

            if v and i:
                power = float(v) * float(i)
            elif v and r:
                power = float(v) ** 2 / float(r)
            elif i and r:
                power = float(i) ** 2 * float(r)
            else:
                self.power_result.setText("Please provide at least two values")
                return

            self.power_result.setText(f"Power: {power:.2f} Watts")
        except Exception as e:
            self.power_result.setText(f"Error: {str(e)}")

    def calculate_capacitive_reactance(self):
        try:
            c = float(self.capacitance.text())
            f = float(self.cap_frequency.text())
            xc = 1 / (2 * math.pi * f * c)
            self.capacitor_result.setText(f"Capacitive Reactance: {xc:.2f} Ω")
        except Exception as e:
            self.capacitor_result.setText(f"Error: {str(e)}")

    def calculate_inductive_reactance(self):
        try:
            l = float(self.inductance.text())
            f = float(self.ind_frequency.text())
            xl = 2 * math.pi * f * l
            self.inductor_result.setText(f"Inductive Reactance: {xl:.2f} Ω")
        except Exception as e:
            self.inductor_result.setText(f"Error: {str(e)}")

    def calculate_resonance(self):
        try:
            l = float(self.res_inductance.text())
            c = float(self.res_capacitance.text())
            fr = 1 / (2 * math.pi * math.sqrt(l * c))
            self.resonance_result.setText(f"Resonant Frequency: {fr:.2f} Hz")
        except Exception as e:
            self.resonance_result.setText(f"Error: {str(e)}") 