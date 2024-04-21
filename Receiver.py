from socket import *
def get_packetid(packet):
    packet_id=packet[:16]
    return int.from_bytes(packet_id, byteorder='big')
def get_data(packet):
    data=packet[32:2016]
    return data[2:]
def get_trailing(packet):
    trailing=packet[2016:]
    return trailing[2:]
server_port=12000
server_socket= socket(AF_INET, SOCK_DGRAM)
server_socket.bind(("",server_port))
print("the server is ready to recieve ")
data=[]
packet_ids=[]
variable=0
while True:
    print(variable)
    message, client_address= server_socket.recvfrom(2048)
    variable=variable+1
    packet_id=get_packetid(message)
    # print(packet_id)
    packet_ids.append(str(packet_id))
    if int(packet_id)==int(packet_ids[-1])+1 or len(packet_ids)==1 :         #making sure that its the right packet, before saving its data. Knowing that packetids are numbers in sequence
        server_socket.sendto(packet_ids[-1].encode(),client_address) #sending ack
        packet_ids.append(packet_id)
        trailing=get_trailing(message)
        message=get_data(message)
        data.append(message)
        if(trailing=='0xFFFF'):
            image_bytes=''
            for i in range(len(data)):
                image_bytes=image_bytes+data[i]
            file=open('sent_image.jpeg')
            file.write()
            file.close()
    else:
        server_socket.sendto(packet_ids[-1].encode(),client_address)   #sending ack
    server_socket.close() #will make sure if i'm allowed to close while packets are still being sent once the program is running