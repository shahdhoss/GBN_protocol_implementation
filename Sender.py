from socket import *
import time

RecieverIp = 'localhost'
ReceiverPort = 12000
MSS = 800            #Maximum segment size
N = 3 #windows size-> how many unacknowledged packets can be in transit at any given time


def read(filee):
    Data = []
    with open(filee, 'rb') as i:  # rb (binary) - images
        while True:
            Chunks = i.read(MSS)
            if not Chunks:
                break
            Data.append(Chunks)
    #print(Data)

filee = 'Computer Networks Project/small file.jpeg'
#read('filee')""" 
def MakePackets(Flag,PacketId,Data,FileId):
    FileId = file_id.to_bytes(2, byteorder='big')
    PacketId = PacketId.bytes(2,byteordeق= 'big')
    if Flag:
        TrailerBits= 0xFFFF
    else:
        TrailerBits =  0x0000
    TrailerBits= TrailerBits.to_bytes(2, byteorder='big')
    Packet = FileId+ PacketId+ TrailerBits+Data
    return Packet

def Sender(Filee,RecieverPort,IpAddress):
    Packets = read(filee) #data
    SenderSocket = socket(AF_INET,SOCK_DGRAM) #UDP
    SendSize= 0
    PacketLength = len(Packets)
    SendBase = 0
    for i in range(window_base, min(SendBase+N,PacketLength)):  #to ensure enna ma3adenash size el packets
        #create packet ->it add (sequence number,checksums,headers)
        Packet =create_packet(i,FileId,Packets[i],i==len(packets)-1) #a5er goz2 ensure en a5er packet wslet
        SenderSocket.sendto(Packet,(IpAddress,ReceiverPort))
      #----
sender(filee,ReceiverIp, ReceiverPort)
#Determine time needed to send ack else yb2a fi moskela..send again