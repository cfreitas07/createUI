from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QLabel, QPushButton, QFrame, QComboBox)
from PyQt6.QtCore import Qt
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from scipy import stats
from scipy.optimize import curve_fit

class CurveFitting(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Curve Fitting Explorer 📈")
        self.setGeometry(100, 100, 1200, 900)

        # Initialize data points
        self.x_points = []
        self.y_points = []

        # Create main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)

        # Create control panel
        control_panel = QHBoxLayout()
        
        # Fit type selection
        fit_label = QLabel("Fit Type:")
        self.fit_combo = QComboBox()
        self.fit_combo.addItems([
            "Linear (y = mx + b)",
            "Quadratic (y = ax² + bx + c)",
            "Cubic (y = ax³ + bx² + cx + d)",
            "Exponential (y = ae^(bx))",
            "Power Law (y = ax^b)",
            "Logarithmic (y = a·ln(x) + b)"
        ])
        self.fit_combo.setStyleSheet("""
            QComboBox {
                padding: 5px;
                border: 2px solid #2196F3;
                border-radius: 5px;
                background: white;
                min-width: 200px;
            }
        """)
        
        # Buttons
        self.fit_button = QPushButton("Fit Curve 📊")
        self.reset_button = QPushButton("Reset 🔄")
        self.undo_button = QPushButton("Undo ↩")
        
        for button in [self.fit_button, self.reset_button, self.undo_button]:
            button.setStyleSheet("""
                QPushButton {
                    padding: 8px 15px;
                    background-color: #2196F3;
                    color: white;
                    border: none;
                    border-radius: 5px;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background-color: #1976D2;
                }
            """)

        self.fit_button.clicked.connect(self.fit_curve)
        self.reset_button.clicked.connect(self.reset_plot)
        self.undo_button.clicked.connect(self.undo_last_point)

        control_panel.addWidget(fit_label)
        control_panel.addWidget(self.fit_combo)
        control_panel.addWidget(self.fit_button)
        control_panel.addWidget(self.undo_button)
        control_panel.addWidget(self.reset_button)
        control_panel.addStretch()

        layout.addLayout(control_panel)

        # Create matplotlib figure
        self.figure = Figure(figsize=(12, 8))
        self.canvas = FigureCanvas(self.figure)
        self.canvas.mpl_connect('button_press_event', self.on_click)
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
        
        # Initialize the plot
        self.update_plot()
        
        # Initial message
        self.info_display.setText(
            "Click anywhere on the plot to add points. "
            "Click 'Fit Curve' when ready to analyze!"
        )

    def on_click(self, event):
        """Handle mouse clicks on the plot"""
        if event.inaxes is not None:
            self.x_points.append(event.xdata)
            self.y_points.append(event.ydata)
            self.update_plot()
            
            # Update point count
            self.info_display.setText(
                f"Points added: {len(self.x_points)}\n"
                "Click 'Fit Curve' when ready to analyze!"
            )

    def update_plot(self):
        """Update the plot with current points"""
        self.figure.clear()
        
        # Create two subplots
        self.ax_main = self.figure.add_subplot(211)  # Main plot
        self.ax_residual = self.figure.add_subplot(212)  # Residual plot
        
        # Plot points on main plot
        if self.x_points:
            self.ax_main.scatter(self.x_points, self.y_points, 
                               color='blue', alpha=0.6, label='Data Points')
            
        # Set labels and grid
        self.ax_main.set_xlabel('X')
        self.ax_main.set_ylabel('Y')
        self.ax_main.grid(True, linestyle='--', alpha=0.7)
        self.ax_main.set_title('Interactive Curve Fitting')
        
        # Configure residual plot
        self.ax_residual.set_xlabel('X')
        self.ax_residual.set_ylabel('Residuals')
        self.ax_residual.grid(True, linestyle='--', alpha=0.7)
        self.ax_residual.axhline(y=0, color='r', linestyle='-', alpha=0.3)
        
        self.figure.tight_layout()
        self.canvas.draw()

    def fit_curve(self):
        """Perform curve fitting based on selected type"""
        if len(self.x_points) < 2:
            self.info_display.setText("Need at least 2 points for fitting!")
            return

        x = np.array(self.x_points)
        y = np.array(self.y_points)
        
        fit_type = self.fit_combo.currentText()
        
        try:
            # Perform fitting based on selected type
            if "Linear" in fit_type:
                slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
                y_fit = slope * x + intercept
                equation = f"y = {slope:.4f}x + {intercept:.4f}"
                r_squared = r_value**2
                
            elif "Quadratic" in fit_type:
                coeffs = np.polyfit(x, y, 2)
                y_fit = np.polyval(coeffs, x)
                equation = f"y = {coeffs[0]:.4f}x² + {coeffs[1]:.4f}x + {coeffs[2]:.4f}"
                r_squared = 1 - np.sum((y - y_fit)**2) / np.sum((y - np.mean(y))**2)
                
            elif "Cubic" in fit_type:
                coeffs = np.polyfit(x, y, 3)
                y_fit = np.polyval(coeffs, x)
                equation = f"y = {coeffs[0]:.4f}x³ + {coeffs[1]:.4f}x² + {coeffs[2]:.4f}x + {coeffs[3]:.4f}"
                r_squared = 1 - np.sum((y - y_fit)**2) / np.sum((y - np.mean(y))**2)
                
            elif "Exponential" in fit_type:
                def exp_func(x, a, b):
                    return a * np.exp(b * x)
                popt, _ = curve_fit(exp_func, x, y)
                y_fit = exp_func(x, *popt)
                equation = f"y = {popt[0]:.4f}·e^({popt[1]:.4f}x)"
                r_squared = 1 - np.sum((y - y_fit)**2) / np.sum((y - np.mean(y))**2)
                
            elif "Power Law" in fit_type:
                def power_func(x, a, b):
                    return a * np.power(x, b)
                popt, _ = curve_fit(power_func, x, y)
                y_fit = power_func(x, *popt)
                equation = f"y = {popt[0]:.4f}·x^{popt[1]:.4f}"
                r_squared = 1 - np.sum((y - y_fit)**2) / np.sum((y - np.mean(y))**2)
                
            else:  # Logarithmic
                def log_func(x, a, b):
                    return a * np.log(x) + b
                popt, _ = curve_fit(log_func, x, y)
                y_fit = log_func(x, *popt)
                equation = f"y = {popt[0]:.4f}·ln(x) + {popt[1]:.4f}"
                r_squared = 1 - np.sum((y - y_fit)**2) / np.sum((y - np.mean(y))**2)

            # Calculate residuals
            residuals = y - y_fit
            
            # Update plots
            self.figure.clear()
            
            # Main plot
            self.ax_main = self.figure.add_subplot(211)
            self.ax_main.scatter(x, y, color='blue', alpha=0.6, label='Data Points')
            
            # Sort x and y_fit for smooth curve
            sort_idx = np.argsort(x)
            x_sorted = x[sort_idx]
            y_fit_sorted = y_fit[sort_idx]
            
            self.ax_main.plot(x_sorted, y_fit_sorted, 'r-', label='Fitted Curve')
            self.ax_main.set_xlabel('X')
            self.ax_main.set_ylabel('Y')
            self.ax_main.grid(True, linestyle='--', alpha=0.7)
            self.ax_main.legend()
            self.ax_main.set_title(f'Curve Fitting: {fit_type}')
            
            # Residual plot
            self.ax_residual = self.figure.add_subplot(212)
            self.ax_residual.scatter(x, residuals, color='green', alpha=0.6)
            self.ax_residual.axhline(y=0, color='r', linestyle='-', alpha=0.3)
            self.ax_residual.set_xlabel('X')
            self.ax_residual.set_ylabel('Residuals')
            self.ax_residual.grid(True, linestyle='--', alpha=0.7)
            
            self.figure.tight_layout()
            self.canvas.draw()
            
            # Update information display
            rmse = np.sqrt(np.mean(residuals**2))
            mae = np.mean(np.abs(residuals))
            
            info_text = f"""
            <b>Fitting Results:</b><br>
            • Equation: {equation}<br>
            • R² Score: {r_squared:.4f}<br>
            • Root Mean Square Error: {rmse:.4f}<br>
            • Mean Absolute Error: {mae:.4f}<br>
            • Number of Points: {len(x)}<br>
            • Fit Type: {fit_type}
            """
            self.info_display.setText(info_text)
            
        except Exception as e:
            self.info_display.setText(f"Fitting error: {str(e)}")

    def reset_plot(self):
        """Clear all points and reset the plot"""
        self.x_points = []
        self.y_points = []
        self.update_plot()
        self.info_display.setText(
            "Plot reset! Click anywhere to add new points."
        )

    def undo_last_point(self):
        """Remove the last added point"""
        if self.x_points:
            self.x_points.pop()
            self.y_points.pop()
            self.update_plot()
            self.info_display.setText(
                f"Last point removed. Remaining points: {len(self.x_points)}"
            ) 