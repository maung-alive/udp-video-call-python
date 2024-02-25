import socket
import cv2
import numpy
import threading

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 10000000)

RHOST = '127.0.0.1'
RPORT = 6001
width, height = 320, 240

capture = cv2.VideoCapture(0)
capture.set(3, width)
capture.set(4, height)

def receive():
    while True:
        (data, addr) = s.recvfrom(65507)
        data = cv2.imdecode(numpy.frombuffer(data, dtype=numpy.uint8), 1)

        cv2.imshow(f"SERVER: {RHOST}", data)

        if cv2.waitKey(10) == 13:  # ENTER key to quit
            break

def transmit(addr):
    while True:
        ret, photo = capture.read()
        encoded_frame = cv2.imencode('.jpg', photo)[1].tobytes()
        s.sendto(encoded_frame, addr)

if __name__ == '__main__':
    s.sendto(b'TESTING', (RHOST, RPORT))
    print("CONNECTED TO SERVER")
    addr = (RHOST, RPORT)
    transmit_thread = threading.Thread(target=transmit, args=(addr,))  # Threading
    receive_thread = threading.Thread(target=receive)  # Threading
    transmit_thread.start()
    receive_thread.start()
