from socket import *
def get_packetid(packet):
    packet_id=packet[:2]
    return int.from_bytes(packet_id, byteorder='big')
def get_data(packet):
    data=packet[4:2044]
    data_tostring=str(data).strip("b'")
    # print("length of the data in bytes: ", len(data_tostring))
    return data_tostring
def get_trailing(packet):
    trailing=packet[2044:]
    trailing_tostring=str(trailing).strip("b'")
    # print("length of the trailing part: ", len(trailing_tostring.encode()))
    return trailing_tostring
server_port=1200
server_socket= socket(AF_INET, SOCK_DGRAM)
server_socket.bind(("",server_port))
print("the server is ready to recieve ")
data=[]
packet_ids=[]
variable=0
while True:
    print(variable)
    message, client_address = server_socket.recvfrom(2048)
    variable=variable+1
    packet_id=get_packetid(message)
    print("this is the packet id:", packet_id)
    if len(packet_ids)==0:
        packet_ids.append(str(packet_id))
    if int(packet_id)==int(packet_ids[-1])+1 or len(packet_ids)==1 :         #making sure that its the right packet, before saving its data. Knowing that packetids are numbers in sequence
        if len(packet_ids)==0:
            continue
        else:
            packet_ids.append(str(packet_id))
        server_socket.sendto(packet_ids[-1].encode(),client_address) #sending ack
        packet_ids.append(packet_id)
        trailing=get_trailing(message)
        print("this is the trailing: ", trailing)
        message=get_data(message)
        print("this is the data: ",message)
        data.append(message)
        # print("the list of all data segments: ",data)
        if(trailing=='0xFFFF'):
            image_bytes=''
            for i in range(len(data)):
                image_bytes=image_bytes+data[i]
            file=open('sent_image.jpeg')
            file.write()
    else:
        server_socket.sendto(packet_ids[-1].encode(),client_address)   #sending ack
