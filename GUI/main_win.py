"""
    This is a main file for the GUI.
"""



import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QDesktopWidget, QMessageBox
from PyQt5.QtCore import Qt


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

        self.label = QLabel('Hello, PyQt!', self)
        self.button = QPushButton('Click me!', self)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.button)
        self.activateWindow()
        self.setLayout(layout)

        self.button.clicked.connect(self.on_button_clicked)
        self.button.clicked.connect(self.dialog)

    def on_button_clicked(self):
        self.label.setText('Button clicked!')
        
    def dialog(self):
        mbox = QMessageBox()

        mbox.setText("Your allegiance has been noted")
        mbox.setDetailedText("You are now a disciple and subject of the all-knowing Guru")
        mbox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        mbox.setWindowFlags(window.windowFlags() | Qt.WindowStaysOnTopHint)
                
        mbox.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.setWindowFlags(window.windowFlags() | Qt.WindowStaysOnTopHint)
    window.show()
    sys.exit(app.exec_())