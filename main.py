# ASSIGNMENT 1 (PART 3)
# AUTHOR1: Karthik Nimma (101650589)
# AUTHOR2: Maheen Tanveer (101673264)
# SUBMITTED TO : DR. ZHONGMEI YAO
# COURSE: DATA COMMUNICATIONS (CPS-570)

# NOTE.............
    # FOR SIMPLICITY THE PROGRAM ONLY ADDS 1000 URLS OUT OF THE 1MURLS, INTO THE QUEUE.(CHECK ADDTOQ FUNCTION TO REMOVE THE RESTRICTION)
    #CURRENTLY 200 THREADS ARE USED FOR PROCESSING THE URLS AND ONE ADDITIONAL THREAD IS USED TO PRINT OUTPUT EVERY 2 SECS
    # WE WERE UNABLE TO PRINT THE  STATS i.e MPBS, PPS EVEN AFTER A LOT OF THINKING.
    # Threads take some time to terminate, therefore the final output may take some time to print out.


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

import myThread


def main():
    # open file
    Path('URL-input-1M.txt').stat()
    # getting file size
    file = Path('URL-input-1M.txt').stat().st_size
    # display the size of the file
    print("Size of file is :", file, "bytes")
    print("\n")

    shared = sharedParameters()
    filename = "URL-input-1M.txt"
    Q = []

    startT = time.time()
    shared.hostnames = AddtoQ(filename, Q)
    print("Queue size", len(shared.hostnames))
    #print(shared.hostnames)

    listOfThreads = []  # empty list
    num_threads = 200

    # shared parameters
    shared.lock = threading.Lock()
    # shared.countUnique_ips = 0
    shared.unique_ips = set()
    shared.unique_host = set()
    shared.pageSize = []
    shared.qsize = len(shared.hostnames)

    for i in range(num_threads):
            worker = myThread.myThread(i + 1, shared)
            worker.start()
            listOfThreads.append(worker)
    t11= threading.Timer(2.0, printing, args=(shared,) )
    # t11.setDaemon(True)
    t11.start()
    time.sleep(3)
    listOfThreads.append(t11)

    for t in listOfThreads:
        t.join()  # wait for each thread to finish



    print("Looked up", shared.dns_count , "DNS names")
    print('Number of crawled URLS', shared.count_crawl)
    print('Number of URLs that have passed robots checks', shared.count_robot)
    print("Number of uniques ips", shared.countUnique_ips)
    print("Number of uniques host", shared.countUnique_host)
    print('Total links found', shared.count_link)
    print('Average Page size:', sum(shared.pageSize) / len(shared.pageSize))


    print("\n HTTP codes seen for GET: 2xx = " +
    str(shared.codeTwo) + ",3xx = " + str(shared.codeThree) + ", 4xx = " + str(shared.codeFour) + ", 5xx = " + str(
    shared.codeFive) +
    ",other = " + str(shared.other))

def printing(shared):
    while(len(shared.hostnames)>0):
        print('',threading.active_count()-2,'Q\t',len(shared.hostnames),'E\t',shared.extractedUrls,'H\t',shared.countUnique_host,'D\t',shared.dns_count,'I\t',shared.countUnique_ips,'R\t',shared.count_robot,'C\t',shared.count_crawl,'L\t',shared.count_link)
        # print('Average Page size:',sum(shared.pageSize)/len(shared.pageSize))
        if (len(shared.hostnames) == 0):
            break
        time.sleep(2)


def checkUniqueness_ip(list_ips, ip):
    size = [1, 1]
    size[0] = len(list_ips)
    list_ips.add(ip)
    size[1] = len(list_ips)
    if (size[1] <= size[0]):
        # print("Checking IP uniqueness....Failed")
        return False
    # print("Checking IP uniqueness....Passed")
    return True


def checkUniqueness_host(list_host, host):
    size = [1, 1]
    size[0] = len(list_host)
    list_host.add(host)
    size[1] = len(list_host)
    if (size[1] <= size[0]):
        # print("Checking Host uniqueness....Failed")
        return False
    # print("Checking Host uniqueness....Passed")
    return True


def AddtoQ(filename, Q):
    try:
        with open(filename) as file:
            count = 0
            for line in file:
                Q.append(line)
                count += 1
                if(count==1000):
                    break
        file.close()
    except IOError:
        print('No such file')
        exit(1)
    return Q


class sharedParameters:
    def __init__(self):
        self.lock = None
        self.extractedUrls = 0
        self.countUnique_ips = 0
        self.countUnique_host = 0
        self.hostnames = None
        self.unique_ips = None
        self.unique_host = None
        self.count_link = 0
        self.count_crawl = 0
        self.count_robot = 0
        self.qsize = 0
        self.dns_count = 0
        self.pageSize = None
        self.codeTwo = 0
        self.codeThree = 0
        self.codeFour = 0
        self.codeFive =0
        self.other =0

# call main() method:
if __name__ == "__main__":
    main()





