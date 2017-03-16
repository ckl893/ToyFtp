#!/usr/bin/python3
#-*- encoding:utf-8 -*-

import sys
sys.path.append('/data/python/')
from CklFtpServer.conf import settings
from CklFtpServer.modules import ServerMain
import socketserver

if __name__ == "__main__":
    HOST, PORT = settings.BindHost, settings.BindPort
    server = socketserver.ThreadingTCPServer((HOST, PORT), ServerMain.CklTcpHandler)
    server.serve_forever()
