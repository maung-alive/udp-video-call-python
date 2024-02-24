import socket
import cv2
import pickle
import numpy

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 65535)

RHOST = '127.0.0.1'
RPORT = 6001

capture = cv2.VideoCapture(0)

def receive():
    while True:
        addr, data = s.recvfrom(65535)
        data = pickle.loads(data)
        data = cv2.imdecode(data, cv2.IMREAD_COLOR)
        cv2.imshow(f"SERVER: {RHOST}", data)

        if cv2.waitKey(10) == 13:  # ENTER key to quit
            break

if __name__ == '__main__':
    s.sendto(b'CONNECTED', (RHOST, RPORT))
    receive()