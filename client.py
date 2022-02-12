'''
Jay Derderian
CS 594

Client module. 

Handles front end of client application, user message input, 
and communicates with the server.
'''

import logging
import socket
import threading

from ui.ui import GUI
from ui.cli import CLI
from info import APP_INFO, CLIENT_COMMANDS


# Constants
HOST = socket.gethostname()
PORT = 5050
ADDR = (HOST, PORT)
BUFFER_MAX = 2048

TEXT_UI = CLI()
UI = GUI()

CLIENT_INFO = {
    "Name": '',       # client user name
    "Address": ADDR,  # (host, port)
    "Messages": []    # messsages sent during session
}

# Debugging stuff. Set DEBUG to true to activate logging.
DEBUG = False
if DEBUG:
    # start a log file for debugging
    logging.basicConfig(filename='IRC_Client.log', 
                        filemode='w', 
                        level=logging.DEBUG, 
                        format='%(asctime)s %(message)s', 
                        datefmt='%m/%d/%Y %I:%M:%S %p')


#----------------------------------START UP-----------------------------------------#

# display welcome message
TEXT_UI.app_info(APP_INFO)
# get the username
CLIENT_INFO["Name"] = input('Enter username > ')

# Create a new socket using IPv4 address familty (AF_INET) and TCP protocol (SOCK_STREAM)
SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# attempt to contact server
print('\nConnecting to server...')    
try:
    # send initial message (the username) to server
    SOCKET.connect(CLIENT_INFO['Address'])
    if DEBUG:
        logging.info(f'Connected to server at host: {CLIENT_INFO["Address"][0]}, port: {CLIENT_INFO["Address"][1]}')
    print(f'...Connected to server at host: {CLIENT_INFO["Address"][0]}, port: {CLIENT_INFO["Address"][1]}\n')
except:
    print('...Could not connect!')
    if DEBUG:
        logging.info(f'Could not connect to server!')
    SOCKET.close()


#-------------------------------CLIENT METHODS--------------------------------------#


# display available commands
def show_commands():
    ''''
    display available commands and how to join/leave rooms 
    '''
    for key in CLIENT_COMMANDS:
        print(CLIENT_COMMANDS[key])


# messaging functionality
def message():
    '''
    handles client messages
    '''
    while True:
        # this isn't great but it's working for now...
        # make sure room name is displayed too, after selecting /join!
        try:
            message = input(f'{CLIENT_INFO["Name"]} > ')
        except KeyError:
            ...
        # display local help menu
        if message.split()[0]=='/help':
            show_commands()
        # exit
        elif message.split()[0] == '/quit':
            print('\n***Disconnecting!***')
            if DEBUG:
                logging.info('Disconnecting from server!')
            SOCKET.close()
        # otherwise, send to server 
        if DEBUG:
            logging.info(f'Sending message: {message}')
        SOCKET.send(message.encode('ascii'))


# main client program
def run_client():
    '''
    main client method for application. 
    handles message I/O and shuts down if a server disconnects.
    '''
    # main communication loop
    while True:
        try:
            # listen for messages from the server
            # FORMAT 
            message = SOCKET.recv(BUFFER_MAX).decode('ascii')
            # case where it's our first connection
            if message == 'Connected to server':
                if DEBUG:
                    logging.info(f'Connected to server!')
                # send user name as the first message.
                SOCKET.send(CLIENT_INFO["Name"].encode('ascii'))
            # otherwise its some other message
            else:
                if DEBUG:
                    logging.info(f'Received a message: {message}')
                # display(message)
                print(message)
        # case where the server shuts down
        except:
            if DEBUG:
                logging.info('Closing connection...')
            # display('SERVER OFFLINE! Closing connection...')
            print('\nClosing connection...')
            SOCKET.close() 
            break


# message parser to use with CLI
def display(fg:str, bg:str, message:str):
    '''
    this parses a message string and applies the CLI to individual elements.

    fg = foreground color
    bg = background color
    message = str

    message format from app - f'{room.name} : {name} > {message}'
    room name and username should be separate colors
    '''
    ...


#----------------------------------------------------------------------------#

# driver code
receive_thread = threading.Thread(target=run_client)
write_thread = threading.Thread(target=message)
receive_thread.start()
write_thread.start()