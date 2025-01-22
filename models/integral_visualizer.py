from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QLabel, QPushButton, QLineEdit, QFrame, QTabWidget,
                            QGridLayout, QSlider, QComboBox, QSpinBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QPen, QColor, QFont
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.patches import Rectangle

class IntegralVisualizer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Integral Explorer 📐")
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
                background-color: #4CAF50;
                color: white;
            }
        """)

        tabs.addTab(self.create_riemann_tab(), "📊 Riemann Sums")
        tabs.addTab(self.create_applications_tab(), "🔧 Applications")
        tabs.addTab(self.create_learn_tab(), "📚 Quick Guide")
        
        layout.addWidget(tabs)

    def create_riemann_tab(self):
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                padding: 20px;
            }
            QLabel {
                color: black;
                font-size: 14px;
            }
            QComboBox {
                padding: 5px;
                border: 2px solid #4CAF50;
                border-radius: 5px;
                background: white;
            }
            QPushButton {
                padding: 10px 20px;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QSpinBox {
                padding: 5px;
                border: 2px solid #4CAF50;
                border-radius: 5px;
            }
        """)
        
        layout = QVBoxLayout(frame)

        # Function selection
        function_layout = QHBoxLayout()
        function_label = QLabel("Select Function:")
        self.function_combo = QComboBox()
        self.function_combo.addItems([
            "x²", "x³", "sin(x)", "e^x", "1/x", "√x"
        ])
        self.function_combo.currentTextChanged.connect(self.update_plot)
        function_layout.addWidget(function_label)
        function_layout.addWidget(self.function_combo)
        
        # Riemann sum type
        sum_type_label = QLabel("Sum Type:")
        self.sum_type_combo = QComboBox()
        self.sum_type_combo.addItems(["Left", "Right", "Midpoint", "Trapezoidal"])
        self.sum_type_combo.currentTextChanged.connect(self.update_plot)
        function_layout.addWidget(sum_type_label)
        function_layout.addWidget(self.sum_type_combo)
        
        # Number of rectangles
        n_rect_label = QLabel("Rectangles:")
        self.n_rect_spin = QSpinBox()
        self.n_rect_spin.setRange(1, 100)
        self.n_rect_spin.setValue(10)
        self.n_rect_spin.valueChanged.connect(self.update_plot)
        function_layout.addWidget(n_rect_label)
        function_layout.addWidget(self.n_rect_spin)
        
        function_layout.addStretch()
        layout.addLayout(function_layout)

        # Create matplotlib figure
        self.figure = Figure(figsize=(12, 6))
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        # Integration bounds
        bounds_layout = QHBoxLayout()
        
        # Lower bound
        lower_label = QLabel("Lower Bound:")
        self.lower_bound = QSlider(Qt.Orientation.Horizontal)
        self.lower_bound.setMinimum(-50)
        self.lower_bound.setMaximum(50)
        self.lower_bound.setValue(0)
        self.lower_bound.valueChanged.connect(self.update_plot)
        self.lower_value = QLabel("0.0")
        
        # Upper bound
        upper_label = QLabel("Upper Bound:")
        self.upper_bound = QSlider(Qt.Orientation.Horizontal)
        self.upper_bound.setMinimum(-50)
        self.upper_bound.setMaximum(50)
        self.upper_bound.setValue(10)
        self.upper_bound.valueChanged.connect(self.update_plot)
        self.upper_value = QLabel("1.0")
        
        bounds_layout.addWidget(lower_label)
        bounds_layout.addWidget(self.lower_bound)
        bounds_layout.addWidget(self.lower_value)
        bounds_layout.addWidget(upper_label)
        bounds_layout.addWidget(self.upper_bound)
        bounds_layout.addWidget(self.upper_value)
        
        layout.addLayout(bounds_layout)

        # Information display
        self.info_display = QLabel()
        self.info_display.setStyleSheet("""
            QLabel {
                background-color: #f8f9fa;
                padding: 15px;
                border-radius: 8px;
                border: 1px solid #dee2e6;
            }
        """)
        layout.addWidget(self.info_display)

        self.update_plot()
        return frame

    def create_applications_tab(self):
        frame = QFrame()
        layout = QVBoxLayout(frame)

        # Application selection
        app_layout = QHBoxLayout()
        app_label = QLabel("Select Application:")
        self.app_combo = QComboBox()
        self.app_combo.addItems([
            "Area Under Curve",
            "Work Done",
            "Fluid Pressure",
            "Center of Mass"
        ])
        self.app_combo.currentTextChanged.connect(self.update_application)
        app_layout.addWidget(app_label)
        app_layout.addWidget(self.app_combo)
        app_layout.addStretch()
        layout.addLayout(app_layout)

        # Create matplotlib figure for applications
        self.app_figure = Figure(figsize=(12, 6))
        self.app_canvas = FigureCanvas(self.app_figure)
        layout.addWidget(self.app_canvas)

        # Application info
        self.app_info = QLabel()
        self.app_info.setStyleSheet("""
            QLabel {
                background-color: #f8f9fa;
                padding: 15px;
                border-radius: 8px;
                border: 1px solid #dee2e6;
            }
        """)
        layout.addWidget(self.app_info)

        self.update_application()
        return frame

    def create_learn_tab(self):
        frame = QFrame()
        layout = QVBoxLayout(frame)

        guide = QLabel("""
        <h2>📚 Understanding Integration</h2>
        
        <h3>🎯 Key Concepts:</h3>
        <ul>
            <li><b>Definite Integral:</b> Area between function and x-axis</li>
            <li><b>Riemann Sums:</b> Approximating area using rectangles</li>
            <li><b>Fundamental Theorem:</b> Connection between derivatives and integrals</li>
        </ul>

        <h3>📐 Common Integrals:</h3>
        <ul>
            <li>∫x dx = x²/2 + C</li>
            <li>∫x² dx = x³/3 + C</li>
            <li>∫sin(x) dx = -cos(x) + C</li>
            <li>∫e^x dx = e^x + C</li>
            <li>∫(1/x) dx = ln|x| + C</li>
        </ul>

        <h3>🔧 Engineering Applications:</h3>
        <ul>
            <li><b>Area:</b> Finding area under curves</li>
            <li><b>Volume:</b> Volumes of revolution</li>
            <li><b>Work:</b> Work done by varying force</li>
            <li><b>Pressure:</b> Fluid pressure on surfaces</li>
            <li><b>Mass:</b> Center of mass calculations</li>
        </ul>

        <h3>💡 Tips:</h3>
        <ul>
            <li>Watch how increasing rectangles improves accuracy</li>
            <li>Compare different Riemann sum methods</li>
            <li>Notice the relationship with derivatives</li>
            <li>Think about physical interpretations</li>
        </ul>
        """)
        guide.setStyleSheet("font-size: 14px; color: black;")
        guide.setWordWrap(True)
        layout.addWidget(guide)

        return frame

    def update_plot(self):
        self.figure.clear()

        # Get parameters
        func_text = self.function_combo.currentText()
        sum_type = self.sum_type_combo.currentText()
        n = self.n_rect_spin.value()
        
        # Get bounds
        a = self.lower_bound.value() / 10
        b = self.upper_bound.value() / 10
        self.lower_value.setText(f"{a:.1f}")
        self.upper_value.setText(f"{b:.1f}")

        if a >= b:
            self.info_display.setText("Upper bound must be greater than lower bound!")
            return

        # Create data
        x = np.linspace(min(a-1, 0), max(b+1, 1), 1000)
        
        # Define function
        if func_text == "x²":
            y = x**2
            f = lambda x: x**2
            antideriv = lambda x: x**3/3
            latex = "f(x) = x^2"
        elif func_text == "x³":
            y = x**3
            f = lambda x: x**3
            antideriv = lambda x: x**4/4
            latex = "f(x) = x^3"
        elif func_text == "sin(x)":
            y = np.sin(x)
            f = lambda x: np.sin(x)
            antideriv = lambda x: -np.cos(x)
            latex = "f(x) = sin(x)"
        elif func_text == "e^x":
            y = np.exp(x)
            f = lambda x: np.exp(x)
            antideriv = lambda x: np.exp(x)
            latex = "f(x) = e^x"
        elif func_text == "1/x":
            x = np.linspace(max(0.1, a-1), b+1, 1000)
            y = 1/x
            f = lambda x: 1/x
            antideriv = lambda x: np.log(abs(x))
            latex = "f(x) = 1/x"
        else:  # √x
            x = np.linspace(max(0, a-1), b+1, 1000)
            y = np.sqrt(x)
            f = lambda x: np.sqrt(x)
            antideriv = lambda x: 2*x**1.5/3
            latex = "f(x) = √x"

        # Create subplot
        ax = self.figure.add_subplot(111)
        ax.plot(x, y, 'b-', linewidth=2, label=latex)
        ax.grid(True, linestyle='--', alpha=0.7)

        # Calculate Riemann sum
        dx = (b - a) / n
        if sum_type == "Left":
            x_points = np.linspace(a, b-dx, n)
            riemann_sum = sum(f(x_points) * dx)
        elif sum_type == "Right":
            x_points = np.linspace(a+dx, b, n)
            riemann_sum = sum(f(x_points) * dx)
        elif sum_type == "Midpoint":
            x_points = np.linspace(a+dx/2, b-dx/2, n)
            riemann_sum = sum(f(x_points) * dx)
        else:  # Trapezoidal
            x_points = np.linspace(a, b, n+1)
            riemann_sum = (sum(f(x_points[1:-1])) + (f(x_points[0]) + f(x_points[-1]))/2) * dx

        # Plot rectangles
        for i, x_val in enumerate(x_points):
            if sum_type == "Trapezoidal":
                if i < len(x_points) - 1:
                    ax.plot([x_points[i], x_points[i+1]], 
                           [f(x_points[i]), f(x_points[i+1])], 
                           'r-', alpha=0.5)
            else:
                rect = Rectangle((x_val, 0), dx, f(x_val),
                               facecolor='r', alpha=0.3)
                ax.add_patch(rect)

        # Calculate actual integral
        actual_integral = antideriv(b) - antideriv(a)

        ax.set_title(f'Integration of {latex} from {a:.1f} to {b:.1f}', fontsize=12)
        ax.legend()

        # Set reasonable y-axis limits
        y_vals = y[(x >= a) & (x <= b)]
        if len(y_vals) > 0:
            y_min, y_max = min(0, np.min(y_vals)), max(0, np.max(y_vals))
            ax.set_ylim(y_min - 0.5, y_max + 0.5)

        # Set x-axis limits
        ax.set_xlim(a - 0.5, b + 0.5)

        self.figure.tight_layout()
        self.canvas.draw()

        # Update information display
        error = abs(actual_integral - riemann_sum)
        error_percent = (error / abs(actual_integral)) * 100 if actual_integral != 0 else 0

        info_text = f"""
        <b>Integration Analysis</b><br>
        • Method: {sum_type} Riemann Sum<br>
        • Number of subdivisions: {n}<br>
        • Approximate integral: {riemann_sum:.4f}<br>
        • Actual integral: {actual_integral:.4f}<br>
        • Absolute error: {error:.4f}<br>
        • Relative error: {error_percent:.2f}%<br>
        • Interpretation: The area between {latex} and the x-axis from x={a:.1f} to x={b:.1f}
        """
        self.info_display.setText(info_text)

    def update_application(self):
        self.app_figure.clear()
        app_type = self.app_combo.currentText()
        
        ax = self.app_figure.add_subplot(111)
        
        if app_type == "Area Under Curve":
            x = np.linspace(0, 2*np.pi, 1000)
            y = np.sin(x)
            ax.plot(x, y, 'b-', linewidth=2)
            ax.fill_between(x, y, alpha=0.3)
            ax.set_title("Area Under Sine Curve")
            
            info = """
            <b>Area Under Curve</b><br>
            • Represents total accumulation<br>
            • Common in probability distributions<br>
            • Used in work and energy calculations<br>
            • Example: ∫sin(x)dx from 0 to 2π = 0
            """
            
        elif app_type == "Work Done":
            x = np.linspace(0, 10, 1000)
            F = 5 * np.exp(-x/5)  # Force function
            ax.plot(x, F, 'b-', linewidth=2)
            ax.fill_between(x, F, alpha=0.3)
            ax.set_title("Work Done by Variable Force")
            
            info = """
            <b>Work Done</b><br>
            • W = ∫F(x)dx<br>
            • Represents energy transfer<br>
            • Important in mechanics and thermodynamics<br>
            • Example: Spring force, fluid compression
            """
            
        elif app_type == "Fluid Pressure":
            x = np.linspace(0, 10, 1000)
            p = 9.81 * x  # Pressure function (ρgh)
            ax.plot(x, p, 'b-', linewidth=2)
            ax.fill_between(x, p, alpha=0.3)
            ax.set_title("Hydrostatic Pressure Distribution")
            
            info = """
            <b>Fluid Pressure</b><br>
            • P = ∫ρgh dh<br>
            • Used in fluid dynamics<br>
            • Important for dam design<br>
            • Example: Pressure force on submerged surfaces
            """
            
        else:  # Center of Mass
            x = np.linspace(-5, 5, 1000)
            y = np.exp(-x**2/4)  # Density distribution
            ax.plot(x, y, 'b-', linewidth=2)
            ax.fill_between(x, y, alpha=0.3)
            ax.set_title("Mass Distribution")
            
            info = """
            <b>Center of Mass</b><br>
            • x̄ = ∫xρ(x)dx / ∫ρ(x)dx<br>
            • Important in mechanics<br>
            • Used in structural analysis<br>
            • Example: Beam loading, stability analysis
            """

        ax.grid(True, linestyle='--', alpha=0.7)
        self.app_figure.tight_layout()
        self.app_canvas.draw()
        
        self.app_info.setText(info) 