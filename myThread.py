import threading
import time
from urllib.error import HTTPError

import requests
from bs4 import BeautifulSoup

from Ass1Request import Request
from Ass1Tcpsocket import TCPsocket
from URLparse import URLparse
from main import checkUniqueness_host, checkUniqueness_ip


class myThread(threading.Thread):
    def __init__(self, threadID, shared):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.shared = shared

    def run(self):
        self.shared.lock.acquire()
        print("\nStarting thread: ", self.threadID)
        self.shared.lock.release()

        while (True):
            self.shared.lock.acquire()
            if (len(self.shared.hostnames) < 1):
                self.shared.lock.release()
                break

            mysocket = TCPsocket()  # create an object of TCP socket
            mysocket.createSocket()

            p = URLparse()
            url = self.shared.hostnames.pop(0)
            host, path, query, port = p.parse(url)
            # print ('port:', port)

            # Check uniqueness host
            unique_status1 = checkUniqueness_host(self.shared.unique_host, host)

            if not unique_status1:
                continue

            # Resolve Ip address using dns
            ip = mysocket.getIP(host)

            # Check uniqueness IP
            unique_status = checkUniqueness_ip(self.shared.unique_ips, ip)

            if not unique_status:
                continue

            start = time.time()
            mysocket.connect(ip, port)
            print('Connecting on Robots..', (time.time() - start) * 1000, 'ms')

            # build our HEAD request for robots
            myrequest = Request()
            msg = myrequest.headRequest(host)

            # send out request
            mysocket.send(msg)
            data = mysocket.receive()  # receive a reply from the server
            # print('Response content length: ', len(data), '')

            if (len(data) == 0):
                print("-------------------------------------------------------------------")
                self.shared.lock.release()
                continue
            x = data.split()
            print("Verifying header...status Code: ", x[1])
            mysocket.close()

            if (x[1] != '200'):

                mysocket = TCPsocket()  # create an object of TCP socket
                mysocket.createSocket()
                start = time.time()
                mysocket.connect(ip, port)
                print('Connecting on  page..', (time.time() - start) * 1000, 'ms')

                # build our GET request
                myrequest = Request()
                msg = myrequest.getRequest(host, path, query)

                # send out request
                mysocket.send(msg)
                data = mysocket.receive()  # receive a reply from the server
                # print('Response content length: ', len(data), '`')

                x = data.split()
                print("Verifying header...status Code: ", x[1])


                r = requests.get(url)
                start = time.time()


                soup = BeautifulSoup(r.text, "html.parser")
                count = 0
                try:
                    for link in soup.find_all('a'):
                        count += 1
                except AttributeError:
                    continue
                print('Parsing Page... Done in ', (time.time() - start) * 1000, 'ms', 'with', count, 'links')
            print("-------------------------------------------------------------------------------------------")

            mysocket.close()
            self.shared.lock.release()

