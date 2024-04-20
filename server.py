from socket import *
serverIP ="192.168.219.236"
serverPort = 12000
clientSocket =socket(AF_INET,SOCK_DGRAM)
message = input('Enter message')
clientSocket.sendto(message,(serverIP,serverPort))
modifiedMessage.serverAddress = clientSocket.revfrom()
print(modifiedMessage.decode())
clientSocket.close()
