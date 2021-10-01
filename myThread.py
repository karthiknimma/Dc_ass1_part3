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
        #print("\nStarting thread: ", self.threadID)
        self.shared.lock.release()

        while (True):
            self.shared.lock.acquire()

            if (len(self.shared.hostnames) < 1):
                self.shared.lock.release()
                break

            p = URLparse()
            url = self.shared.hostnames.pop(0)
            # shared.qsize = len(shared.hostnames)
            #print ("Current size of queue:", self.shared.qsize)
            self.shared.qsize -=1
            self.shared.extractedUrls += 1
            self.shared.lock.release()

            #urlsplit
            host, path, query, port = p.parse(url)
            # print ('port:', port)

            mysocket = TCPsocket()  # create an object of TCP socket
            mysocket.createSocket()

            self.shared.lock.acquire()
            # Check uniqueness host
            unique_status1 = checkUniqueness_host(self.shared.unique_host, host)

            if not unique_status1:
                self.shared.lock.release()
                continue
            else:
                self.shared.countUnique_host += 1
            self.shared.lock.release()

            # Resolve Ip address using dns
            ip = mysocket.getIP(host)

            if ip:
                self.shared.dns_count +=1
            else:
                continue
            self.shared.lock.acquire()
            # Check uniqueness IP
            unique_status = checkUniqueness_ip(self.shared.unique_ips, ip)

            if not unique_status:
                self.shared.lock.release()
                continue
            else:
                self.shared.countUnique_ips +=1

            self.shared.lock.release()


            self.shared.lock.acquire()
            start = time.time()
            mysocket.connect(ip, port)
            #print('Connecting on Robots..', (time.time() - start) * 1000, 'ms')

            # build our HEAD request for robots
            myrequest = Request()
            msg = myrequest.headRequest(host)

            # send out request
            mysocket.send(msg)
            data = mysocket.receive()  # receive a reply from the server
            # print('Response content length: ', len(data), '')
            self.shared.pageSize.append(len(data))

            if (len(data) == 0):
               # print("-------------------------------------------------------------------")
                self.shared.lock.release()
                continue
            x = data.split()
            if(x[1].startswith('2')):
                self.shared.codeTwo  += 1
            elif(x[1].startswith('3')):
                self.shared.codeThree  +=1
            elif (x[1].startswith('4')):
                self.shared.codeFour += 1
            elif (x[1].startswith('5')):
                self.shared.codeFive += 1
            else:
                self.shared.other +=1
            #print("Verifying header...status Code: ", x[1])
            mysocket.close()

            if (x[1] != '200'):

                self.shared.count_crawl +=1

                mysocket = TCPsocket()  # create an object of TCP socket
                mysocket.createSocket()
                start = time.time()
                mysocket.connect(ip, port)
                #print('Connecting on  page..', (time.time() - start) * 1000, 'ms')

                # build our GET request
                myrequest = Request()
                msg = myrequest.getRequest(host, path, query)

                # send out request
                mysocket.send(msg)
                data = mysocket.receive()  # receive a reply from the server
                # print('Response content length: ', len(data), '`')

                self.shared.count_link += data.count("href")

            else:
                self.shared.count_robot += 1

            mysocket.close()

            self.shared.lock.release()

            # time.sleep(2)


