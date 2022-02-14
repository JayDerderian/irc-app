'''
Jay Derderian
CS 594

Server module. Also runs main IRC application (app.py).
'''
import logging
import socket
import threading

from app import IRC_Application, Chatroom

# Constants
HOST = socket.gethostname()
PORT = 5050
ADDR = (HOST, PORT)
BUFFER_MAX = 2048
CLIENT_MAX = 10
DEFAULT_ROOM_NAME = '#main'

SERVER_INFO = {
    "Sockets": [],  # list of client_socket objects
    "Users": [],    # list of tuples (client_socket object, client_username)
}

# Debugging stuff. Set DEBUG to True to activate logging.
DEBUG = False
if DEBUG:
    # start a log file for debugging
    logging.basicConfig(filename='IRC_Server.log', 
                        filemode='w', 
                        level=logging.DEBUG, 
                        format='%(asctime)s %(message)s', 
                        datefmt='%m/%d/%Y %I:%M:%S %p')

# Application and Chatroom instances
APP = IRC_Application()
default_room = Chatroom(room_name=DEFAULT_ROOM_NAME)
APP.rooms[DEFAULT_ROOM_NAME] = default_room

#-------------------------START UP----------------------------------#

# Create a new socket using IPv4 address familty (AF_INET),
# and the TCP protocol (SOCK_STREAM)
print('\n***starting server***')
SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SOCKET.bind(ADDR)
print(f'\n...bound at host: {ADDR[0]}, port:{ADDR[1]}...')
print('...listening...\n')
SOCKET.listen(CLIENT_MAX)              # how many clients do we need to listen for?
if DEBUG:
    logging.info(f'SERVER STARTED \nHost: {HOST}, Port: {PORT}')

#-------------------------------------------------------------------#

def broadcast_to_all(message):
    '''
    NOTE: modify IRC app to do this for the room the user is in!
          this just broadcasts to *everyone*
    '''
    for socket in SERVER_INFO['Sockets']:
        socket.send(message)


def run_server():
    '''
    runs communication loop
    '''
    while True:
        # allow clients to connect
        client, address = SOCKET.accept()
        if DEBUG:
            logging.info(f'Client connected! Address: {address}') 

        # new user!
        if client not in SERVER_INFO["Sockets"]:
            # confirm connection to new user, and broadcast to app
            if DEBUG:
                logging.info(f'Sending new client connection confirmation...')
            client.send(f'Connected to server'.encode('ascii'))

            # get user name since that's the first message
            new_user = client.recv(BUFFER_MAX).decode('ascii')
            if DEBUG:
                logging.info(f'New user - Name: {new_user},  Address:{address}')
            print(f'adding new socket and user name to SERVER_INFO: \nuser: {new_user} \nsocket object: {client} ')
            SERVER_INFO["Sockets"].append(client)
            SERVER_INFO["Users"].append((client, new_user)) # yes, i know clients are being saved twice

            # alert new connection via the terminal
            print(f'...new user connected! name: {new_user}, addr: {str(address)}\n')

            # add user to default room
            APP.rooms[DEFAULT_ROOM_NAME].add_new_client_to_chatroom(new_user, client)
            if DEBUG:
                logging.info(f'Created new chatroom {DEFAULT_ROOM_NAME}')
            print(f'...created new chatroom: {DEFAULT_ROOM_NAME}')

            # create a new thread for this client to handle message I/O
            thread = threading.Thread(target=handle, args=(client,))
            thread.start()

        # message from existing user
        else:
            message = client.recv(BUFFER_MAX).decode('ascii')
            if DEBUG:
                logging.info(f'Message recieved! \nSOCKET: {str(SERVER_INFO["Sockets"][client])} \nMESSAGE: {message}')
            print(message)
            # send to message parser
            APP.message_parse(client, find_user(client), message)


def handle(client):
    '''
    handles individual user I/O. operates on within its own thread.
    '''
    while True:
        # case where the server recieves a message 
        # from an existing client
        try:
            message = client.recv(BUFFER_MAX).decode('ascii')
            # search user list for the username associated with this client
            user = find_user(client)
            if DEBUG:
                logging.info(f'server.hande() - Message from {user}\n Message: {message}')
            print(f'{user}: {message}')
            # parse message in app
            APP.message_parse(client, find_user(client), message)

        # case where a user disconnects
        except:
            print("\n***USER DISCONNECT***")
            # search user list for the username associated with this client
            user = find_user(client)
            # search for and remove user from chatroom if they disconnect
            for room in APP.rooms:
                if client in APP.rooms[room].client_sockets:
                    APP.rooms[room].remove_client_from_chatroom(user, client)

            SERVER_INFO["Sockets"].remove(client)
            SERVER_INFO["Users"].remove((client, user))
            '''
            NOTE: broadcast within app to the room the user was in
            '''
            print(f'{user} left the server!\n')
            if DEBUG:
                logging.info(f'{user} left the server! \nsocket: {str(SERVER_INFO["Sockets"].index(client))}\n')
            client.close()
            break


def find_user(client):
    '''
    finds a user_name associated with a client socket object.

    client = client socket() object
    
    returns: user_name (str)
    '''
    user_list = SERVER_INFO["Users"]
    index = [i for i, user_list in enumerate(user_list) if user_list[0] == client]
    return SERVER_INFO["Users"][index[0]][1]


#------------------------------------------------------------------------------------#

# driver code
if __name__ == '__main__':
    run_server()
