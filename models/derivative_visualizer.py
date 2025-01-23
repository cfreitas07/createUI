from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QLabel, QSplitter, QComboBox, QPushButton)
from PyQt6.QtCore import Qt, QTimer
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

class DerivativeVisualizer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Derivative Applications 📈")
        self.setGeometry(100, 100, 1400, 800)
        
        # Create main widget
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        
        # Top controls layout
        top_layout = QHBoxLayout()
        
        # Model selector
        selector_label = QLabel("Select Model:")
        self.model_selector = QComboBox()
        self.model_selector.addItems([
            "Robot Arm Motion",
            "Spring-Mass System",
            "Beam Bending",
            "Edge Detection",
            "Chemical Reactor",
            "Vehicle Dynamics",
            "Drone Control",
            "Maglev Train",
            "Vibration Analysis"
        ])
        self.model_selector.currentTextChanged.connect(self.change_model)
        
        # Play button
        self.play_button = QPushButton("▶ Play (3s)")
        self.play_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border-radius: 5px;
                padding: 5px 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.play_button.clicked.connect(self.toggle_animation)
        
        top_layout.addWidget(selector_label)
        top_layout.addWidget(self.model_selector)
        top_layout.addWidget(self.play_button)
        top_layout.addStretch()
        main_layout.addLayout(top_layout)
        
        # Content layout
        self.content_layout = QHBoxLayout()
        main_layout.addLayout(self.content_layout)
        
        # Initialize parameters
        self.animation_time = 0
        self.current_model = None
        self.animation_duration = 3.0  # 3 seconds
        
        # Initialize timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_animation)
        
        # Initialize first model
        self.change_model("Robot Arm Motion")
        
    def toggle_animation(self):
        """Toggle animation play/stop"""
        if not self.timer.isActive():
            # Start animation
            self.animation_time = 0
            self.timer.start(50)  # 50ms interval = 20fps
            self.play_button.setText("■ Stop")
            self.play_button.setStyleSheet("""
                QPushButton {
                    background-color: #f44336;
                    color: white;
                    border-radius: 5px;
                    padding: 5px 15px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #da190b;
                }
            """)
        else:
            # Stop animation
            self.timer.stop()
            self.animation_time = 0
            self.play_button.setText("▶ Play (3s)")
            self.play_button.setStyleSheet("""
                QPushButton {
                    background-color: #4CAF50;
                    color: white;
                    border-radius: 5px;
                    padding: 5px 15px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #45a049;
                }
            """)
            self.update_animation()  # Reset to initial state

    def update_animation(self):
        """Update animation frame"""
        if self.current_model == "Robot Arm Motion":
            self.update_robot_animation()
        elif self.current_model == "Spring-Mass System":
            self.update_spring_animation()
        elif self.current_model == "Beam Bending":
            self.update_beam_animation()
        elif self.current_model == "Edge Detection":
            self.update_edge_detection()
        elif self.current_model == "Chemical Reactor":
            self.update_chemical_reactor()
        elif self.current_model == "Vehicle Dynamics":
            self.update_vehicle_dynamics()
        elif self.current_model == "Drone Control":
            self.update_drone_control()
        elif self.current_model == "Maglev Train":
            self.update_maglev_train()
        elif self.current_model == "Vibration Analysis":
            self.update_vibration_analysis()
            
        # Check if animation duration is reached
        if self.animation_time >= self.animation_duration:
            self.timer.stop()
            self.animation_time = 0
            self.play_button.setText("▶ Play (3s)")
            self.play_button.setStyleSheet("""
                QPushButton {
                    background-color: #4CAF50;
                    color: white;
                    border-radius: 5px;
                    padding: 5px 15px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #45a049;
                }
            """)
        else:
            self.animation_time += 0.05  # 50ms in seconds

    def change_model(self, model_name):
        """Change the current simulation model"""
        # Stop any running animation
        if self.timer.isActive():
            self.timer.stop()
            self.play_button.setText("▶ Play (3s)")
            self.play_button.setStyleSheet("""
                QPushButton {
                    background-color: #4CAF50;
                    color: white;
                    border-radius: 5px;
                    padding: 5px 15px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #45a049;
                }
            """)
        
        # Clear the entire content layout
        while self.content_layout.count():
            child = self.content_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        # Reset animation time
        self.animation_time = 0
        self.current_model = model_name
        
        # Initialize model-specific parameters
        if model_name == "Robot Arm Motion":
            self.arm_length1 = 2.0
            self.arm_length2 = 1.5
        elif model_name == "Spring-Mass System":
            self.spring_k = 1.0
            self.mass_m = 1.0
        
        # Create new content
        # Left side - Animation
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        
        self.figure = Figure(figsize=(8, 8))
        self.canvas = FigureCanvas(self.figure)
        left_layout.addWidget(self.canvas)
        self.content_layout.addWidget(left_widget, stretch=60)
        
        # Right side - Analysis
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        
        # Initialize title and explanation
        title = ""
        explanation = ""
        
        # Set title and explanation based on model
        if model_name == "Robot Arm Motion":
            title = "Understanding Derivatives in Robotics"
            explanation = """
                <h3>Derivatives in Robot Motion</h3>
                <p>Watch how derivatives describe the robot's motion:</p>
                <ul>
                    <li><b>Position (x, y)</b>: Where the robot arm is</li>
                    <li><b>First Derivative (dx/dt, dy/dt)</b>: How fast it's moving</li>
                    <li><b>Purple Arrow</b>: Direction and speed of motion</li>
                </ul>
                <p>Key Concepts:</p>
                <ul>
                    <li>The derivative tells us the instantaneous rate of change</li>
                    <li>Larger derivatives mean faster motion</li>
                    <li>The direction of the derivative shows where the arm is heading</li>
                    <li>This helps robots move smoothly and precisely</li>
                </ul>
            """
        elif model_name == "Spring-Mass System":
            title = "Understanding Derivatives in Oscillation"
            explanation = """
                <h3>Derivatives in Spring Motion</h3>
                <p>Observe how derivatives describe oscillatory motion:</p>
                <ul>
                    <li><b>Position (x)</b>: Distance from equilibrium</li>
                    <li><b>First Derivative (dx/dt)</b>: Velocity</li>
                    <li><b>Second Derivative (d²x/dt²)</b>: Acceleration</li>
                </ul>
                <p>Key Concepts:</p>
                <ul>
                    <li>Position follows simple harmonic motion</li>
                    <li>Velocity is maximum at equilibrium</li>
                    <li>Acceleration is proportional to displacement</li>
                    <li>Energy oscillates between potential and kinetic</li>
                </ul>
            """
        elif model_name == "Beam Bending":
            title = "Understanding Derivatives in Beam Bending"
            explanation = """
                <h3>Derivatives in Beam Bending</h3>
                <p>Observe how derivatives relate to beam deformation:</p>
                <ul>
                    <li><b>y(x)</b>: Deflection curve</li>
                    <li><b>dy/dx</b>: Slope (First Derivative)</li>
                    <li><b>d²y/dx²</b>: Moment (Second Derivative)</li>
                    <li><b>d³y/dx³</b>: Shear Force (Third Derivative)</li>
                </ul>
                <p>Key Concepts:</p>
                <ul>
                    <li>Each derivative reveals different aspects of beam behavior</li>
                    <li>Maximum deflection occurs at the point of loading</li>
                    <li>Slope shows the rate of deflection change</li>
                    <li>Moment and shear are critical for beam design</li>
                </ul>
            """
        elif model_name == "Edge Detection":
            title = "Understanding Derivatives in Edge Detection"
            explanation = """
                <h3>Derivatives in Edge Detection</h3>
                <p>See how derivatives help detect edges:</p>
                <ul>
                    <li><b>Original Signal</b>: Light intensity values</li>
                    <li><b>First Derivative</b>: Rate of intensity change</li>
                    <li><b>Edge Detection</b>: High derivative locations</li>
                </ul>
                <p>Key Concepts:</p>
                <ul>
                    <li>Edges occur at sudden intensity changes</li>
                    <li>Large derivatives indicate edge locations</li>
                    <li>This principle extends to 2D for image processing</li>
                    <li>Foundation of computer vision algorithms</li>
                </ul>
            """
        elif model_name == "Chemical Reactor":
            title = "Understanding Derivatives in Chemical Reactor"
            explanation = """
                <h3>Derivatives in Chemical Reactor</h3>
                <p>Watch how derivatives help control temperature:</p>
                <ul>
                    <li><b>Temperature (T):</b> Current temperature</li>
                    <li><b>Concentration (C):</b> Current concentration</li>
                    <li><b>Heat Removal (Q):</b> Rate of heat removal</li>
                </ul>
                <p>Key Concepts:</p>
                <ul>
                    <li>Temperature control</li>
                    <li>Concentration control</li>
                    <li>Heat removal</li>
                    <li>Derivatives help prevent runaway reactions</li>
                </ul>
            """
        elif model_name == "Vehicle Dynamics":
            title = "Understanding Derivatives in Vehicle Dynamics"
            explanation = """
                <h3>Derivatives in Vehicle Dynamics</h3>
                <p>Watch how derivatives describe vehicle motion and suspension response:</p>
                <ul>
                    <li><b>Position (s):</b> Where the vehicle is</li>
                    <li><b>Velocity (v = ds/dt):</b> How fast it's moving</li>
                    <li><b>Acceleration (a = d²s/dt²):</b> Rate of speed change</li>
                </ul>
                <p>Key Concepts:</p>
                <ul>
                    <li><b>Motion Derivatives:</b>
                    <br>- Position (s): Where the vehicle is
                    <br>- Velocity (v = ds/dt): How fast it's moving
                    <br>- Acceleration (a = d²s/dt²): Rate of speed change</li>
                    
                    <li><b>Suspension System:</b>
                    <br>- Responds to road irregularities
                    <br>- Uses damped second-order dynamics
                    <br>- Balances comfort and control</li>
                </ul>
            """
        elif model_name == "Drone Control":
            title = "Understanding Derivatives in Drone Control"
            explanation = """
                <h3>Derivatives in Drone Control</h3>
                <p>Watch how derivatives help maintain stable flight:</p>
                <ul>
                    <li><b>PID Control:</b>
                    <br>- Proportional (P): Responds to current error
                    <br>- Integral (I): Accumulates past errors
                    <br>- Derivative (D): Anticipates future error</li>
                </ul>
                <p>Key Concepts:</p>
                <ul>
                    <li>PID control helps drones maintain a stable altitude</li>
                    <li>Derivatives help predict future behavior</li>
                    <li>This is crucial for autonomous flight</li>
                </ul>
            """
        elif model_name == "Maglev Train":
            title = "Understanding Derivatives in Maglev Train"
            explanation = """
                <h3>Derivatives in Maglev Train</h3>
                <p>Watch how derivatives control precise levitation and propulsion:</p>
                <ul>
                    <li><b>Gap:</b> Levitation gap</li>
                    <li><b>Current:</b> Electromagnet current</li>
                    <li><b>Magnetic Force:</b> Magnetic force</li>
                </ul>
                <p>Key Concepts:</p>
                <ul>
                    <li>Electromagnetic levitation</li>
                    <li>Real-time gap control</li>
                    <li>Disturbance rejection</li>
                    <li>Energy efficiency</li>
                </ul>
            """
        elif model_name == "Vibration Analysis":
            title = "Understanding Derivatives in Vibration Analysis"
            explanation = """
                <h3>Derivatives in Vibration Analysis</h3>
                <p>Watch how derivatives describe the behavior of a multi-degree-of-freedom system:</p>
                <ul>
                    <li><b>Mass Positions:</b> Displacements of individual masses</li>
                    <li><b>Velocities:</b> Rates of change in mass positions</li>
                    <li><b>Energy Components:</b> Kinetic and potential energy</li>
                </ul>
                <p>Key Concepts:</p>
                <ul>
                    <li>Derivatives help understand the dynamics of the system</li>
                    <li>They reveal the rate of change in various quantities</li>
                    <li>This is crucial for analyzing and controlling complex systems</li>
                </ul>
            """
        
        # Create and style title label
        title_label = QLabel(title)
        title_label.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #2196F3;
                padding: 10px;
            }
        """)
        right_layout.addWidget(title_label)
        
        # Analysis display
        self.analysis_label = QLabel()
        self.analysis_label.setStyleSheet("""
            QLabel {
                background-color: white;
                padding: 15px;
                border-radius: 10px;
                font-size: 14px;
                line-height: 1.6;
                margin: 5px;
            }
        """)
        right_layout.addWidget(self.analysis_label)
        
        # Explanation
        explanation_label = QLabel(explanation)
        explanation_label.setStyleSheet("""
            QLabel {
                background-color: #f5f5f5;
                padding: 20px;
                border-radius: 10px;
                font-size: 14px;
                line-height: 1.6;
                margin: 5px;
            }
        """)
        explanation_label.setWordWrap(True)
        right_layout.addWidget(explanation_label)
        
        self.content_layout.addWidget(right_widget, stretch=40)
        
        # Update initial state
        self.update_animation()

    def update_robot_animation(self):
        """Update robot arm animation"""
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        
        # Calculate joint angles
        theta1 = 0.5 * self.animation_time  # Base joint rotation
        theta2 = np.sin(self.animation_time)  # Elbow joint motion
        
        # Calculate joint positions
        x1 = self.arm_length1 * np.cos(theta1)
        y1 = self.arm_length1 * np.sin(theta1)
        
        x2 = x1 + self.arm_length2 * np.cos(theta1 + theta2)
        y2 = y1 + self.arm_length2 * np.sin(theta1 + theta2)
        
        # Plot robot arm
        ax.plot([0, x1], [0, y1], '-', color='#2196F3', linewidth=4, label='Link 1')
        ax.plot([x1, x2], [y1, y2], '-', color='#4CAF50', linewidth=4, label='Link 2')
        
        # Plot joints
        ax.plot(0, 0, 'o', color='#FFC107', markersize=15, label='Base')
        ax.plot(x1, y1, 'o', color='#FF9800', markersize=12, label='Elbow')
        ax.plot(x2, y2, 'o', color='#F44336', markersize=12, label='End')
        
        # Calculate velocities (derivatives)
        omega1 = 0.5  # Angular velocity of first joint
        omega2 = np.cos(self.animation_time)  # Varying second joint velocity
        
        dx = -self.arm_length1 * omega1 * np.sin(theta1) \
             - self.arm_length2 * (omega1 + omega2) * np.sin(theta1 + theta2)
        dy = self.arm_length1 * omega1 * np.cos(theta1) \
             + self.arm_length2 * (omega1 + omega2) * np.cos(theta1 + theta2)
        
        # Plot velocity vector
        velocity_magnitude = np.sqrt(dx**2 + dy**2)
        scale = 0.5
        ax.arrow(x2, y2, dx * scale, dy * scale, 
                head_width=0.1, head_length=0.2, fc='#9C27B0', ec='#9C27B0',
                label='Velocity')
        
        # Set plot properties
        ax.set_xlim(-4, 4)
        ax.set_ylim(-4, 4)
        ax.grid(True, linestyle='--', alpha=0.7)
        ax.set_aspect('equal')
        ax.legend(loc='upper right')
        ax.set_title('Robot Arm Motion and Derivatives', pad=20)
        
        self.canvas.draw()
        
        # Update analysis text
        self.analysis_label.setText(f"""
            <h4>Real-time Analysis:</h4>
            <p><b>Position:</b>
            <br>x = {x2:.2f}
            <br>y = {y2:.2f}</p>
            <p><b>Velocity (First Derivative):</b>
            <br>dx/dt = {dx:.2f}
            <br>dy/dt = {dy:.2f}
            <br>Speed = {velocity_magnitude:.2f}</p>
            <p>Notice how the velocity vector (purple arrow) 
            shows the instantaneous direction and speed of motion.</p>
        """)

    def update_spring_animation(self):
        """Update spring-mass animation"""
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        
        # Spring-mass parameters
        k = 1.0  # Spring constant
        m = 1.0  # Mass
        omega = np.sqrt(k/m)  # Natural frequency
        A = 2.0  # Amplitude
        
        # Calculate position and derivatives
        x = A * np.cos(3 * omega * self.animation_time)  # Position (faster animation)
        v = -3 * A * omega * np.sin(3 * omega * self.animation_time)  # Velocity
        a = -9 * A * omega**2 * np.cos(3 * omega * self.animation_time)  # Acceleration
        
        # Draw spring and mass
        wall_x = -3
        equilibrium_x = 0
        mass_x = equilibrium_x + x
        
        # Draw wall
        ax.plot([wall_x, wall_x], [-1, 1], 'k-', linewidth=3)
        
        # Draw spring (simplified zigzag)
        spring_x = np.linspace(wall_x, mass_x, 20)
        spring_y = 0.2 * np.sin(np.linspace(0, 4*np.pi, 20))
        ax.plot(spring_x, spring_y, 'b-', linewidth=2)
        
        # Draw mass
        mass = plt.Circle((mass_x, 0), 0.3, color='#4CAF50', fill=True)
        ax.add_artist(mass)
        
        # Draw velocity vector
        if abs(v) > 0.1:
            ax.arrow(mass_x, 0, v*0.2, 0, 
                    head_width=0.1, head_length=0.2, fc='#9C27B0', ec='#9C27B0')
        
        # Set plot properties
        ax.set_xlim(-4, 4)
        ax.set_ylim(-2, 2)
        ax.grid(True, linestyle='--', alpha=0.7)
        ax.set_aspect('equal')
        ax.set_title('Spring-Mass System Motion', pad=20)
        
        # Add equilibrium line
        ax.axvline(x=equilibrium_x, color='gray', linestyle='--', alpha=0.5)
        
        self.canvas.draw()
        
        # Update analysis text
        self.analysis_label.setText(f"""
            <h4>Real-time Analysis:</h4>
            <p><b>Position:</b>
            <br>x = {x:.2f}</p>
            <p><b>Velocity (First Derivative):</b>
            <br>dx/dt = {v:.2f}</p>
            <p><b>Acceleration (Second Derivative):</b>
            <br>d²x/dt² = {a:.2f}</p>
            <p>Notice how velocity is zero at maximum displacement
            and maximum at equilibrium position.</p>
        """)

    def update_beam_animation(self):
        """Update beam bending animation"""
        self.figure.clear()
        
        # Create two subplots: beam and moment diagram
        gs = self.figure.add_gridspec(2, 1, height_ratios=[2, 1])
        
        # Beam deflection plot
        ax_beam = self.figure.add_subplot(gs[0])
        
        # Calculate beam properties
        L = 10.0  # Beam length
        x = np.linspace(0, L, 100)
        P = 1000 * (1 + 0.5 * np.sin(5 * self.animation_time))  # Faster varying load
        E = 200e9  # Young's modulus (Pa)
        I = 1e-6   # Moment of inertia (m⁴)
        
        # Calculate deflection for simply supported beam with center point load
        deflection = -np.where(x <= L/2,
                            P*x*(L**2 - x**2)/(48*E*I*L),
                            P*(L-x)*(L**2 - (L-x)**2)/(48*E*I*L))
        
        # Calculate moment
        moment = np.where(x <= L/2, P*x/2, P*(L-x)/2)
        
        # Plot undeformed beam
        ax_beam.plot([0, L], [0, 0], 'k--', alpha=0.3, label='Undeformed')
        
        # Plot deformed beam
        scale = 100  # Scale factor for visible deflection
        ax_beam.plot(x, scale*deflection, 'b-', linewidth=3, label='Deformed')
        
        # Plot supports
        ax_beam.plot([0], [0], 'ks', markersize=15, label='Support')  # Left support
        ax_beam.plot([L], [0], 'ks', markersize=15)  # Right support
        
        # Plot load arrow
        arrow_length = 2
        ax_beam.arrow(L/2, arrow_length, 0, -1.5, 
                     head_width=0.2, head_length=0.5, fc='r', ec='r',
                     linewidth=2, label='Load')
        
        ax_beam.set_title('Beam Deflection', fontsize=12, pad=10)
        ax_beam.grid(True, linestyle='--', alpha=0.7)
        ax_beam.legend(loc='upper right')
        ax_beam.set_ylim(-3, 3)
        ax_beam.set_xlabel('Length (m)')
        ax_beam.set_ylabel('Deflection')
        
        # Moment diagram
        ax_moment = self.figure.add_subplot(gs[1])
        ax_moment.plot(x, moment/1000, 'r-', linewidth=2)
        ax_moment.fill_between(x, moment/1000, alpha=0.2, color='red')
        ax_moment.set_title('Bending Moment Diagram', fontsize=12, pad=10)
        ax_moment.grid(True, linestyle='--', alpha=0.7)
        ax_moment.set_xlabel('Length (m)')
        ax_moment.set_ylabel('Moment (kN⋅m)')
        
        self.figure.tight_layout()
        self.canvas.draw()
        
        # Update analysis text
        max_deflection = np.min(deflection)  # Using min since deflection is negative
        max_moment = np.max(moment)
        
        self.analysis_label.setText(f"""
            <h4>Real-time Analysis:</h4>
            <p><b>Applied Load:</b> {P/1000:.2f} kN</p>
            <p><b>Maximum Values:</b>
            <br>Deflection: {-max_deflection*1000:.2f} mm (at midspan)
            <br>Moment: {max_moment/1000:.2f} kN⋅m (at midspan)</p>
            <p>Key Points:</p>
            <ul>
                <li>The beam deflects downward under the load</li>
                <li>Maximum deflection occurs at the center</li>
                <li>Moment is maximum where the load is applied</li>
                <li>The relationship between load, moment, and deflection 
                    is described by derivatives</li>
            </ul>
        """)

    def update_edge_detection(self):
        """Update edge detection visualization"""
        self.figure.clear()
        
        # Create a 2x2 subplot grid
        gs = self.figure.add_gridspec(2, 2)
        
        # Generate a simple shape (circle)
        x = np.linspace(-5, 5, 100)
        y = np.linspace(-5, 5, 100)
        X, Y = np.meshgrid(x, y)
        
        # Create moving circle
        center_x = 2 * np.cos(3 * self.animation_time)
        radius = 3
        image = np.where((X - center_x)**2 + Y**2 < radius**2, 1, 0)
        
        # Calculate derivatives
        dx = np.gradient(image, axis=1)  # derivative in x direction
        dy = np.gradient(image, axis=0)  # derivative in y direction
        edges = np.sqrt(dx**2 + dy**2)   # combined edge strength
        
        # Plot original image
        ax1 = self.figure.add_subplot(gs[0, 0])
        ax1.imshow(image, cmap='gray')
        ax1.set_title('Original Image\nf(x,y)')
        ax1.axis('off')
        
        # Plot x-derivative
        ax2 = self.figure.add_subplot(gs[0, 1])
        ax2.imshow(dx, cmap='RdBu')
        ax2.set_title('X Derivative\n∂f/∂x')
        ax2.axis('off')
        
        # Plot y-derivative
        ax3 = self.figure.add_subplot(gs[1, 0])
        ax3.imshow(dy, cmap='RdBu')
        ax3.set_title('Y Derivative\n∂f/∂y')
        ax3.axis('off')
        
        # Plot combined edges
        ax4 = self.figure.add_subplot(gs[1, 1])
        ax4.imshow(edges, cmap='hot')
        ax4.set_title('Edge Strength\n√[(∂f/∂x)² + (∂f/∂y)²]')
        ax4.axis('off')
        
        self.figure.tight_layout()
        self.canvas.draw()
        
        # Update analysis text
        self.analysis_label.setText(f"""
            <h4>Understanding Derivatives in Edge Detection:</h4>
            <p>The process uses partial derivatives to find edges:</p>
            <ol>
                <li><b>Original Image [f(x,y)]:</b>
                <br>- Black and white regions
                <br>- Sharp intensity changes at boundaries</li>
                
                <li><b>X Derivative [∂f/∂x]:</b>
                <br>- Blue: Negative change (dark to light)
                <br>- Red: Positive change (light to dark)
                <br>- Detects vertical edges</li>
                
                <li><b>Y Derivative [∂f/∂y]:</b>
                <br>- Blue: Negative change (dark to light)
                <br>- Red: Positive change (light to dark)
                <br>- Detects horizontal edges</li>
                
                <li><b>Edge Strength:</b>
                <br>- Combines both derivatives
                <br>- Brighter = Stronger edge
                <br>- Formula: √[(∂f/∂x)² + (∂f/∂y)²]</li>
            </ol>
            <p>This is how derivatives help computers find object boundaries!</p>
        """)

    def update_chemical_reactor(self):
        """Update chemical reactor visualization"""
        self.figure.clear()
        gs = self.figure.add_gridspec(2, 2, height_ratios=[1.2, 1])
        
        # Reactor parameters
        V = 1000  # Reactor volume (L)
        Ea = 50000  # Activation energy (J/mol)
        R = 8.314   # Gas constant (J/mol·K)
        dH = -85000 # Heat of reaction (J/mol)
        k0 = 1e10   # Pre-exponential factor
        
        # Time array
        t = np.linspace(0, 3, 300)
        current_t = self.animation_time % 3
        current_idx = min(int(current_t * 100), len(t)-1)
        
        # Initialize arrays
        T = np.zeros_like(t)  # Temperature (K)
        C = np.zeros_like(t)  # Concentration (mol/L)
        Tc = np.zeros_like(t) # Coolant temperature (K)
        Q = np.zeros_like(t)  # Heat removal rate (kW)
        
        # Initial conditions
        T[0] = 300  # Initial temperature (K)
        C[0] = 2.0  # Initial concentration (mol/L)
        
        # Simulate reactor dynamics
        dt = t[1] - t[0]
        for i in range(1, len(t)):
            # Control system for coolant temperature
            T_set = 320  # Setpoint temperature
            error = T_set - T[i-1]
            
            # Adjust coolant temperature with constraints
            Tc[i] = T_set - 20 + 40 * np.clip(error/30, -1, 1)
            
            # Calculate reaction rate
            k = k0 * np.exp(-Ea/(R * T[i-1]))
            reaction_rate = k * C[i-1]
            
            # Heat generation from reaction
            Q_gen = reaction_rate * dH * V / 1000  # kW
            
            # Heat removal by coolant
            UA = 2.0  # Overall heat transfer coefficient * Area
            Q[i] = UA * (T[i-1] - Tc[i])  # Heat removal rate (kW)
            
            # Temperature change
            Cp = 4.18  # Heat capacity (kJ/kg·K)
            rho = 1.0  # Density (kg/L)
            dT = (Q_gen - Q[i]) / (V * rho * Cp) * dt
            T[i] = T[i-1] + dT
            
            # Concentration change
            dC = -reaction_rate * dt
            C[i] = C[i-1] + dC
        
        # Calculate derivatives
        dT_dt = np.gradient(T, t)
        dC_dt = np.gradient(C, t)
        
        # Plot reactor animation
        ax1 = self.figure.add_subplot(gs[0, :])
        ax1.set_aspect('equal')
        
        # Draw reactor vessel
        vessel = plt.Rectangle((3, 1), 4, 4, fc='lightgray', ec='black')
        ax1.add_patch(vessel)
        
        # Draw cooling jacket
        jacket = plt.Rectangle((2.7, 0.7), 4.6, 4.6, fc='none', ec='blue', ls='--')
        ax1.add_patch(jacket)
        
        # Draw fluid level with temperature-based color
        T_normalized = (T[current_idx] - 300) / 50  # Normalize temperature
        fluid_color = plt.cm.RdYlBu_r(T_normalized)
        fluid = plt.Rectangle((3, 1), 4, 4 * C[current_idx]/2, fc=fluid_color)
        ax1.add_patch(fluid)
        
        # Draw bubbles for reaction visualization
        for i in range(int(10 * reaction_rate)):
            x = 3 + 4 * np.random.random()
            y = 1 + 4 * C[current_idx]/2 * np.random.random()
            size = 0.2 * np.random.random()
            circle = plt.Circle((x, y), size, fc='white', alpha=0.6)
            ax1.add_patch(circle)
        
        # Draw cooling pipes
        ax1.plot([2.5, 2.5], [0.5, 6], 'b-', linewidth=2)
        ax1.plot([7.5, 7.5], [0.5, 6], 'b-', linewidth=2)
        
        # Add coolant flow indicators
        coolant_speed = abs(Q[current_idx]) / 10
        arrow_spacing = np.linspace(0.5, 6, 6)
        for y in arrow_spacing:
            ax1.arrow(2.5, y, 0, 0.3 * coolant_speed, 
                     head_width=0.1, head_length=0.1, fc='blue', ec='blue', alpha=0.6)
            ax1.arrow(7.5, y, 0, -0.3 * coolant_speed, 
                     head_width=0.1, head_length=0.1, fc='blue', ec='blue', alpha=0.6)
        
        # Add temperature indicators
        ax1.text(5, 5.5, f'T = {T[current_idx]:.1f} K', ha='center')
        ax1.text(2, 5.5, f'Tc = {Tc[current_idx]:.1f} K', ha='center', color='blue')
        ax1.text(5, 0.5, f'C = {C[current_idx]:.3f} mol/L', ha='center')
        
        ax1.set_xlim(0, 10)
        ax1.set_ylim(0, 7)
        ax1.axis('off')
        
        # Plot temperature and concentration
        ax2 = self.figure.add_subplot(gs[1, 0])
        if current_idx > 1:
            ax2.plot(t[:current_idx], T[:current_idx]-273.15, 'r-', label='Temp (°C)')
            ax2.plot(t[:current_idx], C[:current_idx], 'b-', label='Conc (M)')
            ax2.plot(t[:current_idx], Tc[:current_idx]-273.15, 'g--', label='Coolant (°C)')
            ax2.legend(loc='upper right')
        ax2.grid(True, linestyle='--', alpha=0.7)
        ax2.set_title('Reactor Conditions')
        
        # Plot derivatives and heat
        ax3 = self.figure.add_subplot(gs[1, 1])
        if current_idx > 1:
            ax3.plot(t[:current_idx], dT_dt[:current_idx], 'r-', label='dT/dt (K/s)')
            ax3.plot(t[:current_idx], dC_dt[:current_idx], 'b-', label='dC/dt (M/s)')
            ax3.plot(t[:current_idx], Q[:current_idx], 'g-', label='Q (kW)')
            ax3.legend(loc='upper right')
        ax3.grid(True, linestyle='--', alpha=0.7)
        ax3.set_title('Rates of Change')
        
        self.figure.tight_layout()
        self.canvas.draw()
        
        # Update analysis text
        self.analysis_label.setText(f"""
            <h4>Chemical Reactor Analysis:</h4>
            <p>Current State:</p>
            <ul>
                <li><b>Temperature:</b> {T[current_idx]-273.15:.1f}°C</li>
                <li><b>Concentration:</b> {C[current_idx]:.3f} mol/L</li>
                <li><b>Reaction Rate:</b> {reaction_rate:.3e} mol/L·s</li>
            </ul>
            <p>Heat Transfer:</p>
            <ul>
                <li><b>Heat Generated:</b> {Q_gen:.1f} kW</li>
                <li><b>Heat Removed:</b> {Q[current_idx]:.1f} kW</li>
                <li><b>Coolant Temp:</b> {Tc[current_idx]-273.15:.1f}°C</li>
            </ul>
            <p>Derivatives in Action:</p>
            <ul>
                <li><b>dT/dt:</b> {dT_dt[current_idx]:.2f} K/s</li>
                <li><b>dC/dt:</b> {dC_dt[current_idx]:.3e} mol/L·s</li>
                <li><b>Activation Energy:</b> {Ea/1000:.1f} kJ/mol</li>
            </ul>
            <p>Safety Indicators:</p>
            <ul>
                <li>Temperature control: {abs(T[current_idx]-T_set) < 10 and "✓ Stable" or "⚠ Check"}</li>
                <li>Reaction rate: {abs(reaction_rate) < 0.1 and "✓ Normal" or "⚠ High"}</li>
                <li>Cooling system: {abs(Q[current_idx]) > abs(Q_gen*0.9) and "✓ Effective" or "⚠ Warning"}</li>
            </ul>
        """)

    def update_vehicle_dynamics(self):
        """Update vehicle dynamics visualization"""
        self.figure.clear()
        
        # Create subplots
        gs = self.figure.add_gridspec(2, 2, height_ratios=[1.2, 1])
        
        # Time array
        t = np.linspace(0, 10, 1000)
        current_t = self.animation_time % 10
        
        # Vehicle position (s), velocity (v), and acceleration (a)
        # Simulate acceleration, cruise, and braking
        a = np.zeros_like(t)
        a[(t >= 1) & (t < 3)] = 3  # Acceleration
        a[(t >= 7) & (t < 9)] = -4  # Braking
        
        v = np.zeros_like(t)
        s = np.zeros_like(t)
        
        # Integrate acceleration to get velocity and position
        for i in range(1, len(t)):
            v[i] = v[i-1] + a[i-1] * (t[i] - t[i-1])
            s[i] = s[i-1] + v[i-1] * (t[i] - t[i-1])
        
        # Road profile (bumpy road)
        road = 0.1 * np.sin(2 * np.pi * t) + 0.05 * np.sin(5 * np.pi * t)
        
        # Suspension response (damped)
        omega = 2 * np.pi  # Natural frequency
        zeta = 0.3        # Damping ratio
        
        # Solve damped oscillator equation
        suspension = np.zeros_like(t)
        for i in range(1, len(t)):
            dt = t[i] - t[i-1]
            # Second-order response to road input
            suspension[i] = suspension[i-1] + dt * (
                omega * (road[i-1] - suspension[i-1]) - 
                2 * zeta * omega * suspension[i-1]
            )
        
        # Plot vehicle motion
        ax1 = self.figure.add_subplot(gs[0, :])
        
        # Draw road and vehicle
        road_x = np.linspace(0, 15, 100)
        current_idx = int(current_t * 100)
        
        # Plot road
        ax1.plot(road_x, 0.5 * road[:100], 'k-', alpha=0.3)
        
        # Draw vehicle (simplified)
        car_x = s[current_idx]
        car_y = 0.5 * suspension[current_idx] + 1
        
        # Vehicle body
        ax1.plot([car_x-1, car_x+1], [car_y, car_y], 'b-', linewidth=3)
        # Wheels
        ax1.plot([car_x-0.8, car_x+0.8], 
                [car_y-0.5, car_y-0.5], 'k-', linewidth=2)
        circle1 = plt.Circle((car_x-0.8, car_y-0.5), 0.2, color='k')
        circle2 = plt.Circle((car_x+0.8, car_y-0.5), 0.2, color='k')
        ax1.add_artist(circle1)
        ax1.add_artist(circle2)
        
        # Velocity vector
        if abs(v[current_idx]) > 0.1:
            ax1.arrow(car_x, car_y, 0.5*v[current_idx], 0, 
                     head_width=0.1, head_length=0.2, fc='r', ec='r')
        
        ax1.set_xlim(0, 15)
        ax1.set_ylim(-0.5, 2.5)
        ax1.set_title('Vehicle Motion and Suspension Response')
        ax1.grid(True, linestyle='--', alpha=0.7)
        
        # Plot velocity and acceleration
        ax2 = self.figure.add_subplot(gs[1, 0])
        ax2.plot(t[:current_idx], v[:current_idx], 'g-', label='Velocity (v)')
        ax2.plot(t[:current_idx], a[:current_idx], 'r-', label='Acceleration (a)')
        ax2.set_title('Velocity and Acceleration\n(First and Second Derivatives)')
        ax2.grid(True, linestyle='--', alpha=0.7)
        ax2.legend()
        
        # Plot suspension response
        ax3 = self.figure.add_subplot(gs[1, 1])
        ax3.plot(t[:current_idx], road[:current_idx], 'k--', 
                label='Road Profile', alpha=0.5)
        ax3.plot(t[:current_idx], suspension[:current_idx], 'b-', 
                label='Suspension')
        ax3.set_title('Suspension Response\n(Second-Order Dynamics)')
        ax3.grid(True, linestyle='--', alpha=0.7)
        ax3.legend()
        
        self.figure.tight_layout()
        self.canvas.draw()
        
        # Update analysis text
        self.analysis_label.setText(f"""
            <h4>Vehicle Dynamics and Derivatives:</h4>
            <p>Current Values:</p>
            <ul>
                <li><b>Position (s):</b> {s[current_idx]:.1f} m</li>
                <li><b>Velocity (v = ds/dt):</b> {v[current_idx]:.1f} m/s</li>
                <li><b>Acceleration (a = d²s/dt²):</b> {a[current_idx]:.1f} m/s²</li>
            </ul>
            <p>Key Concepts:</p>
            <ul>
                <li><b>Motion Derivatives:</b>
                <br>- Position (s): Where the vehicle is
                <br>- Velocity (v = ds/dt): How fast it's moving
                <br>- Acceleration (a = d²s/dt²): Rate of speed change</li>
                
                <li><b>Suspension System:</b>
                <br>- Responds to road irregularities
                <br>- Uses damped second-order dynamics
                <br>- Balances comfort and control</li>
            </ul>
        """)

    def update_drone_control(self):
        """Update drone PID control visualization"""
        self.figure.clear()
        gs = self.figure.add_gridspec(2, 2, height_ratios=[1.2, 1])
        
        # Time array (adjusted for 3-second animation)
        t = np.linspace(0, 3, 300)
        current_t = min(self.animation_time, 3.0)  # Limit time to 3 seconds
        current_idx = min(int(current_t * 100), len(t)-1)  # Ensure index is within bounds
        
        # Target altitude (setpoint) with more dynamic changes
        setpoint = 5.0 + 1.0 * np.sin(2 * np.pi * t) + 0.5 * np.sin(4 * np.pi * t)
        
        # PID parameters (tuned for faster response)
        Kp = 4.0  # Increased proportional gain
        Ki = 1.0  # Increased integral gain
        Kd = 1.5  # Increased derivative gain
        
        # Initialize arrays
        position = np.zeros_like(t)
        velocity = np.zeros_like(t)
        error = np.zeros_like(t)
        error_integral = np.zeros_like(t)
        control_signal = np.zeros_like(t)
        
        # Simulate drone dynamics with PID control
        dt = t[1] - t[0]
        position[0] = 4.0  # Initial position
        
        for i in range(1, len(t)):
            # Calculate error and its derivative
            error[i] = setpoint[i] - position[i-1]
            error_derivative = (error[i] - error[i-1]) / dt
            error_integral[i] = error_integral[i-1] + error[i] * dt
            
            # PID control signal with limits
            control_signal[i] = np.clip(
                Kp * error[i] + Ki * error_integral[i] + Kd * error_derivative,
                -20, 20  # Limit control signal
            )
            
            # Simulate drone physics (simplified)
            acceleration = control_signal[i] - 9.81  # Gravity compensation
            velocity[i] = velocity[i-1] + acceleration * dt
            position[i] = position[i-1] + velocity[i] * dt
        
        # Plot drone and setpoint
        ax1 = self.figure.add_subplot(gs[0, :])
        
        # Draw target altitude with trail
        ax1.plot(t[:current_idx], setpoint[:current_idx], 'g--', alpha=0.5)
        ax1.axhline(y=setpoint[current_idx-1], color='g', linestyle='--', 
                   label='Target', alpha=0.8)
        
        # Draw drone with dynamic elements
        drone_size = 0.5
        drone_x = 5
        drone_y = position[current_idx-1]
        
        # Drone body with thrust indication
        thrust = control_signal[current_idx-1]
        body_color = plt.cm.RdYlBu(thrust/20 + 0.5)  # Color based on thrust
        drone_body = plt.Rectangle((drone_x-drone_size, drone_y-drone_size/4), 
                                 drone_size*2, drone_size/2, 
                                 color=body_color, alpha=0.8)
        ax1.add_patch(drone_body)
        
        # Rotor animation
        rotor_speed = thrust * 0.3
        rotor_size = drone_size * 0.8
        angles = np.linspace(0, 2*np.pi, 20)
        rotor_x = rotor_size * np.cos(angles + rotor_speed * current_t)
        rotor_y = rotor_size * np.sin(angles + rotor_speed * current_t)
        
        # Left rotor
        ax1.plot(drone_x-drone_size + rotor_x, drone_y + rotor_y, 'k-', linewidth=1)
        # Right rotor
        ax1.plot(drone_x+drone_size + rotor_x, drone_y + rotor_y, 'k-', linewidth=1)
        
        # Thrust indicators
        if thrust > 0:
            thrust_height = 0.5 * thrust/20
            ax1.plot([drone_x-drone_size, drone_x+drone_size], 
                    [drone_y-drone_size, drone_y-drone_size], 
                    'r-', linewidth=2*thrust/20)
            ax1.plot([drone_x, drone_x], 
                    [drone_y-drone_size, drone_y-drone_size-thrust_height],
                    'r-', linewidth=2*thrust/20)
        
        ax1.set_xlim(0, 10)
        ax1.set_ylim(0, 8)
        ax1.set_title('Drone Altitude Control')
        ax1.grid(True, linestyle='--', alpha=0.7)
        
        # Plot error and control components
        ax2 = self.figure.add_subplot(gs[1, 0])
        if current_idx > 1:
            ax2.plot(t[:current_idx], error[:current_idx], 'r-', 
                    label='Error', alpha=0.7)
            ax2.plot(t[:current_idx], error_integral[:current_idx], 'g-', 
                    label='∫e dt', alpha=0.7)
            if current_idx > 2:
                derivative = np.gradient(error[:current_idx], t[:current_idx])
                ax2.plot(t[:current_idx], derivative, 'b-',
                        label='de/dt', alpha=0.7)
            ax2.legend(loc='upper right')
        
        ax2.set_title('PID Components')
        ax2.grid(True, linestyle='--', alpha=0.7)
        
        # Plot control signal and position
        ax3 = self.figure.add_subplot(gs[1, 1])
        if current_idx > 1:
            ax3.plot(t[:current_idx], control_signal[:current_idx], 'r-', 
                    label='Control')
            ax3.plot(t[:current_idx], position[:current_idx], 'b-', 
                    label='Altitude')
            ax3.plot(t[:current_idx], setpoint[:current_idx], 'g--', 
                    label='Target')
            ax3.legend(loc='upper right')
        
        ax3.set_title('System Response')
        ax3.grid(True, linestyle='--', alpha=0.7)
        
        self.figure.tight_layout()
        self.canvas.draw()
        
        # Update analysis text with more concise format
        self.analysis_label.setText(f"""
            <h4>PID Control in Drone Altitude:</h4>
            <p>Current Values:</p>
            <ul>
                <li><b>Target:</b> {setpoint[current_idx-1]:.1f} m</li>
                <li><b>Altitude:</b> {position[current_idx-1]:.1f} m</li>
                <li><b>Error:</b> {error[current_idx-1]:.2f} m</li>
            </ul>
            <p>PID Components:</p>
            <ul>
                <li><b>Proportional (P):</b> {Kp * error[current_idx-1]:.2f}</li>
                <li><b>Integral (I):</b> {Ki * error_integral[current_idx-1]:.2f}</li>
                <li><b>Derivative (D):</b> {Kd * (error[current_idx-1] - error[max(0, current_idx-2)]):.2f}</li>
                <li><b>Total Control:</b> {control_signal[current_idx-1]:.2f}</li>
            </ul>
        """)

    def update_maglev_train(self):
        """Update magnetic levitation train visualization"""
        self.figure.clear()
        gs = self.figure.add_gridspec(2, 2, height_ratios=[1.2, 1])
        
        # Adjusted system parameters
        m = 1000  # Train mass (kg)
        g = 9.81  # Gravity (m/s²)
        target_gap = 0.05  # Target levitation gap (m)
        k = 5e-6   # Magnetic force constant
        
        # PID control parameters (tuned for better stability)
        Kp = 8000
        Ki = 2000
        Kd = 4000
        
        # Time array
        t = np.linspace(0, 3, 300)
        current_t = self.animation_time % 3
        current_idx = min(int(current_t * 100), len(t)-1)
        
        # Initialize arrays
        gap = np.zeros_like(t)        # Levitation gap
        current = np.zeros_like(t)    # Electromagnet current
        force = np.zeros_like(t)      # Magnetic force
        velocity = np.zeros_like(t)   # Vertical velocity
        
        # Add external disturbances
        track_irregularity = 0.02 * np.sin(2 * np.pi * t)  # Track roughness
        passenger_movement = 0.01 * np.sin(5 * np.pi * t)   # Passenger movement
        
        # Simulate maglev dynamics
        dt = t[1] - t[0]
        gap[0] = target_gap
        error_integral = 0
        
        for i in range(1, len(t)):
            # Calculate error and its derivatives
            error = target_gap - gap[i-1]
            error_integral = np.clip(error_integral + error * dt, -10, 10)  # Anti-windup
            error_derivative = -velocity[i-1]
            
            # PID control for electromagnet current
            current[i] = np.clip(
                Kp * error + Ki * error_integral + Kd * error_derivative,
                0, 2000  # Increased current limit
            )
            
            # Improved magnetic force equation (more realistic)
            force[i] = k * (current[i]**2) / (gap[i-1]**2)
            
            # Net acceleration including damping
            damping = -50 * velocity[i-1]  # Add damping force
            acceleration = (force[i] - m*g + damping) / m
            
            # Update velocity and position with limits
            velocity[i] = np.clip(velocity[i-1] + acceleration * dt, -0.5, 0.5)
            gap[i] = np.clip(gap[i-1] + velocity[i] * dt, 0.01, 0.1)
            
            # Reduced disturbances for stability
            gap[i] += 0.2 * (track_irregularity[i] + passenger_movement[i])
        
        # Calculate magnetic field strength (more realistic)
        B = 2e-4 * current * np.exp(-20 * gap)  # Exponential field decay
        
        # Plot maglev system
        ax1 = self.figure.add_subplot(gs[0, :])
        
        # Draw track
        track_x = np.linspace(0, 10, 100)
        track_y = 3 + track_irregularity[current_idx] * np.sin(2*np.pi*track_x/2)
        ax1.plot(track_x, track_y, 'k-', linewidth=3)
        
        # Draw train
        train_width = 3
        train_height = 1
        gap_current = gap[current_idx]
        
        # Train body with aerodynamic shape
        train_x = np.array([3, 3, 3.5, 5.5, 6, 6])
        train_y = np.array([track_y[30] + gap_current + train_height,
                          track_y[30] + gap_current,
                          track_y[30] + gap_current - 0.2,
                          track_y[30] + gap_current - 0.2,
                          track_y[30] + gap_current,
                          track_y[30] + gap_current + train_height])
        
        # Draw train with gradient color based on speed
        train_color = plt.cm.viridis(current_idx/len(t))
        ax1.fill(train_x, train_y, color=train_color, alpha=0.8)
        
        # Draw electromagnets
        magnet_positions = [3.5, 4.0, 4.5, 5.0, 5.5]
        current_normalized = current[current_idx] / 1000
        
        for x_pos in magnet_positions:
            # Draw electromagnet
            magnet_color = plt.cm.plasma(current_normalized)
            ax1.fill([x_pos-0.1, x_pos+0.1, x_pos+0.1, x_pos-0.1],
                    [train_y[2], train_y[2], train_y[2]-0.2, train_y[2]-0.2],
                    color=magnet_color)
            
            # Draw magnetic field lines
            if current[current_idx] > 100:
                field_strength = current_normalized * 0.3
                for offset in [-0.05, 0, 0.05]:
                    ax1.plot([x_pos+offset, x_pos+offset],
                            [train_y[2]-0.2, track_y[int(x_pos*10)]],
                            'b-', alpha=0.2, linewidth=field_strength)
        
        # Add passengers (simplified)
        for i in range(3):
            x = 4 + i * 0.5
            y = train_y[0] - 0.3 + 0.1 * np.sin(5*current_t + i)
            ax1.plot([x, x], [y-0.2, y], 'k-', linewidth=2)
            ax1.plot([x-0.1, x+0.1], [y, y], 'k-', linewidth=2)
        
        ax1.set_xlim(0, 10)
        ax1.set_ylim(2, 5)
        ax1.axis('off')
        
        # Plot gap and current
        ax2 = self.figure.add_subplot(gs[1, 0])
        if current_idx > 1:
            ax2.plot(t[:current_idx], gap[:current_idx]*1000, 'b-', label='Gap (mm)')
            ax2.plot(t[:current_idx], current[:current_idx]/100, 'r-', label='Current (A/100)')
            ax2.axhline(y=target_gap*1000, color='g', linestyle='--', label='Target Gap')
            ax2.legend(loc='upper right')
        ax2.grid(True, linestyle='--', alpha=0.7)
        ax2.set_title('Levitation Control')
        
        # Plot forces and field strength
        ax3 = self.figure.add_subplot(gs[1, 1])
        if current_idx > 1:
            ax3.plot(t[:current_idx], force[:current_idx]/1000, 'r-', label='Force (kN)')
            ax3.plot(t[:current_idx], B[:current_idx], 'b-', label='B-field (T)')
            ax3.legend(loc='upper right')
        ax3.grid(True, linestyle='--', alpha=0.7)
        ax3.set_title('Electromagnetic Effects')
        
        self.figure.tight_layout()
        self.canvas.draw()
        
        # Update analysis text with complete information
        self.analysis_label.setText(f"""
            <h4>Maglev Control Analysis</h4>
            
            <p><b>Current State:</b></p>
            <ul>
                <li>Gap: {gap[current_idx]*1000:.1f} mm</li>
                <li>Current: {current[current_idx]:.0f} A</li>
                <li>Force: {force[current_idx]/1000:.1f} kN</li>
            </ul>
            
            <p><b>Derivatives:</b></p>
            <ul>
                <li>dGap/dt: {velocity[current_idx]*1000:.1f} mm/s</li>
                <li>dB/dt: {np.gradient(B, t)[current_idx]:.2f} T/s</li>
                <li>dI/dt: {np.gradient(current, t)[current_idx]:.0f} A/s</li>
            </ul>
            
        """)

    def update_vibration_analysis(self):
        """Update vibration system visualization"""
        self.figure.clear()
        gs = self.figure.add_gridspec(2, 2, height_ratios=[1.2, 1])
        
        # System parameters
        m1, m2, m3 = 1.0, 1.0, 1.0  # Masses (kg)
        k1, k2, k3, k4 = 150, 100, 100, 150  # Spring constants (N/m)
        c1, c2, c3 = 0.8, 0.8, 0.8  # Damping coefficients (Ns/m)
        
        # Time array
        t = np.linspace(0, 3, 300)
        current_t = self.animation_time % 3
        current_idx = min(int(current_t * 100), len(t)-1)
        
        # External forcing frequency
        forcing_freq = 2 * np.pi * (1 + np.sin(current_t))  # Varying frequency
        F0 = 10  # Force amplitude
        
        # Initialize arrays for each mass
        x1 = np.zeros_like(t)  # Position of mass 1
        x2 = np.zeros_like(t)  # Position of mass 2
        x3 = np.zeros_like(t)  # Position of mass 3
        v1 = np.zeros_like(t)  # Velocity of mass 1
        v2 = np.zeros_like(t)  # Velocity of mass 2
        v3 = np.zeros_like(t)  # Velocity of mass 3
        
        # Initial conditions with slight offset
        x1[0], x2[0], x3[0] = 0.1, 0.0, -0.1
        
        # Simulate system dynamics
        dt = t[1] - t[0]
        for i in range(1, len(t)):
            # External force
            F_ext = F0 * np.sin(forcing_freq * t[i])
            
            # Spring forces
            F_spring1 = -k1 * x1[i-1]
            F_spring2 = -k2 * (x1[i-1] - x2[i-1])
            F_spring3 = -k3 * (x2[i-1] - x3[i-1])
            F_spring4 = -k4 * x3[i-1]
            
            # Damping forces
            F_damp1 = -c1 * v1[i-1]
            F_damp2 = -c2 * (v1[i-1] - v2[i-1])
            F_damp3 = -c3 * (v2[i-1] - v3[i-1])
            
            # Accelerations
            a1 = (F_ext + F_spring1 + F_spring2 + F_damp1 + F_damp2) / m1
            a2 = (-F_spring2 + F_spring3 - F_damp2 + F_damp3) / m2
            a3 = (-F_spring3 + F_spring4 - F_damp3) / m3
            
            # Update velocities and positions
            v1[i] = v1[i-1] + a1 * dt
            v2[i] = v2[i-1] + a2 * dt
            v3[i] = v3[i-1] + a3 * dt
            x1[i] = x1[i-1] + v1[i] * dt
            x2[i] = x2[i-1] + v2[i] * dt
            x3[i] = x3[i-1] + v3[i] * dt
        
        # Calculate energy components
        KE = 0.5 * (m1*v1**2 + m2*v2**2 + m3*v3**2)  # Kinetic energy
        PE = 0.5 * (k1*x1**2 + k2*(x1-x2)**2 + k3*(x2-x3)**2 + k4*x3**2)  # Potential energy
        
        # Plot system visualization
        ax1 = self.figure.add_subplot(gs[0, :])
        
        # Base structure
        ax1.plot([0, 10], [3, 3], 'k-', linewidth=2)
        
        # Draw springs
        def draw_spring(x1, x2, y1, y2, turns=12):
            dx = x2 - x1
            dy = y2 - y1
            length = np.sqrt(dx**2 + dy**2)
            phi = np.arctan2(dy, dx)
            
            t = np.linspace(0, turns*2*np.pi, 100)
            x = np.linspace(x1, x2, 100)
            y = y1 + (y2-y1)*(x-x1)/(x2-x1) + 0.15*np.sin(t)*np.cos(phi)
            return x, y
        
        # Current positions
        y_base = 3
        x_pos1 = 3.0 + x1[current_idx]
        x_pos2 = 5.0 + x2[current_idx]
        x_pos3 = 7.0 + x3[current_idx]
        
        # Draw springs with different colors
        spring1_x, spring1_y = draw_spring(1.0, x_pos1, y_base, y_base)
        spring2_x, spring2_y = draw_spring(x_pos1, x_pos2, y_base, y_base)
        spring3_x, spring3_y = draw_spring(x_pos2, x_pos3, y_base, y_base)
        spring4_x, spring4_y = draw_spring(x_pos3, 9.0, y_base, y_base)
        
        ax1.plot(spring1_x, spring1_y, 'b-', linewidth=1.5, label=f'k₁={k1} N/m')
        ax1.plot(spring2_x, spring2_y, 'g-', linewidth=1.5, label=f'k₂={k2} N/m')
        ax1.plot(spring3_x, spring3_y, 'g-', linewidth=1.5, label=f'k₃={k3} N/m')
        ax1.plot(spring4_x, spring4_y, 'b-', linewidth=1.5, label=f'k₄={k4} N/m')
        
        # Draw masses with velocity-based color
        velocities = [v1[current_idx], v2[current_idx], v3[current_idx]]
        positions = [x_pos1, x_pos2, x_pos3]
        
        for i, (v, x) in enumerate(zip(velocities, positions), 1):
            color = plt.cm.RdYlBu(0.5 + v/2)
            ax1.add_patch(plt.Rectangle((x-0.4, y_base-0.4), 0.8, 0.8, 
                                      fc=color, ec='k', label=f'm{i}={1.0} kg'))
            
        # Add force arrow
        if abs(F_ext) > 0.1:
            ax1.arrow(0.5, y_base, 0.5*F_ext/F0, 0, 
                     head_width=0.1, head_length=0.2, fc='r', ec='r',
                     label=f'F={F_ext:.1f} N')
        
        ax1.legend(loc='upper right', bbox_to_anchor=(1.0, 0.95))
        ax1.set_xlim(0, 10)
        ax1.set_ylim(2, 4)
        ax1.axis('off')
        
        # Plot displacements
        ax2 = self.figure.add_subplot(gs[1, 0])
        if current_idx > 1:
            ax2.plot(t[:current_idx], x1[:current_idx], 'r-', label='Mass 1')
            ax2.plot(t[:current_idx], x2[:current_idx], 'g-', label='Mass 2')
            ax2.plot(t[:current_idx], x3[:current_idx], 'b-', label='Mass 3')
            ax2.legend(loc='upper right')
        ax2.grid(True, linestyle='--', alpha=0.7)
        ax2.set_title('Mass Displacements')
        ax2.set_xlabel('Time (s)')
        ax2.set_ylabel('Position (m)')
        
        # Plot energy
        ax3 = self.figure.add_subplot(gs[1, 1])
        if current_idx > 1:
            ax3.plot(t[:current_idx], KE[:current_idx], 'r-', label='Kinetic')
            ax3.plot(t[:current_idx], PE[:current_idx], 'b-', label='Potential')
            ax3.plot(t[:current_idx], KE[:current_idx]+PE[:current_idx], 'g-', 
                    label='Total')
            ax3.legend(loc='upper right')
        ax3.grid(True, linestyle='--', alpha=0.7)
        ax3.set_title('System Energy')
        ax3.set_xlabel('Time (s)')
        ax3.set_ylabel('Energy (J)')
        
        self.figure.tight_layout()
        self.canvas.draw()
        
        # Calculate approximate natural frequencies
        wn1 = np.sqrt((k1 + k2)/m1)
        wn2 = np.sqrt((k2 + k3)/m2)
        wn3 = np.sqrt((k3 + k4)/m3)
        
        # Update analysis text
        self.analysis_label.setText(f"""
            <h4>Three-Mass Vibration Analysis</h4>
            
            <p><b>System Energy:</b></p>
            <ul>
                <li>Kinetic: {KE[current_idx]:.3f} J</li>
                <li>Potential: {PE[current_idx]:.3f} J</li>
                <li>Total: {(KE[current_idx]+PE[current_idx]):.3f} J</li>
            </ul>
            
            <p><b>Dynamic Parameters:</b></p>
            <ul>
                <li>Forcing: {forcing_freq/(2*np.pi):.1f} Hz, {F_ext:.1f} N</li>
                <li>Natural Freq: {wn1/(2*np.pi):.1f}, {wn2/(2*np.pi):.1f}, {wn3/(2*np.pi):.1f} Hz</li>
                <li>Damping: ζ={c1/(2*np.sqrt(k1*m1)):.3f}</li>
            </ul>
        """)