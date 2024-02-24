import socket
import cv2

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 10000000)

LHOST = "127.0.0.1"   # Change your own
LPORT = 6001        # Change your own

s.bind((LHOST, LPORT))

capture = cv2.VideoCapture(0)   # Change to your own webcam or video file
def transmit(addr):
    while True:
        ret, photo = capture.read()


        photo = cv2.resize(photo, (400,400))
        encoded_frame = cv2.imencode('.jpg', photo)[1].tobytes()

        s.sendto(encoded_frame, addr)
        if cv2.waitKey(10) == 13:   # Enter Key then quit
            break

def main():
    while True:
        print(f"Listening Incoming connections...")
        (data, addr) = s.recvfrom(65507)
        print(f"Connected from : {addr[0]}:{addr[1]}")  # Logging client
        transmit(addr)


if __name__ == '__main__':
    print(f"Running server at {LHOST}:{LPORT}")
    main()