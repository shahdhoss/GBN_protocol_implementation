from socket import *
import time
from datetime import datetime
ReceiverIp = 'localhost'
ReceiverPort = 1200
MSS = 2040           #Maximum segment size
N = 3                #windows size-> how many unacknowledged packets can be in transit at any given time

def get_packetid(packet):
    packet_id=packet[:2]
    return int.from_bytes(packet_id, byteorder='big')

#divide the IMAGE into chunks based on SIZE OF MSS
def read(filee):
    Data = []
    with open(filee, 'rb') as i:  # rb (binary) - images
        while True:
            Chunks = i.read(MSS)
            if not Chunks:
                break
            Data.append(Chunks)
    return Data

file1= 'Computer Networks Project\medium file.jpeg'
file2= 'Computer Networks Project\small file.jpeg'
file3 ='Computer Networks Project\large file.jpeg'

# print(len(read(filee)))
#
def make_packets(flag, packet_id, data, file_id):
    packet_id = packet_id.to_bytes(2, byteorder='big') #16 bits
    file_id = file_id.to_bytes(2, byteorder='big') # 16 bits
    if flag:  
        trailer_bits = 0xFFFF   #lesa mwselnash l2a5er packet 
    else:    
        trailer_bits = 0x0000
    trailer_bits = trailer_bits.to_bytes(4, byteorder='big') # 32 bits
    Packet = packet_id+ file_id + data+ trailer_bits 
    return Packet

def send_to_receiver(packets, ip_address, port):
    SenderSocket = socket(AF_INET, SOCK_DGRAM)
    for i in packets:
        SenderSocket.sendto(i, (ip_address, port))
    SenderSocket.close()


def sender(filee, receiver_port, ip_address):
    Packets = read(filee)
    SenderSocket = socket(AF_INET, SOCK_DGRAM) 
    PacketLength = len(Packets)
    SendBase = 0
    NextSeqNum = 0
    Timer = False
     #Makepacket ->it adds (sequence number,checksums,headers)
     # yb3at tany el packets elli ma7asalahash ack
    while SendBase < PacketLength:
        if NextSeqNum < SendBase + N and NextSeqNum < PacketLength:    #to ensure enna ma3adenash size el packets
            Packet = make_packets(NextSeqNum == PacketLength - 1, NextSeqNum, Packets[NextSeqNum], 1) #awl goz2 ensure en a5er packet wslet
            print("this is the packetid inside the while loop: " ,get_packetid(Packet))
            SenderSocket.sendto(Packet, (ip_address, receiver_port))
            print(f"Packet {NextSeqNum} sent..")
            hour_time_of_sending= datetime.now().hour
            minute_time_of_sending= datetime.now().minute
            second_time_of_sending =datetime.now().second
            print(f"Packet sent at: {hour_time_of_sending}:{minute_time_of_sending}:{second_time_of_sending}")
            if not Timer:  
                StartTime = time.time()
                Timer = True
            NextSeqNum += 1

        try:
            AckPacket, _ = SenderSocket.recvfrom(2048)  #return tuple -> data + address of the sender - me7adgin awl wa7ed bs
            AckNumber = int.from_bytes(AckPacket[:2], byteorder='big')  
            # print("this is the packet no: ", AckNumber)
            if SendBase <= AckNumber < SendBase + N:   #'<'3lshan momken yb3at nafs el packet kaza mara
                SendBase = AckNumber + 1
                Timer = False
        except timeout:
            if time.time() - StartTime >= 5:
                print("Timeout !! Retransmitting unacknowledged packets..")
                NextSeqNum = SendBase  # Reset NextSeqNum to SendBase
                for i in range(SendBase, min(SendBase + N, PacketLength)):  # Retransmit packets within the current window
                    Packet = make_packets(i == PacketLength - 1, i, Packets[i], 1)
                    SenderSocket.sendto(Packet, (ip_address, receiver_port))
                    print(f"Packet {i} retransmitted..")
    
        
    print("Packets are sent successfully!")
    SenderSocket.close()

sender(filee, ReceiverPort, ReceiverIp)