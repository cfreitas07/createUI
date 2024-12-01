#MDI Manager to simplify the creation of subwindows
from PyQt6.QtWidgets import QMdiArea, QMdiSubWindow
from PyQt6.QtCore import Qt

class MDIManager:
    def __init__(self, mdi_area: QMdiArea):
        self.mdi_area = mdi_area

    def openSubWindow(self, title:str, widget):
        #check if a subwindow with the same name already exists
        for window in self.mdi_area.subWindowList():
            if window.windowTitle() == title:
                window.setFocus()
                return
            else:
                self.mdi_area.removeSubWindow(window)
                break
            
        #create a new subwindow
        sub_window = QMdiSubWindow()
        sub_window.setWindowTitle(title)
        sub_window.setWidget(widget)
        sub_window.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        self.mdi_area.addSubWindow(sub_window)
        sub_window.show()