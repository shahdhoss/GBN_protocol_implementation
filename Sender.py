from socket import *
import time

ReceiverIp = 'localhost'
ReceiverPort = 1200
MSS = 2040           #Maximum segment size
N = 3                #windows size-> how many unacknowledged packets can be in transit at any given time

def get_packetid(packet):
    packet_id=packet[:2]
    return int.from_bytes(packet_id, byteorder='big')
def read(filee):
    Data = []
    with open(filee, 'rb') as i:  # rb (binary) - images
        while True:
            Chunks = i.read(MSS)
            if not Chunks:
                break
            Data.append(Chunks)
    return Data

filee= 'Computer Networks Project\large file.jpeg'
# print(len(read(filee)))

def make_packets(flag, packet_id, data, file_id):
    packet_id = packet_id.to_bytes(2, byteorder='big') 
    file_id = file_id.to_bytes(2, byteorder='big')
    if flag:  
        trailer_bits = 0xFFFF   #lesa mwselnash l2a5er packet 
    else:    
        trailer_bits = 0x0000
    trailer_bits = trailer_bits.to_bytes(4, byteorder='big')
    Packet = packet_id+ file_id + data+ trailer_bits 
    return Packet

def send_to_receiver(packets, ip_address, port):
    SenderSocket = socket(AF_INET, SOCK_DGRAM)
    for i in packets:
        SenderSocket.sendto(i, (ip_address, port))
    SenderSocket.close()

#bosy this is your code please dont be mad at me
# def sender(filee, receiver_port, ip_address):
#     Packets = read(filee)
#     SenderSocket = socket(AF_INET, SOCK_DGRAM) 
#     PacketLength = len(Packets)
#     SendBase = 0
#     Timer = False
#     for NextSeqNum in range(SendBase, min(SendBase + N, PacketLength)):   #to ensure enna ma3adenash size el packets
#          #Makepacket ->it adds (sequence number,checksums,headers)
#         # yb3at tany el packets elli ma7asalahash ack
#         Packet = make_packets(NextSeqNum == PacketLength - 1, NextSeqNum, Packets[NextSeqNum], 1) #awl goz2 ensure en a5er packet wslet
#         SenderSocket.sendto(Packet, (ip_address, receiver_port))  # Encode packet to bytes before sending
#         print(f"Packet {NextSeqNum} sent..")
#         if not Timer:  
#             StartTime = time.time()
#             Timer = True
#         while True:
#             if time.time() - StartTime >= 5:  
#                 print("Timeout !! The unacknowledged packets will be sent again..")
#                 NextSeqNum = SendBase
#                 Timer= False  #reset el timer
#                 break
#             else:
#                 try:
#                     AckPacket, _ = SenderSocket.recvfrom(2048)   #return tuple -> data + address of the sender - me7adgin awl wa7ed bs
#                     AckNumber = int.from_bytes(AckPacket[:2], byteorder='big')  
#                     if SendBase<=AckNumber:  #'<'3lshan momken yb3at nafs el packet kaza mara
#                         SendBase = AckNumber + 1 
#                         Timer = False 
#                 except timeout:  
#                     continue

#     print("Packets are sent successfully!")
#     SenderSocket.close()
# sender(filee, ReceiverPort, ReceiverIp)

def sender(filee, receiver_port, ip_address):
    Packets = read(filee)
    SenderSocket = socket(AF_INET, SOCK_DGRAM) 
    PacketLength = len(Packets)
    SendBase = 0
    NextSeqNum = 0
    Timer = False
    while SendBase < PacketLength:
        if NextSeqNum < SendBase + N and NextSeqNum < PacketLength:
            Packet = make_packets(NextSeqNum == PacketLength - 1, NextSeqNum, Packets[NextSeqNum], 1)
            print("this is the packetid inside the while loop: " ,get_packetid(Packet))
            SenderSocket.sendto(Packet, (ip_address, receiver_port))
            print(f"Packet {NextSeqNum} sent..")
            if not Timer:  
                StartTime = time.time()
                Timer = True
            NextSeqNum += 1

        try:
            AckPacket, _ = SenderSocket.recvfrom(2048)
            AckNumber = int.from_bytes(AckPacket[:2], byteorder='big')  
            # print("this is the packet no: ", AckNumber)
            if SendBase <= AckNumber < SendBase + N:     
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

