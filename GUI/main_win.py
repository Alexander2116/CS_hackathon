"""
    This is a main file for the GUI.
"""



import sys
from PyQt5.QtWidgets import * #QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QDesktopWidget, QFormLayout, QLineEdit, QMessageBox, QListWidget, QMainWindow, QAction
from PyQt5.QtCore import Qt, QMimeData, QPoint, pyqtSignal, QTimer
from PyQt5.QtGui import QIcon, QDrag, QImage, QPixmap
import cv2
import json
import subprocess

class VideoBackground(QLabel):
    def __init__(self, video_path):
        super().__init__()
        self.video_capture = cv2.VideoCapture(video_path)
        self.setAcceptDrops(True)
        # Set up timer to update the frame
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(int(1000 // self.video_capture.get(cv2.CAP_PROP_FPS)))

    def update_frame(self):
        ret, frame = self.video_capture.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = frame.shape
            bytes_per_line = ch * w
            q_image = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
            self.setPixmap(QPixmap.fromImage(q_image))
        else:
            self.video_capture.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Reset video to the beginning


class enter_parametrs(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle("Enter parametrs")
        self.setGeometry(100, 100, 200, 150)
        layout = QFormLayout(self)
        
        self.p = QLineEdit(self)
        self.vel = QLineEdit(self)
        
        layout.addRow("Position (x,y,z)", self.p)
        layout.addRow("Velocity (x,y,z)", self.vel)
        
        self.ok_button = QPushButton("OK", self)
        self.ok_button.clicked.connect(self.ok_button_pressed)
        layout.addRow(self.ok_button)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        
    def ok_button_pressed(self):
        if(self.p.text() == "" or self.vel.text() == ""):
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Please fill all the fields")
            msg.setWindowTitle("Error")
            msg.setWindowFlags(Qt.WindowStaysOnTopHint)
            msg.exec_()
            
        elif(len(self.p.text().split(",")) != 3 or len(self.vel.text().split(",")) != 3):
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Incorrect values, follow the pattern")
            msg.setWindowTitle("Error")
            msg.setWindowFlags(Qt.WindowStaysOnTopHint)
            msg.exec_()
            
        elif(not ((self.p.text().split(",")[0].isnumeric() and self.p.text().split(",")[1].isnumeric() and self.p.text().split(",")[2].isnumeric()) and (self.vel.text().split(",")[0].isnumeric() and self.vel.text().split(",")[1].isnumeric() and self.vel.text().split(",")[2].isnumeric()))):
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
            "vel":(float(self.vel.text().split(",")[0]), float(self.vel.text().split(",")[1]), float(self.vel.text().split(",")[2]))
        }

class PopUp(QDialog):
    textEntered = pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle("Pop Up")
        self.setGeometry(100, 100, 100, 100)
        layout = QVBoxLayout(self)
        label = QLabel("Select your object")
        layout.addWidget(label)
        button1 = QPushButton("Rock",self)
        button2 = QPushButton("Satellite",self)
        button2.setDisabled(True)
        button1.clicked.connect(self.button1_pressed)
        button2.clicked.connect(self.button2_pressed)
        
        layout.addWidget(button1)
        layout.addWidget(button2)
        self.setWindowFlags(Qt.WindowStaysOnTopHint )
        
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

        runAct = QAction('Run', self)
        runAct.triggered.connect(self.run_animation)
        # Create the toolbar
        toolbar = self.addToolBar('Toolbar')
        toolbar.addAction(exitAct)
        toolbar.addAction(runAct)
        
        
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
                
            self.object_params.append(param)
            pos = param["pos"]
            temp = QGraphicsRectItem(pos[0], pos[1], 20, 20)
            temp.setFlag(QGraphicsRectItem.ItemIsMovable)
            
            if(self.add_new_object == "rock"):
                temp.setBrush(Qt.red)
            elif(self.add_new_object == "satellite"):
                temp.setBrush(Qt.blue)
                
            self.scene.addItem(temp)
        
    def run_animation(self):
        # update pos for all objects
        positions = []
        velocities = []
        for i in range(len(self.scene.items())):
            if isinstance(self.scene.items()[i], QGraphicsRectItem):
                object_params = self.object_params[i]
                temp_pos = (self.scene.items()[i].pos().x(),self.scene.items()[i].pos().y(),object_params["pos"][2])
                self.object_params[i].update({"pos":temp_pos})
                positions.append(self.object_params[i]["pos"])
                velocities.append(self.object_params[i]["vel"])
                
        # Replace 'script_to_run.py' with the path to the Python script you want to run
        script_path = 'models/multiple_objects.py'

        # List of lists to pass as arguments

        # Serialize the list of lists into a JSON string
        args1 = json.dumps(positions)
        args2 = json.dumps(velocities)

        # Run the script with the serialized JSON string as an argument
        subprocess.call(['python', script_path, args1, args2])
        
        self.central_widget = VideoBackground("media/videos/1080p60/Example.mp4")
        self.central_widget.setAcceptDrops(True)
        self.central_widget.setAlignment(Qt.AlignCenter)
        self.setCentralWidget(self.central_widget)
        

    
    def on_text_entered(self, text):
        self.add_new_object = text
        
        
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