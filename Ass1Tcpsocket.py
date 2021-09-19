

import socket, select
import time

TIMEOUT = 10 # unit is seconds
BUF_SIZE = 1024 # unit is bytes

class TCPsocket:
    def __init__(self):
        self.sock = None
        self.host = ""

    def createSocket(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # self.sock is an instance variable
            # print("Created a tcp socket!")
        except socket.error as e:
            print("Failed to create a TCP socket {}".format(e))
            self.sock = None


    def getIP(self, hostname):
        self.host = hostname
        try:
            start = time.time()
            ip = socket.gethostbyname(hostname)   # ip is a local variable to getIP(hostname), ip is of string type
            print('Doing DNS. Done in..',(time.time()-start)*1000,'ms')
        except socket.gaierror:
            print("Failed to gethostbyname")
            return None
        return ip


    # connect to a remote server: IP address, port
    def connect(self, ip, port):
        if self.sock is None or ip is None:
            self.sock = None
            return
        try:
            self.sock.connect((ip, port))   # server address is defined by (ip, port)
            print("Successfully connect to host:", ip)
        except socket.error as e:
            print("Failed to connect: {}".format(e))
            self.sock.close()
            self.sock = None

    # return the number of bytes sent
    def send(self, request):
        bytesSent = 0       # bytesSent is a local variable
        if self.sock is None:
            return 0
        try:
            bytesSent = self.sock.sendall(request.encode())   # encode(): convert string to bytes
        except socket.error as e:
            print("socket error in send: {}".format(e))
            self.sock.close()
            self.sock = None
        return bytesSent

    # Receive the reply from the server. Return the reply as string
    def receive(self):
        reply = bytearray()    # b'', local variable, bytearray is multable
        if self.sock is None:
            return reply

        self.sock.settimeout(TIMEOUT)

        bytesRecd = 0   # local integer
        start = time.time()
        try:
            while True:         # use a loop to receive data until we receive all data
                data = self.sock.recv(BUF_SIZE)  # returned chunk of data with max length BUF_SIZE. data is in bytes
                if data == b'':  # if empty bytes
                   break
                else:
                   reply += data  # append to reply
                   bytesRecd += len(data)
            print('Loading done in ..', (time.time() - start) * 1000, 'ms', 'with', bytesRecd , 'bytes' )
        except socket.error as e:
            print("socket error in receive: {}".format(e))
            self.sock.close()
            self.sock = None
        reply_str = reply.decode()
        return reply_str

    # Close socket
    def close(self):
        if not (self.sock is None):
            self.sock.close()

