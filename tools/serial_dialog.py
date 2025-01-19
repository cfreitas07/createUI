from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QComboBox, 
                            QPushButton, QLabel, QGridLayout,
                            QHBoxLayout, QFrame, QMdiSubWindow)
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt
import serial.tools.list_ports
import serial

class SerialPortDialog(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.selected_port = None
        self.serial_connection = None
        self.setup_ui()
        
        # Set a reasonable default size
        self.resize(400, 300)

    def setup_ui(self):
        # Main layout
        main_layout = QVBoxLayout(self)
        
        # Create grid layout for port selection and parameters
        grid_layout = QGridLayout()
        
        # Port selection
        grid_layout.addWidget(QLabel("Select Serial Port:"), 0, 0)
        self.port_combo = QComboBox()
        self.refresh_ports()
        grid_layout.addWidget(self.port_combo, 0, 1)
        
        # Baud rate selection
        grid_layout.addWidget(QLabel("Baud Rate:"), 1, 0)
        self.baud_combo = QComboBox()
        self.baud_combo.addItems(['9600', '19200', '38400', '57600', '115200'])
        self.baud_combo.setCurrentText('9600')
        grid_layout.addWidget(self.baud_combo, 1, 1)
        
        main_layout.addLayout(grid_layout)
        
        # Buttons layout
        button_layout = QHBoxLayout()
        
        # Refresh button
        refresh_btn = QPushButton("Refresh Ports")
        refresh_btn.clicked.connect(self.refresh_ports)
        button_layout.addWidget(refresh_btn)
        
        # Connect/Disconnect button
        self.connect_btn = QPushButton("Connect")
        self.connect_btn.clicked.connect(self.toggle_connection)
        button_layout.addWidget(self.connect_btn)
        
        main_layout.addLayout(button_layout)
        
        # Status frame
        status_frame = QFrame()
        status_frame.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Sunken)
        status_layout = QVBoxLayout()
        
        # Connection status
        self.status_label = QLabel("Status: Not Connected")
        self.status_label.setStyleSheet("color: red;")
        status_layout.addWidget(self.status_label)
        
        # Port info
        self.port_info = QLabel("Port: None")
        status_layout.addWidget(self.port_info)
        
        # Parameters info
        self.params_info = QLabel("Parameters: None")
        status_layout.addWidget(self.params_info)
        
        status_frame.setLayout(status_layout)
        main_layout.addWidget(status_frame)

    def refresh_ports(self):
        """Refresh the list of available serial ports"""
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
    
    def toggle_connection(self):
        """Handle connection/disconnection"""
        if self.serial_connection is None:  # Not connected
            try:
                port = self.port_combo.currentText().split(' - ')[0]
                baud_rate = int(self.baud_combo.currentText())
                
                # Try to establish connection
                self.serial_connection = serial.Serial(
                    port=port,
                    baudrate=baud_rate,
                    timeout=1
                )
                
                # Update UI for connected state
                self.status_label.setText("Status: Connected")
                self.status_label.setStyleSheet("color: green;")
                self.port_info.setText(f"Port: {port}")
                self.params_info.setText(
                    f"Parameters: {baud_rate} baud, "
                    f"Data bits: {self.serial_connection.bytesize}, "
                    f"Parity: {self.serial_connection.parity}, "
                    f"Stop bits: {self.serial_connection.stopbits}"
                )
                self.connect_btn.setText("Disconnect")
                
                # Disable port and baud selection while connected
                self.port_combo.setEnabled(False)
                self.baud_combo.setEnabled(False)
                
            except serial.SerialException as e:
                self.status_label.setText(f"Status: Error - {str(e)}")
                self.status_label.setStyleSheet("color: red;")
                self.serial_connection = None
                
        else:  # Connected, so disconnect
            if self.serial_connection:
                self.serial_connection.close()
            self.serial_connection = None
            
            # Update UI for disconnected state
            self.status_label.setText("Status: Not Connected")
            self.status_label.setStyleSheet("color: red;")
            self.port_info.setText("Port: None")
            self.params_info.setText("Parameters: None")
            self.connect_btn.setText("Connect")
            
            # Re-enable port and baud selection
            self.port_combo.setEnabled(True)
            self.baud_combo.setEnabled(True)