"""
    This is simple drag and drop window. It will be integrated into the main window.
"""

from PyQt5.QtWidgets import QApplication, QWidget, QListWidget, QHBoxLayout,QListWidgetItem, QLabel
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
import sys
import json


class DraggableLabel(QListWidgetItem):
    def __init__(self, text):
        super().__init__()
        

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.offset = event.pos()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            self.move(self.pos() + event.pos() - self.offset)
 
class DD_Window(QWidget):
    
    object_list = json.load(open("GUI\\object.json"))
    params = {
        "name": "Objects",
        "win_size": (300, 350, 200, 100),
    }
    
    def __init__(self):
        super().__init__()
 
        self.myListWidget1 = QListWidget()
        #self.myListWidget1.setAcceptDrops(True)
        self.myListWidget1.setDragEnabled(True)
        self.myListWidget1.setDragDropMode(QListWidget.DragOnly)
        #self.myListWidget1.setDragDropMode(QListWidget.InternalMove)
        
        self.setGeometry(self.params["win_size"][0], self.params["win_size"][1], self.params["win_size"][2], self.params["win_size"][3])
        self.myLayout = QHBoxLayout()
        self.activateWindow()
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMaximizeButtonHint & ~Qt.WindowMinimizeButtonHint | Qt.WindowStaysOnTopHint)

        obj_comp = []
        keys = self.object_list.keys()
        for key in keys:
            obj_comp.append(QListWidgetItem(QIcon("Objects\\icons\\"+self.object_list[key]), key))
        
        for i in range(len(obj_comp)):
            self.myListWidget1.insertItem(i, obj_comp[i])
 
        self.myLayout.addWidget(self.myListWidget1)
        self.setWindowTitle(self.params["name"])
        self.setLayout(self.myLayout)
 
        self.show()
 
 
 
"""
App = QApplication(sys.argv)
window = DD_Window()
sys.exit(App.exec())"""