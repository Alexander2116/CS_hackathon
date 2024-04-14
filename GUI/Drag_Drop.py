"""
    This is simple drag and drop window. It will be integrated into the main window.
"""

from PyQt5.QtWidgets import * #QApplication, QWidget, QListWidget, QHBoxLayout,QListWidgetItem, QLabel, QMessageBox, QInputDialog
from PyQt5.QtGui import QIcon, QDrag
from PyQt5.QtCore import Qt, QMimeData, QPointF
import sys
from Objects.base_objects import rock_base, sattelite_base

class Def_Widget(QListWidgetItem):
    def __init__(self, image, name):
        super().__init__(QIcon("GUI\\Objects\\icons\\"+image), name)
        
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.offset = event.pos()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            self.move(self.pos() + event.pos() - self.offset)
    
    def dialog(self):
        mbox = QMessageBox()
        mbox.setWindowModality(2)
        name, done1 = QInputDialog.getText(
             self, 'Input Dialog', 'Enter your name:') 
                
        mbox.exec_()
        
    def dragEnterEvent(self, event):
        print("dragEnterEvent:")

        if event.mimeData().hasUrls():
            event.accept()   # must accept the dragEnterEvent or else the dropEvent can't occur !!!
        else:
            event.ignore()
            
    def dropEvent(self, event):

        self.dialog()
        #self.drop_area_label.setText(text)
        

    # mouse click event
    def mousePressEvent(self, event):
        pass

    def mouseMoveEvent(self, event):
        orig_cursor_position = event.lastScenePos()
        updated_cursor_position = event.scenePos()

        orig_position = self.scenePos()

        updated_cursor_x = updated_cursor_position.x() - orig_cursor_position.x() + orig_position.x()
        updated_cursor_y = updated_cursor_position.y() - orig_cursor_position.y() + orig_position.y()
        self.setPos(QPointF(updated_cursor_x, updated_cursor_y))

    def mouseReleaseEvent(self, event):
        print('x: {0}, y: {1}'.format(self.pos().x(), self.pos().y()))

class rock(Def_Widget):
    def __init__(self):
        self.rock = rock_base()
        super().__init__(self.rock.image, "rock")  
        
class satellite(Def_Widget):
    def __init__(self):
        self.satellite = sattelite_base()
        super().__init__(self.satellite.image, "satellite")
        
 
class DD_Window(QWidget):
    
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

        #### Append objects to the list
        obj_comp = []
        obj_comp.append(rock())
        obj_comp.append(satellite())
        
        ####
        
        for i in range(len(obj_comp)):
            self.myListWidget1.insertItem(i, obj_comp[i])
 
        self.myLayout.addWidget(self.myListWidget1)
        self.setWindowTitle(self.params["name"])
        self.setLayout(self.myLayout)
 
        self.show()
 
    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dropEvent(self, event):
        text = event.mimeData().text()
        self.drop_area_label.setText(text)
 
 
"""
App = QApplication(sys.argv)
window = DD_Window()
sys.exit(App.exec())"""