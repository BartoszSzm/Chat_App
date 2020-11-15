import socket
import threading

HOST = '' #Type your public IP here or localhost (chat will work only over your local network)
PORT = 5555

#Create socket, start server and set it to listen incomming connections
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((HOST,PORT))
print(f'Server is starting...')
server.listen()

#Globals holding nicknames of connected users and their connections data
clients = []
nicknames = []

#Send message to all connected clients
def broadcast(message):
    for client in clients:
        client.send(message)

#Handle single connection
#Try recieve message from client and broadcast over chat room
#When exception occured or disconnect message recieved - remove client from globals        
def handle(client):
    while True:
        try:
            message = client.recv(1024)
            if '!DISCONNECT' in message.decode('cp852'):
                client.send('!DISCONNECT'.encode('cp852'))
                raise Exception
            else:
                broadcast(message)       
        except:
            index = clients.index(client)
            clients.remove(client)
            nickname = nicknames[index]
            broadcast(f'{nickname} disconnected from chat!'.encode('cp852'))
            print(f'{nickname} disconnected from chat!')
            nicknames.remove(nickname)
 
#Accept incomming connection, ask for nickname
#Add connection data and nickname to globals   
def recieve():
    while True:
        client, address = server.accept()
        print(f'Connected with adress {address}')
        client.send('NICK'.encode('cp852'))
        nickname = client.recv(1024).decode('cp852')
        nicknames.append(nickname)
        clients.append(client)
        print(f'{nickname} connected to the chat!')
        broadcast(f'{nickname} connected to the chat!'.encode('cp852'))
        #Run thread
        thread2 = threading.Thread(target=handle, args=(client,))
        thread2.start()

#Start server
thread1 = threading.Thread(target=recieve)
thread1.start()
        
        
        
        
    