'''
Jay Derderian
CS 594

This module handles the cli for this application. 

NOTE:
    read these:
        -> http://patorjk.com/software/taag/#p=display&f=Alpha&t=ART
        -> https://pypi.org/project/art/
        -> https://www.geeksforgeeks.org/print-colors-python-terminal/
        -> https://en.wikipedia.org/wiki/ANSI_escape_code#Colors
    

    find a way to detect system and determine which library to use?
    some command terminals might not work with these libraries...

    execute during import lines, possiblity in def __init(self)__?
    ex:
        if os.getenv('ANSI_COLORS_DISABLED') is None:

    the goal is to make this module reusable between projects!

    cool fonts (text2art):
        - tarty1 & tarty2
        - alligator
        - charact4
        - tiles
        - isometric2
        - tinker-toy
        - usaflag
        - dietcola
        - 1943
        - slant
        - soft
        - alpha
        - threepoint
        - georgia11
        - block
        - fireing
        - strikethrough
        - rev

'''
import os

from sys import stdout, stdin
from random import choice

from art import (
    tprint, text2art, aprint, art_dic, font_list,
    FONT_NAMES, decor, decor_dic, randart,
) 
from colorama import (
    Fore, Back, Style
)
from termcolor import (
    colored, cprint 
)

class CLI:
    '''
    import and instantiate this class to use foreground and background
    colors in the terminal while using the IRC application. 

    made using ANSI Escape Sequence color constants and the termcolor module
    '''
    def __init__(self, debug=False):
        
        self.debug = debug

        self.reset = '\033[0m'
        self.bold = '\033[01m'
        self.disable = '\033[02m'
        self.underline = '\033[04m'
        self.reverse = '\033[07m'
        self.strikethrough = '\033[09m'
        self.invisible = '\033[08m'
    
        # foreground colors
        self.fg = {
            'black': '\033[30m',
            'red':  '\033[31m',
            'green': '\033[32m',
            'orange': '\033[33m',
            'blue': '\033[34m',
            'purple': '\033[35m',
            'cyan': '\033[36m',
            'lightgrey': '\033[37m',
            'darkgrey': '\033[90m',
            'lightred': '\033[91m',
            'lightgreen': '\033[92m',
            'yellow': '\033[93m',
            'lightblue': '\033[94m',
            'pink': '\033[95m',
            'lightcyan': '\033[96m'
        }

        # background colors
        self.bg = {
            'black': '\033[40m',
            'red': '\033[41m',
            'green': '\033[42m',
            'orange': '\033[43m',
            'blue': '\033[44m',
            'purple': '\033[45m',
            'cyan': '\033[46m',
            'lightgrey': '\033[47m'
        }


    ## TESTER ###

    def test(self):
        f = choice(FONT_NAMES) 
        print('\n', text2art(text='HELLO', font=f))
        print(f'\nFONT: {f}\n')
        


    ## FANCY STUFF ##

    def rainbow_word(self, word):
        '''
        prints a word out letter by letter each with an individual color
        '''
        ...


    ## CLIENT UI ##

    def app_name(self, app_name:str, f=None):
        '''
        welcome! should display the app name, author,
        version.
        then display options
            - join new room?
            - see current room list
            - 
        '''
        if f is not None:
            if type(f) == str:
                return tprint(f'{app_name}', font=f)
            else:
                raise TypeError('font name must be a string!')
        return tprint(f'{app_name}')


    def client_info(self, info:dict):
        '''
        displays app info
        (author, version # (with date))
        '''
        print(text2art(info["Name"], font='tarty2'))
        print(art_dic.art_dic["kirby dance"], '\n')
        print(text2art(info["Version"], font='tiny2'))
        print(text2art(info["Author"], font='tiny2'), '\n')

    def client_menu(self, menu:list[str]):
        '''
        displays a menu utilizing a list of strings representing 
        each line in the menu.
        '''
        for line in menu:
            print(text2art(menu[line], font='tiny2'))



    ## APP UI ##
    
    def input_prompt(self, name):
        stdout.write(f'{Fore.LIGHTBLUE_EX}{name} > ')
        stdout.flush()
    
    def room_list(self, rooms):
        ...
    
    def user_list(self, users):
        ...
    
    def error_messages(self, errors):
        '''
        Display an error message, or list of messages
        '''
        if type(errors) == str:
            print(f'{Fore.RED} ERROR: {errors}')
        elif type(errors) == list:
            print(f'{Fore.RED} ERROR')
            for e in range(len(errors)):
                print(f'{Fore.RED}{e} : {errors[e]}')
        else:
            raise TypeError('erros must be a single str or list[str]! type is:', type(errors))