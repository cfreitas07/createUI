#author: Claudio de Freitas

import sys
import serial.tools.list_ports
from PyQt6.QtWidgets import QApplication, QMainWindow, QMdiArea, QToolBar, QLabel, QPushButton, QComboBox, QHBoxLayout, QWidget, QFrame
from PyQt6.QtWidgets import QMenuBar
from PyQt6.QtGui import QAction, QIcon, QFont
from core.mdi_manager import MDIManager
from components.calculator import CalculatorWindow
from tests.text_editor import TextEditorWindow
from tools.serial_dialog import SerialPortDialog
from models.temperature_lab import TemperatureLab
from PyQt6.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initializeUI()

        # Load the stylesheet
        self.loadStylesheet()

        #MDI Area Management
        #link the manager to the main window using self.mdi_manager
        self.mdi = QMdiArea()
        self.mdi.setActivationOrder(QMdiArea.WindowOrder.CreationOrder)
        self.mdi.setViewMode(QMdiArea.ViewMode.SubWindowView)
        
        # Store window positions
        self.window_positions = {}

        self.setCentralWidget(self.mdi)

        #initialize MDI Manager
        self.mdi_manager = MDIManager(self.mdi)

        #menu bar
        menu_bar = self.menuBar()

        # File Menu
        file_menu = menu_bar.addMenu("File")
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Tools Menu
        tools_menu = menu_bar.addMenu("Tools")
        serial_action = QAction("Serial Connection", self)
        serial_action.triggered.connect(self.open_serial_dialog)
        tools_menu.addAction(serial_action)

        # Components Menu
        component_menu = menu_bar.addMenu("Components")
        calculator_action = QAction("Calculator", self)
        calculator_action.triggered.connect(self.open_calculator)
        component_menu.addAction(calculator_action)

        # Components -> Text Editor
        text_editor_action = QAction("Text Editor",self)
        text_editor_action.triggered.connect(self.openTextEditorWindow)
        component_menu.addAction(text_editor_action)

        # Models Menu
        models_menu = menu_bar.addMenu("Models")
        temp_lab_action = QAction("Temperature Lab", self)
        temp_lab_action.triggered.connect(self.open_temperature_lab)
        models_menu.addAction(temp_lab_action)

        # Create and add toolbar before MDI area setup
        self.create_quick_access_toolbar()

        # Set window icon
        icon_path = "resources/tesla.png"
        self.setWindowIcon(QIcon(icon_path))

    def open_calculator(self):
        calc = CalculatorWindow()
        self.add_mdi_window(calc, "Calculator")

    def open_temperature_lab(self):
        temp_lab = TemperatureLab()
        self.add_mdi_window(temp_lab, "Temperature Lab")

    def openTextEditorWindow(self):
        text_editor_widget = TextEditorWindow()
        self.mdi_manager.openSubWindow("Text Editor",text_editor_widget)

    def open_serial_dialog(self):
        """Open the serial port selection dialog in the MDI area"""
        serial_window = SerialPortDialog()
        subwindow = self.mdi_manager.openSubWindow("Serial Port Connection", serial_window)
        if hasattr(subwindow, 'setWindowTitle'):
            subwindow.setWindowTitle("Serial Port Connection")

    def initializeUI(self):
        self.setGeometry(400, 200, 1200, 800)
        self.setWindowTitle("CREATE Platform")

    def loadStylesheet(self):
        """Load the stylesheet for the application."""
        try:
            with open("resources/styles.qss", "r") as file:
                self.setStyleSheet(file.read())
        except FileNotFoundError:
            print("Stylesheet not found!")

    def create_quick_access_toolbar(self):
        """Create toolbar for quick serial connection access"""
        self.serial_toolbar = QToolBar("Device Connection")
        self.serial_toolbar.setMovable(False)
        self.serial_toolbar.setStyleSheet("""
            QToolBar {
                spacing: 10px;
                padding: 5px;
                background: #f0f0f0;
                border-bottom: 1px solid #dcdcdc;
            }
            QComboBox {
                min-height: 25px;
                min-width: 150px;
                padding: 3px;
                border: 1px solid #c0c0c0;
                border-radius: 3px;
                background: white;
                color: black;
            }
            QPushButton {
                min-height: 25px;
                padding: 3px 15px;
                border: 1px solid #c0c0c0;
                border-radius: 3px;
                background: #ffffff;
                color: black;
            }
            QPushButton:hover {
                background: #e6e6e6;
                color: black;
            }
            QPushButton:checked {
                background: #dff0d8;
                border-color: #5cb85c;
                color: black;
            }
            QLabel {
                font-family: 'Segoe UI', Arial;
                padding: 0px 5px;
                color: black;
            }
        """)
        
        # Create a widget to hold the toolbar contents
        toolbar_widget = QWidget()
        toolbar_layout = QHBoxLayout(toolbar_widget)
        toolbar_layout.setContentsMargins(5, 0, 5, 0)
        toolbar_layout.setSpacing(10)
        
        # Device selection combo box
        port_label = QLabel("Device Port:")
        port_label.setFont(QFont("Segoe UI", 9))
        toolbar_layout.addWidget(port_label)
        
        self.port_combo = QComboBox()
        self.port_combo.setFont(QFont("Segoe UI", 9))
        self.port_combo.setMinimumWidth(200)
        toolbar_layout.addWidget(self.port_combo)

        # Baud Rate selection
        baud_label = QLabel("Baud Rate:")
        baud_label.setFont(QFont("Segoe UI", 9))
        toolbar_layout.addWidget(baud_label)
        
        self.baud_combo = QComboBox()
        self.baud_combo.setFont(QFont("Segoe UI", 9))
        self.baud_combo.addItems(['9600', '19200', '38400', '57600', '115200'])
        self.baud_combo.setCurrentText('115200')
        toolbar_layout.addWidget(self.baud_combo)
        
        # Refresh ports button
        refresh_btn = QPushButton("Refresh")
        refresh_btn.setFont(QFont("Segoe UI", 9))
        refresh_btn.clicked.connect(self.refresh_ports)
        toolbar_layout.addWidget(refresh_btn)
        
        # Add a vertical separator
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.VLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        toolbar_layout.addWidget(separator)
        
        # Connect/Disconnect button
        self.connect_btn = QPushButton("Connect")
        self.connect_btn.setFont(QFont("Segoe UI", 9))
        self.connect_btn.setCheckable(True)
        self.connect_btn.clicked.connect(self.toggle_connection)
        toolbar_layout.addWidget(self.connect_btn)
        
        # Status label
        self.status_label = QLabel("Not Connected")
        self.status_label.setFont(QFont("Segoe UI", 9))
        self.status_label.setStyleSheet("color: #d9534f;")
        toolbar_layout.addWidget(self.status_label)

        # Connection parameters (hidden by default)
        self.params_label = QLabel("")
        self.params_label.setFont(QFont("Segoe UI", 9))
        self.params_label.hide()
        toolbar_layout.addWidget(self.params_label)
        
        # Add stretch to push everything to the left
        toolbar_layout.addStretch()
        
        # Add the widget to the toolbar
        self.serial_toolbar.addWidget(toolbar_widget)
        
        # Add toolbar to main window
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.serial_toolbar)
        
        # Initialize ports list
        self.refresh_ports()
        
    def refresh_ports(self):
        """Refresh the available serial ports"""
        current_port = self.port_combo.currentText()
        self.port_combo.clear()
        ports = serial.tools.list_ports.comports()
        for port in ports:
            self.port_combo.addItem(f"{port.device} - {port.description}")
        
        # Try to restore the previous selection
        if current_port:
            index = self.port_combo.findText(current_port)
            if index >= 0:
                self.port_combo.setCurrentIndex(index)
            
    def toggle_connection(self, checked):
        """Handle serial connection/disconnection"""
        if checked:
            try:
                port = self.port_combo.currentText().split(' - ')[0]
                baud_rate = int(self.baud_combo.currentText())
                self.serial_connection = serial.Serial(
                    port=port,
                    baudrate=baud_rate,
                    bytesize=serial.EIGHTBITS,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    timeout=1
                )
                
                # Simple check if port is open
                if self.serial_connection.is_open:
                    self.connect_btn.setText("Disconnect")
                    self.status_label.setText("Connected")
                    self.status_label.setStyleSheet("color: #5cb85c;")
                    
                    # Show connection parameters
                    params = (f"Port: {self.serial_connection.port} | "
                            f"Baud: {self.serial_connection.baudrate} | "
                            f"Data: {self.serial_connection.bytesize} | "
                            f"Parity: {self.serial_connection.parity} | "
                            f"Stop: {self.serial_connection.stopbits}")
                    self.params_label.setText(params)
                    self.params_label.show()
                    
                    # Disable port and baud selection while connected
                    self.port_combo.setEnabled(False)
                    self.baud_combo.setEnabled(False)
                else:
                    raise Exception("Failed to open port")
                    
            except Exception as e:
                print(f"Connection error: {str(e)}")
                self.connect_btn.setChecked(False)
                if hasattr(self, 'serial_connection') and self.serial_connection:
                    self.serial_connection.close()
                self.serial_connection = None
                self.status_label.setText("Connection Failed")
                self.status_label.setStyleSheet("color: #d9534f;")
                self.params_label.hide()
                
        else:
            if hasattr(self, 'serial_connection') and self.serial_connection:
                self.serial_connection.close()
            self.serial_connection = None
            self.connect_btn.setText("Connect")
            self.status_label.setText("Not Connected")
            self.status_label.setStyleSheet("color: #d9534f;")
            self.params_label.hide()
            
            # Re-enable port and baud selection
            self.port_combo.setEnabled(True)
            self.baud_combo.setEnabled(True)

    def add_mdi_window(self, window, title):
        sub_window = self.mdi.addSubWindow(window)
        sub_window.setWindowTitle(title)
        
        # Check if we have a saved position for this type of window
        window_type = type(window).__name__
        if window_type in self.window_positions:
            sub_window.move(self.window_positions[window_type])
        
        sub_window.show()
        
        # Connect to the window's move event to save its position
        sub_window.moveEvent = lambda e: self.save_window_position(sub_window, window_type)
        
        return sub_window

    def save_window_position(self, sub_window, window_type):
        """Save the position of a window type when it's moved"""
        self.window_positions[window_type] = sub_window.pos()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())