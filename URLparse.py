from urllib.parse import urlparse


class URLparse:
    def __init__(self):
        self.host = ""  # each object's instance variables
        self.port = 0
        self.path = ""  # remote host name
        self.query = ""
        self.path = ""

    def parse(self,url):
        o = urlparse(url)
        if(o.netloc) != '':
            self.host = o.netloc

        if(o.port != None):
            self.port = o.port
        else:
            self.port = 80

        if(o.path != ''):
            self.path=o.path
        else:
            self.path = '/'

        if(o.query != ''):
            self.query=o.query
        else:
            self.query=''

        print('Parsing URl...host' , self.host , 'Port', self.port)
        return self.host, self.path, self.query, self.port
