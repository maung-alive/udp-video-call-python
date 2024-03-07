import base64
import socket
import cv2
import numpy
import threading
from datetime import datetime

RHOST = '127.0.0.1'
RPORT = 4444
ADDRESS = (RHOST, RPORT)

BUF_SIZE = 65535

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUF_SIZE)
sock.sendto(b"Hello", ADDRESS)

WIDTH = 400

capture = cv2.VideoCapture(0)    # Change your camera
def transmit(addr):
    print(f"Transmitting to {addr[0]}:{addr[1]}")
    while True:
        _, captured = capture.read()
        frame = cv2.resize(captured, (WIDTH, WIDTH))
        frame = cv2.flip(frame, 1)
        frame = cv2.putText(frame, str(datetime.now()), (15, 15), cv2.FONT_HERSHEY_PLAIN, 1, (0,0,255), 2)
        encoded, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
        encoded_frame = base64.b64encode(buffer)
        sock.sendto(encoded_frame, addr)

def receive():
    while True:
        data, addr = sock.recvfrom(BUF_SIZE)
        data = base64.b64decode(data)
        npdata = numpy.frombuffer(data, dtype=numpy.uint8)
        frame = cv2.imdecode(npdata, cv2.IMREAD_COLOR)
        cv2.imshow("Client", frame)

        key = cv2.waitKey(1) & 0xFF

        if key == ord('q'):
            break

t1 = threading.Thread(target=transmit, args=(ADDRESS,))
t2 = threading.Thread(target=receive)
t1.start()
t2.start()
