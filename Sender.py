import socket
import time
from datetime import datetime

ReceiverIp = 'localhost'
ReceiverPort = 1200
MSS = 2040  # Maximum segment size
N = 3  # Window size - how many unacknowledged packets can be in transit at any given time

def get_packetid(packet):
    packet_id = packet[:2]
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

filee = 'Computer Networks Project/medium file.jpeg'

def make_packets(flag, packet_id, data, file_id):
    packet_id = packet_id.to_bytes(2, byteorder='big')
    file_id = file_id.to_bytes(2, byteorder='big')
    if flag:
        trailer_bits = 0xFFFF  # Indicates the last packet
    else:
        trailer_bits = 0x0000
    trailer_bits = trailer_bits.to_bytes(4, byteorder='big')
    Packet = packet_id + file_id + data + trailer_bits
    return Packet

def resend(NextSeqNum, receiver_port, ip_address):
    Packets = read(filee)
    SenderSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    PacketLength = len(Packets)
    Packet = make_packets(NextSeqNum == PacketLength - 1, NextSeqNum, Packets[NextSeqNum], 1)
    SenderSocket.sendto(Packet, (ip_address, receiver_port))
    print(f"Packet {NextSeqNum} resent..")
    hour_time_of_sending = datetime.now().hour
    minute_time_of_sending = datetime.now().minute
    second_time_of_sending = datetime.now().second
    print(f"Packet sent at: {hour_time_of_sending}:{minute_time_of_sending}:{second_time_of_sending}")

def sender(filee, receiver_port, ip_address):
    Packets = read(filee)
    SenderSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    SenderSocket.settimeout(5)  # Set a timeout for the socket to handle retransmissions
    PacketLength = len(Packets)
    SendBase = 0
    NextSeqNum = 0
    Timer = False
    StartTime = None

    while SendBase < PacketLength:
        while NextSeqNum < SendBase + N and NextSeqNum < PacketLength:
            Packet = make_packets(NextSeqNum == PacketLength - 1, NextSeqNum, Packets[NextSeqNum], 1)
            print("This is the packet ID inside the while loop: ", get_packetid(Packet))
            SenderSocket.sendto(Packet, (ip_address, receiver_port))
            print(f"Packet {NextSeqNum} sent..")
            hour_time_of_sending = datetime.now().hour
            minute_time_of_sending = datetime.now().minute
            second_time_of_sending = datetime.now().second
            print(f"Packet sent at: {hour_time_of_sending}:{minute_time_of_sending}:{second_time_of_sending}")
            if not Timer:
                StartTime = time.time()
                Timer = True
            NextSeqNum += 1

        try:
            AckPacket, _ = SenderSocket.recvfrom(2048)
            AckNumber = int.from_bytes(AckPacket, byteorder='big')
            if SendBase <= AckNumber < SendBase + N:
                SendBase = AckNumber + 1
                if SendBase == NextSeqNum:
                    Timer = False
                else:
                    StartTime = time.time()
                print("Acknowledgment received for packet", AckNumber)

        except socket.timeout:
            if Timer and time.time() - StartTime >= 5:
                print("Timeout! Retransmitting unacknowledged packets..")
                for i in range(SendBase, min(SendBase + N, PacketLength)):
                    Packet = make_packets(i == PacketLength - 1, i, Packets[i], 1)
                    SenderSocket.sendto(Packet, (ip_address, receiver_port))
                    print(f"Packet {i} retransmitted..")
                StartTime = time.time()  # Restart the timer after retransmitting

    print("Packets are sent successfully!")
    SenderSocket.close()

sender(filee, ReceiverPort, ReceiverIp)