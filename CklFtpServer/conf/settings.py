#!/usr/bin/python3
#-*- coding:utf-8 -*-

BindHost = '0.0.0.0'
BindPort = 9999

LogPath = '/data/python/CklFtpServer/var/logs'
HomeDir = '/data/python/CklFtpServer/var/users'
UserAccount = {
    'ckl': {
        'password':'12345',
        'quotation': 1000000,
        'expit': '2017-12-12'
     },
    'zld': {
        'password':'12345',
        'quotation': 1000000,
        'expit': '2017-12-12'
     },
}

HelpDict = {
     '?':'display the help message',
     'ls':'list the file on the server',
     'put file':'upload file to server',
     'get file':'downloaf file from server'
}


if __name__ == "__main__":
    pass
