"""
    This is a main file for the GUI.
"""



import sys
from PyQt5.QtWidgets import * #QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QDesktopWidget, QFormLayout, QLineEdit, QMessageBox, QListWidget, QMainWindow, QAction
from PyQt5.QtCore import Qt, QMimeData, QPoint, pyqtSignal
from Drag_Drop import DD_Window
from animated_back import VideoBackground
from PyQt5.QtGui import QIcon, QDrag


class enter_parametrs(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle("Enter parametrs")
        self.setGeometry(100, 100, 400, 200)
        layout = QFormLayout(self)
        
        self.p = QLineEdit(self)
        self.vel = QLineEdit(self)
        self.m = QLineEdit(self)
        self.s = QLineEdit(self)
        
        layout.addRow("Position (x,y)", self.p)
        layout.addRow("Velocity (x,y)", self.vel)
        layout.addRow("Mass", self.m)
        layout.addRow("Size (H,W)", self.s)
        
        self.ok_button = QPushButton("OK", self)
        self.ok_button.clicked.connect(self.ok_button_pressed)
        layout.addRow(self.ok_button)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        
    def ok_button_pressed(self):
        if(self.p.text() == "" or self.vel.text() == "" or self.m.text() == "" or self.s.text() == ""):
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Please fill all the fields")
            msg.setWindowTitle("Error")
            msg.setWindowFlags(Qt.WindowStaysOnTopHint)
            msg.exec_()
            
        elif(len(self.p.text().split(",")) != 3 or len(self.vel.text().split(",")) != 3 or len(self.s.text().split(",")) != 2):
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Incorrect values, follow the pattern")
            msg.setWindowTitle("Error")
            msg.setWindowFlags(Qt.WindowStaysOnTopHint)
            msg.exec_()
            
        elif(not ((self.p.text().split(",")[0].isnumeric() and self.p.text().split(",")[1].isnumeric() and self.p.text().split(",")[2].isnumeric()) and (self.vel.text().split(",")[0].isnumeric() and self.vel.text().split(",")[1].isnumeric() and self.vel.text().split(",")[2].isnumeric()) and self.m.text().isnumeric() and \
             (self.s.text().split(",")[0].isnumeric() and self.s.text().split(",")[1].isnumeric()))):
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Incorrect values, enter numeric values only")
            msg.setWindowTitle("Error")
            msg.setWindowFlags(Qt.WindowStaysOnTopHint)
            msg.exec_()
            
        else:
            self.accept()
        
    def get_params(self):
        return {
            "pos":(float(self.p.text().split(",")[0]), float(self.p.text().split(",")[1]), float(self.p.text().split(",")[2])),
            "vel":(float(self.vel.text().split(",")[0]), float(self.vel.text().split(",")[1]), float(self.vel.text().split(",")[2])),
            "mass":float(self.m.text()),
            "size":(float(self.s.text().split(",")[0]), float(self.s.text().split(",")[1] ))
        }

class PopUp(QDialog):
    textEntered = pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle("Pop Up")
        self.setGeometry(100, 100, 400, 200)
        layout = QVBoxLayout(self)
        label = QLabel("This is a pop up window")
        layout.addWidget(label)
        button1 = QPushButton("Rock",self)
        button2 = QPushButton("Satellite",self)
        button1.clicked.connect(self.button1_pressed)
        button2.clicked.connect(self.button2_pressed)
        
        layout.addWidget(button1)
        layout.addWidget(button2)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        
        self.show()

    def button1_pressed(self):
        
        self.textEntered.emit("rock")
        self.accept()
    
    def button2_pressed(self):
        self.textEntered.emit("satellite")
        self.accept()
    
    
class DragLabel(QLabel):
    def __init__(self, title, parent):
        super().__init__(title, parent)
        self.setAcceptDrops(True)
        self.setFrameShape(QFrame.Box)
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("border: 2px dashed #aaa;")
        self.setFixedSize(200, 200)

    def dragEnterEvent(self, event):
        if event.mimeData().hasImage or event.mimeData().hasText():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasImage:
            self.setPixmap(event.mimeData().image)
        elif event.mimeData().hasText():
            self.setText(event.mimeData().text())
        event.accept()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_start_position = event.pos()

    def mouseMoveEvent(self, event):
        if not (event.buttons() & Qt.LeftButton):
            return

        if (event.pos() - self.drag_start_position).manhattanLength() < QApplication.startDragDistance():
            return
class MainWindow(QMainWindow):
    object_params = []
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
        exitAct = QAction('Add new', self)
        exitAct.triggered.connect(self.add_menu)

        # Create the toolbar
        toolbar = self.addToolBar('Toolbar')
        toolbar.addAction(exitAct)
        
    
        
        # Create a QGraphicsView and set its scene
        self.graphics_view = QGraphicsView()
        self.setCentralWidget(self.graphics_view)
        self.scene = QGraphicsScene()
        self.graphics_view.setScene(self.scene)

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

        
    def add_menu(self):
        dialog = PopUp()
        dialog.textEntered.connect(self.on_text_entered)
        dialog.exec_()
        
        if(self.add_new_object == "rock" or self.add_new_object == "satellite"):
            param_win = enter_parametrs()
            if param_win.exec_() == QDialog.Accepted:
                param = param_win.get_params()
            print(param)
            param_win.exec_()
            size = param["size"]
            pos = param["pos"]
            temp = QGraphicsRectItem(pos[0], pos[1], size[0], size[1])
            temp.setFlag(QGraphicsRectItem.ItemIsMovable)
            
            if(self.add_new_object == "rock"):
                temp.setBrush(Qt.red)
            elif(self.add_new_object == "satellite"):
                temp.setBrush(Qt.blue)
                
            self.scene.addItem(temp)
        
    def run_animation(self):
        for item in self.scene.items():
            if isinstance(item, QGraphicsRectItem):
                print(f"Found QGraphicsRectItem at position ({item.pos().x()}, {item.pos().y()})")
    
    def on_text_entered(self, text):
        self.add_new_object = text
        
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
        
    def get_object_from_scene(self):
        # Iterate over all items in the scene
        for item in self.scene.items():
            # Check if the item is a QGraphicsRectItem
            if isinstance(item, QGraphicsRectItem):
                # Here you can access the QGraphicsRectItem and perform actions
                print(f"Found QGraphicsRectItem at position ({item.pos().x()}, {item.pos().y()})")
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setWindowFlags(window.windowFlags() | Qt.WindowStaysOnTopHint)
    window.show()
    sys.exit(app.exec_())