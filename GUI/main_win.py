"""
    This is a main file for the GUI.
"""



import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QDesktopWidget, QMessageBox, QListWidget, QMainWindow, QAction
from PyQt5.QtCore import Qt
from Drag_Drop import DD_Window
from animated_back import VideoBackground

class MainWindow(QMainWindow):
    
    params = {
        "name":"space rocks!"
    }
    
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # Create actions for the toolbar
        exitAct = QAction('Objects', self)
        exitAct.triggered.connect(self.DD_win)

        # Create the toolbar
        toolbar = self.addToolBar('Toolbar')
        toolbar.addAction(exitAct)

        screen_rect = QApplication.desktop().screenGeometry(QApplication.desktop().primaryScreen())
        # Create a central widget
        self.central_widget = VideoBackground("C:\\Program Files (x86)\\GitHub\\CS_hackathon\\media\\videos\\1080p60\\Earth.mp4")
        self.setCentralWidget(self.central_widget)
        self.setAcceptDrops(True)
        self.central_widget.setAcceptDrops(True)
        self.central_widget.setAlignment(Qt.AlignCenter)

        # Set window title and size
        self.setWindowTitle(self.params["name"])
        self.setGeometry(0, 0, screen_rect.width(), screen_rect.height())

    def on_button_clicked(self):
        self.label.setText('Button clicked!')
        
    def dialog(self):
        mbox = QMessageBox()

        mbox.setText("Your allegiance has been noted")
        mbox.setDetailedText("You are now a disciple and subject of the all-knowing Guru")
        mbox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        mbox.setWindowFlags(window.windowFlags() | Qt.WindowStaysOnTopHint)
                
        mbox.exec_()
        
    def DD_win(self):
        self.DD_window = DD_Window()
        
    
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setWindowFlags(window.windowFlags() | Qt.WindowStaysOnTopHint)
    window.show()
    sys.exit(app.exec_())