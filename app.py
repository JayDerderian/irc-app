'''
Jay Derderian
CS 594

Application module - the core functionality of the IRC Chat program.

This handles tracking of clients and their associated sockets, sending
and recieving messages, message parsing, and other neccessary functionality.

There is also built-in debugging functionality using logs. 
Set DEBUG to true to turn on logging system.
'''

# Constants
DEFAULT_ROOM_NAME = '#lobby'

# Broadcast a message to the server and to all clients in that room
def message_broadcast(room, sender_name, message, sender_socket):
    '''
    sends a message to all the users in a Chatroom() instance

    parameters
    -----------
    - room = Chatroom() object
    - name = senders name (str)
    - socket = sender's socket (socket() object)
    - message = message string
    '''
    # Display message
    print(f'{sender_name} {room.name} > {message}\n')
    # Send the message to all clients in this room *except* the one that sent the messaage
    for client in room.clients:
        if room.clients[client] != sender_socket:
            client.send(f'{sender_name} {room.name} > {message}'.encode('ascii'))
        else:
            continue


# The container that has rooms, which have lists of clients
class IRC_App:
    '''
    The main IRC application. One default room - #lobby - is created when
    this class is instantiated. Irc_App() also keeps tracks of current users 
    and their socket info.

    Irc_App().message_parser(message:str) is the main point of entry for this
    application. All message strings recieved from the client should be sent 
    through here.
    '''
    def __init__(self):
        # Dictionary of active rooms. Key is room name, value is the Chatroom() object. 
        # This is initiated with a default #lobby room
        self.rooms = {}
        self.rooms[DEFAULT_ROOM_NAME] = Chatroom(room_name=DEFAULT_ROOM_NAME)  
        # Dictionary of active users (User() objects). Key is username, value is User() object
        self.users = {}

    # add a new user to the instance
    def add_user(self, user_name, new_user_socket):
        if user_name not in self.users.keys():
            self.users[user_name] = User(name=user_name, 
                                         socket=new_user_socket)
        else:
            print(f'{user_name} is already in the server!')

    # remove a user from the instance
    def remove_user(self, user_name):
        if user_name in self.users.keys():
            del self.users[user_name]
        else:
            print(f'{user_name} is not in the server!')
    
    # get a list of all active users
    def get_all_users(self):
        '''
        returns a list[str] of all active users in the instance.

        NOTE: Users can be found by searching each room via their names. Each room has a list
              of active clients. 
        '''
        ...

    # Function to create a space-separated list of rooms
    def list_all_rooms(self):
        '''
        returns a list of all active rooms.
        ---------
        room_list = list[str]
        '''
        return list(self.rooms.keys())
    

    def show_current_room(self, user_name, room):
        '''
        display name of current room
        '''
        ...
    
    def show_connection_info(self, user_name):
        '''
        show current client's name, and socket info.
        '''
        ...

    # Check if the room name begins with '#', check if user is already in the room,
    # create the room if it does not exist, then join the room the user specified
    def join_room(self, room_to_join, sender_name, sender_socket):
        '''
        parameters
        --------------
        - room_to_join = '#room_name'
        - sender_socket = sender socket() object
        - sender_name = ''
        '''
        ...

    # Create a new Chatroom, add the room to the room list, and add the client to the chatroom
    # A room cannot exist without a client, so one must be supplied
    def create_room(self, room_to_join, sender_name, sender_socket):
        '''
        parameters
        -------------
        - room_to_join = '#room_name
        - sender_socket = sender socket() object
        - sender_name = ''
        '''
        # create new Chatroom() instance
        new_room = Chatroom(room_name=room_to_join)
        # save to IRC_App instance
        self.rooms[room_to_join] = new_room
        self.rooms[room_to_join].add_new_client_to_chatroom(sender_name, sender_socket)
        # save info to Chatroom() instance
        new_room.client_sockets.append(sender_socket)
        new_room.clients[sender_name] = sender_socket

    # Check if the room exists, check if user is in the room,
    # remove user from room and delete room if it is empty
    def leave_room(self, room_to_leave, sender_name, sender_socket):
        '''
        parameters
        -------------
        - room_to_leave = '' (key for app.rooms dict)
        - sender_socket = sender socket() objet
        - sender_name = ''
        '''
        if room_to_leave not in self.rooms:
            sender_socket.send(f'Error: {room_to_leave} does not exist\n'.encode())
        elif sender_socket not in self.rooms[room_to_leave].client_sockets:
            sender_socket.send(f'Error: You are not in {room_to_leave}\n'.encode())
        else:
            self.rooms[room_to_leave].remove_client_from_chatroom(sender_name, sender_socket)
            # update user's location. 
            self.users[sender_name] = (DEFAULT_ROOM_NAME, sender_socket)
            # remove the room if it's empty
            if not self.rooms[room_to_leave].client_sockets:
                self.rooms.pop(room_to_leave)

    # Check if rooms exist, check if user is in room,
    # if room exists and user is in it then send message, otherwise skip
    def message_room(self, rooms_to_send, sender_socket, sender_name, message):
        '''
        parameters
        ------------
        - rooms_to_send = list[str] of '#room_name' or single room name (str)
        - sender_socket = sender socket() instance.
        - sender_name = string
        - message = string
        '''
        if type(rooms_to_send) == list:
            for room in rooms_to_send:
                if room not in self.rooms:
                    sender_socket.send(f'Error: {room} does not exist\n'.encode())
                    continue
                if sender_socket not in self.rooms[room].client_sockets:
                    sender_socket.send(f'Error: You are not in {room}\n'.encode())
                    continue
                message_broadcast(room, sender_name, sender_socket, message)
        elif type(rooms_to_send) == str:
            if rooms_to_send not in self.rooms.keys():
                sender_socket.send(f'Error: {room} does not exist\n'.encode())
            if sender_socket not in self.rooms[rooms_to_send].client_sockets:
                sender_socket.send(f'Error: You are not in {room}\n'.encode())
            else:
                message_broadcast(room, sender_name, sender_socket, message)

    # main message parser.
    def message_parser(self, message, sender_name, sender_socket):
        '''
        top-level entry for client messages to the application. 

        parameters 
        -----------
        - sender_socket = sender socket() object
        - sender_name = ''
        - message = ''

        message strings are split into word lists, then parsed accordingly.

        messages should, by default, go out the room the user is currently in.
        no need for a #room_name specification. typical syntax should be:

        user_name #room > <message>

        #lobby is the default room that any user can be in at any given time, 
        and is the one new users are sent to by default.

        splits message into individual word list and checks each element, 
        then executes action accordingly. 

        commands
        ----------
        - /join #room_name
            - join a chatroom. a new one will be created if it doesn't already exist.
        - /leave #room_name
            - leave current room. if you are in the main lobby, you will be asked if you 
            want to exit. if yes, then client will terminate.
        - /list (opt) #room_name. 
            - will list all members active in the application by default. 
            - you can also specifiy n number of rooms to get user lists, assuming those rooms exist. 
            - if not, it will be skipped and the user will be notified of its non-existance.
        - /message <user>
            - send a direct message to another user, regardless if they're in the same room with you.
        - /block <user>
            - block DM's from other users
        - /unblock <user>
            - unblocks a user
        - /help
            - displays a list of available commands
        - /quit
            - leave current instance.

        NOTE: /quit and /help are handled on the client side!

        NOTE: maybe simplify so we don't have to use /send to send a message to the current room?
              just have the current room displayed next to the user_name then send to all members in that room

        NOTE: Will need to coordinate with the CLI instance on the Client application!
        '''
        
        '''TEST OUTPUT'''
        print(f"\napp.message_parse() \nsender sock: {sender_socket} \nsender_name: {sender_name} \nmessage: {message}")
        print(f'message as word list: {message.split()}')

        # send to default room 
        if message[0] != '/':
            message_broadcast(self.rooms[DEFAULT_ROOM_NAME], sender_name, sender_socket, message)

        # Case where user wants to join a room:
        elif message.split()[0] == "/join":
            if len(message.strip().split()) < 2:
                sender_socket.send("/join requires a #room_name argument.\nPlease enter: /join #roomname\n".encode('ascii'))
            else:
                self.join_room(message.split()[1], sender_name, sender_socket)

        # Case where user wants to leave a room:
        elif message.split()[0] == "/leave":
            if len(message.strip().split()) < 2:
                sender_socket.send("/leave requires a #roomname argument.\nPlease enter: /leave #roomname\n".encode('ascii'))
            else:
                room_to_leave = message.strip().split()[1]
                if room_to_leave[0] != "#":
                    sender_socket.send("/leave requires a #roomname argument to begin with '#'.\n".encode('ascii'))
                else:
                    self.leave_room(room_to_leave, sender_name, sender_socket)
                    # send back to #main
                    if DEFAULT_ROOM_NAME in self.rooms.keys():
                        sender_socket.send(f'Rejoining {DEFAULT_ROOM_NAME}...\n'.encode('ascii'))
                        self.join_room(DEFAULT_ROOM_NAME,  sender_name, sender_socket)
                    # create it if it's not there for some reason...
                    else:
                        sender_socket.send(f'Rejoining {DEFAULT_ROOM_NAME}...\n'.encode('ascii'))
                        self.create_room(DEFAULT_ROOM_NAME, sender_name, sender_socket)


        # Case where user wants to list all (or some) active members in the app
        # elif message.split()[0] == "/list"


        # Case where user wants to directly message another user    
        # elif message.split()[0] == "/message":


        # Case where user wants to block DM's from another user
        # elif message.split()[0] == "/block":


        # Case where user wants to un-block another user.
        # elif message.split()[] == "/unblock":


