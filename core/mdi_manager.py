from PyQt6.QtWidgets import QMdiArea, QMdiSubWindow
from PyQt6.QtCore import Qt

class MDIManager:
    def __init__(self, mdi_area: QMdiArea):
        self.mdi_area = mdi_area

    def openSubWindow(self, title: str, widget):
        # Check if a subwindow with the same name already exists and is visible
        for window in self.mdi_area.subWindowList():
            if window.windowTitle() == title:
                if window.isVisible():
                    window.setFocus()
                    return
                else:
                    # Remove the closed window
                    self.mdi_area.removeSubWindow(window)
                    break  # Exit the loop to create a new window

        # Create a new subwindow
        sub_window = QMdiSubWindow()
        sub_window.setWindowTitle(title)
        sub_window.setWidget(widget)
        sub_window.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)  # Ensure the window is deleted on close
        self.mdi_area.addSubWindow(sub_window)
        sub_window.show()

        # **Cascade subwindows to prevent overlapping**
        self.mdi_area.cascadeSubWindows()
