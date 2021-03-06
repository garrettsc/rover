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
        self.timer.start(10)
        self.msg_timer = QtCore.QTimer()
        self.msg_timer.timeout.connect(self.msg)

        self.active = False

    def keyPressEvent(self,event):

        if self.msg_timer.isActive():
            return

        key = event.key()

        FORWARD = 87
        REVERSE = 83
        RIGHT = 68
        LEFT = 65

        if key == FORWARD:
            self.m1 = 1
            self.m2 = 1
            #print('fwd')
        
        elif key == REVERSE:
            self.m1 = -1
            self.m2 = -1
            #print('rv')

        elif key == RIGHT:
            self.m1 = -1
            self.m2 = 1
            #print('right')

        elif key == LEFT:
            self.m1 = 1
            self.m2 = -1
            #print('left')
        else:
            return

        self.msg_timer.start(10)




    def keyReleaseEvent(self,event):
        
        if not event.isAutoRepeat():
            print('released')
            self.msg_timer.stop()

    def msg(self):

        packet = self.topic + ',' + str(self.m1) +',' + str(self.m2)
        print(packet)
        self.socket.send_string(packet)



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

