"""
    This is a main file for the GUI.
"""



import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QDesktopWidget, QMessageBox, QListWidget, QMainWindow, QAction
from PyQt5.QtCore import Qt, QMimeData, QPoint
from Drag_Drop import DD_Window, rock
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
        # Create actions for the toolbar
        exitAct = QAction('Objects', self)
        exitAct.triggered.connect(self.DD_win)

        # Create the toolbar
        toolbar = self.addToolBar('Toolbar')
        toolbar.addAction(exitAct)
        screen_rect = QApplication.desktop().screenGeometry(QApplication.desktop().primaryScreen())
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
        self.central_layout.addWidget(self.drop_area)
        # Enable drop events
        self.setAcceptDrops(True)

        # Create a central widget
        """
        self.central_widget = VideoBackground("C:\\Program Files (x86)\\GitHub\\CS_hackathon\\media\\videos\\1080p60\\Earth.mp4")
        self.setCentralWidget(self.central_widget)
        self.setAcceptDrops(True)
        self.central_widget.setAcceptDrops(True)
        self.central_widget.setAlignment(Qt.AlignCenter)"""

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
        
    def dragEnterEvent(self, event):
        if event.mimeData().hasImage or event.mimeData().hasText():
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasImage or event.mimeData().hasText():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, e):
        # get the relative position from the mime data
        mime = e.mimeData().object()
        x, y = map(int, mime.split(','))

        if e.keyboardModifiers() & Qt.ShiftModifier:
            # copy
            # so create a new button
            button = rock(self)
            # move it to the position adjusted with the cursor position at drag
            button.move(e.pos()-QPoint(x, y))
            # show it
            button.show()
            # store it
            self.buttons.append(button)
            # set the drop action as Copy
            e.setDropAction(Qt.CopyAction)
        else:
            # move
            # so move the dragged button (i.e. event.source())
            e.source().move(e.pos()-QPoint(x, y))
            # set the drop action as Move
            e.setDropAction(Qt.MoveAction)
        # tell the QDrag we accepted it
        e.accept()
        
    def mouseMoveEvent(self, event):
        if not (event.buttons() & Qt.LeftButton):
            return

        if (event.pos() - self.drag_start_position).manhattanLength() < QApplication.startDragDistance():
            return

        drag = QApplication.instance().primaryScreen().grabWindow(self.winId())
        mime_data = Qt.QMimeData()
        mime_data.setImageData(drag)

        drag = Qt.QDrag(self)
        drag.setMimeData(mime_data)
        drag.exec_(Qt.MoveAction)
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setWindowFlags(window.windowFlags() | Qt.WindowStaysOnTopHint)
    window.show()
    sys.exit(app.exec_())