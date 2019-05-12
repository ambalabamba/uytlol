import time
import socket
import struct
import random
import requests
import threading
 
# will generate specified amount of accounts, store in a text file, and then rank 6 of them at a time to rank 1
 
class Rank:
    def __init__(self, Username, Password, ServerIP, ServerPort):
        self.NullByte = struct.pack("B", 0)
        self.BufSize = 4096
        self.RoomList = []
        self.BanAttempts = 0
        self.Username = Username
        self.Password = Password
        self.MaxKills = 100000000000

        #socket.create_connection = socks.create_connection
        #socket.socket = socks.socksocket
 
        self.connectToServer(ServerIP, ServerPort)
 
    def sendPacket(self, PacketData, Receive = False):
        Packet = bytes(PacketData, "utf-8")
 
        try:
            self.SocketConn.send(Packet + self.NullByte)
 
            if Receive:
                return self.SocketConn.recv(self.BufSize).decode("utf-8")
        except:
            return
 
    def startKeepAlive(self, TimerSeconds = 20):
        if hasattr(self, "SocketConn"):
            KeepAliveTimer = threading.Timer(TimerSeconds, self.startKeepAlive)
            KeepAliveTimer.daemon = True
            KeepAliveTimer.start()
 
            self.sendPacket("0")
 
    def connectionHandler(self):
        Buffer = b""
 
        while hasattr(self, "SocketConn"):
            try:
                Buffer += self.SocketConn.recv(self.BufSize)
            except:
                break
 
            if len(Buffer) == 0:
                if hasattr(self, "SocketConn"):
                    self.SocketConn.close()
                    del self.SocketConn
 
                break
            elif Buffer.endswith(self.NullByte):
                Receive = Buffer.split(self.NullByte)
                Buffer = b""
 
                for Data in Receive:
                    Data = Data.decode("utf-8")
 
                    if Data.startswith("0g") or Data.startswith("0j"):
                        print("{{Server}}: {}".format(Data[2:]))
                    elif Data.startswith("093"):
                        print("Secondary login")
 
                        break
                    elif Data.startswith("0f") or Data.startswith("0e"):
                        Time, Reason = Data[2:].split(";")
                        print("This account has just been banned [Time: {} / Reason: {}]".format(Time, Reason))
                        break
                    elif Data.startswith("01"):
                        self.RoomList = Data[2:].split(":")
 
    def connectToServer(self, ServerIP, ServerPort):
        try:
            self.SocketConn = socket.create_connection((ServerIP, ServerPort))
        except Exception as Error:
            print(Error)
            return
 
        Handshake = self.sendPacket("08HxO9TdCC62Nwln1P", True).strip(self.NullByte.decode("utf-8"))
 
        if Handshake == "08":
            Credentials = "09{};{}".format(self.Username, self.Password)
            RawData = self.sendPacket(Credentials, True).split(self.NullByte.decode("utf-8"))
 
            for Data in RawData:
                if Data.startswith("A"):
                    self.UserID = Data[1:][:3]
                    self.Username = Data[4:][:20].replace("#", "")
 
                    EntryPackets = ["02Z900_", "0a"]
 
                    for Packet in EntryPackets:
                        self.sendPacket(Packet)
 
                    print(self.Username + " has been logged in.")
 
                    self.startKeepAlive()
 
                    ConnectionThread = threading.Thread(target=self.connectionHandler)
                    ConnectionThread.start()
 
                    RankingThread = threading.Thread(target=self.beginRanking)
                    RankingThread.daemon = True
                    RankingThread.start()
 
                    break
                elif Data == "09":
                    print("Incorrect password")
                    break
                elif Data == "091":
                    self.BanAttempts += 1
                    print("Currently banned.")
 
                    break
 
    def beginRanking(self):
        time.sleep(5.5)
        self.sendPacket("03_")
        KillCounter = 0
        RoomName = '1v1'
        CreateRoom = ["027200{}".format(RoomName)]
        JoinRoom = ["04{}".format(RoomName), "03{}".format(RoomName)]#, "06{};mp".format(RoomName)]
        Sepuku = ["509", "804500700", "6807000", "7{}7000".self.UserID] #self.UserID
 
        for Packet in CreateRoom:
            self.sendPacket(Packet)
            
        while KillCounter < self.MaxKills:
            time.sleep(1)
            KillCounter += 1
 
            for Packet in Sepuku:
                self.sendPacket(Packet)
 
class AFunStickArenaExperience:
    def __init__(self):
        self.NullByte = struct.pack("B", 0)
        self.BufSize = 4096
        self.RoomList = []
 
        Username, Password = "Suffering;uyt123".split(";")
        Rank(Username, Password, "ballistick1.xgenstudios.com", 1139) # 45.32.193.38
 
if __name__ == "__main__":
    AFunStickArenaExperience()
