from socket import *

sourcePort = 12000
serverName = "localhost"
serverSocket = socket(AF_INET, SOCK_DGRAM)

try:
    serverSocket.bind((serverName, sourcePort))
    print('The server is ready to receive.')
    while True:
        message, clientAddress = serverSocket.recvfrom(2048)
        modifiedMessage = message.decode().upper()
        print(modifiedMessage)
        serverSocket.sendto(modifiedMessage.encode(), clientAddress)

finally:
    serverSocket.close()
