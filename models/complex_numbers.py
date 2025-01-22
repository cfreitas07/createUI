from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QLabel, QPushButton, QLineEdit, QFrame, QTabWidget,
                            QGridLayout, QSlider, QComboBox)
from PyQt6.QtCore import Qt
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.patches import Circle, Arrow

class ComplexNumberVisualizer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Complex Numbers Explorer 🔄")
        self.setGeometry(100, 100, 1200, 900)

        # Create main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)

        # Create tabs
        tabs = QTabWidget()
        tabs.setStyleSheet("""
            QTabWidget {
                background-color: white;
            }
            QTabBar::tab {
                background-color: #f0f0f0;
                color: black;
                padding: 10px 20px;
                margin: 2px;
                border-radius: 8px;
                font-size: 14px;
            }
            QTabBar::tab:selected {
                background-color: #9C27B0;
                color: white;
            }
        """)

        tabs.addTab(self.create_visualization_tab(), "📊 Complex Plane")
        tabs.addTab(self.create_operations_tab(), "🔢 Operations")
        tabs.addTab(self.create_polar_tab(), "🔄 Polar Form")
        
        layout.addWidget(tabs)

    def create_visualization_tab(self):
        frame = QFrame()
        layout = QVBoxLayout(frame)

        # Input controls
        input_layout = QHBoxLayout()
        
        # Real part input
        real_layout = QHBoxLayout()
        real_label = QLabel("Real Part:")
        self.real_input = QLineEdit()
        self.real_input.setPlaceholderText("Enter real part")
        real_layout.addWidget(real_label)
        real_layout.addWidget(self.real_input)
        
        # Imaginary part input
        imag_layout = QHBoxLayout()
        imag_label = QLabel("Imaginary Part:")
        self.imag_input = QLineEdit()
        self.imag_input.setPlaceholderText("Enter imaginary part")
        imag_layout.addWidget(imag_label)
        imag_layout.addWidget(self.imag_input)
        
        # Plot button
        self.plot_button = QPushButton("Plot Number")
        self.plot_button.clicked.connect(self.update_plot)
        
        input_layout.addLayout(real_layout)
        input_layout.addLayout(imag_layout)
        input_layout.addWidget(self.plot_button)
        
        layout.addLayout(input_layout)

        # Create matplotlib figure
        self.figure = Figure(figsize=(12, 8))
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        # Information display
        self.info_display = QLabel()
        self.info_display.setStyleSheet("""
            QLabel {
                background-color: #f8f9fa;
                padding: 15px;
                border-radius: 8px;
                border: 1px solid #dee2e6;
                font-size: 14px;
            }
        """)
        layout.addWidget(self.info_display)

        self.init_plot()
        return frame

    def create_operations_tab(self):
        frame = QFrame()
        layout = QVBoxLayout(frame)

        # Operation selection
        op_layout = QHBoxLayout()
        op_label = QLabel("Operation:")
        self.op_combo = QComboBox()
        self.op_combo.addItems([
            "Addition", "Subtraction", "Multiplication", "Division",
            "Power", "Root", "Conjugate"
        ])
        op_layout.addWidget(op_label)
        op_layout.addWidget(self.op_combo)
        
        # Number inputs
        num1_layout = QHBoxLayout()
        num1_label = QLabel("Number 1:")
        self.num1_real = QLineEdit()
        self.num1_imag = QLineEdit()
        num1_layout.addWidget(num1_label)
        num1_layout.addWidget(self.num1_real)
        num1_layout.addWidget(QLabel("+"))
        num1_layout.addWidget(self.num1_imag)
        num1_layout.addWidget(QLabel("i"))
        
        num2_layout = QHBoxLayout()
        num2_label = QLabel("Number 2:")
        self.num2_real = QLineEdit()
        self.num2_imag = QLineEdit()
        num2_layout.addWidget(num2_label)
        num2_layout.addWidget(self.num2_real)
        num2_layout.addWidget(QLabel("+"))
        num2_layout.addWidget(self.num2_imag)
        num2_layout.addWidget(QLabel("i"))
        
        # Calculate button
        calc_button = QPushButton("Calculate")
        calc_button.clicked.connect(self.perform_operation)
        
        layout.addLayout(op_layout)
        layout.addLayout(num1_layout)
        layout.addLayout(num2_layout)
        layout.addWidget(calc_button)

        # Result plot
        self.op_figure = Figure(figsize=(12, 8))
        self.op_canvas = FigureCanvas(self.op_figure)
        layout.addWidget(self.op_canvas)

        # Operation result display
        self.op_result = QLabel()
        self.op_result.setStyleSheet("""
            QLabel {
                background-color: #f8f9fa;
                padding: 15px;
                border-radius: 8px;
                border: 1px solid #dee2e6;
                font-size: 14px;
            }
        """)
        layout.addWidget(self.op_result)

        return frame

    def create_polar_tab(self):
        frame = QFrame()
        layout = QVBoxLayout(frame)

        # Input controls for polar form
        polar_layout = QHBoxLayout()
        
        # Magnitude input
        mag_layout = QHBoxLayout()
        mag_label = QLabel("Magnitude (r):")
        self.mag_input = QLineEdit()
        mag_layout.addWidget(mag_label)
        mag_layout.addWidget(self.mag_input)
        
        # Angle input
        angle_layout = QHBoxLayout()
        angle_label = QLabel("Angle (θ) in degrees:")
        self.angle_input = QLineEdit()
        angle_layout.addWidget(angle_label)
        angle_layout.addWidget(self.angle_input)
        
        # Convert button
        convert_button = QPushButton("Convert")
        convert_button.clicked.connect(self.convert_polar)
        
        polar_layout.addLayout(mag_layout)
        polar_layout.addLayout(angle_layout)
        polar_layout.addWidget(convert_button)
        
        layout.addLayout(polar_layout)

        # Polar plot
        self.polar_figure = Figure(figsize=(12, 8))
        self.polar_canvas = FigureCanvas(self.polar_figure)
        layout.addWidget(self.polar_canvas)

        # Conversion result display
        self.polar_result = QLabel()
        self.polar_result.setStyleSheet("""
            QLabel {
                background-color: #f8f9fa;
                padding: 15px;
                border-radius: 8px;
                border: 1px solid #dee2e6;
                font-size: 14px;
            }
        """)
        layout.addWidget(self.polar_result)

        return frame

    def init_plot(self):
        """Initialize the complex plane plot"""
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        
        # Set equal aspect ratio
        ax.set_aspect('equal')
        
        # Add grid
        ax.grid(True, linestyle='--', alpha=0.7)
        
        # Add axes
        ax.axhline(y=0, color='k', linestyle='-', alpha=0.5)
        ax.axvline(x=0, color='k', linestyle='-', alpha=0.5)
        
        # Set labels
        ax.set_xlabel('Real Part')
        ax.set_ylabel('Imaginary Part')
        ax.set_title('Complex Plane')
        
        # Set reasonable limits
        ax.set_xlim(-5, 5)
        ax.set_ylim(-5, 5)
        
        self.canvas.draw()

    def update_plot(self):
        """Update plot with new complex number"""
        try:
            real = float(self.real_input.text())
            imag = float(self.imag_input.text())
            
            self.figure.clear()
            ax = self.figure.add_subplot(111)
            
            # Plot complex number
            ax.plot([0, real], [0, imag], 'b-', linewidth=2)
            ax.plot(real, imag, 'bo')
            
            # Add grid and axes
            ax.grid(True, linestyle='--', alpha=0.7)
            ax.axhline(y=0, color='k', linestyle='-', alpha=0.5)
            ax.axvline(x=0, color='k', linestyle='-', alpha=0.5)
            
            # Add unit circle
            circle = Circle((0, 0), 1, fill=False, linestyle='--', alpha=0.5)
            ax.add_artist(circle)
            
            # Set labels and title
            ax.set_xlabel('Real Part')
            ax.set_ylabel('Imaginary Part')
            ax.set_title('Complex Plane')
            
            # Set equal aspect ratio and limits
            ax.set_aspect('equal')
            max_val = max(abs(real), abs(imag), 1) + 1
            ax.set_xlim(-max_val, max_val)
            ax.set_ylim(-max_val, max_val)
            
            self.canvas.draw()
            
            # Update information display
            z = complex(real, imag)
            magnitude = abs(z)
            angle = np.angle(z, deg=True)
            
            info_text = f"""
            <b>Complex Number Analysis:</b><br>
            • Cartesian Form: {real:.2f} + {imag:.2f}i<br>
            • Polar Form: {magnitude:.2f}∠{angle:.2f}°<br>
            • Magnitude: {magnitude:.2f}<br>
            • Angle: {angle:.2f}°<br>
            • Conjugate: {real:.2f} - {imag:.2f}i
            """
            self.info_display.setText(info_text)
            
        except ValueError:
            self.info_display.setText("Please enter valid numbers")

    def perform_operation(self):
        """Perform selected complex number operation"""
        try:
            # Get complex numbers
            z1 = complex(float(self.num1_real.text()), float(self.num1_imag.text()))
            z2 = complex(float(self.num2_real.text()), float(self.num2_imag.text()))
            
            # Perform operation
            operation = self.op_combo.currentText()
            if operation == "Addition":
                result = z1 + z2
            elif operation == "Subtraction":
                result = z1 - z2
            elif operation == "Multiplication":
                result = z1 * z2
            elif operation == "Division":
                result = z1 / z2
            elif operation == "Power":
                result = z1 ** 2
            elif operation == "Root":
                result = z1 ** 0.5
            else:  # Conjugate
                result = z1.conjugate()
            
            # Plot result
            self.op_figure.clear()
            ax = self.op_figure.add_subplot(111)
            
            # Plot original numbers and result
            ax.plot([0, z1.real], [0, z1.imag], 'b-', label='z1', linewidth=2)
            ax.plot(z1.real, z1.imag, 'bo')
            
            if operation != "Conjugate":
                ax.plot([0, z2.real], [0, z2.imag], 'g-', label='z2', linewidth=2)
                ax.plot(z2.real, z2.imag, 'go')
            
            ax.plot([0, result.real], [0, result.imag], 'r-', label='result', linewidth=2)
            ax.plot(result.real, result.imag, 'ro')
            
            # Add grid and axes
            ax.grid(True, linestyle='--', alpha=0.7)
            ax.axhline(y=0, color='k', linestyle='-', alpha=0.5)
            ax.axvline(x=0, color='k', linestyle='-', alpha=0.5)
            
            # Set labels and title
            ax.set_xlabel('Real Part')
            ax.set_ylabel('Imaginary Part')
            ax.set_title(f'Complex {operation}')
            ax.legend()
            
            # Set equal aspect ratio and limits
            ax.set_aspect('equal')
            max_val = max(abs(z1.real), abs(z1.imag), 
                         abs(z2.real), abs(z2.imag),
                         abs(result.real), abs(result.imag)) + 1
            ax.set_xlim(-max_val, max_val)
            ax.set_ylim(-max_val, max_val)
            
            self.op_canvas.draw()
            
            # Update result display
            result_text = f"""
            <b>Operation Result:</b><br>
            • z1 = {z1.real:.2f} + {z1.imag:.2f}i<br>
            • z2 = {z2.real:.2f} + {z2.imag:.2f}i<br>
            • Result = {result.real:.2f} + {result.imag:.2f}i<br>
            • Magnitude = {abs(result):.2f}<br>
            • Angle = {np.angle(result, deg=True):.2f}°
            """
            self.op_result.setText(result_text)
            
        except ValueError:
            self.op_result.setText("Please enter valid numbers")
        except ZeroDivisionError:
            self.op_result.setText("Division by zero is undefined")

    def convert_polar(self):
        """Convert between polar and rectangular forms"""
        try:
            magnitude = float(self.mag_input.text())
            angle = float(self.angle_input.text())
            
            # Convert to rectangular form
            z = magnitude * np.exp(1j * np.deg2rad(angle))
            
            # Plot
            self.polar_figure.clear()
            ax = self.polar_figure.add_subplot(111, projection='polar')
            
            # Plot point
            ax.plot([0, np.deg2rad(angle)], [0, magnitude], 'b-', linewidth=2)
            ax.plot(np.deg2rad(angle), magnitude, 'bo')
            
            # Add grid
            ax.grid(True)
            
            # Set title
            ax.set_title('Polar Form Visualization')
            
            self.polar_canvas.draw()
            
            # Update result display
            result_text = f"""
            <b>Conversion Result:</b><br>
            • Polar Form: {magnitude:.2f}∠{angle:.2f}°<br>
            • Rectangular Form: {z.real:.2f} + {z.imag:.2f}i<br>
            • Magnitude: {magnitude:.2f}<br>
            • Angle: {angle:.2f}°
            """
            self.polar_result.setText(result_text)
            
        except ValueError:
            self.polar_result.setText("Please enter valid numbers") 