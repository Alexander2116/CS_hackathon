import sys
import cv2
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt, QTimer

class VideoBackground(QLabel):
    def __init__(self, video_path):
        super().__init__()
        self.video_capture = cv2.VideoCapture(video_path)

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

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Looping Video Background")
        self.setGeometry(100, 100, 800, 600)

        # Set central widget
        self.central_widget = VideoBackground("C:\\Program Files (x86)\\GitHub\\CS_hackathon\\media\\videos\\1080p60\\Earth.mp4")
        self.setCentralWidget(self.central_widget)
        self.central_widget.setAlignment(Qt.AlignCenter)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())