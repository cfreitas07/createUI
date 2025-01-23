from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QLabel, QPushButton, QLineEdit, QFrame, QTabWidget,
                            QGridLayout, QSlider, QComboBox, QScrollArea)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPainter, QPen, QColor, QFont
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.animation import FuncAnimation
from matplotlib.collections import LineCollection

class DerivativeVisualizer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Engineering Derivative Explorer")
        self.setGeometry(100, 100, 1400, 800)

        # Create main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)

        # Create tabs
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet("""
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

        self.setup_geometric_tab()
        self.setup_motion_tab()
        self.setup_engineering_tab()
        
        layout.addWidget(self.tab_widget)

    def setup_geometric_tab(self):
        """Interactive geometric interpretation of derivatives"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Create matplotlib figure
        self.geo_figure, (self.geo_ax1, self.geo_ax2) = plt.subplots(2, 1, figsize=(12, 8))
        self.geo_canvas = FigureCanvas(self.geo_figure)
        layout.addWidget(self.geo_canvas)
        
        # Add controls
        controls = QHBoxLayout()
        
        # Point slider
        point_layout = QHBoxLayout()
        point_label = QLabel("Move Point:")
        self.point_slider = QSlider(Qt.Orientation.Horizontal)
        self.point_slider.setRange(0, 100)
        self.point_slider.setValue(50)
        self.point_slider.valueChanged.connect(self.update_geometric)
        point_layout.addWidget(point_label)
        point_layout.addWidget(self.point_slider)
        controls.addLayout(point_layout)
        
        # Δx slider
        dx_layout = QHBoxLayout()
        dx_label = QLabel("Adjust Δx:")
        self.dx_slider = QSlider(Qt.Orientation.Horizontal)
        self.dx_slider.setRange(1, 50)
        self.dx_slider.setValue(10)
        self.dx_slider.valueChanged.connect(self.update_geometric)
        dx_layout.addWidget(dx_label)
        dx_layout.addWidget(self.dx_slider)
        controls.addLayout(dx_layout)
        
        layout.addLayout(controls)
        
        # Add explanation
        self.geo_explanation = QLabel()
        self.geo_explanation.setWordWrap(True)
        self.geo_explanation.setStyleSheet("font-size: 12pt; margin: 10px;")
        layout.addWidget(self.geo_explanation)
        
        self.tab_widget.addTab(tab, "🔍 Geometric View")
        self.update_geometric()

    def setup_motion_tab(self):
        """Setup the motion analysis tab with improved visualization and explanations"""
        motion_tab = QWidget()
        layout = QVBoxLayout()
        
        # Create matplotlib figure with 2 subplots
        self.motion_fig, (self.motion_ax1, self.motion_ax2) = plt.subplots(2, 1, figsize=(8, 8))
        self.motion_canvas = FigureCanvas(self.motion_fig)
        
        # Add explanation text area
        self.motion_explanation = QLabel()
        self.motion_explanation.setWordWrap(True)
        self.motion_explanation.setStyleSheet("QLabel { background-color: white; padding: 10px; border-radius: 5px; }")
        
        # Add controls
        controls_layout = QHBoxLayout()
        
        # Add amplitude slider
        amplitude_layout = QVBoxLayout()
        amplitude_label = QLabel("Amplitude:")
        self.amplitude_slider = QSlider()  # Simplified
        self.amplitude_slider.setOrientation(Qt.Orientation.Horizontal)  # Set orientation this way
        self.amplitude_slider.setMinimum(1)
        self.amplitude_slider.setMaximum(5)
        self.amplitude_slider.setValue(2)
        amplitude_layout.addWidget(amplitude_label)
        amplitude_layout.addWidget(self.amplitude_slider)
        
        # Add frequency slider
        frequency_layout = QVBoxLayout()
        frequency_label = QLabel("Frequency:")
        self.frequency_slider = QSlider()  # Simplified
        self.frequency_slider.setOrientation(Qt.Orientation.Horizontal)  # Set orientation this way
        self.frequency_slider.setMinimum(1)
        self.frequency_slider.setMaximum(5)
        self.frequency_slider.setValue(1)
        frequency_layout.addWidget(frequency_label)
        frequency_layout.addWidget(self.frequency_slider)
        
        # Add pause button
        self.motion_pause_button = QPushButton("Pause")
        self.motion_pause_button.setCheckable(True)
        self.motion_pause_button.clicked.connect(self.toggle_motion_animation)
        
        # Add reset button
        self.motion_reset_button = QPushButton("Reset")
        self.motion_reset_button.clicked.connect(self.reset_motion_animation)
        
        # Add controls to layout
        controls_layout.addLayout(amplitude_layout)
        controls_layout.addLayout(frequency_layout)
        controls_layout.addWidget(self.motion_pause_button)
        controls_layout.addWidget(self.motion_reset_button)
        
        # Add widgets to main layout
        layout.addWidget(self.motion_canvas)
        layout.addLayout(controls_layout)
        layout.addWidget(self.motion_explanation)
        
        motion_tab.setLayout(layout)
        
        # Initialize animation time
        self.motion_time = 0
        self.motion_paused = False
        
        # Setup animation with explicit save_count
        self.motion_anim = FuncAnimation(
            self.motion_fig,
            self.update_motion_animation,
            interval=50,
            cache_frame_data=False,  # Disable frame caching
            blit=False
        )
        
        return motion_tab

    def update_geometric(self):
        """Update geometric interpretation visualization"""
        self.geo_ax1.clear()
        self.geo_ax2.clear()
        
        # Get values from sliders
        x = self.point_slider.value() / 100 * 4 * np.pi
        dx = self.dx_slider.value() / 100
        
        # Generate function and derivative
        t = np.linspace(0, 4*np.pi, 1000)
        y = np.sin(t)
        dy = np.cos(t)
        
        # Plot function
        self.geo_ax1.plot(t, y, 'b-', label='f(x) = sin(x)')
        self.geo_ax1.plot(x, np.sin(x), 'ro')
        
        # Plot secant line
        x2 = x + dx
        y1, y2 = np.sin(x), np.sin(x2)
        self.geo_ax1.plot([x, x2], [y1, y2], 'g-', label=f'Secant (Δx = {dx:.2f})')
        
        # Plot tangent line
        slope = np.cos(x)
        x_tan = np.array([x - 0.5, x + 0.5])
        y_tan = slope * (x_tan - x) + np.sin(x)
        self.geo_ax1.plot(x_tan, y_tan, 'r--', label=f'Tangent (slope = {slope:.2f})')
        
        self.geo_ax1.grid(True)
        self.geo_ax1.legend()
        self.geo_ax1.set_title('Function and Slopes')
        
        # Plot derivative
        self.geo_ax2.plot(t, dy, 'r-', label='f\'(x) = cos(x)')
        self.geo_ax2.plot(x, np.cos(x), 'ro')
        self.geo_ax2.grid(True)
        self.geo_ax2.legend()
        self.geo_ax2.set_title('Derivative Function')
        
        # Update explanation
        self.geo_explanation.setText(
            f"<b>Current Point:</b> x = {x:.2f}<br>"
            f"<b>Function Value:</b> f({x:.2f}) = {np.sin(x):.2f}<br>"
            f"<b>Derivative Value:</b> f'({x:.2f}) = {np.cos(x):.2f}<br>"
            f"<b>Secant Slope:</b> {((y2-y1)/dx):.2f}<br>"
            f"<b>As Δx → 0, the secant line approaches the tangent line!</b>"
        )
        
        self.geo_canvas.draw()

    def update_motion_animation(self, frame):
        """Update the motion analysis animation with improved visualization"""
        if not self.motion_paused:
            self.motion_time += 0.05
        
        # Get current parameters
        A = self.amplitude_slider.value()
        ω = self.frequency_slider.value() * np.pi  # Angular frequency
        
        # Create time array
        t = np.linspace(0, 10, 500)
        
        # Calculate motion equations
        position = A * np.sin(ω * t)
        velocity = A * ω * np.cos(ω * t)
        acceleration = -A * ω**2 * np.sin(ω * t)
        
        # Get current values
        current_t = self.motion_time % 10
        current_pos = A * np.sin(ω * current_t)
        current_vel = A * ω * np.cos(ω * current_t)
        current_acc = -A * ω**2 * np.sin(ω * current_t)
        
        # Clear plots
        self.motion_ax1.clear()
        self.motion_ax2.clear()
        
        # Plot 1: Moving object and trace
        # Draw reference line
        self.motion_ax1.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
        
        # Draw position trace
        self.motion_ax1.plot(t[:int(current_t*50)], position[:int(current_t*50)], 
                            'b-', alpha=0.3, label='Position trace')
        
        # Draw current position
        self.motion_ax1.plot(current_t, current_pos, 'bo', markersize=15, 
                            label=f'Position: {current_pos:.2f} m')
        
        # Draw velocity vector
        vector_scale = 0.5
        self.motion_ax1.arrow(current_t, current_pos, 
                             vector_scale, vector_scale*current_vel,
                             head_width=0.1, color='g', 
                             label=f'Velocity: {current_vel:.2f} m/s')
        
        # Draw acceleration vector
        self.motion_ax1.arrow(current_t, current_pos, 
                             vector_scale, vector_scale*current_acc/10,
                             head_width=0.1, color='r', 
                             label=f'Acceleration: {current_acc:.2f} m/s²')
        
        self.motion_ax1.set_xlim(current_t - 2, current_t + 2)
        self.motion_ax1.set_ylim(-6, 6)
        self.motion_ax1.set_title('Motion Analysis', fontsize=12)
        self.motion_ax1.grid(True)
        self.motion_ax1.legend(loc='upper right')
        
        # Plot 2: Position, velocity, and acceleration graphs
        self.motion_ax2.plot(t, position, 'b-', label='Position (m)', linewidth=2)
        self.motion_ax2.plot(t, velocity, 'g-', label='Velocity (m/s)', linewidth=2)
        self.motion_ax2.plot(t, acceleration/10, 'r-', 
                            label='Acceleration/10 (m/s²)', linewidth=2)
        
        # Add current time marker
        self.motion_ax2.axvline(x=current_t, color='gray', linestyle='--', alpha=0.5)
        self.motion_ax2.plot(current_t, current_pos, 'bo', markersize=8)
        self.motion_ax2.plot(current_t, current_vel, 'go', markersize=8)
        self.motion_ax2.plot(current_t, current_acc/10, 'ro', markersize=8)
        
        self.motion_ax2.set_xlim(current_t - 2, current_t + 2)
        self.motion_ax2.set_ylim(-6, 6)
        self.motion_ax2.grid(True)
        self.motion_ax2.legend(loc='upper right')
        
        # Update explanation text
        self.motion_explanation.setText(f"""
            <h2>📊 Motion Analysis and Derivatives</h2>
            
            <p><b>Current Values:</b><br>
            • Position (x) = {current_pos:.2f} m<br>
            • Velocity (dx/dt) = {current_vel:.2f} m/s<br>
            • Acceleration (d²x/dt²) = {current_acc:.2f} m/s²</p>
            
            <p><b>Understanding Derivatives:</b><br>
            • Velocity is the rate of change of position (first derivative)<br>
            • Acceleration is the rate of change of velocity (second derivative)<br>
            • Notice how velocity is maximum when position crosses zero<br>
            • Acceleration is opposite to position (for simple harmonic motion)</p>
            
            <p><b>Controls:</b><br>
            • Amplitude: Changes the maximum displacement<br>
            • Frequency: Changes how fast the motion repeats<br>
            • Try different combinations to see their effects!</p>
            
            <p><b>Real-world Examples:</b><br>
            • Pendulum motion<br>
            • Spring oscillations<br>
            • Sound waves<br>
            • AC electrical signals</p>
        """)

    def toggle_motion_animation(self):
        """Toggle motion animation pause state"""
        self.motion_paused = not self.motion_paused
        self.motion_pause_button.setText("Resume" if self.motion_paused else "Pause")

    def reset_motion_animation(self):
        """Reset motion animation to initial state"""
        self.motion_time = 0
        self.amplitude_slider.setValue(2)
        self.frequency_slider.setValue(1)
        self.motion_paused = False
        self.motion_pause_button.setText("Pause")

    def setup_engineering_tab(self):
        """Real engineering applications with balanced layout"""
        tab = QWidget()
        main_layout = QHBoxLayout(tab)
        
        # Left side - Plots and Controls (50%)
        plot_layout = QVBoxLayout()
        
        # Selector at the top
        selector_layout = QHBoxLayout()
        selector_label = QLabel("Select Engineering Example:")
        selector_label.setStyleSheet("font-size: 14pt; font-weight: bold;")
        
        self.app_selector = QComboBox()
        self.app_selector.setStyleSheet("""
            QComboBox {
                font-size: 12pt;
                padding: 8px;
                min-width: 300px;
            }
        """)
        
        # Complete list of examples
        examples = [
            "Select one example!",
            "⚡ Electrical: Simple Voltage Ramp",
            "🔧 Mechanical: Spring-Mass Oscillation",
            "🔧 Mechanical: Robot Arm Kinematics",
            "🏗️ Civil: Cantilever Beam Analysis",
            "🌊 Fluid Dynamics: The Venturi Effect",
            "💻 Computer: Gradient Descent Optimization",
            "🔍 Computer: Edge Detection in Computer Vision"
        ]
        
        self.app_selector.addItems(examples)
        self.app_selector.currentIndexChanged.connect(self.update_engineering)
        selector_layout.addWidget(selector_label)
        selector_layout.addWidget(self.app_selector)
        plot_layout.addLayout(selector_layout)
        
        # Create matplotlib figure with adjusted size
        self.eng_figure, (self.eng_ax1, self.eng_ax2) = plt.subplots(2, 1, figsize=(8, 8))
        self.eng_figure.subplots_adjust(left=0.15, bottom=0.15, right=0.95, top=0.95)
        self.eng_canvas = FigureCanvas(self.eng_figure)
        plot_layout.addWidget(self.eng_canvas)
        
        # Animation controls
        controls_layout = QHBoxLayout()
        self.eng_play_button = QPushButton("▶ Play")
        self.eng_play_button.clicked.connect(self.toggle_engineering_animation)
        self.eng_play_button.setStyleSheet("""
            QPushButton {
                font-size: 12pt;
                padding: 8px 15px;
                background-color: #4CAF50;
                color: white;
                border-radius: 5px;
                margin: 10px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        controls_layout.addWidget(self.eng_play_button)
        plot_layout.addLayout(controls_layout)
        
        # Add plot layout to main layout (50%)
        plot_widget = QWidget()
        plot_widget.setLayout(plot_layout)
        plot_widget.setMaximumWidth(int(self.width() * 0.5))
        main_layout.addWidget(plot_widget)
        
        # Right side - Description (50%)
        description_layout = QVBoxLayout()
        
        # Styled explanation panel
        self.eng_explanation = QLabel()
        self.eng_explanation.setWordWrap(True)
        self.eng_explanation.setStyleSheet("""
            QLabel {
                font-size: 13pt;
                line-height: 1.6;
                padding: 20px;
                background-color: #f8f9fa;
                border-radius: 10px;
                margin: 10px;
            }
        """)
        self.eng_explanation.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        # Add explanation to a scroll area
        scroll = QScrollArea()
        scroll.setWidget(self.eng_explanation)
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
        """)
        description_layout.addWidget(scroll)
        
        # Add description layout to main layout (50%)
        description_widget = QWidget()
        description_widget.setLayout(description_layout)
        description_widget.setMaximumWidth(int(self.width() * 0.5))
        main_layout.addWidget(description_widget)
        
        # Initialize animation variables
        self.eng_time = 0
        self.eng_paused = False
        
        # Setup timer for animation
        self.eng_timer = QTimer()
        self.eng_timer.timeout.connect(self.update_engineering_animation)
        self.eng_timer.start(50)  # 50ms interval
        
        self.tab_widget.addTab(tab, "🔧 Engineering Applications")
        self.update_engineering()

    def update_engineering(self):
        """Initial setup of engineering example"""
        self.eng_time = 0
        self.update_engineering_animation()  # Draw initial state

    def toggle_engineering_animation(self):
        """Toggle engineering animation pause state"""
        self.eng_paused = not self.eng_paused
        self.eng_play_button.setText("▶ Play" if self.eng_paused else "⏸ Pause")

    def update_engineering_animation(self):
        """Update engineering example animation"""
        if not hasattr(self, 'eng_paused'):
            self.eng_paused = False
        
        if not self.eng_paused:
            self.eng_time += 0.05
        
        app_index = self.app_selector.currentIndex()
        
        if app_index == 1:  # Electrical: Simple Voltage Ramp
            # Time array
            t = np.linspace(0, 10, 500)
            
            # Voltage ramp parameters
            V_max = 12  # Maximum voltage
            ramp_period = 4  # Time for one complete ramp
            t_current = self.eng_time % ramp_period
            
            # Calculate voltage and its derivatives
            voltage = (V_max * t_current / ramp_period) % V_max
            dv_dt = V_max / ramp_period  # Voltage rate of change
            d2v_dt2 = 0  # Second derivative is zero for a linear ramp
            
            # Clear previous plots
            self.eng_ax1.clear()
            self.eng_ax2.clear()
            
            # Plot 1: Circuit Visualization
            circuit_fig = self.eng_ax1
            circuit_fig.set_xlim(-2, 2)
            circuit_fig.set_ylim(-2, 2)
            
            # Draw battery symbol
            circuit_fig.plot([-1, -1], [-0.5, 0.5], 'k-', linewidth=2)
            circuit_fig.plot([-1.2, -1], [0.5, 0.5], 'k-', linewidth=2)
            circuit_fig.plot([-0.8, -1], [-0.5, -0.5], 'k-', linewidth=2)
            
            # Draw resistor symbol
            circuit_fig.plot([0.5, 0.7, 0.9, 1.1, 1.3, 1.5], 
                            [0.5, 0.8, 0.2, 0.8, 0.2, 0.5], 'k-', linewidth=2)
            
            # Draw wires
            circuit_fig.plot([-1, 1.5], [0.5, 0.5], 'k-', linewidth=2)
            circuit_fig.plot([-1, 1.5], [-0.5, -0.5], 'k-', linewidth=2)
            
            # Add voltage indicator
            voltage_height = 0.3 + 0.7 * (voltage / V_max)
            circuit_fig.arrow(-1, -0.5, 0, voltage_height, 
                             head_width=0.1, color='red', length_includes_head=True)
            
            # Add current indicator (proportional to voltage)
            current_scale = 0.3 + 0.7 * (voltage / V_max)
            circuit_fig.arrow(0, -0.5, 0.2, 0, 
                             head_width=0.1, color='blue', 
                             length_includes_head=True,
                             width=0.02 * current_scale)
            
            circuit_fig.set_title('Circuit Visualization')
            circuit_fig.axis('equal')
            circuit_fig.axis('off')
            
            # Plot 2: Voltage and Derivatives
            self.eng_ax2.plot(t % ramp_period, 
                             (V_max * t / ramp_period) % V_max, 
                             'b-', label='Voltage (V)')
            self.eng_ax2.axhline(y=dv_dt, color='g', linestyle='--', 
                                label='dV/dt (V/s)')
            self.eng_ax2.axhline(y=d2v_dt2, color='r', linestyle=':', 
                                label='d²V/dt² (V/s²)')
            
            # Add current point indicator
            self.eng_ax2.plot(t_current, voltage, 'bo', markersize=10)
            
            self.eng_ax2.set_xlim(0, ramp_period)
            self.eng_ax2.set_ylim(-2, V_max + 2)
            self.eng_ax2.grid(True)
            self.eng_ax2.legend()
            self.eng_ax2.set_title('Voltage and Derivatives')
            
            # Update explanation
            self.eng_explanation.setText(f"""
                <h2>⚡ Voltage Ramp Analysis</h2>
                
                <p><b>Current Values:</b><br>
                • Voltage: {voltage:.2f} V<br>
                • Rate of Change (dV/dt): {dv_dt:.2f} V/s<br>
                • Acceleration (d²V/dt²): {d2v_dt2:.2f} V/s²</p>
                
                <p><b>Circuit Behavior:</b><br>
                • Voltage increases linearly with time<br>
                • Current is proportional to voltage (Ohm's Law)<br>
                • Rate of change is constant<br>
                • No acceleration (linear ramp)</p>
                
                <p><b>Key Derivatives:</b><br>
                • First derivative (dV/dt) shows rate of voltage change<br>
                • Second derivative (d²V/dt²) is zero for linear ramp<br>
                • Constant dV/dt means steady increase<br>
                • Zero d²V/dt² means no curvature</p>
                
                <p><b>Applications:</b><br>
                • Power supply testing<br>
                • Motor speed control<br>
                • Signal generation<br>
                • Capacitor charging</p>
            """)

        # ... (other examples will be restored next) ...