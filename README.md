# video-monitoring-server

## What is it ?

This repository contains a Python Flask application designed to be ran on a Raspberry Pi with a Pi Camera.

Client side, I created a small mobile cross-platform application with React-Native framework. It is available [here](https://github.com/BMatthai/video-monitoring-client-mobile).

I am still working on this project, my plan is to integrate some shape recognition and motion detection with OpenCV library and also a Push Notification service. 

## Usage

Ensure you've properly installed all dependencies.

Then run the following command (replace path/port/host if needed):

*FLASK_APP=/home/pi/video-monitoring-server/pystream.py flask run --port 8554 --host=0.0.0.0*