class Chatroom:

    def __init__(self, room_name, text_color=None):
        self.name = room_name
        self.text_color = text_color
        # A dictionary of clients with username as the key and the socket as the value 
        self.clients = {}  

    # Adds a new client to a chatroom and notifies clients in that room
    def add_new_client_to_room(self, client_name, new_socket):
        print(f'\nadding {client_name} to {self.name}')
        self.clients[client_name] = new_socket
        message = f"{client_name} has joined the room!\n"
        message_broadcast(self, client_name, new_socket, message)

    # Removes an existing client from a chatroom and notifies the clients in that room
    def remove_client_from_room(self, client_name, client_socket):
        print(f'\nremoving {client_name} from {self.name}')
        self.clients.pop(client_name)
        message = f"{client_name} has left the room!\n"
        message_broadcast(self, client_name, client_socket, message)

    # returns a list of current users in this room as a string.
    def list_clients_in_room(self):
        return str([key for key in self.clients])


class User:

    def __init__(self, name, socket):
        self.name = name        # username
        self.socket = socket    # user's socket object
        self.blocked = []       # list of blocked users
        self.dms = {}           # dictionary of direct messages. key is sender, value is the message
    
    def dm(self, sender, message):
        '''
        ability to recieve DM's from another user.
        if the user isn't blocked, then the message will be saved to self.dms
        with the senders name as the key
        '''
        ...
    
    def read_dms(self):
        '''
        displays messages from other users. 
        '''
        ...

    def block(self, sender):
        '''
        block another user
        '''
        ...
    
    def unblock(self, sender):
        '''
        unblock another user.
        '''
        ...
