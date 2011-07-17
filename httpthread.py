#!/usr/bin/python
# -*- coding: utf-8 -*-
import httphandler
import BaseHTTPServer
import threading
import var
import sys

class HTTPThread(threading.Thread):
    def run(self):
        sys.stdout.write("Starting HTTP server...\n")
        httpd = BaseHTTPServer.HTTPServer((var.HTTP_ADDRESS, var.HTTP_PORT), httphandler.HTTPHandler, True)
        sys.stdout.write("HTTP server started!\n")
        while (True):
            httpd.handle_request()