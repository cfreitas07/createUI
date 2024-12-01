#author: Claudio de Freitas

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QMdiArea
from PyQt6.QtGui import QAction
from core.mdi_manager import MDIManager
from components.calculator import CalculatorWindow
from tests.text_editor import TextEditorWindow

class mainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initializeUI()

        # Load the stylesheet
        self.loadStylesheet()

        #MDI Area Management
        #link the manager to the main window using self.mdi_manager
        self.mdi_area = QMdiArea()
        self.setCentralWidget(self.mdi_area)

        #initialize MDI Manager
        self.mdi_manager = MDIManager(self.mdi_area)

        #menu bar
        menu_bar = self.menuBar()

        # File Menu
        file_menu = menu_bar.addMenu("File")
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Tools Menu
        tools_menu = menu_bar.addMenu("Tools")

        # Components Menu
        component_menu = menu_bar.addMenu("Components")
        calculator_action = QAction("Calculator", self)
        calculator_action.triggered.connect(self.openCalculatorWindow)
        component_menu.addAction(calculator_action)

        # Components -> Text Editor
        text_editor_action = QAction("Text Editor",self)
        text_editor_action.triggered.connect(self.openTextEditorWindow)
        component_menu.addAction(text_editor_action)

        # Models Menu
        models_menu = menu_bar.addMenu("Models")

    def openCalculatorWindow(self):
        """Open the Calculator as a subwindow."""
        calculator_widget = CalculatorWindow()
        self.mdi_manager.openSubWindow("Calculator", calculator_widget)

    def openTextEditorWindow(self):
        text_editor_widget = TextEditorWindow()
        self.mdi_manager.openSubWindow("Text Editor",text_editor_widget)


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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = mainWindow()
    window.show()
    sys.exit(app.exec())