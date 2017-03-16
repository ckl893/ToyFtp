#!/usr/bin/env python
# -*- coding:utf-8 -*-

import socket
import sys
sys.path.append('/data/python/')
from CklFtpClient.conf import settings
import re
import os
import time
import progressbar

IpPort = ('172.16.110.47', 9999)
Fsk = socket.socket()
Fsk.connect(IpPort)


class AuthClient():
    def __init__(self):
        pass

    def ClientLogin(self):
        UserCircleNum = 0
        while UserCircleNum < 2:
            AskUser = input("Your UserName: ")
            Fsk.send(bytes(AskUser, "utf8"))
            UserResult = Fsk.recv(1024)
            UserStrResult = UserResult.decode()
            if UserStrResult == "UserPassed":
                PassCircleNum = 0
                while PassCircleNum < 2:
                    AskPass = input("Your Password: ")
                    Fsk.send(bytes(AskPass, "utf8"))
                    PassResult = Fsk.recv(1024)
                    PassStrResult = PassResult.decode()
                    if PassStrResult == "PassPassed":
                        print("Welcome Login ckl ftp system!")
                        UserCircleNum = 2
                        break
                    else:
                        PassCircleNum += 1
                        print(PassCircleNum)
                        if PassCircleNum >= 2:
                            print("Your password tries is too much,will be quit")
                            Fsk.close()
                            sys.exit()
                        continue
            else:
                UserCircleNum += 1
                if UserCircleNum >= 2:
                    print("Your name tries is too much,will be quit!")
                    Fsk.close()
                    sys.exit()
                print(UserStrResult)
                continue
                # Fsk.close()


class ClientTrans(AuthClient):
    def __init__(self):
        pass

    def ClientFtp(self):
        while True:
            try:
                ClientSaid = input("Client>> ")
                MatchPutFirst = re.findall('\s?put\s+.*', ClientSaid)
                MatchPutResult = ''.join(MatchPutFirst).strip().split()
                MatchGetFirst = re.findall('\s?get\s+.*', ClientSaid)
                MatchGetResult = ''.join(MatchGetFirst).strip().split()
                if len(ClientSaid) <= 0:
                    continue

                if ClientSaid == 'quit':
                    print("Clinet System will be quit!")
                    break

                if len(MatchPutResult) > 0:
                    print(MatchPutResult)
                    if os.path.exists(MatchPutResult[1]):
                        with open(MatchPutResult[1], 'rb') as fu:
                            UpData = fu.read()
                            DataLength = len(UpData)
                            print(DataLength)

                        RealFileName = os.path.basename(MatchPutResult[1])
                        Fsk.send(bytes("put:%s:%s" % (RealFileName, DataLength), "utf8"))
                        ReadyResult = Fsk.recv(500)
                        if ReadyResult.decode() == "ReadyDone":
                            SendData = UpData
                            Fsk.send(SendData)
                        print("-- %s send finished --" % RealFileName)
                    else:
                        print("%s is not found!" % MatchPutResult[1])
                        continue

                if len(MatchGetResult) > 0:
                    Fsk.send(bytes("get:%s" % (MatchGetResult[1]), "utf8"))
                    FileLength = Fsk.recv(500)
                    if FileLength.decode() == "%s is not found" % MatchGetResult[1]:
                        print("Sorry,%s is not found!" % MatchGetResult[1])
                        continue
                    GetFileSize = int(FileLength.decode())
                    print(GetFileSize)
                    Fsk.send(bytes("ReadyDone", "utf8"))
                    RecievedSize = 0
                    with progressbar.ProgressBar(max_value=GetFileSize) as bar:
                        while RecievedSize < GetFileSize:
                            RecievedData = Fsk.recv(4096)
                            RecievedSize += len(RecievedData)
                            with open(MatchGetResult[1], 'ab+') as fu:
                                fu.write(RecievedData)
                            time.sleep(0.01)
                            bar.update(RecievedSize)
                        else:
                            pass


                    print("-- %s recieved finished --" % MatchGetResult[1])

                if ClientSaid == "ls":
                    Fsk.send(bytes("ls", "utf8"))
                    LenRes = Fsk.recv(500)
                    Lsize = int(LenRes.decode())
                    Fsk.send(bytes("ReadyDone", "utf8"))
                    RecievedLresult = ""
                    RecievedLSize = 0
                    while RecievedLSize < Lsize:
                        RecievedData = Fsk.recv(500)
                        RecievedLSize += len(RecievedData)
                        RecievedLresult += str(RecievedData.decode())
                    else:
                        print(RecievedLresult)
                elif ClientSaid == "?":
                    Fsk.send(bytes("?", "utf8"))
                    RecievedData = Fsk.recv(1024)
                    print(RecievedData.decode())
            except IndexError:
                pass
        Fsk.close()


if __name__ == "__main__":
    ClientOp = ClientTrans()
    ClientOp.ClientLogin()
    ClientOp.ClientFtp()
