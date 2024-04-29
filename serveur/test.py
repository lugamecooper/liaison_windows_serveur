import socket
import time

TCP_IP = 'localhost'
TCP_PORT = 9001
BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
recived_f = 'convocation.pdf'

with open(recived_f, 'wb') as f:
    print('file opened')
    while True:
        #print('receiving data...')
        data = s.recv(BUFFER_SIZE)
        if not data:
            f.close()
            break
        # write data to a file
        f.write(data)