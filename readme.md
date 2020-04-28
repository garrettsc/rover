# Rover

RC tag rover library



# Setup instructions

Currently running in a 'prototyping' phase. On the rover pi (pi zero) I currently have the user setting up a virtual environment to install all of the libraries. I have seen some issues with this on the pi 3 when trying to install PyQt, OpenCv, etc.

To run the camera, ssh into the rover pi and execute the /tests/camera/rover_camera_server.py script. This was pulled from the picameras document pages and seems to work really well. Essentially this captures the camera to a buffer which is then pushed out via an http server. Cool thing about this is that you could potentially view the stream from multiple devices at once....maybe even incorporate some buttons for a web ui.

To capture the camera on the pi 3 (connected to a TV o VNC) run the /tests/camera/client_video_capture.py. This uses some opencv utilities to capture the stream in real time and throw it to the screen. Future versions of this I will put into a qt application and capture keystrokes for motor commands.
