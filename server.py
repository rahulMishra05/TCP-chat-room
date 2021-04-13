# Importing modules
import threading
import socket


# Localhost because we want to use it on our local machine
host = '127.0.0.1'

# Port number, remember do not choose reserved port.
port = 55555

# Starting the servcie
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()     # By this server start listning for the new incomming connections

# Client list to put the detail of clients connected, and nickname list to put the name of the cilents connected.
clients = []
nicknames = []


def broadcast(message):
    ''' This function will send message to all the clients presnt in the "clinets" list '''
    for client in clients:
        client.send(message)


def handle(client):
    '''
    This function will constantly try to recive message from the client, but if the client fails to send the message than in that 
    case it will cut the connection, and remove the client from the clients list and name from the nicknames list
    Note: This will not give to an error when clinet is not sending something, but give you error when he/she is unable to send
    '''
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]

            # Showing a message to all the other clinets that this client is offline
            broadcast(f'[X] {nickname} left the chat...'.encode('ascii'))
            nicknames.remove(nickname)
            break 


def receive():
    '''This method is the main method'''
    while True:
        client, address = server.accept()       # By this server is accepting client all the time
        print(f'[+] Successfully connected to {str(address)}...')

        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        print(f'[+] Nickname of the client is {nickname}')
        broadcast(f'[+] {nickname} joined the chat...'.encode('ascii'))
        print("/n")
        client.send("[+] Connected to the server...".encode('ascii'))

        # Definig a thread and run a thread. We will run one thread for each client so that they can run simultaneously
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


print(f'Server is listning on port number {port} and address {str(host)}')
# Calling the function
receive()
