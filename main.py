# ASSIGNMENT 1 (PART 3)
# AUTHOR1: Karthik Nimma (101650589)
# AUTHOR2: Maheen Tanveer (101673264)
# SUBMITTED TO : DR. ZHONGMEI YAO
# COURSE: DATA COMMUNICATIONS (CPS-570)
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
    Path('URL-input-100.txt').stat()
    # getting file size
    file = Path('URL-input-100.txt').stat().st_size
    # display the size of the file
    print("Size of file is :", file, "bytes")
    print("\n")

    shared = sharedParameters()
    filename = "URL-input-100.txt"
    Q = []

    startT = time.time()
    shared.hostnames = AddtoQ(filename, Q)
    print("Queue size", len(shared.hostnames))
    #print(shared.hostnames)

    listOfThreads = []  # empty list
    num_threads = 10

    # shared parameters
    shared.lock = threading.Lock()
    # shared.countUnique_ips = 0
    shared.unique_ips = set()
    shared.unique_host = set()
    shared.qsize = len(shared.hostnames)


    for i in range(num_threads):
            worker = myThread.myThread(i + 1, shared)
            worker.start()
            listOfThreads.append(worker)
    for t in listOfThreads:
        t.join()  # wait for each thread to finish


    print('Number of crawled URLS', shared.count_crawl)
    print('Number of URLs that have passed robots checks', shared.count_robot)
    print("Number of uniques ips", shared.countUnique_ips)
    print("Number of uniques host", shared.countUnique_host)
    print("Number of Sucessful DNS lookups", shared.dns_count)
    # print('Total links found', shared.count_link)

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

# call main() method:
if __name__ == "__main__":
    main()