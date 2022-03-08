'''
Jay Derderian
CS 594

Client module. 

Handles front end of client application, user message input, and communicates with the server.
'''

import socket
import threading

from ui.tui import (
    TUI, supports_color, app_info
)
from info import APP_INFO, CLIENT_COMMANDS


### Constants ###
HOST = socket.gethostname()
PORT = 5050
ADDR = (HOST, PORT)
BUFFER_MAX = 2048
CLIENT_INFO = {
    "Name": '',          # client user name
    "Address": ADDR,     # (host, port)
}

#### TUI ####

# This checks whether a given terminal can display colors
SUPPORTS_COLOR = False
if supports_color():
    TEXT_UI = TUI()
    SUPPORTS_COLOR = True

# messaging functionality
def message():
    '''
    handles client messages sent tot he server. 
    runs in its own thread.
    '''
    while True:
        # get message from user. 
        message = input()
        # print()

        # display local help menu
        if message.split()[0]=='/help':
            show_commands()
        
        # disconnect from server and exit application.
        elif message.split()[0] == '/quit':
            print('\n***Disconnecting!***')
            SOCKET.shutdown(socket.SHUT_RDWR)
            SOCKET.close()
            exit()

        # send to server
        else:
            if SUPPORTS_COLOR and message.split()[0] == '/join':
                # assign a color to this room if we're joining a new one
                for word in message.split():
                    if word[0] == '#':
                        TEXT_UI.assign_colors(word)
            SOCKET.send(message.encode('ascii'))

# main client program
def run_client():
    '''
    main client method for application. handles messages from the server

    runs in its own thread.
    '''
    # main communication loop
    while True:
        try: 
            # listen for messages from the server
            message = SOCKET.recv(BUFFER_MAX).decode('ascii')

            # case where it's our first connection
            if message == 'Connected to server':
                # CLIENT_INFO['Rooms'].append('#lobby')
                if SUPPORTS_COLOR:
                    TEXT_UI.assign_colors('#lobby')
                # send user name as the first message.
                SOCKET.send(CLIENT_INFO["Name"].encode('ascii'))

            # case where the server shuts down
            elif not message:
                if SUPPORTS_COLOR:
                    TEXT_UI.shut_down_message('SERVER OFFLINE! Closing connection...')
                else:
                    print('\nSERVER OFFLINE! Closing connection...')
                SOCKET.close()
                break
            # otherwise its some other message
            else:
                # get any room names, assign colors as needed, then display
                if SUPPORTS_COLOR:
                    TEXT_UI.display(message)
                else:
                    print(message)

        # case where there's a problem with the server
        except ConnectionResetError:
            pass

# display available commands
def show_commands():
    ''''
    display available commands
    '''
    for key in CLIENT_COMMANDS:
        print(CLIENT_COMMANDS[key])

# # get room names from server
# def check_for_rooms(message):
#     # find room names
#     message_ = message.split()
#     for word in message_:
#         # make sure this is a room name and not just an acknowledgement that we've 
#         # joinded a room. 
#         if word[0] == '#' and word[-1] != '!' and word not in CLIENT_INFO['Rooms']:
#             CLIENT_INFO['Rooms'].append(word)
#         if SUPPORTS_COLOR:
#             # randomly assign a room name color and background color
#             TEXT_UI.assign_colors(message) 


######## DRIVER CODE #########
if __name__ == '__main__':

    ### START UP ###
    app_info(APP_INFO)                                 # display welcome message
    CLIENT_INFO["Name"] = input('Enter username > ')   # get the username

    # Create a new socket using IPv4 address familty (AF_INET) and TCP protocol (SOCK_STREAM)
    SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # attempt to contact server
    print('\nConnecting to server...')    
    try:
        # send initial message (the username) to server
        SOCKET.connect(CLIENT_INFO['Address'])
        if SUPPORTS_COLOR:
            TEXT_UI.connected_message('Connected!')
            print(f'Host: {CLIENT_INFO["Address"][0]}, Port: {CLIENT_INFO["Address"][1]}\n')
        else:
            print(f'...Connected to server at host: {CLIENT_INFO["Address"][0]}, port: {CLIENT_INFO["Address"][1]}\n')
        
        ### MAIN THREADS ###
        rt = threading.Thread(name='receive thread', target=run_client)
        wt = threading.Thread(name='write thread', target=message)
        rt.start()
        wt.start()
        # this continually checks to make sure each thread is running. 
        # its janky af and probably really silly, but it seems to 
        # handle thread exceptions when the client shuts down using the
        # /quit command
        try:
            while rt.is_alive() and wt.is_alive():
                pass
        except threading.ThreadError:
            exit()

    except:
        if SUPPORTS_COLOR:
            TEXT_UI.error_messages('Unable to connect!')
        else:
            print('...Unable to connect!')
        try:
            SOCKET.shutdown(socket.SHUT_RDWR)
            SOCKET.close()
            exit()
        except:
            exit()