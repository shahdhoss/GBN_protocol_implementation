from socket import *
from PIL import Image
import PIL
import io
from random import randint
import time
import matplotlib.pyplot as plt
from datetime import datetime

def get_packetid(packet):
    packet_id=packet[:2]
    return int.from_bytes(packet_id, byteorder='big')
def get_data(packet):
    data=packet[4:2044]
    return data
def get_trailing(packet):
    trailing=packet[2044:]
    return trailing
server_port=1200
server_ip='localhost'
server_socket= socket(AF_INET, SOCK_DGRAM)
server_socket.bind((server_ip,server_port))
print("the server is ready to recieve ")
data=[]
packet_ids=[]
variable=0
received_times = []
received_packet_ids = []
lost_packets = []

# retransmitted_packet_ids = []

N=3  #window size
while True:
    message, client_address = server_socket.recvfrom(2048)
    variable=variable+1
    packet_id=get_packetid(message)
    if len(packet_ids)==0:
        packet_ids.append(packet_id)
    if int(packet_id)==int(packet_ids[-1]) + 1 or len(packet_ids)==1 :         #making sure that its the right packet, before saving its data. Knowing that packetids are numbers in sequence
        if len(packet_ids)==0:
            continue
        # Simulate packet loss
        drop_probability = randint(1, 100)
        if drop_probability >= 5 and drop_probability <= 15:
            print(f"Packet {packet_id} dropped (simulated)")
            if packet_id==packet_ids[0]:
                packet_ids=[]
                lost_packets.append(packet_id)
            continue
        else:
            packet_ids.append(packet_id)
            server_socket.sendto(packet_ids[-1].to_bytes(2,byteorder='big'),client_address)     #sending ack
            print("packet id:(ack): ",packet_ids[-1])
            hour_time_of_sending= datetime.now().hour
            minute_time_of_sending= datetime.now().minute
            second_time_of_sending =datetime.now().second
            print(f"Packet recieved at: {hour_time_of_sending}:{minute_time_of_sending}:{second_time_of_sending}")
            trailing=get_trailing(message)
            message=get_data(message)
            data.append(message)

            received_times.append(time.time())
            received_packet_ids.append(packet_id)
            if(trailing== b''):
                image_bytes= b''
                print("image bytes type: ",type(image_bytes))
                print("image bytes type: ",type(data))
                for i in range(len(data)):
                    image_bytes=image_bytes+data[i]
                with open('sent_image.jpeg', 'wb') as file:
                    file.write(image_bytes)
                try:
                    with open('sent_image.jpeg', 'rb') as file:  
                        binary_stream = io.BytesIO(file.read())
                        image=Image.open(file)
                        image.show()
                    print("Image file 'sent_image.jpeg' has been created successfully.")
                except PIL.UnidentifiedImageError:
                    print("Error: Unable to identify the image file. Make sure the file contains valid image data.")
                except FileNotFoundError:
                    print("Error: File 'sent_image.jpeg' not found.")
                except Exception as e:
                    print("An unexpected error occurred:", e)
                break
    else:
        server_socket.sendto(packet_ids[-1].to_bytes(2,byteorder='big'),client_address)   #sending ack


plt.figure()
plt.scatter(received_times, received_packet_ids, label='Received Packets', color='blue')
plt.xlabel('Time')
plt.ylabel('Packet ID')
plt.title('Received Packet ID vs. Time')
plt.legend()
plt.grid(True)
plt.show()
