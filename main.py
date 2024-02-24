import socket
import cv2
import pickle
import numpy

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

RHOST = "192.168.100.156"   # Change your own
RPORT = 6001        # Change your own

s.bind((RHOST, RPORT))

capture = cv2.VideoCapture(0)   # Change to your own webcam or video file
def transmit(addr, data):
    while True:
        ret, photo = capture.read()

        ret, buffer = cv2.imencode(".jpg", photo, [int(cv2.IMWRITE_JPEG_QUALITY),30])
        data = cv2.imdecode(data, cv2.IMREAD_COLOR)
        bytes = pickle.dumps(data)
        cv2.imshow(f"Client {addr[0]}", buffer) # Show opencv window
        s.sendto(bytes, addr)
        if cv2.waitKey(10) == 13:   # Enter Key then quit
            break

def main():
    while True:
        (addr, data) = s.recvfrom(65535)
        print(f"Connected from : {addr[0]}:{addr[1]}")  # Logging client
        transmit(addr)


if __name__ == '__main__':
    print('PyCharm')
    main()