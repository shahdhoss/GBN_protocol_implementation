from socket import *
from PIL import Image
import PIL
import io
from random import randint
import time
import matplotlib.pyplot as plt
from datetime import datetime

def get_packetid(packet):
    packet_id = packet[:2]
    return int.from_bytes(packet_id, byteorder='big')

def get_data(packet):
    data = packet[4:2044]
    return data

def get_trailing(packet):
    trailing = packet[2044:]
    return trailing

server_port = 1200
server_ip = 'localhost'
server_socket = socket(AF_INET, SOCK_DGRAM)
server_socket.bind((server_ip, server_port))
print("the server is ready to receive ")
data = []
packet_ids = []
variable = 0
received_times = []
received_packet_ids = []
lost_packets = []
start_time = None
end_time = None
total_bytes_received = 0
retransmissions = 0

N = 3  
while True:
    message, client_address = server_socket.recvfrom(2048)
    variable += 1
    packet_id = get_packetid(message)
    
    if len(packet_ids) == 0:
        start_time = time.time()  
        packet_ids.append(packet_id)
        
    if int(packet_id) == int(packet_ids[-1]) + 1 or len(packet_ids) == 1:
        if len(packet_ids) == 0:
            continue
        
        # Simulate packet loss
        drop_probability = randint(1, 100)
        if drop_probability >= 5 and drop_probability <= 15:
            print(f"Packet {packet_id} dropped (simulated)")
            if packet_id == packet_ids[0]:
                packet_ids = []
                lost_packets.append(packet_id)
            retransmissions += 1
            continue
        else:
            packet_ids.append(packet_id)
            server_socket.sendto(packet_ids[-1].to_bytes(2, byteorder='big'), client_address)  # sending ack
            print("packet id:(ack): ", packet_ids[-1])
            hour_time_of_sending = datetime.now().hour
            minute_time_of_sending = datetime.now().minute
            second_time_of_sending = datetime.now().second
            print(f"Packet received at: {hour_time_of_sending}:{minute_time_of_sending}:{second_time_of_sending}")
            trailing = get_trailing(message)
            message = get_data(message)
            data.append(message)
            total_bytes_received += len(message)
            received_times.append(time.time())
            received_packet_ids.append(packet_id)
            
            if trailing == b'':
                end_time = time.time() 
                image_bytes = b''
                for i in range(len(data)):
                    image_bytes += data[i]
                with open('sent_image.jpeg', 'wb') as file:
                    file.write(image_bytes)
                try:
                    with open('sent_image.jpeg', 'rb') as file:
                        binary_stream = io.BytesIO(file.read())
                        image = Image.open(file)
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
        server_socket.sendto(packet_ids[-1].to_bytes(2, byteorder='big'), client_address)  # sending ack

        lost_packets.append(packet_ids[-1])  
        retransmissions += 1

plt.figure(figsize=(8, 6)) 
plt.scatter(received_times, received_packet_ids, label='Received Packets', color='blue')


for lost_packet_id in lost_packets:
    for i, received_packet_id in enumerate(received_packet_ids):
        if lost_packet_id == received_packet_id:
            plt.scatter(received_times[i], lost_packet_id, color='red', marker='x')
            break

plt.xlabel('Time')
plt.ylabel('Packet ID')
plt.title('Received Packet ID vs. Time')

elapsed_time = end_time - start_time
num_packets = len(received_packet_ids)
average_transfer_rate_bytes = total_bytes_received / elapsed_time
average_transfer_rate_packets = num_packets / elapsed_time

transfer_stats = f"Start Time:\t{datetime.fromtimestamp(start_time)}\t" \
                 f"End Time:\t{datetime.fromtimestamp(end_time)}\t" \
                 f"Elapsed Time:\t{elapsed_time:.2f} sec\t" \
                 f"Num. of Packets:\t{num_packets}\t" \
                 f"Num. of Bytes:\t{total_bytes_received}\t" \
                 f"Num. of Retrans.:\t{retransmissions}\t" \
                 f"Avg. Transfer Rate (Bytes/sec):\t{average_transfer_rate_bytes:.2f}\t" \
                 f"Avg. Transfer Rate (Pkts/sec):\t{average_transfer_rate_packets:.2f}"

# plt.text(0.02, -0.1, transfer_stats, fontsize=8, transform=plt.gca().transAxes, horizontalalignment='left', verticalalignment='top', multialignment='left')

plt.grid(True)
plt.tight_layout()  
plt.show()
