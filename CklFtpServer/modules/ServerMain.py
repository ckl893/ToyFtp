#!/usr/bin/python3
#-*- coding:utf-8 -*-

"""
Do not say a dirty word!
"""
import sys
sys.path.append('/data/python/')
from CklFtpServer.conf import settings 
import socketserver
import json
import os
import subprocess
import time
import logging
CurTime = time.strftime('%Y%m%d',time.localtime(time.time())) 
LogFile = '%s/Server_%s.log' %(settings.LogPath,CurTime)


class CklTcpHandler(socketserver.BaseRequestHandler):
    def LoginAuth(self):
        UserCircle = True
        while UserCircle:
            UserData = self.request.recv(1024)
            UserStrData = UserData.decode()
            print(UserStrData)
            if UserStrData in settings.UserAccount.keys():
                self.request.send(bytes("UserPassed", "utf8"))
                while True:
                    PassData = self.request.recv(1024)
                    PassStrData = PassData.decode()
                    print(PassStrData)
                    if PassStrData == settings.UserAccount[UserStrData]['password']:
                        self.request.send(bytes("PassPassed", "utf8"))
                        UserCircle = False
                        UserHome = settings.HomeDir + "/" + UserStrData
                        os.chdir(UserHome)
                        CurTime = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time())) 
                        Content = "%s: %s login ftp server succeed\n" %(CurTime,UserStrData)
                        with open(LogFile,'a') as fl:
                            fl.write(Content) 
                        break
                    else:
                        PassTry = "Sorry,your pass is wrong,try again!"
                        self.request.send(bytes(PassTry, "utf8"))
                        CurTime = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time())) 
                        Content = "%s: %s login ftp failed password failed\n" %(CurTime,UserStrData)
                        with open(LogFile,'a') as fl:
                            fl.write(Content) 
            else:
                UserTry = "Sorry,%s not found,try again!" % UserStrData
                self.request.send(bytes(UserTry, "utf8"))
                CurTime = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time())) 
                Content = "%s: %s login failed, not found\n" %(CurTime,UserStrData) 
                with open(LogFile,'a') as fl:
                    fl.write(Content) 
                continue

    def TransActive(self):
        while True:
            print("Top")
            ClientData = self.request.recv(1024)
            FileMsg = ClientData.decode()
            time.sleep(1)
            FileList = ''.join(FileMsg).strip().split(":")
            print(FileList[0])

            if FileList[0] == "put":
                PutFileName = FileList[1]
                PutFileSize = int(FileList[2])
                self.request.send(bytes("ReadyDone", "utf8"))
                print(PutFileName)
                RecievedSize = 0
                while RecievedSize < PutFileSize:
                    RecievedData = self.request.recv(500)
                    with open(PutFileName, 'ab+') as fu:
                        fu.write(RecievedData)
                    RecievedSize += len(RecievedData)
                else:
                    pass
                CurTime = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time())) 
                Content = "%s: %s upload file %s ,size is %s\n" %(CurTime,UserStrData,PutFileName,PutFileSize)
                with open(LogFile,'a') as fl:
                    fl.write(Content) 
                print("--- recieved done ---")
            elif FileList[0] == "get":
                GetFileName = FileList[1]
                print(GetFileName)
                if os.path.exists(GetFileName):
                    with open(GetFileName, 'rb') as fu:
                        GetData = fu.read()
                        DataLength = len(GetData)
                        print(DataLength)
                    GetFileSize = int(DataLength)
                    self.request.send(bytes("%s" % (DataLength), "utf8"))
                    ReadyResult = self.request.recv(500)
                    if ReadyResult.decode() == "ReadyDone":
                        SendData = GetData
                        self.request.send(SendData)
                        CurTime = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time())) 
                        Content = "%s: %s download %s size is %s\n" %(CurTime,UserStrData,GetFileName,GetFileSize) 
                        with open(LogFile,'a') as fl:
                            fl.write(Content) 
                else:
                    self.request.send(bytes("%s is not found" % GetFileName, "utf8"))
            elif FileList[0] == "ls":
                Fresult = subprocess.Popen("ls -l", shell=True, stdout=subprocess.PIPE)
                Sresult = Fresult.stdout.read().decode()
                LenResult = str(len(Sresult))
                self.request.send(bytes(LenResult, "utf8"))
                Ready = self.request.recv(200)
                if Ready.decode() == "ReadyDone":
                    self.request.send(bytes(Sresult, "utf8"))
            elif FileList[0] == "?":
                HelpContent = ""
                for x,m in settings.HelpDict.items():
                    Data = "%8s : %s \n"%(x,m)
                    HelpContent += Data
                self.request.send(bytes(HelpContent, "utf8"))

    def handle(self):
        self.LoginAuth()
        self.TransActive()

if __name__ == "__main__":
    pass
