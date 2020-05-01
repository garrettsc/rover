from PyQt5 import QtGui, QtCore, QtWidgets
import cv2
import sys
import zmq

VIDEO_FEED_RE_CONNECT_TIMEO = 1000
V_FEED_UPDATE_TIMEO = 40

class RoverDisplayWidget(QtWidgets.QWidget):
    
    def __init__(self, *args, **kwargs):
        super(RoverDisplayWidget, self).__init__(*args, **kwargs)

        self.rover_port = 5555
        self.topic = 'rover1'
        context = zmq.Context()
        self.socket = context.socket(zmq.PUB)
        self.socket.bind("tcp://*:%s" % self.rover_port)

        self.image_frame = QtWidgets.QLabel()

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.image_frame)
        self.setLayout(self.layout)

        self.rover_name = 'rover.local'
        self.url = 'http://{}:8000/stream.mjpg'.format(self.rover_name)
        
        self.cap = cv2.VideoCapture()
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.show_image)
        self.msg_timer = QtCore.QTimer()
        self.msg_timer.timeout.connect(self.msg)

        self.video_connect_timer = QtCore.QTimer()
        self.video_connect_timer.timeout.connect(self.connect)
        
        self.video_connect_timer.start(VIDEO_FEED_RE_CONNECT_TIMEO)
        self.timer.start(V_FEED_UPDATE_TIMEO)

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
        
        elif key == REVERSE:
            self.m1 = -1
            self.m2 = -1

        elif key == RIGHT:
            self.m1 = -1
            self.m2 = 1

        elif key == LEFT:
            self.m1 = 1
            self.m2 = -1
        else:
            return

        self.msg_timer.start(10)


    def connect(self):
        self.image_frame.setText('Attempting to connect to {}...'.format(self.rover_name))
        self.cap.open(self.url)
        if self.cap.isOpened():
            self.video_connect_timer.stop()

    def keyReleaseEvent(self,event):
        
        if not event.isAutoRepeat():
            self.msg_timer.stop()

    def msg(self):

        packet = self.topic + ',' + str(self.m1) +',' + str(self.m2)
        self.socket.send_string(packet)



    def show_image(self):

        #Attempt to read a frame from the video stream
        success, frame = self.cap.read()

        #Show frame if there is one
        if success:
            self.image = QtGui.QImage(frame.data, frame.shape[1], frame.shape[0], QtGui.QImage.Format_RGB888).rgbSwapped()
            self.image_frame.setPixmap(QtGui.QPixmap.fromImage(self.image))

        #Otherwise clear label and try to re-connect
        else:
            if not self.video_connect_timer.isActive():
                self.image_frame.clear()
                self.video_connect_timer.start(VIDEO_FEED_RE_CONNECT_TIMEO)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    display_image_widget = RoverDisplayWidget()
    display_image_widget.show()
    sys.exit(app.exec_())

