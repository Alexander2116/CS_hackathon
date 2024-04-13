"""
    This is simple drag and drop window. It will be integrated into the main window.
"""

from PyQt5.QtWidgets import QApplication, QWidget, QListWidget, QHBoxLayout,QListWidgetItem
from PyQt5.QtGui import QIcon
import sys
import json

 
class DD_Window(QWidget):
    object_list = json.load(open("GUI\\object.json"))
    params = {
        "name": "Drag and Drop Example",
        "win_size": (300, 350, 500, 300),
    }
    def __init__(self):
        super().__init__()
 
        self.myListWidget1 = QListWidget()
        self.myListWidget2 = QListWidget()
        self.myListWidget2.setViewMode(QListWidget.IconMode)
        self.myListWidget1.setAcceptDrops(True)
        self.myListWidget1.setDragEnabled(True)
        self.myListWidget2.setAcceptDrops(True)
        self.myListWidget2.setDragEnabled(True)
        self.setGeometry(self.params["win_size"][0], self.params["win_size"][1], self.params["win_size"][2], self.params["win_size"][3])
        self.myLayout = QHBoxLayout()
        self.myLayout.addWidget(self.myListWidget1)
        self.myLayout.addWidget(self.myListWidget2)

        obj_comp = []
        keys = self.object_list.keys()
        for key in keys:
            obj_comp.append(QListWidgetItem(QIcon("Objects\\icons\\"+self.object_list[key]), key))
        
        for i in range(len(obj_comp)):
            self.myListWidget1.insertItem(i, obj_comp[i])
 
 
        self.setWindowTitle('Drag and Drop Example')
        self.setLayout(self.myLayout)
 
        self.show()
 
 
 
 
App = QApplication(sys.argv)
window = DD_Window()
sys.exit(App.exec())