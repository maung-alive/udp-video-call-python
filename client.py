import socket
import cv2
import numpy

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 10000000)

RHOST = '127.0.0.1'
RPORT = 6001

capture = cv2.VideoCapture(0)

def receive():
    while True:
        (data, addr) = s.recvfrom(65507)
        data = cv2.imdecode(numpy.frombuffer(data, dtype=numpy.uint8), 1)

        cv2.imshow(f"SERVER: {RHOST}", data)

        if cv2.waitKey(10) == 13:  # ENTER key to quit
            break

if __name__ == '__main__':
    s.sendto(b'TESTING', (RHOST, RPORT))
    print("CONNECTED TO SERVER")
    receive()