import cv2
import numpy as np
import socket
import sys
import pickle
import struct ### new code

HOST=''
PORT=8554

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

s.bind((HOST,PORT))
s.listen(10)

conn,addr=s.accept()


cap=cv2.VideoCapture(0)
while True:
    ret,frame=cap.read()
    data = pickle.dumps(frame) ### new code
    clientsocket.sendall(struct.pack("L", len(data))+data) ### new code
