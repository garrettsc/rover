from PyQt5 import QtGui, QtCore, QtWidgets
import cv2
import sys
import zmq



class DisplayImageWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(DisplayImageWidget, self).__init__(parent)

        self.rover_port = 5555
        self.topic = 'rover1'
        context = zmq.Context()
        self.socket = context.socket(zmq.PUB)
        self.socket.bind("tcp://*:%s" % self.rover_port)

        self.image_frame = QtWidgets.QLabel()

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.image_frame)
        self.setLayout(self.layout)

        url = 'http://rover.local:8000/stream.mjpg'

        self.cap = cv2.VideoCapture(url)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.show_image)
        self.timer.start(1)

    def keyPressEvent(self,event):
        print(event.key())
        key = event.key()

        FORWARD = 16777235
        REVERSE = 16777237 

        if key == FORWARD:
            m1 = 1
            m2 = 1
            print('fwd')
        
        elif key == REVERSE:
            m1 = -1
            m2 = -1
            print('rev')
    
        else:
            return
        

        packet = self.topic + ',' + m1 +',' + m2
        self.socket.send(packet)
        

    def show_image(self):

        ret, frame = self.cap.read()

        self.image = frame
        self.image = QtGui.QImage(self.image.data, self.image.shape[1], self.image.shape[0], QtGui.QImage.Format_RGB888).rgbSwapped()
        self.image_frame.setPixmap(QtGui.QPixmap.fromImage(self.image))

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    display_image_widget = DisplayImageWidget()
    display_image_widget.show()
    sys.exit(app.exec_())
