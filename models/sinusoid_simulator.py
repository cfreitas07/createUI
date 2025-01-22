from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QLabel, QPushButton, QLineEdit, QFrame, QTabWidget,
                            QGridLayout, QSlider, QComboBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QPen, QColor, QFont
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class SinusoidSimulator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sinusoid Wave Explorer 📊")
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
                background-color: #2196F3;
                color: white;
            }
        """)

        tabs.addTab(self.create_wave_simulator_tab(), "🌊 Wave Simulator")
        tabs.addTab(self.create_phase_analysis_tab(), "📐 Phase Analysis")
        tabs.addTab(self.create_learn_tab(), "📚 Quick Guide")
        
        layout.addWidget(tabs)

    def create_wave_simulator_tab(self):
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
            QLineEdit {
                padding: 8px;
                border: 2px solid #2196F3;
                border-radius: 8px;
                font-size: 14px;
                color: black;
                background-color: white;
            }
            QPushButton {
                padding: 10px 20px;
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QSlider {
                height: 25px;
            }
            QSlider::groove:horizontal {
                border: 1px solid #999999;
                height: 8px;
                background: #ffffff;
                margin: 2px 0;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: #2196F3;
                border: 1px solid #5c5c5c;
                width: 18px;
                margin: -2px 0;
                border-radius: 9px;
            }
        """)
        
        layout = QVBoxLayout(frame)

        # Title
        title = QLabel("🌊 Interactive Sinusoid Wave")
        title.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Create matplotlib figure with greater height
        self.figure = Figure(figsize=(12, 6))  # Increased height from 4 to 6
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        # Add more vertical space for the plot
        self.figure.subplots_adjust(left=0.05, right=0.95, top=0.92, bottom=0.12)

        # Parameters control panel
        controls = QGridLayout()

        # Amplitude control
        amp_label = QLabel("Amplitude (A):")
        self.amp_slider = QSlider(Qt.Orientation.Horizontal)
        self.amp_slider.setMinimum(0)
        self.amp_slider.setMaximum(100)
        self.amp_slider.setValue(50)
        self.amp_slider.valueChanged.connect(self.update_plot)
        controls.addWidget(amp_label, 0, 0)
        controls.addWidget(self.amp_slider, 0, 1)
        self.amp_value = QLabel("1.0")
        controls.addWidget(self.amp_value, 0, 2)

        # Frequency control
        freq_label = QLabel("Frequency (f):")
        self.freq_slider = QSlider(Qt.Orientation.Horizontal)
        self.freq_slider.setMinimum(1)
        self.freq_slider.setMaximum(100)
        self.freq_slider.setValue(10)
        self.freq_slider.valueChanged.connect(self.update_plot)
        controls.addWidget(freq_label, 1, 0)
        controls.addWidget(self.freq_slider, 1, 1)
        self.freq_value = QLabel("1.0 Hz")
        controls.addWidget(self.freq_value, 1, 2)

        # Phase control
        phase_label = QLabel("Phase (φ):")
        self.phase_slider = QSlider(Qt.Orientation.Horizontal)
        self.phase_slider.setMinimum(-180)
        self.phase_slider.setMaximum(180)
        self.phase_slider.setValue(0)
        self.phase_slider.valueChanged.connect(self.update_plot)
        controls.addWidget(phase_label, 2, 0)
        controls.addWidget(self.phase_slider, 2, 1)
        self.phase_value = QLabel("0°")
        controls.addWidget(self.phase_value, 2, 2)

        # DC Offset control
        offset_label = QLabel("DC Offset:")
        self.offset_slider = QSlider(Qt.Orientation.Horizontal)
        self.offset_slider.setMinimum(-100)
        self.offset_slider.setMaximum(100)
        self.offset_slider.setValue(0)
        self.offset_slider.valueChanged.connect(self.update_plot)
        controls.addWidget(offset_label, 3, 0)
        controls.addWidget(self.offset_slider, 3, 1)
        self.offset_value = QLabel("0.0")
        controls.addWidget(self.offset_value, 3, 2)

        layout.addLayout(controls)

        # Wave information display
        self.info_display = QLabel()
        self.info_display.setStyleSheet("""
            QLabel {
                background-color: #f8f9fa;
                padding: 10px;
                border-radius: 8px;
                border: 1px solid #dee2e6;
            }
        """)
        layout.addWidget(self.info_display)

        # Initialize the plot
        self.update_plot()

        return frame

    def create_phase_analysis_tab(self):
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                padding: 20px;
            }
        """)
        
        layout = QVBoxLayout(frame)

        # Title
        title = QLabel("📐 Phase Relationship Analysis")
        title.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Create matplotlib figure for phase comparison
        self.phase_figure = Figure(figsize=(8, 6))
        self.phase_canvas = FigureCanvas(self.phase_figure)
        layout.addWidget(self.phase_canvas)

        # Phase comparison controls
        phase_controls = QHBoxLayout()
        
        # Wave 1 phase
        self.wave1_phase = QSlider(Qt.Orientation.Horizontal)
        self.wave1_phase.setMinimum(-180)
        self.wave1_phase.setMaximum(180)
        self.wave1_phase.setValue(0)
        self.wave1_phase.valueChanged.connect(self.update_phase_plot)
        
        # Wave 2 phase
        self.wave2_phase = QSlider(Qt.Orientation.Horizontal)
        self.wave2_phase.setMinimum(-180)
        self.wave2_phase.setMaximum(180)
        self.wave2_phase.setValue(90)
        self.wave2_phase.valueChanged.connect(self.update_phase_plot)

        phase_controls.addWidget(QLabel("Wave 1 Phase:"))
        phase_controls.addWidget(self.wave1_phase)
        phase_controls.addWidget(QLabel("Wave 2 Phase:"))
        phase_controls.addWidget(self.wave2_phase)
        
        layout.addLayout(phase_controls)

        # Phase difference display
        self.phase_info = QLabel()
        self.phase_info.setStyleSheet("""
            QLabel {
                background-color: #f8f9fa;
                padding: 10px;
                border-radius: 8px;
                border: 1px solid #dee2e6;
            }
        """)
        layout.addWidget(self.phase_info)

        # Initialize the phase plot
        self.update_phase_plot()

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
        <h2>📚 Understanding Sinusoidal Waves</h2>
        
        <h3>🌊 Wave Components:</h3>
        <ul>
            <li><b>Amplitude (A):</b> The peak value of the wave</li>
            <li><b>Frequency (f):</b> Number of cycles per second (Hz)</li>
            <li><b>Phase (φ):</b> Horizontal shift of the wave</li>
            <li><b>Period (T):</b> Time for one complete cycle (T = 1/f)</li>
        </ul>

        <h3>📐 Important Relationships:</h3>
        <ul>
            <li>Angular frequency: ω = 2πf</li>
            <li>Wave equation: y = A·sin(ωt + φ)</li>
            <li>Phase in radians = Phase in degrees × (π/180)</li>
        </ul>

        <h3>💡 Tips:</h3>
        <ul>
            <li>Experiment with different parameters</li>
            <li>Observe how phase shifts affect the wave</li>
            <li>Compare multiple waves to understand phase relationships</li>
            <li>Notice the relationship between frequency and period</li>
        </ul>
        """)
        guide.setStyleSheet("font-size: 14px; color: black;")
        guide.setWordWrap(True)
        layout.addWidget(guide)

        return frame

    def update_plot(self):
        # Clear the figure
        self.figure.clear()

        # Get values from sliders
        amplitude = self.amp_slider.value() / 50.0  # Scale to 0-2
        frequency = self.freq_slider.value() / 10.0  # Scale to 0.1-10 Hz
        phase = self.phase_slider.value() * np.pi / 180  # Convert to radians
        offset = self.offset_slider.value() / 50.0  # Scale to -2 to 2

        # Update value labels
        self.amp_value.setText(f"{amplitude:.1f}")
        self.freq_value.setText(f"{frequency:.1f} Hz")
        self.phase_value.setText(f"{self.phase_slider.value()}°")
        self.offset_value.setText(f"{offset:.1f}")

        # Create time array with more points for smoother curve
        t = np.linspace(0, 4, 4000)  # Show 4 seconds of wave with high resolution

        # Calculate wave
        y = amplitude * np.sin(2 * np.pi * frequency * t + phase) + offset

        # Create subplot with larger vertical range
        ax = self.figure.add_subplot(111)
        ax.plot(t, y, 'b-', linewidth=2.5)
        
        # Set fixed axis limits with larger vertical range
        ax.set_xlim(0, 4)
        ax.set_ylim(-4, 4)  # Increased from (-3, 3) to (-4, 4)
        
        # Adjust font sizes for better visibility
        ax.set_xlabel('Time (s)', fontsize=12)
        ax.set_ylabel('Amplitude', fontsize=12)
        ax.set_title('Sinusoidal Wave', fontsize=14, pad=10)
        ax.tick_params(axis='both', which='major', labelsize=10)
        
        # Grid settings
        ax.grid(True, linestyle='--', alpha=0.7)
        ax.grid(True, which='minor', linestyle=':', alpha=0.4)
        ax.minorticks_on()

        # Update reference lines for larger range
        ax.axhline(y=0, color='k', linestyle='-', alpha=0.3)
        ax.axhline(y=amplitude + offset, color='r', linestyle=':', alpha=0.5)
        ax.axhline(y=-amplitude + offset, color='r', linestyle=':', alpha=0.5)

        # Add vertical grid lines at period intervals if frequency > 0
        if frequency > 0:
            period = 1/frequency
            for i in range(int(4/period) + 1):
                ax.axvline(x=i*period, color='g', linestyle=':', alpha=0.3)

        # Adjust layout
        self.figure.tight_layout()

        # Draw the canvas
        self.canvas.draw()

        # Update information display with more details
        period = 1/frequency if frequency != 0 else float('inf')
        angular_freq = 2 * np.pi * frequency
        
        info_text = f"""
        <b>Wave Parameters:</b><br>
        • Amplitude (A): {amplitude:.2f} units<br>
        • Period (T): {period:.2f} s<br>
        • Frequency (f): {frequency:.2f} Hz<br>
        • Angular Frequency (ω): {angular_freq:.2f} rad/s<br>
        • Phase (φ): {self.phase_slider.value()}°<br>
        • DC Offset: {offset:.2f} units<br>
        • Equation: y = {amplitude:.1f} · sin(2π · {frequency:.1f}t + {self.phase_slider.value()}°) + {offset:.1f}
        """
        self.info_display.setText(info_text)

    def update_phase_plot(self):
        # Clear the figure
        self.phase_figure.clear()

        # Get phase values
        phase1 = self.wave1_phase.value() * np.pi / 180
        phase2 = self.wave2_phase.value() * np.pi / 180

        # Create time array
        t = np.linspace(0, 2, 1000)

        # Calculate waves
        y1 = np.sin(2 * np.pi * t + phase1)
        y2 = np.sin(2 * np.pi * t + phase2)

        # Create subplot
        ax = self.phase_figure.add_subplot(111)
        ax.plot(t, y1, 'b-', label='Wave 1', linewidth=2)
        ax.plot(t, y2, 'r--', label='Wave 2', linewidth=2)
        ax.grid(True)
        ax.legend()
        ax.set_xlabel('Time (s)')
        ax.set_ylabel('Amplitude')
        ax.set_title('Phase Relationship')

        # Set y-axis limits
        ax.set_ylim(-1.5, 1.5)

        # Draw the canvas
        self.phase_canvas.draw()

        # Calculate phase difference
        phase_diff = abs(self.wave1_phase.value() - self.wave2_phase.value())
        phase_diff = phase_diff % 360
        if phase_diff > 180:
            phase_diff = 360 - phase_diff

        # Update phase information
        relationship = "In Phase" if phase_diff == 0 else \
                      "180° Out of Phase" if phase_diff == 180 else \
                      "Quadrature (90°)" if phase_diff == 90 else \
                      f"{phase_diff}° Phase Difference"

        info_text = f"""
        <b>Phase Analysis:</b><br>
        • Wave 1 Phase: {self.wave1_phase.value()}°<br>
        • Wave 2 Phase: {self.wave2_phase.value()}°<br>
        • Phase Difference: {phase_diff}°<br>
        • Relationship: {relationship}
        """
        self.phase_info.setText(info_text) 