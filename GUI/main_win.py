"""
    This is a main file for the GUI.
"""



import sys
from PyQt5.QtWidgets import * #QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QDesktopWidget, QFormLayout, QLineEdit, QMessageBox, QListWidget, QMainWindow, QAction
from PyQt5.QtCore import Qt, QMimeData, QPoint
from Drag_Drop import DD_Window
from animated_back import VideoBackground
from PyQt5.QtGui import QIcon, QDrag

class MainWindow(QMainWindow):
    
    params = {
        "name":"space rocks!"
    }
    
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        
        screen_rect = QApplication.desktop().screenGeometry(QApplication.desktop().primaryScreen())
        # Set window title and size
        self.setWindowTitle(self.params["name"])
        self.setGeometry(0, 0, screen_rect.width(), screen_rect.height())
        # Create actions for the toolbar
        exitAct = QAction('Objects', self)
        exitAct.triggered.connect(self.DD_win)

        # Create the toolbar
        toolbar = self.addToolBar('Toolbar')
        toolbar.addAction(exitAct)
        
    
        
        # Create a QGraphicsView and set its scene
        self.graphics_view = QGraphicsView()
        self.setCentralWidget(self.graphics_view)
        self.scene = QGraphicsScene()
        self.graphics_view.setScene(self.scene)

        # Add a rectangle item to the scene
        self.rect_item = QGraphicsRectItem(0, 0, 100, 100)
        self.rect_item.setBrush(Qt.blue)
        self.scene.addItem(self.rect_item)

        # Enable item movement
        self.rect_item.setFlag(QGraphicsRectItem.ItemIsMovable)
        """
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.central_layout = QVBoxLayout()
        self.central_widget.setLayout(self.central_layout)
                # Create drop area label
                
        self.drop_area = QLabel("Drop items here", self)
        self.drop_area.setGeometry(100, 100, 400, 400)
        self.drop_area.setAlignment(Qt.AlignCenter)
        self.drop_area.setStyleSheet("border: 2px dashed #aaa;")
        self.drop_area.setAcceptDrops(True)
        self.central_layout.addWidget(self.drop_area)"""
        # Create a central widget
        """
        self.central_layout = QVBoxLayout()
        
        self.central_widget = VideoBackground("C:\\Program Files (x86)\\GitHub\\CS_hackathon\\media\\videos\\1080p60\\Earth.mp4")
        self.central_widget.setAcceptDrops(True)
        self.central_widget.setAlignment(Qt.AlignCenter)
        self.setCentralWidget(self.central_widget)"""

        
    def DD_win(self):
        self.DD_window = DD_Window()
        
    def dragEnterEvent(self, event):
        print("dragEnterEvent")
        if event.mimeData().hasImage or event.mimeData().hasText():
            self.scene.addItem(event.mimeData().image)
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        print("dragMoveEvent")
        if event.mimeData().hasImage or event.mimeData().hasText():
            event.accept()
        else:
            event.ignore()
        
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setWindowFlags(window.windowFlags() | Qt.WindowStaysOnTopHint)
    window.show()
    sys.exit(app.exec_())