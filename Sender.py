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
    return Data
    #print(Data)

def make_packets(flag, packet_id, data, file_id):
    packet_id = packet_id.to_bytes(2, byteorder='big').decode()  
    file_id = file_id.to_bytes(2, byteorder='big').decode() 
    if flag:  
        trailer_bits = 0xFFFF   #lesa mwselnash l2a5er packet 
    else:    
        trailer_bits = 0x0000
    trailer_bits = trailer_bits.to_bytes(2, byteorder='big').decode()  
    Packet = file_id + packet_id+trailer_bits + data.decode() 
    return Packet

def send_to_receiver(packets, ip_address, port):
    SenderSocket = socket(AF_INET, SOCK_DGRAM)
    for i in packets:
        SenderSocket.sendto(packets, (ip_address, port))
    SenderSocket.close()

def sender(filee, receiver_port, ip_address):
    Packets = read(filee)
    SenderSocket = socket(AF_INET, SOCK_DGRAM) 
    PacketLength = len(Packets)
    SendBase = 0
    Timer = False
    for NextSeqNum in range(SendBase, min(SendBase + N, PacketLength)):   #to ensure enna ma3adenash size el packets
         #Makepacket ->it adds (sequence number,checksums,headers)
        # yb3at tany el packets elli ma7asalahash ack
        Packet = make_packets(NextSeqNum == PacketLength - 1, NextSeqNum, Packets[NextSeqNum], 1) #awl goz2 ensure en a5er packet wslet
        SenderSocket.sendto(Packet.encode(), (ip_address, receiver_port))  # Encode packet to bytes before sending
        print(f"Packet {NextSeqNum} sent..")
        if not Timer:  
            StartTime = time.time()
            Timer = True
        while True:
            if time.time() - StartTime >= 5:  
                print("Timeout !! The unacknowledged packets will be sent again..")
                NextSeqNum = SendBase
                Timer= False  #reset el timer
                break
            else:
                try:
                    AckPacket, _ = SenderSocket.recvfrom(1024)   #return tuple -> data + address of the sender - me7adgin awl wa7ed bs
                    AckNumber = int.from_bytes(AckPacket[:2], byteorder='big')  
                    if SendBase<=AckNumber:  
                        SendBase = AckNumber + 1 
                        Timer = False 
                except timeout:  
                    continue

    print("Packets are sent successfully!")
    SenderSocket.close()

filee = 'Computer Networks Project/small file.jpeg'
sender(filee, ReceiverPort, ReceiverIp)
