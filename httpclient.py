#!/usr/bin/env python3
# coding: utf-8
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
import urllib.parse

def help():
    print("httpclient.py [GET/POST] [URL]\n")

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    #def get_host_port(self,url):

    # Connect to host/port
    def connect(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        return None

    # Send data over socket
    def sendall(self, data):
        self.socket.sendall(data.encode('utf-8'))
    
    # Close socket
    def close(self):
        self.socket.close()

    # Read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return buffer.decode('utf-8')

    # Return the status code
    def get_code(self, data):
        return data.split(' ')[1]

    # Return the HTTP headers in an array 
    def get_headers(self,data):
        return data.split('\r\n')[:-1]

    # Return the body of the response
    def get_body(self, data):
        return data.split('\r\n')[-1]

    # Do a GET request
    def GET(self, url, args=None):
        url_host = urllib.parse.urlparse(url).netloc.split(':')[0]
        url_path = urllib.parse.urlparse(url).path
        url_path = url_path if url_path != '' else '/'
        url_port = 80 if urllib.parse.urlparse(url).port == None else urllib.parse.urlparse(url).port
        request = f'GET {url_path} HTTP/1.1\r\nHost: {url_host}\r\nConnection: close\r\nAccept: text/html, application/x-www-form-urlencoded\r\n\r\n'
        self.connect(url_host, url_port)
        self.sendall(request)
        data=self.recvall(self.socket)
        self.close()
        print(int(self.get_code(data)))
        print(self.get_body(data))
        return HTTPResponse(int(self.get_code(data)), self.get_body(data))

    # Do a POST request
    def POST(self, url, args=None):
        url_host = urllib.parse.urlparse(url).netloc.split(':')[0]
        url_path = urllib.parse.urlparse(url).path
        url_port = 80 if urllib.parse.urlparse(url).port == None else urllib.parse.urlparse(url).port
        data_size = 0
        if args!=None:
            data = ''
            for i, (k, v) in enumerate(args.items()):
                if i == len(args) - 1:
                    data = data + (k + '=' + v)
                else:
                    data = data + (k + '=' + v + '&')
            data_size = len(data.encode('utf-8'))

        request = f'POST {url_path} HTTP/1.1\r\nHost: {url_host}\r\nConnection: close\r\nContent-Type: application/x-www-form-urlencoded\r\nContent-Length: {data_size}\r\n\r\n'
        request = request + data if args!=None else request

        self.connect(url_host, url_port)
        self.sendall(request)
        data=self.recvall(self.socket)
        self.close()
        print(int(self.get_code(data)))
        print(self.get_body(data))
        return HTTPResponse(int(self.get_code(data)), self.get_body(data))

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            print(args)
            return self.POST( url, args )
        else:
            return self.GET( url, args )
    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        #print('You asked for: ', sys.argv[0], sys.argv[1], sys.argv[2])
        print(client.command( sys.argv[2], sys.argv[1] ))
    else:
        #print('You asked for: ', sys.argv[1])
        print(client.command( sys.argv[1] ))

# Sources Consulted:
#
# For enumerate over a dictionary:
# https://stackoverflow.com/questions/20838839/how-to-get-the-last-item-of-the-dictionary-when-looping?rq=1