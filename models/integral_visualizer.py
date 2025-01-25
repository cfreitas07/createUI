from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                            QLabel, QComboBox, QSpinBox, QDoubleSpinBox, QGroupBox, QGridLayout, QSlider)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QPen, QColor, QBrush, QPainterPath, QFont, QPixmap
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib
matplotlib.use('Qt5Agg')

class IntegralVisualizer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        main_layout = QHBoxLayout(self)
        left_panel = QVBoxLayout()
        
        # Function Selection Group
        function_group = QGroupBox("Functions")
        function_group.setStyleSheet("""
            QGroupBox {
                font-size: 14px;
                font-weight: bold;
                border: 2px solid #bdc3c7;
                border-radius: 8px;
                margin-top: 10px;
                padding: 15px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
        """)
        
        function_layout = QGridLayout()
        
        # Upper Function
        upper_label = QLabel("Upper Function:")
        upper_label.setStyleSheet("color: #3498db; font-weight: bold;")
        self.upper_function = QComboBox()
        self.upper_function.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border: 2px solid #3498db;
                border-radius: 5px;
                min-width: 150px;
                background: white;
            }
            QComboBox::drop-down {
                border: none;
                background: #3498db;
                width: 30px;
            }
            QComboBox::down-arrow {
                image: none;
                border-top: 6px solid white;
                border-left: 4px solid transparent;
                border-right: 4px solid transparent;
                margin-top: 2px;
            }
        """)
        
        # Lower Function
        lower_label = QLabel("Lower Function:")
        lower_label.setStyleSheet("color: #2ecc71; font-weight: bold;")
        self.lower_function = QComboBox()
        self.lower_function.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border: 2px solid #2ecc71;
                border-radius: 5px;
                min-width: 150px;
                background: white;
            }
            QComboBox::drop-down {
                border: none;
                background: #2ecc71;
                width: 30px;
            }
            QComboBox::down-arrow {
                image: none;
                border-top: 6px solid white;
                border-left: 4px solid transparent;
                border-right: 4px solid transparent;
                margin-top: 2px;
            }
        """)
        
        # Interval Group
        interval_group = QGroupBox("Interval")
        interval_group.setStyleSheet("""
            QGroupBox {
                font-size: 14px;
                font-weight: bold;
                border: 2px solid #bdc3c7;
                border-radius: 8px;
                margin-top: 10px;
                padding: 15px;
            }
        """)
        
        interval_layout = QVBoxLayout()
        
        # Slider Layout
        slider_layout = QHBoxLayout()
        
        # From Slider
        from_layout = QVBoxLayout()
        from_label = QLabel("From:")
        self.from_slider = QSlider(Qt.Orientation.Horizontal)
        self.from_slider.setRange(-100, 100)
        self.from_slider.setValue(0)
        self.from_value = QLabel("0.0")
        self.from_slider.setStyleSheet("""
            QSlider::groove:horizontal {
                height: 8px;
                background: #e0e0e0;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: #9b59b6;
                width: 18px;
                height: 18px;
                margin: -5px 0;
                border-radius: 9px;
            }
            QSlider::sub-page:horizontal {
                background: #9b59b6;
                border-radius: 4px;
            }
        """)
        
        # To Slider
        to_layout = QVBoxLayout()
        to_label = QLabel("To:")
        self.to_slider = QSlider(Qt.Orientation.Horizontal)
        self.to_slider.setRange(-100, 100)
        self.to_slider.setValue(50)
        self.to_value = QLabel("5.0")
        self.to_slider.setStyleSheet(self.from_slider.styleSheet())
        
        # Add widgets to layouts
        function_layout.addWidget(upper_label, 0, 0)
        function_layout.addWidget(self.upper_function, 0, 1)
        function_layout.addWidget(lower_label, 1, 0)
        function_layout.addWidget(self.lower_function, 1, 1)
        function_group.setLayout(function_layout)
        
        from_layout.addWidget(from_label)
        from_layout.addWidget(self.from_slider)
        from_layout.addWidget(self.from_value)
        
        to_layout.addWidget(to_label)
        to_layout.addWidget(self.to_slider)
        to_layout.addWidget(self.to_value)
        
        slider_layout.addLayout(from_layout)
        slider_layout.addLayout(to_layout)
        interval_layout.addLayout(slider_layout)
        interval_group.setLayout(interval_layout)
        
        # Connect slider signals
        self.from_slider.valueChanged.connect(self.update_from_value)
        self.to_slider.valueChanged.connect(self.update_to_value)
        
        # Add groups to left panel
        left_panel.addWidget(function_group)
        left_panel.addWidget(interval_group)
        left_panel.addStretch()
        
        main_layout.addLayout(left_panel)

        # Graph area
        self.graph = GraphWidget()
        self.graph.setMinimumHeight(400)
        self.graph.setStyleSheet("""
            background-color: white;
            border: 2px solid #3498db;
            border-radius: 10px;
        """)
        left_panel.addWidget(self.graph)

        # Right panel - Steps and Equations
        right_panel = QVBoxLayout()
        
        # Title for steps
        steps_title = QLabel("Integration Process")
        steps_title.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #2c3e50;
                margin: 10px 0;
            }
        """)
        right_panel.addWidget(steps_title)

        # Steps display
        self.steps_display = QLabel()
        self.steps_display.setWordWrap(True)
        self.steps_display.setStyleSheet("""
            QLabel {
                font-size: 14px;
                padding: 15px;
                background-color: white;
                border: 2px solid #3498db;
                border-radius: 10px;
                margin: 10px 0;
            }
        """)
        right_panel.addWidget(self.steps_display)

        # Equation display
        self.equation_figure = Figure(figsize=(6, 3), dpi=100)
        self.equation_canvas = FigureCanvas(self.equation_figure)
        right_panel.addWidget(self.equation_canvas)

        # Final result
        self.result_label = QLabel()
        self.result_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                padding: 15px;
                background-color: #f8f9fa;
                border-radius: 8px;
                margin: 10px 0;
                font-weight: bold;
            }
        """)
        right_panel.addWidget(self.result_label)

        # Add stretch to push everything up
        right_panel.addStretch()

        # Add both panels to main layout with equal width
        main_layout.addLayout(right_panel, 1)

        # Initial update
        self.update_graph()

        # Add function options with default selections
        upper_functions = [
            "x²", 
            "x³/3",
            "2x + 1",
            "sin(x) + 2",
            "√x + 1",
            "e^x",
            "ln(x)",
            "cos(x)",
            "tan(x)",
            "x⁴/4",
            "|x|",
            "1/x"
        ]
        
        lower_functions = [
            "0",
            "x",
            "-x + 1",
            "sin(x)",
            "-x²/2",
            "-x³/3",
            "-|x|",
            "-e^x",
            "-ln(x)",
            "-cos(x)",
            "-1/x",
            "-√x"
        ]
        
        # Add items and set defaults
        self.upper_function.addItems(upper_functions)
        self.lower_function.addItems(lower_functions)
        
        # Set default selections
        self.upper_function.setCurrentText("x²")
        self.lower_function.setCurrentText("0")
        
        # Connect signals after setting defaults
        self.upper_function.currentTextChanged.connect(self.update_graph)
        self.lower_function.currentTextChanged.connect(self.update_graph)

    def evaluate_function(self, func_str, x):
        """Evaluate the selected function with error handling"""
        if not func_str:  # Handle empty string case
            return np.zeros_like(x)
        
        function_map = {
            "x²": lambda x: x**2,
            "x³/3": lambda x: x**3/3,
            "2x + 1": lambda x: 2*x + 1,
            "sin(x) + 2": lambda x: np.sin(x) + 2,
            "√x + 1": lambda x: np.sqrt(np.abs(x)) + 1,
            "e^x": lambda x: np.exp(x),
            "ln(x)": lambda x: np.log(np.abs(x) + 1e-10),
            "cos(x)": lambda x: np.cos(x),
            "tan(x)": lambda x: np.tan(x),
            "x⁴/4": lambda x: x**4/4,
            "|x|": lambda x: np.abs(x),
            "1/x": lambda x: 1/(x + 1e-10),
            "0": lambda x: np.zeros_like(x),
            "x": lambda x: x,
            "-x + 1": lambda x: -x + 1,
            "-x²/2": lambda x: -x**2/2,
            "-x³/3": lambda x: -x**3/3,
            "-|x|": lambda x: -np.abs(x),
            "-e^x": lambda x: -np.exp(x),
            "-ln(x)": lambda x: -np.log(np.abs(x) + 1e-10),
            "-cos(x)": lambda x: -np.cos(x),
            "-1/x": lambda x: -1/(x + 1e-10),
            "-√x": lambda x: -np.sqrt(np.abs(x))
        }
        
        # Return zeros if function not found
        return function_map.get(func_str, lambda x: np.zeros_like(x))(x)

    def update_graph(self):
        try:
            # Get current values with error checking
            upper_func = self.upper_function.currentText() or "x²"
            lower_func = self.lower_function.currentText() or "0"
            
            a = self.from_slider.value() / 10.0
            b = self.to_slider.value() / 10.0
            
            if a >= b:
                self.result_label.setText("Invalid interval: start must be less than end")
                return
            
            x = np.linspace(a, b, 200)
            
            upper = self.evaluate_function(upper_func, x)
            lower = self.evaluate_function(lower_func, x)
            
            # Calculate area using numerical integration
            dx = (b - a) / 199
            area = np.sum((upper - lower) * dx)
            
            # Update graph
            self.graph.update_data(x, upper, lower, upper_func, lower_func)
            
            # Update steps and equations
            self.update_steps_and_equations(upper_func, lower_func, a, b, dx, area)
            
        except Exception as e:
            print(f"Error updating graph: {e}")
            # Set to default state if error occurs
            self.upper_function.setCurrentText("x²")
            self.lower_function.setCurrentText("0")

    def update_steps_and_equations(self, upper_func, lower_func, a, b, dx, area):
        # Update steps display
        steps_text = f"""
            <h3>Step-by-Step Solution:</h3>
            <p>1. Identify the functions:
               <br>• Upper function: f(x) = {upper_func}
               <br>• Lower function: g(x) = {lower_func}</p>
            <p>2. Set up the integral:
               <br>• Interval: [{a:.1f}, {b:.1f}]
               <br>• Area = ∫[f(x) - g(x)]dx</p>
            <p>3. Numerical Integration:
               <br>• Divide interval into small segments (Δx = {dx:.4f})
               <br>• Sum the areas of rectangles</p>
            <p>4. Calculate the area:
               <br>• Using numerical integration
               <br>• Number of segments: {int((b-a)/dx)}</p>
        """
        self.steps_display.setText(steps_text)
        
        # Update equation display
        self.update_equation_display(upper_func, lower_func, a, b, dx, area)
        
        # Update final result
        self.result_label.setText(f"Final Area = {area:.4f} square units")

    def update_equation_display(self, upper_func, lower_func, a, b, dx, area):
        # Clear previous equation
        self.equation_figure.clear()
        ax = self.equation_figure.add_subplot(111)
        ax.axis('off')
        
        # Convert function strings to LaTeX
        upper_latex = self.convert_to_latex(upper_func)
        lower_latex = self.convert_to_latex(lower_func)
        
        # Create full equation text with proper LaTeX syntax
        equation = (
            r"$\int_{" + f"{a:.1f}" + r"}^{" + f"{b:.1f}" + r"} "
            r"[" + upper_latex + r" - (" + lower_latex + r")] dx$"
            "\n"
            r"$\sum [f(x_i) - g(x_i)]\Delta x, \Delta x = " + f"{dx:.4f}$"
            "\n"
            r"$\mathrm{Area} = " + f"{area:.4f}$ square units"
        )
        
        # Display equation with proper font size and centering
        ax.text(0.5, 0.5, equation,
                horizontalalignment='center',
                verticalalignment='center',
                transform=ax.transAxes,
                fontsize=12)
        
        # Update the figure
        self.equation_canvas.draw()

    def convert_to_latex(self, func_str):
        # Convert function strings to proper LaTeX notation
        latex_map = {
            "x²": "x^2",
            "2x + 1": "2x + 1",
            "sin(x) + 2": r"\sin(x) + 2",
            "x³/3": r"\frac{x^3}{3}",
            "√x + 1": r"\sqrt{x} + 1",
            "e^x": "e^x",
            "0": "0",
            "x": "x",
            "-x + 1": "-x + 1",
            "sin(x)": r"\sin(x)",
            "-x²/2": r"-\frac{x^2}{2}",
            "ln(x)": r"\ln(x)"
        }
        return latex_map.get(func_str, func_str)

    def update_from_value(self, value):
        scaled_value = value / 10.0
        self.from_value.setText(f"{scaled_value:.1f}")
        self.update_graph()

    def update_to_value(self, value):
        scaled_value = value / 10.0
        self.to_value.setText(f"{scaled_value:.1f}")
        self.update_graph()

class GraphWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.figure = Figure(figsize=(8, 6), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        layout = QVBoxLayout(self)
        layout.addWidget(self.canvas)
        
        # Initialize data
        self.x_data = None
        self.upper_data = None
        self.lower_data = None
        self.upper_func = None
        self.lower_func = None

    def update_data(self, x, upper, lower, upper_func, lower_func):
        self.x_data = x
        self.upper_data = upper
        self.lower_data = lower
        self.upper_func = upper_func
        self.lower_func = lower_func
        self.plot_data()

    def plot_data(self):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        
        # Plot filled area
        ax.fill_between(self.x_data, self.lower_data, self.upper_data, 
                       alpha=0.3, color='#3498db')
        
        # Plot functions
        ax.plot(self.x_data, self.upper_data, '-', 
                color='#3498db', label=f'f(x) = {self.upper_func}')
        ax.plot(self.x_data, self.lower_data, '-', 
                color='#2ecc71', label=f'g(x) = {self.lower_func}')
        
        # Customize plot
        ax.grid(True, linestyle='--', alpha=0.7)
        ax.set_xlabel('x', fontsize=12)
        ax.set_ylabel('y', fontsize=12)
        ax.legend(fontsize=10)
        
        # Use LaTeX for tick labels
        ax.set_title('Area Between Curves', fontsize=14)
        
        self.figure.tight_layout()
        self.canvas.draw() 