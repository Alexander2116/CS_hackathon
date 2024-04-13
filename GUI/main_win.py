"""
    This is a main file for the GUI.
"""



import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QDesktopWidget, QMessageBox, QListWidget
from PyQt5.QtCore import Qt
from Drag_Drop import DD_Window

class MyWindow(QWidget):
    names_parameters = {
    "name": "Space rocks!"
}
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.names_parameters['name'])
        self.setFixedSize(QDesktopWidget().availableGeometry().size())

        self.myListWidget1 = QListWidget()
        self.myListWidget1.setAcceptDrops(True)
        
        self.label = QLabel('Hello, PyQt!', self)
        self.button = QPushButton('Click me!', self)
        self.DDbutton = QPushButton('Items', self)

        
        layout = QVBoxLayout()
        layout.addWidget(self.myListWidget1)
        layout.addWidget(self.label)
        layout.addWidget(self.button)
        layout.addWidget(self.DDbutton)
        self.activateWindow()
        self.setLayout(layout)

        self.button.clicked.connect(self.on_button_clicked)
        self.button.clicked.connect(self.dialog)
        self.DDbutton.clicked.connect(self.DD_win)

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
    window = MyWindow()
    window.setWindowFlags(window.windowFlags() | Qt.WindowStaysOnTopHint)
    window.show()
    sys.exit(app.exec_())