# Importing modules
import threading
import socket


nickname = input("[+] Please enter you nickname: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 55555))


def receive():
    ''' This is a endless loop, to receive message until the connection is closed'''
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
            else:
                print(message)
        except:
            print("[X] An error occurred!!")
            client.close()
            break 


def write():
    '''This is also a end less loop, it constantly asks the user to enter message'''
    while True:
        message = f'{nickname}: {input("")}'
        client.send(message.encode('ascii'))


# Now we need to run two threads.
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()