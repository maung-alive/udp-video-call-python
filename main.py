import socket
import cv2
import pickle
import numpy

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

RHOST = "192.168.100.156"   # Change your own
RPORT = 6001        # Change your own

s.bind((RHOST, RPORT))

while True:
    (addr, data) = s.recvfrom(65535)
    print(f"Connected from : {addr[0]}:{addr[1]}")

    data = pickle.loads(data)
    data = cv2.imdecode(data, cv2.IMREAD_COLOR)
    cv2.imshow('my pic', data)
    if cv2.waitKey(10) == 13:
        break

cv2.destroyAllWindows()        # Close all windows

if __name__ == '__main__':
    print('PyCharm')