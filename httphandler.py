#!/usr/bin/python
# -*- coding: utf-8 -*-
import BaseHTTPServer
import random
import re
import var

class HTTPHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self):
        if (var.HLDS_ISRUNNING == True):
            content = open("static/error.html", "r").read()
            content = content.format(var.HTTP_DOMAIN, var.HLDS_PORT, var.HLDS_TIMELEFT)
        else:
            content = open("static/index.html", "r").read()
            content = content.format(var.HTTP_DOMAIN, var.HTTP_PORT)

        self.send_response(200)
        self.send_header("content-type", "text/html")
        self.end_headers()
        self.wfile.write(content)

    def do_POST(self):
        length = int(self.headers.getheader('content-length'))
        data = self.rfile.read(length)
        err = self.verify(data)

        if (err == var.ERR_RUNSERVER):
            port = random.randrange(27016, 27099)
            var.HLDS_PORT = port
            var.HLDS_WAIT = True

        content = open("static/error.html", "r").read()
        content = content.format(var.HTTP_DOMAIN, var.HLDS_PORT, var.HLDS_TIMELEFT)
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(content)

    def verify(self, data):
        if (var.HLDS_ISRUNNING):
            result = var.ERR_PASSWORD
            return result

        match = re.search('code=(.*)&', data)
        if match <> None:
            code = match.group(1)
            result = var.ERR_RUNSERVER

        match = re.search('time=(.*)&', data)
        if match <> None:
            time = match.group(1)
            var.HLDS_TIMELEFT = int(time) * 60

        match = re.search('map=(.*)', data)
        if match <> None:
            map = match.group(1)
            var.HLDS_MAP = map

        return result

