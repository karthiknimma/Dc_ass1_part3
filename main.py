#ASSIGNMENT 1 (PART 3)
#AUTHOR1: Karthik Nimma (101650589)
#AUTHOR2: Maheen Tanveer (101673264)
#SUBMITTED TO : DR. ZHONGMEI YAO
#COURSE: DATA COMMUNICATIONS (CPS-570)
import time
from pathlib import Path
from bs4 import BeautifulSoup
import requests
from queue import Queue
import threading


from Ass1Tcpsocket import TCPsocket
from Ass1Request import Request
from URLparse import URLparse

import sys

def main():

    # open file
    Path('URL-input-100.txt').stat()
    # getting file size
    file = Path('URL-input-100.txt').stat().st_size
    # display the size of the file
    print("Size of file is :", file, "bytes")
    print("\n")

    # shared parameters
    shared = sharedParameters()
    shared.lock = threading.Lock()
    shared.countUniques = 0
    shared.unique_ips = set()
    shared.unique_host = set()
    #shared.hostnames = None

    filename = "URL-input-100.txt"
    Q = []

    shared.hostnames = AddtoQ(filename,Q)
    #print(shared.hostnames)

    listOfThreads = []  # empty list
    num_threads = 5

    for i in range(num_threads):
        worker = myThread(i+1,shared)
        worker.start()
        listOfThreads.append(worker)
        for t in listOfThreads:
            t.join()  # wait for each thread to finish

    print("Number of uniques", shared.countUniques)
    print("Uniques", shared.unique)

    unique_ips = set()
    unique_host = set()

   # for i in range (10):



def checkUniqueness_ip(list_ips,ip):
    size = [1, 1]
    size[0] = len(list_ips)
    list_ips.add(ip)
    size[1] = len(list_ips)
    if (size[1] <= size[0]):
        print("Checking IP uniqueness....Failed")
        return False
    print("Checking IP uniqueness....Passed")
    return True


def checkUniqueness_host(list_host,host):
    size = [1, 1]
    size[0] = len(list_host)
    list_host.add(host)
    size[1] = len(list_host)
    if (size[1] <= size[0]):
        print("Checking Host uniqueness....Failed")
        return False
    print("Checking Host uniqueness....Passed")
    return True


def AddtoQ(filename,Q):
    try:
        with open(filename) as file:
            for line in file:
                Q.append(line)
        file.close()
    except IOError:
        print('No such file')
        exit(1)
    return Q

class sharedParameters:
    def __init__(self):
        self.lock = None
        self.countUniques = 0
        self.hostnames = None
        self.unique_ips = None
        self.unique_host = None

class myThread (threading.Thread):
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
               for link in soup.find_all('a'):
                   # print(link.get('href'))
                   count += 1
               print('Parsing Page... Done in ', (time.time() - start) * 1000, 'ms', 'with', count, 'links')
           print("-------------------------------------------------------------------------------------------")

           mysocket.close()

       # size = [1, 1]
       # number = [1]
       #
       # while (True):
       #     self.shared.lock.acquire()
       #     if (len(self.shared.hostnames) < 1):
       #         self.shared.lock.release()
       #         break
       #
       #     number[0] = self.shared.hostnames.pop(0)
       #     size[0] = len(self.shared.unique)
       #     self.shared.unique.add(number[0])
       #     size[1] = len(self.shared.unique)
       #
       #     if (size[1] > size[0]):
       #         print("Thread:" + str(self.threadID) + " " + "Working on unique number" + " " + str(number[0]))
       #         #print("threadID: %d prints: unique number %d" % (self.threadID, number[0]))
       #         self.shared.countUniques += 1
       #     self.shared.lock.release()
           #time.sleep(2)


# call main() method:
if __name__ == "__main__":
   main()