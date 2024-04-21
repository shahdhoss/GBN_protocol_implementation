def sender(filee, receiver_port, ip_address):
#     Packets = read(filee)
#     SenderSocket = socket(AF_INET, SOCK_DGRAM) 
#     PacketLength = len(Packets)
#     SendBase = 0
#     Timer = False
#     for NextSeqNum in range(SendBase, min(SendBase + N, PacketLength)):   #to ensure enna ma3adenash size el packets
#          #Makepacket ->it adds (sequence number,checksums,headers)
#         # yb3at tany el packets elli ma7asalahash ack
#         Packet = make_packets(NextSeqNum == PacketLength - 1, NextSeqNum, Packets[NextSeqNum], 1) #awl goz2 ensure en a5er packet wslet
#         SenderSocket.sendto(Packet.encode(), (ip_address, receiver_port))  # Encode packet to bytes before sending
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
#                     AckPacket, _ = SenderSocket.recvfrom(1024)   #return tuple -> data + address of the sender - me7adgin awl wa7ed bs
#                     AckNumber = int.from_bytes(AckPacket[:2], byteorder='big')  
#                     if SendBase<=AckNumber:  #'<'3lshan momken yb3at nafs el packet kaza mara
#                         SendBase = AckNumber + 1 
#                         Timer = False 
#                 except timeout:  
#                     continue

#     print("Packets are sent successfully!")
#     SenderSocket.close()


# sender(filee, ReceiverPort, ReceiverIp)
