from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QLabel, QPushButton, QLineEdit, QFrame, QTabWidget,
                            QGridLayout, QSlider, QComboBox, QSpinBox, QDoubleSpinBox,
                            QDialog, QScrollArea)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QPen, QColor, QFont, QPixmap
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class SinusoidSimulator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sinusoid Wave Explorer")
        
        # Create main layout
        layout = QVBoxLayout(self)
        
        # Create tab widget
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #cccccc;
                background: white;
                border-radius: 5px;
            }
            QTabBar::tab {
                background: #f0f0f0;
                border: 1px solid #cccccc;
                padding: 8px 12px;
                margin-right: 2px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected {
                background: white;
                border-bottom-color: white;
            }
            QTabBar::tab:hover {
                background: #e0e0e0;
            }
        """)
        
        # Create Wave Simulator tab
        simulator_tab = QWidget()
        self.setup_simulator_tab(simulator_tab)
        self.tab_widget.addTab(simulator_tab, "🌊 Wave Simulator")
        
        # Create Real World Examples tab
        examples_tab = QWidget()
        self.create_examples_tab(examples_tab)
        self.tab_widget.addTab(examples_tab, "🔬 Real World Examples")
        
        # Add tab widget to main layout
        layout.addWidget(self.tab_widget)
        
        # Set window size
        self.resize(1400, 800)

    def setup_simulator_tab(self, tab):
        """Setup the wave simulator tab"""
        # Create layout for the tab
        tab_layout = QVBoxLayout(tab)
        
        # Create matplotlib figure
        self.figure, self.ax = plt.subplots(figsize=(15, 6))
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setMinimumHeight(300)
        tab_layout.addWidget(self.canvas)
        
        # Create controls
        controls_layout = QVBoxLayout()
        controls_layout.setSpacing(15)
        
        # Amplitude control
        amp_layout = QHBoxLayout()
        amp_label = QLabel("Amplitude (A):")
        amp_label.setMinimumWidth(100)
        self.amp_slider = QSlider(Qt.Orientation.Horizontal)
        self.amp_slider.setRange(0, 500)
        self.amp_slider.setValue(100)
        self.amp_value_label = QLabel("1.0")
        self.amp_value_label.setMinimumWidth(50)
        self.amp_slider.valueChanged.connect(self.update_wave)
        self.amp_slider.valueChanged.connect(
            lambda v: self.amp_value_label.setText(f"{v/100:.1f}")
        )
        amp_layout.addWidget(amp_label)
        amp_layout.addWidget(self.amp_slider)
        amp_layout.addWidget(self.amp_value_label)
        controls_layout.addLayout(amp_layout)
        
        # Frequency control
        freq_layout = QHBoxLayout()
        freq_label = QLabel("Frequency (f):")
        freq_label.setMinimumWidth(100)
        self.freq_slider = QSlider(Qt.Orientation.Horizontal)
        self.freq_slider.setRange(0, 500)
        self.freq_slider.setValue(100)
        self.freq_value_label = QLabel("1.0")
        self.freq_value_label.setMinimumWidth(50)
        self.freq_slider.valueChanged.connect(self.update_wave)
        self.freq_slider.valueChanged.connect(
            lambda v: self.freq_value_label.setText(f"{v/100:.1f}")
        )
        freq_layout.addWidget(freq_label)
        freq_layout.addWidget(self.freq_slider)
        freq_layout.addWidget(self.freq_value_label)
        controls_layout.addLayout(freq_layout)
        
        # Phase control
        phase_layout = QHBoxLayout()
        phase_label = QLabel("Phase (φ):")
        phase_label.setMinimumWidth(100)
        self.phase_slider = QSlider(Qt.Orientation.Horizontal)
        self.phase_slider.setRange(0, 360)
        self.phase_slider.setValue(0)
        self.phase_value_label = QLabel("0°")
        self.phase_value_label.setMinimumWidth(50)
        self.phase_slider.valueChanged.connect(self.update_wave)
        self.phase_slider.valueChanged.connect(
            lambda v: self.phase_value_label.setText(f"{v}°")
        )
        phase_layout.addWidget(phase_label)
        phase_layout.addWidget(self.phase_slider)
        phase_layout.addWidget(self.phase_value_label)
        controls_layout.addLayout(phase_layout)
        
        # DC Offset control
        offset_layout = QHBoxLayout()
        offset_label = QLabel("DC Offset:")
        offset_label.setMinimumWidth(100)
        self.offset_slider = QSlider(Qt.Orientation.Horizontal)
        self.offset_slider.setRange(-200, 200)
        self.offset_slider.setValue(0)
        self.offset_value_label = QLabel("0.0")
        self.offset_value_label.setMinimumWidth(50)
        self.offset_slider.valueChanged.connect(self.update_wave)
        self.offset_slider.valueChanged.connect(
            lambda v: self.offset_value_label.setText(f"{v/100:.1f}")
        )
        offset_layout.addWidget(offset_label)
        offset_layout.addWidget(self.offset_slider)
        offset_layout.addWidget(self.offset_value_label)
        controls_layout.addLayout(offset_layout)
        
        # Add wave parameters display
        params_frame = QFrame()
        params_frame.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 5px;
                padding: 10px;
                margin-top: 10px;
            }
        """)
        params_layout = QVBoxLayout(params_frame)
        self.params_label = QLabel()
        self.params_label.setStyleSheet("""
            QLabel {
                font-size: 12pt;
                line-height: 1.6;
            }
        """)
        params_layout.addWidget(self.params_label)
        controls_layout.addWidget(params_frame)
        
        # Add equation display
        equation_frame = QFrame()
        equation_frame.setStyleSheet("""
            QFrame {
                background-color: #e8f4f8;
                border: 1px solid #bee5eb;
                border-radius: 5px;
                padding: 15px;
                margin-top: 10px;
            }
        """)
        equation_layout = QVBoxLayout(equation_frame)
        self.equation_label = QLabel()
        self.equation_label.setStyleSheet("""
            QLabel {
                font-size: 14pt;
                font-weight: bold;
                color: #2c3e50;
            }
        """)
        self.equation_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        equation_layout.addWidget(self.equation_label)
        controls_layout.addWidget(equation_frame)
        
        # Add the controls layout to the tab layout
        tab_layout.addLayout(controls_layout)
        
        # Initial wave update
        self.update_wave()

    def create_examples_tab(self, tab):
        """Create the real world examples tab"""
        layout = QVBoxLayout()
        
        # Create example selector
        selector_layout = QHBoxLayout()
        selector_label = QLabel("Select Engineering Application:")
        selector_label.setStyleSheet("font-size: 14pt; font-weight: bold;")
        
        self.example_selector = QComboBox()
        self.example_selector.setStyleSheet("""
            QComboBox {
                font-size: 12pt;
                padding: 8px;
                min-width: 400px;
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                background-color: white;
            }
        """)
        
        # Add examples
        examples = [
            "⚡ Electrical: AC Power Signal (60 Hz)",
            "⚡ Electrical: Radio Wave Modulation",
            "⚡ Electrical: Power Factor Analysis",
            "🔧 Mechanical: Engine Piston Motion",
            "🔧 Mechanical: Spring-Mass Oscillation",
            "🔧 Mechanical: Damped Vibration",
            "🏗️ Civil: Bridge Resonance",
            "🏗️ Civil: Seismic Wave Analysis",
            "🏗️ Civil: Wind Load Oscillation",
            "💻 Computer: Digital Signal Sampling",
            "💻 Computer: Carrier Wave Modulation",
            "💻 Computer: Noise Filtering"
        ]
        
        self.example_selector.addItems(examples)
        self.example_selector.currentIndexChanged.connect(self.update_example)
        
        selector_layout.addWidget(selector_label)
        selector_layout.addWidget(self.example_selector)
        selector_layout.addStretch()
        layout.addLayout(selector_layout)
        
        # Create content display
        content_frame = QFrame()
        content_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 2px solid #bdc3c7;
                border-radius: 10px;
                padding: 20px;
                margin-top: 10px;
            }
        """)
        
        content_layout = QVBoxLayout(content_frame)
        
        # Add visualization
        self.example_figure, self.example_ax = plt.subplots(figsize=(12, 4))
        self.example_canvas = FigureCanvas(self.example_figure)
        content_layout.addWidget(self.example_canvas)
        
        # Add description
        self.example_description = QLabel()
        self.example_description.setWordWrap(True)
        self.example_description.setStyleSheet("""
            QLabel {
                font-size: 12pt;
                line-height: 1.6;
                padding: 15px;
                background-color: #f8f9fa;
                border-radius: 5px;
            }
        """)
        content_layout.addWidget(self.example_description)
        
        layout.addWidget(content_frame)
        tab.setLayout(layout)
        
        # Initial example
        self.update_example(0)

    def update_wave(self):
        """Update wave with enhanced visualizations"""
        self.setup_plot()
        
        # Get values from sliders
        amp = self.amp_slider.value() / 100
        freq = self.freq_slider.value() / 100
        phase_deg = self.phase_slider.value()
        offset = self.offset_slider.value() / 100
        
        # Generate wave
        x = np.linspace(0, 4*np.pi, 1000)
        y = amp * np.sin(freq * x - np.deg2rad(phase_deg)) + offset
        
        # Plot main wave
        wave_line, = self.ax.plot(x, y, 'b-', linewidth=2, label='Sine Wave')
        
        # Add amplitude markers
        max_point = np.max(y)
        min_point = np.min(y)
        mid_point = offset
        
        # Draw amplitude lines and markers
        self.ax.vlines(x[0], mid_point, max_point, colors='r', linestyles='--', alpha=0.5)
        self.ax.vlines(x[0], mid_point, min_point, colors='r', linestyles='--', alpha=0.5)
        self.ax.hlines(mid_point, 0, 4*np.pi, colors='g', linestyles='--', alpha=0.5)
        
        # Add amplitude annotations
        self.ax.annotate(f'A = {amp:.2f}', 
                        xy=(x[0], max_point),
                        xytext=(x[0] + 0.2, max_point),
                        fontsize=10,
                        color='red')
        
        # Mark period
        period = 2*np.pi/freq
        self.ax.annotate(f'T = {period:.2f}',
                        xy=(period, offset),
                        xytext=(period, offset - 0.5),
                        fontsize=10,
                        color='blue',
                        arrowprops=dict(arrowstyle='->'))
        
        # Show phase shift
        if phase_deg != 0:
            phase_shift = np.deg2rad(phase_deg)
            shift_point = -phase_shift/freq
            self.ax.annotate(f'φ = {phase_deg}°',
                            xy=(0, 0),
                            xytext=(shift_point, -2),
                            fontsize=10,
                            color='purple',
                            arrowprops=dict(arrowstyle='->'))
        
        # Add legend for key components
        self.ax.legend(['Wave',
                       'Amplitude',
                       'Offset',
                       f'Period (T={period:.2f})',
                       f'Phase (φ={phase_deg}°)'])
        
        # Add key points markers
        zero_crossings = x[np.where(np.abs(y - offset) < 0.01)]
        peaks = x[np.where(np.abs(y - max_point) < 0.01)]
        troughs = x[np.where(np.abs(y - min_point) < 0.01)]
        
        self.ax.plot(zero_crossings, [offset]*len(zero_crossings), 'go', alpha=0.5, label='Zero Crossings')
        self.ax.plot(peaks, [max_point]*len(peaks), 'ro', alpha=0.5, label='Peaks')
        self.ax.plot(troughs, [min_point]*len(troughs), 'mo', alpha=0.5, label='Troughs')
        
        # Add frequency information
        angular_freq = freq * 2 * np.pi
        self.ax.text(0.02, 0.98, 
                    f'f = {freq:.2f} Hz\nω = {angular_freq:.2f} rad/s', 
                    transform=self.ax.transAxes,
                    verticalalignment='top',
                    bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        
        # Update parameters display
        self.params_label.setText(
            f"<div style='font-size: 12pt;'>"
            f"Wave Parameters:<br><br>"
            f"• Amplitude (A): {amp:.2f} units<br>"
            f"• Frequency (f): {freq:.2f} Hz<br>"
            f"• Phase (φ): {phase_deg}°<br>"
            f"• DC Offset: {offset:.2f} units<br>"
            f"• Angular Frequency (ω): {freq*2*np.pi:.2f} rad/s"
            f"</div>"
        )
        
        # Update equation display
        if offset >= 0:
            offset_str = f"+ {offset:.2f}"
        else:
            offset_str = f"- {abs(offset):.2f}"
        
        self.equation_label.setText(
            f"y = {amp:.2f} · sin(2π · {freq:.2f}t - {phase_deg}°) {offset_str}"
        )
        
        # Refresh canvas
        self.canvas.draw()

    def update_example(self, index):
        """Update the example display based on selection"""
        self.example_ax.clear()
        t = np.linspace(0, 4*np.pi, 1000)
        
        examples = {
            0: {  # AC Power
                'wave': 3*np.sin(2*np.pi*60*t/100),
                'title': '⚡ AC Power Signal (60 Hz)',
                'description': """
                <h3 style='color: #2980b9;'>Electrical Engineering: AC Power</h3>
                <p>Standard household electricity follows this sinusoidal pattern:</p>
                • Voltage: 120V RMS (170V peak)<br>
                • Frequency: 60 Hz (US standard)<br>
                • Complete cycle every 1/60th second<br>
                • Powers homes and industries worldwide
                """
            },
            1: {  # Radio Wave
                'wave': (1 + 0.3*np.sin(t)) * np.sin(10*t),
                'title': '⚡ AM Radio Wave Modulation',
                'description': """
                <h3 style='color: #2980b9;'>Electrical Engineering: Radio Communication</h3>
                <p>Amplitude Modulation (AM) combines carrier and signal waves:</p>
                • Carrier wave: High frequency<br>
                • Signal wave: Information to transmit<br>
                • Modulation depth: 30%<br>
                • Used in broadcasting and communication
                """
            },
            2: {  # Power Factor
                'wave': np.sin(t) + np.sin(t + np.pi/4),
                'title': '⚡ Power Factor Analysis',
                'description': """
                <h3 style='color: #2980b9;'>Electrical Engineering: Power Factor</h3>
                <p>Phase difference between voltage and current waves:</p>
                • Voltage and current signals<br>
                • Phase shift indicates power factor<br>
                • Critical for power efficiency<br>
                • Important in industrial applications
                """
            },
            3: {  # Engine Piston
                'wave': 2*np.cos(t) + 0.2*np.cos(3*t),
                'title': '🔧 Engine Piston Motion',
                'description': """
                <h3 style='color: #2980b9;'>Mechanical Engineering: Piston Motion</h3>
                <p>Piston displacement in an engine cylinder:</p>
                • Primary motion: Sinusoidal<br>
                • Harmonics from mechanical linkages<br>
                • Critical for engine timing<br>
                • Basis for engine dynamics
                """
            },
            4: {  # Spring-Mass
                'wave': 2*np.sin(2*t)*np.exp(-t/8),
                'title': '🔧 Spring-Mass Oscillation',
                'description': """
                <h3 style='color: #2980b9;'>Mechanical Engineering: Spring-Mass System</h3>
                <p>Natural oscillation with damping:</p>
                • Natural frequency determined by mass and spring<br>
                • Damping from friction and air resistance<br>
                • Amplitude decreases over time<br>
                • Fundamental mechanical system
                """
            },
            5: {  # Damped Vibration
                'wave': np.exp(-t/2)*np.sin(4*t),
                'title': '🔧 Damped Mechanical Vibration',
                'description': """
                <h3 style='color: #2980b9;'>Mechanical Engineering: Damped Vibration</h3>
                <p>Vibration analysis in mechanical systems:</p>
                • Exponential decay envelope<br>
                • Critical for machine design<br>
                • Used in shock absorber design<br>
                • Important for structural safety
                """
            },
            6: {  # Bridge Resonance
                'wave': np.sin(t) + 0.5*np.sin(2*t) + 0.2*np.sin(3*t),
                'title': '🏗️ Bridge Resonance',
                'description': """
                <h3 style='color: #2980b9;'>Civil Engineering: Bridge Dynamics</h3>
                <p>Multiple frequency components in bridge motion:</p>
                • Fundamental mode and harmonics<br>
                • Wind and traffic induced vibrations<br>
                • Critical for bridge design<br>
                • Safety monitoring parameter
                """
            },
            7: {  # Seismic Waves
                'wave': np.exp(-t/3)*(np.sin(8*t) + 0.5*np.sin(15*t)),
                'title': '🏗️ Seismic Wave Analysis',
                'description': """
                <h3 style='color: #2980b9;'>Civil Engineering: Seismic Analysis</h3>
                <p>Earthquake ground motion patterns:</p>
                • Multiple frequency components<br>
                • Rapid initial motion<br>
                • Gradual damping<br>
                • Used in structural design
                """
            },
            8: {  # Wind Load
                'wave': 2*np.sin(t/2) + 0.5*np.random.randn(len(t)),
                'title': '🏗️ Wind Load Oscillation',
                'description': """
                <h3 style='color: #2980b9;'>Civil Engineering: Wind Effects</h3>
                <p>Wind-induced structural motion:</p>
                • Base oscillation from wind<br>
                • Random turbulence components<br>
                • Critical for tall structures<br>
                • Used in facade design
                """
            },
            9: {  # Digital Sampling
                'wave': np.sin(3*t) + np.where(np.mod(t, 0.5) < 0.1, 0.3, 0),
                'title': '💻 Digital Signal Sampling',
                'description': """
                <h3 style='color: #2980b9;'>Computer Engineering: Signal Sampling</h3>
                <p>Analog to digital conversion process:</p>
                • Continuous signal<br>
                • Sampling points<br>
                • Quantization effects<br>
                • Nyquist sampling theorem
                """
            },
            10: {  # Carrier Wave
                'wave': np.sin(20*t) * np.sign(np.sin(2*t)),
                'title': '💻 Digital Carrier Modulation',
                'description': """
                <h3 style='color: #2980b9;'>Computer Engineering: Digital Communication</h3>
                <p>Digital data modulation techniques:</p>
                • Carrier signal<br>
                • Digital data encoding<br>
                • Binary phase shifts<br>
                • Used in digital communications
                """
            },
            11: {  # Noise Filtering
                'wave': np.sin(3*t) + 0.3*np.random.randn(len(t)),
                'title': '💻 Signal Noise Filtering',
                'description': """
                <h3 style='color: #2980b9;'>Computer Engineering: Noise Reduction</h3>
                <p>Digital signal processing for noise removal:</p>
                • Original signal with noise<br>
                • Random noise components<br>
                • Filtering techniques<br>
                • Signal recovery methods
                """
            }
        }
        
        example = examples.get(index, examples[0])
        
        # Plot with consistent styling
        self.example_ax.plot(t, example['wave'], 'b-', linewidth=2)
        self.example_ax.set_title(example['title'], fontsize=14, pad=10)
        self.example_ax.grid(True, alpha=0.3)
        self.example_ax.set_ylim(-3.5, 3.5)
        
        # Update description
        self.example_description.setText(example['description'])
        self.example_description.setTextFormat(Qt.TextFormat.RichText)
        
        # Refresh canvas
        self.example_canvas.draw()

    def setup_plot(self):
        """Enhanced plot setup with better visualization aids"""
        self.ax.clear()
        
        # Set up grid with π markings
        self.ax.grid(True, which='major', linestyle='-', alpha=0.3)
        self.ax.grid(True, which='minor', linestyle=':', alpha=0.2)
        
        # Set π-based x-ticks
        pi_ticks = np.arange(0, 4.5*np.pi, np.pi/2)
        pi_labels = ['0', 'π/2', 'π', '3π/2', '2π', '5π/2', '3π', '7π/2', '4π']
        self.ax.set_xticks(pi_ticks)
        self.ax.set_xticklabels(pi_labels)
        
        # Set y-axis limits and ticks
        self.ax.set_ylim(-4, 4)
        self.ax.set_yticks(np.arange(-4, 5, 1))
        
        # Labels with better formatting
        self.ax.set_xlabel('Phase (radians)', fontsize=12, labelpad=10)
        self.ax.set_ylabel('Amplitude', fontsize=12)
        
        # Add horizontal line at y=0
        self.ax.axhline(y=0, color='k', linestyle='-', alpha=0.3)

    def show_quick_guide(self):
        """Show the quick guide dialog"""
        guide = QDialog(self)
        guide.setWindowTitle("Understanding Sinusoids")
        guide.setMinimumSize(800, 600)
        
        # Create layout
        layout = QVBoxLayout(guide)
        
        # Create scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background-color: white; }")
        
        # Create content widget
        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setSpacing(20)
        
        # Add rich text content
        guide_text = f"""
        <div style='font-size: 14pt; line-height: 1.6; color: #2c3e50;'>
            <h1 style='color: #2980b9; font-size: 24pt; margin-bottom: 20px;'>
                Understanding Sinusoidal Waves
            </h1>
            
            <h2 style='color: #2980b9; margin-top: 20px;'>Key Components</h2>
            
            <div style='background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin: 10px 0;'>
                <p><b>1. Amplitude (A)</b></p>
                • Controls the height of the wave<br>
                • Measured from center to peak<br>
                • Example: A = 2 means the wave peaks at +2 and -2
            </div>
            
            <div style='background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin: 10px 0;'>
                <p><b>2. Frequency (f)</b></p>
                • Determines how many cycles per second<br>
                • Measured in Hertz (Hz)<br>
                • Example: f = 2 Hz means 2 complete cycles per second
            </div>
            
            <div style='background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin: 10px 0;'>
                <p><b>3. Phase (φ)</b></p>
                • Shifts the wave left or right<br>
                • Measured in degrees (°)<br>
                • 360° = one complete cycle<br>
                • Positive phase → shifts left<br>
                • Negative phase → shifts right
            </div>
            
            <div style='background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin: 10px 0;'>
                <p><b>4. DC Offset</b></p>
                • Moves the entire wave up or down<br>
                • Doesn't change the shape<br>
                • Example: +1 offset moves everything up 1 unit
            </div>
            
            <h2 style='color: #2980b9; margin-top: 20px;'>Reading the Wave Equation</h2>
            
            <div style='background-color: #e8f4f8; padding: 20px; border-radius: 5px; margin: 10px 0;'>
                <p style='font-size: 16pt; font-weight: bold;'>y = A · sin(2πft - φ) + offset</p>
                
                <p>Example: y = 2.0 · sin(2π · 1.5t - 90°) + 1.0</p>
                • Amplitude = 2.0 units (peak-to-peak = 4.0)<br>
                • Frequency = 1.5 Hz (1.5 cycles per second)<br>
                • Phase = 90° (quarter cycle shift left)<br>
                • DC Offset = +1.0 (entire wave shifted up)
            </div>
            
            <h2 style='color: #2980b9; margin-top: 20px;'>Quick Tips</h2>
            
            <div style='background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin: 10px 0;'>
                1. Start by setting amplitude to see wave height<br>
                2. Adjust frequency to compress/expand the wave<br>
                3. Use phase to shift the wave position<br>
                4. Add offset to move the wave up/down<br>
                5. Watch how changes affect the equation
            </div>
            
            <h2 style='color: #2980b9; margin-top: 20px;'>Important Relationships</h2>
            
            <div style='background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin: 10px 0;'>
                • Period (T) = 1/frequency<br>
                • Angular frequency (ω) = 2πf<br>
                • One cycle = 2π radians = 360°
            </div>
        </div>
        """
        
        guide_label = QLabel(guide_text)
        guide_label.setWordWrap(True)
        guide_label.setTextFormat(Qt.TextFormat.RichText)
        content_layout.addWidget(guide_label)
        
        # Set content widget to scroll area
        scroll.setWidget(content)
        layout.addWidget(scroll)
        
        # Add close button
        close_button = QPushButton("Close")
        close_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 10px 20px;
                border-radius: 5px;
                font-size: 12pt;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        close_button.clicked.connect(guide.close)
        layout.addWidget(close_button)
        
        # Show dialog
        guide.exec() 