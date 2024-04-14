import sys
from PyQt5.QtWidgets import * #QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QDesktopWidget, QFormLayout, QLineEdit, QMessageBox, QListWidget, QMainWindow, QAction
from PyQt5.QtCore import Qt, QMimeData, QPoint, pyqtSignal
from PyQt5.QtGui import QIcon, QDrag
from GUI.main_win import MainWindow


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setWindowFlags(window.windowFlags() | Qt.WindowStaysOnTopHint)
    window.show()
    sys.exit(app.exec_())