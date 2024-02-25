import socket
import cv2
import threading
import numpy

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 10000000)

LHOST = "127.0.0.1"   # Change your own
LPORT = 6001        # Change your own
width, height = 320, 240

s.bind((LHOST, LPORT))

capture = cv2.VideoCapture(0)   # Change to your own webcam or video file
capture.set(3, width)
capture.set(4, height)
def transmit(addr):
    while True:
        ret, photo = capture.read()
        encoded_frame = cv2.imencode('.jpg', photo)[1].tobytes()

        s.sendto(encoded_frame, addr)

def receive():
    while True:
        (data, addr) = s.recvfrom(65507)
        data = cv2.imdecode(numpy.frombuffer(data, dtype=numpy.uint8), 1)

        cv2.imshow(f"CLIENT: {addr[0]}:{addr[1]}", data)
        if cv2.waitKey(10) == 13:
            break

def main():
    while True:
        print(f"Listening Incoming connections...")
        (data, addr) = s.recvfrom(65507)
        print(f"Connected from : {addr[0]}:{addr[1]}")  # Logging client on Terminal

        transmit_thread = threading.Thread(target=transmit, args=(addr,))   # Threading
        receive_thread = threading.Thread(target=receive)   # Threading
        # Start Threads
        transmit_thread.start()
        receive_thread.start()


if __name__ == '__main__':
    print(f"Running server at {LHOST}:{LPORT}")
    main()