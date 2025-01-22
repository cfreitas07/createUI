from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QLabel, QPushButton, QLineEdit, QFrame, QTabWidget,
                            QGridLayout, QSlider, QComboBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QPen, QColor, QFont
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class DerivativeVisualizer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Derivative Explorer 📈")
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
                background-color: #FF6B6B;
                color: white;
            }
        """)

        tabs.addTab(self.create_derivative_tab(), "📊 Derivative Explorer")
        tabs.addTab(self.create_slope_tab(), "📐 Slope Analysis")
        tabs.addTab(self.create_learn_tab(), "📚 Quick Guide")
        
        layout.addWidget(tabs)

    def create_derivative_tab(self):
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
                border: 2px solid #FF6B6B;
                border-radius: 5px;
                background: white;
            }
            QPushButton {
                padding: 10px 20px;
                background-color: #FF6B6B;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #FF5252;
            }
        """)
        
        layout = QVBoxLayout(frame)

        # Function selection
        function_layout = QHBoxLayout()
        function_label = QLabel("Select Function:")
        self.function_combo = QComboBox()
        self.function_combo.addItems([
            "x²", "x³", "sin(x)", "cos(x)", "e^x", "ln(x)"
        ])
        self.function_combo.currentTextChanged.connect(self.update_plot)
        function_layout.addWidget(function_label)
        function_layout.addWidget(self.function_combo)
        function_layout.addStretch()
        layout.addLayout(function_layout)

        # Create matplotlib figure
        self.figure = Figure(figsize=(12, 6))
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        # Point slider
        slider_layout = QHBoxLayout()
        slider_label = QLabel("Point x:")
        self.point_slider = QSlider(Qt.Orientation.Horizontal)
        self.point_slider.setMinimum(-100)
        self.point_slider.setMaximum(100)
        self.point_slider.setValue(0)
        self.point_slider.valueChanged.connect(self.update_plot)
        self.point_value = QLabel("0.0")
        slider_layout.addWidget(slider_label)
        slider_layout.addWidget(self.point_slider)
        slider_layout.addWidget(self.point_value)
        layout.addLayout(slider_layout)

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

    def create_slope_tab(self):
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                padding: 20px;
            }
        """)
        
        layout = QVBoxLayout(frame)

        # Create matplotlib figure for slope visualization
        self.slope_figure = Figure(figsize=(12, 6))
        self.slope_canvas = FigureCanvas(self.slope_figure)
        layout.addWidget(self.slope_canvas)

        # Delta x slider
        dx_layout = QHBoxLayout()
        dx_label = QLabel("Δx:")
        self.dx_slider = QSlider(Qt.Orientation.Horizontal)
        self.dx_slider.setMinimum(1)
        self.dx_slider.setMaximum(100)
        self.dx_slider.setValue(20)
        self.dx_slider.valueChanged.connect(self.update_slope_plot)
        self.dx_value = QLabel("0.2")
        dx_layout.addWidget(dx_label)
        dx_layout.addWidget(self.dx_slider)
        dx_layout.addWidget(self.dx_value)
        layout.addLayout(dx_layout)

        # Slope information
        self.slope_info = QLabel()
        self.slope_info.setStyleSheet("""
            QLabel {
                background-color: #f8f9fa;
                padding: 15px;
                border-radius: 8px;
                border: 1px solid #dee2e6;
            }
        """)
        layout.addWidget(self.slope_info)

        self.update_slope_plot()
        return frame

    def create_learn_tab(self):
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                padding: 20px;
            }
        """)
        
        layout = QVBoxLayout(frame)

        guide = QLabel("""
        <h2>📚 Understanding Derivatives</h2>
        
        <h3>🎯 Key Concepts:</h3>
        <ul>
            <li><b>Derivative:</b> Rate of change of a function at a point</li>
            <li><b>Slope:</b> The steepness of the tangent line</li>
            <li><b>Instantaneous Rate:</b> The limit of the average rate of change</li>
        </ul>

        <h3>📐 Common Derivatives:</h3>
        <ul>
            <li>d/dx(x²) = 2x</li>
            <li>d/dx(x³) = 3x²</li>
            <li>d/dx(sin(x)) = cos(x)</li>
            <li>d/dx(cos(x)) = -sin(x)</li>
            <li>d/dx(e^x) = e^x</li>
            <li>d/dx(ln(x)) = 1/x</li>
        </ul>

        <h3>💡 Tips:</h3>
        <ul>
            <li>Watch how the slope changes at different points</li>
            <li>Notice where derivatives are zero (horizontal tangents)</li>
            <li>Observe the relationship between function and derivative</li>
            <li>Try different Δx values to understand limits</li>
        </ul>
        """)
        guide.setStyleSheet("font-size: 14px; color: black;")
        guide.setWordWrap(True)
        layout.addWidget(guide)

        return frame

    def update_plot(self):
        self.figure.clear()

        # Get current function and point
        func_text = self.function_combo.currentText()
        x_point = self.point_slider.value() / 50  # Scale to reasonable range
        self.point_value.setText(f"{x_point:.1f}")

        # Create data
        x = np.linspace(-5, 5, 1000)
        
        # Calculate function and derivative
        if func_text == "x²":
            y = x**2
            dy = 2*x
            func_latex = "f(x) = x^2"
            deriv_latex = "f'(x) = 2x"
        elif func_text == "x³":
            y = x**3
            dy = 3*x**2
            func_latex = "f(x) = x^3"
            deriv_latex = "f'(x) = 3x^2"
        elif func_text == "sin(x)":
            y = np.sin(x)
            dy = np.cos(x)
            func_latex = "f(x) = sin(x)"
            deriv_latex = "f'(x) = cos(x)"
        elif func_text == "cos(x)":
            y = np.cos(x)
            dy = -np.sin(x)
            func_latex = "f(x) = cos(x)"
            deriv_latex = "f'(x) = -sin(x)"
        elif func_text == "e^x":
            y = np.exp(x)
            dy = np.exp(x)
            func_latex = "f(x) = e^x"
            deriv_latex = "f'(x) = e^x"
        else:  # ln(x)
            x = np.linspace(0.1, 5, 1000)  # Avoid negative values
            y = np.log(x)
            dy = 1/x
            func_latex = "f(x) = ln(x)"
            deriv_latex = "f'(x) = 1/x"

        # Create subplots
        ax1 = self.figure.add_subplot(211)
        ax2 = self.figure.add_subplot(212)

        # Plot function
        ax1.plot(x, y, 'b-', label='f(x)', linewidth=2)
        ax1.grid(True, linestyle='--', alpha=0.7)
        ax1.set_title(f'Function: {func_latex}', fontsize=12)
        
        # Plot point and tangent line
        if x_point >= min(x) and x_point <= max(x):
            idx = np.abs(x - x_point).argmin()
            point_y = y[idx]
            slope = dy[idx]
            
            # Plot point
            ax1.plot(x_point, point_y, 'ro')
            
            # Plot tangent line
            x_tangent = np.array([x_point - 1, x_point + 1])
            y_tangent = point_y + slope * (x_tangent - x_point)
            ax1.plot(x_tangent, y_tangent, 'r--', label=f'Slope: {slope:.2f}')

        ax1.legend()

        # Plot derivative
        ax2.plot(x, dy, 'g-', label="f'(x)", linewidth=2)
        ax2.grid(True, linestyle='--', alpha=0.7)
        ax2.set_title(f'Derivative: {deriv_latex}', fontsize=12)
        
        if x_point >= min(x) and x_point <= max(x):
            ax2.plot(x_point, dy[idx], 'ro')

        ax2.legend()

        # Adjust layout
        self.figure.tight_layout()
        self.canvas.draw()

        # Update information display
        if x_point >= min(x) and x_point <= max(x):
            info_text = f"""
            <b>Point Analysis at x = {x_point:.2f}</b><br>
            • Function Value: f({x_point:.2f}) = {point_y:.2f}<br>
            • Derivative Value: f'({x_point:.2f}) = {slope:.2f}<br>
            • Interpretation: The function is {'increasing' if slope > 0 else 'decreasing' if slope < 0 else 'at a critical point'} at this point
            """
            self.info_display.setText(info_text)

    def update_slope_plot(self):
        self.slope_figure.clear()
        
        # Get current function and delta x
        func_text = self.function_combo.currentText()
        dx = self.dx_slider.value() / 100  # Scale to reasonable range
        self.dx_value.setText(f"{dx:.2f}")
        
        # Create data
        x = np.linspace(-5, 5, 1000)
        
        # Calculate function
        if func_text == "x²":
            y = x**2
        elif func_text == "x³":
            y = x**3
        elif func_text == "sin(x)":
            y = np.sin(x)
        elif func_text == "cos(x)":
            y = np.cos(x)
        elif func_text == "e^x":
            y = np.exp(x)
        else:  # ln(x)
            x = np.linspace(0.1, 5, 1000)
            y = np.log(x)

        # Plot
        ax = self.slope_figure.add_subplot(111)
        ax.plot(x, y, 'b-', linewidth=2)
        ax.grid(True, linestyle='--', alpha=0.7)
        
        # Plot secant lines
        x0 = 0  # Fixed point
        y0 = np.interp(x0, x, y)
        x1 = x0 + dx
        y1 = np.interp(x1, x, y)
        
        # Secant line
        ax.plot([x0, x1], [y0, y1], 'r--', linewidth=2)
        
        # Points
        ax.plot([x0, x1], [y0, y1], 'ro')
        
        # Calculate slope
        slope = (y1 - y0) / (x1 - x0)
        
        ax.set_title(f'Slope Analysis (Δx = {dx:.2f})', fontsize=12)
        
        self.slope_figure.tight_layout()
        self.slope_canvas.draw()
        
        # Update slope information
        info_text = f"""
        <b>Slope Analysis</b><br>
        • Δx = {dx:.2f}<br>
        • Δy = {y1-y0:.2f}<br>
        • Slope = Δy/Δx = {slope:.2f}<br>
        • As Δx → 0, the secant line approaches the tangent line
        """
        self.slope_info.setText(info_text) 