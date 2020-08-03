import pathlib
import sys
import tkinter as tk
from tkinter import messagebox
from threading import Thread

import socketio
from PIL import Image, ImageTk

# Dictionary that holds general player info. Variables are type of info to store & value
player_dict = {
    'name': '',
    'room_name': '',
    'in_a_room': False,
    'vip': False,
    'room_list': [None] * 6,
    'room_list_len': 0,
    'card1': '',
    'card2': '',
    'running': False,
    'balance': 0,
    'investment': 0,
    'minimumBet': 0,
    'checkOrCall': 'Call',
    'my_turn': False,
    'choice': '',
    'raise_amount': 0
}


def player_dict_set(specifier, value):
    player_dict[specifier] = value


def player_dict_get(specifier):
    return player_dict[specifier]


game_info = {
    'cwd': str(pathlib.Path(__file__).parent.resolve()),
    'curr_turn': '',
    'curr_action': '',
    'pot': 0,
    'round_num': '',
    'server_message': '',
    'dealer': '',
    'small_blind': '',
    'big_blind': '',
    'board': ['', '', '', '', ''],
    'flop': False,
    'turn': False,
    'river': False,
    'up': True,
    'won_message': '',
    'reset_round': False,
    'update_tokens': False,
    'display_message': '',
    'message_received': False,
    'game_ended': False,
    'showing_rules': False
}


def game_info_set(specifier, value):
    game_info[specifier] = value


def game_info_get(specifier):
    return game_info[specifier]


# SocketIO connection calls
sio = socketio.Client()


@sio.event
def connect():
    print("Welcome", player_dict_get('name') + "!")
    print("You have successfully connected to the Gator Hold \'em server!")
    print("Good Luck!")
    game_info_set('up', True)


@sio.event
def connect_error(data):
    if str(data) == "Unauthorized":
        print("The game has started or has reached maximum player limit")
    else:
        print("The connection failed!")
    game_info_set('up', True)


@sio.event
def disconnect():
    print("You have left the game. Come back soon!")
    player_dict_set('in_a_room', False)
    player_dict_set('running', False)
    player_dict_set('vip', False)
    player_dict_set("room_name", '')
    player_dict_set("name", '')
    game_info_set('up', True)


@sio.on('user_connection')
def on_event(message):
    print(message)
    update_room_list()
    game_info_set('up', True)


@sio.on('user_disconnect')
def on_event(message):
    print(message)
    update_room_list()
    game_info_set('up', True)


@sio.on('joined_room')
def on_event(message, room):

    player_dict_set('in_a_room', True)
    sio.emit('my_name', (player_dict_get('name'), player_dict_get('room_name')))
    print(message)
    game_info_set('up', True)


@sio.on('you_timed_out')
def on_event():
    player_dict_set('your_turn', False)
    game_info_set('up', True)
    print('you timed out pal')


@sio.on('vip')
def on_event():
    player_dict_set('vip', True)
    print("Ayyyy you da vip")


@sio.on('game_ended')
def on_event(message):
    game_info_set("game_ended", True)
    game_info_set('up', True)
    print("Game ended")
    # sio.disconnect()


@sio.on('your_turn')
def on_event(balance, investment, minimumBet, checkOrCall):
    game_info_set('up', True)

    # CHECK/CALL = 1, FOLD = 2, RAISE = 3
    # THIS IS WHERE TURN CHOICE IS SENT
    new_balance = balance.replace('Your balance: ', '')
    new_investment = investment.replace('Your Investment: ', '')
    new_minimumBet = minimumBet.replace('Minimum Bet to Play: ', '')
    new_checkOrCall = checkOrCall.replace('1.) ', '').replace('2.) ', '').replace('3. ', '')
    player_dict_set('balance', new_balance)
    player_dict_set('investment', new_investment)
    player_dict_set('minimumBet', new_minimumBet)
    player_dict_set('checkOrCall', new_checkOrCall)

    player_dict_set('my_turn', True)

    while player_dict_get('my_turn'):
        if player_dict_get('choice') != '':
            choice = player_dict_get('choice')
            player_dict_set('my_turn', False)
            player_dict_set('choice', '')

    game_info_set('up', True)

    return choice


@sio.on('new_hand')
def on_event():
    game_info_set('up', True)
    game_info['board'] = ['', '', '', '', '']


@sio.on('flop')
def on_event(flop):
    game_info_set('won_message', '')
    temp = flop.split()
    game_info['board'][0] = temp[1] + " " + temp[3]
    game_info['board'][1] = temp[5] + " " + temp[7]
    game_info['board'][2] = temp[9] + " " + temp[11]
    game_info_set('flop', True)
    game_info_set('up', True)


@sio.on('turn')
def on_event(turn):
    temp = turn.split()
    game_info['board'][3] = temp[13] + " " + temp[15]
    game_info_set('turn', True)
    game_info_set('up', True)


@sio.on('river')
def on_event(river):
    temp = river.split()
    game_info['board'][4] = temp[17] + " " + temp[19]
    game_info_set('river', True)
    game_info_set('up', True)


@sio.on('board_init_info')
def on_event(board_info):
    # dealer, small_blind, big_blind, min_bet
    game_info_set('dealer', board_info[0])
    game_info_set('small_blind', board_info[1])
    game_info_set('big_blind', board_info[2])
    player_dict_set('minimumBet', board_info[3])
    game_info_set('round_num', board_info[4])
    game_info_set('update_tokens', True)
    game_info_set('up', True)

    print("Called the new board_init_info function")


@sio.on('message')
def on_event(message):
    print(message)
    game_info_set('message_received', True)
    game_info_set('display_message', message)
    if message == "Game Starting...":
        player_dict_set('running', True)



    if 'has won the pot' in message:
        game_info_set('won_message', message)

    game_info_set('up', True)


@sio.on('emit_hand')
def on_event(card1, card2):
    print("Your hand:", card1, card2)

    player_dict_set("card1", card1)
    player_dict_set("card2", card2)
    game_info_set('reset_round', True)
    game_info_set('up', True)


@sio.on('round_ended')
def on_event():
    game_info_set('up', True)
    # print('round ended')


@sio.on('ai_joined')
def on_event():
    print('ai joined room lol')


@sio.on('connection_error')
def on_event(error):
    print("The game has started or has reached maximum player limit")
    if error == "Unauthorized":
        print(error)

    game_info_set('up', True)


@sio.on('raise')
def on_event(ask):
    game_info_set('up', True)
    howMuch = player_dict_get('raise_amount')
    return howMuch


@sio.on('which_players_turn')
def on_event(data):
    game_info_set('curr_turn', data[0])
    player_dict_set('minimumBet', data[1])
    print(data[0], 'has to go')
    game_info_set('up', True)


@sio.on('player_action')
def on_event(player, option):
    print(player, 'chose option', option)
    print(player)
    print(option)


# General global functions
def update_room_list():
    room_members = sio.call(event='active_player_list', data=player_dict_get('room_name'))
    curr_room_members = player_dict_get('room_list')
    if room_members:
        player_dict_set('room_list_len', len(room_members))
        for index, player in enumerate(curr_room_members):
            if index < len(room_members):
                curr_room_members[index].set(room_members[index]['_name'])
            else:
                curr_room_members[index].set('')
    else:
        return


"""
GatorHoldEm is the main tkinter container that hold different frames.
Initialize the container and create frames objects.
Show the main menu (initial frame) at the end.
"""


class GatorHoldEm(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("GatorHoldEm")
        self.geometry('1267x781')
        self.resizable(False, False)
        # self.protocol("WM_DELETE_WINDOW", self.on_closing)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Create StringVar list room_list to hold lobby members
        new_room_list = []
        for index in range(6):
            new_string_var = tk.StringVar()
            new_room_list.append(new_string_var)

        player_dict_set('room_list', new_room_list)

        self.frames = {}

        for F in (MainMenu, Lobby, Game):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(MainMenu)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.init_update()
        frame.tkraise()

    # def on_closing(self):
    #     if messagebox.askokcancel("Quit", "Do you want to quit?"):
    #         if sio.connected:
    #             sio.disconnect()
    #         self.destroy()
    #         quit()


class MainMenu(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        # Widget declarations

        # Importing main menu background
        self.background_image = tk.PhotoImage(file=game_info_get('cwd') + "/res/main_menu.png")
        self.background_label = tk.Label(self, image=self.background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Room input
        self.room_entry = tk.Entry(self, fg="black", bg="white", width=15, font=("Verdana", "18"))
        self.room_entry.place(x=710, y=400)

        # Name input
        self.name_entry = tk.Entry(self, fg="black", bg="white", width=15, font=("Verdana", "18"))
        self.name_entry.place(x=710, y=575)

        # Submit button
        self.submit = tk.Button(self, activebackground='#003fa3', text="Submit", bg="#004ecc", width=10, height=2,
                                font=("Verdana", "18"), command=self.handle_click)
        self.submit.place(x=735, y=660)

    def init_update(self):
        print("Hi you're in the main menu right now!")
        player_dict_set('vip', False)

    # Event handle for submit and connecting to server
    def handle_click(self):
        # Error check for proper name and room inputs
        if self.name_entry.get() == '':
            print("Invalid entry. Try again!")
            messagebox.showerror("Error: Invalid name",
                                 "Please type a new name!")
            return

        if self.room_entry.get() == '':
            messagebox.showerror("Error: Invalid room name",
                                 "Please type a new room name!")
            return

        # Set up local name and room values
        player_dict_set("name", self.name_entry.get())
        player_dict_set("room_name", self.room_entry.get())

        # Server connect call and error handling
        # sio.connect('http://172.105.159.124:5000')
        try:
            sio.connect('http://localhost:5000')
        except socketio.exceptions.ConnectionError as err:
            if not sio.connected:
                messagebox.showerror("Error: GatorHoldEm connection failure",
                                     "Unable to connect to GatorHoldEm servers. Please check your connection and try "
                                     "again.")
                return

        # Server call to create new player and join/create room, error handling

        # sio.emit('goto_room', player_dict_get('room_name'))
        # print(player_dict_get('in_a_room'))

        sio.emit('goto_room', player_dict_get('room_name'))
        room_members = sio.call(event='active_player_list', data=player_dict_get('room_name'))
        in_room = sio.call(event='in_room', data=[player_dict_get('name'), player_dict_get('room_name')])

        # If successful, update room members and display lobby page
        # If failed, display error message

        # if player_dict_get('in_a_room'):
        if in_room:
            update_room_list()
            self.controller.show_frame(Lobby)
        else:
            sio.disconnect()
            messagebox.showerror("Error: unable to connect to lobby",
                                 "The game has started or has reached maximum player limit. Please try again.")


class Lobby(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Class variables
        self.in_lobby = False

        # Lobby title
        self.config(bg="#c9efd3")
        self.lobby_title_text = tk.StringVar()
        self.changed_title = False

        # Back to home button
        self.back_to_home = tk.Button(self, text="Back to Home", bg = "#e2221d", activebackground = "#c81e1a",
                                      command=self.back_to_menu)
        # self.back_to_home.place(x=0, y=0)
        self.back_to_home.grid(column=0, row=0, sticky='NW')

        self.lobby_title = tk.Label(self, textvariable=self.lobby_title_text, bg="#c9efd3", fg="#029D8A",
                                    font=("Verdana", "60", "bold"))
        # self.lobby_title.pack(padx=10, pady=10)
        self.lobby_title.grid(column=2, row=0)
        # self.grid_columnconfigure(2, weight=1)
        # self.grid_rowconfigure(0, weight=1)

        # Creation of player list in lobby and remove buttons
        self.player_list_frame = [0] * 6
        self.current_lobby_list = [0] * 6
        self.remove_player_list = [0] * 6
        player_list = player_dict_get('room_list')

        for index, label in enumerate(self.current_lobby_list):
            self.player_list_frame[index] = tk.Frame(self)
            self.player_list_frame[index].config(bg="#c9efd3")

            self.current_lobby_list[index] = tk.Label(self.player_list_frame[index], background="#c9efd3",
                                                      textvariable=player_list[index], font=("Verdana", "20"))
            self.current_lobby_list[index].grid(column=2, row=0)

            self.remove_player_list[index] = tk.Button(self.player_list_frame[index], background="#c9efd3",
                                                       height=1, text="Remove", bg = "#e2221d", activebackground = "#c81e1a", font=("Verdana", "12"),
                                                       command=lambda i=index: self.remove_player(i))
            self.remove_player_list[index].grid(column=0, row=0)

            self.player_list_frame[index].grid(column=2, row=index + 1, pady=15)
            self.player_list_frame[index].grid_columnconfigure(0, weight=5)
            self.player_list_frame[index].grid_columnconfigure(1, minsize=100)
            self.player_list_frame[index].grid_columnconfigure(0, minsize=100)
            # self.label_list[index] = tk.Label(self, textvariable=player_list[index],
            #                                   font=("Verdana", "20")).pack(pady=15)
            # self.label_list[index] = tk.Label(self, textvariable=player_list[index], bg="#c9efd3",
            #                                  font=("Verdana", "20")).pack(pady=15)

        # Start the game button
        self.start_the_game = tk.Button(self, activebackground="#00893d", text="Start the Game!", bg="#009944",
                                        width=15, height=3, font=("Verdana", "18"), borderwidth=4,
                                        command=self.handle_submit)
        # self.start_the_game.pack(pady=10)
        self.start_the_game.grid(column=2, row=11, pady=25)

        # Waiting animation
        self.wait_text = tk.StringVar()
        self.wait_tracker = 0
        self.wait = tk.Label(self, textvariable=self.wait_text, bg="#c9efd3", font=("Verdana", "16"),
                             fg="#029D8A")
        # self.wait.place(x=420, y=530)
        self.wait.grid(column=2, row=9)

        # Information for vip
        self.help_text = tk.StringVar()

        # Render help info
        self.help = tk.Label(self, textvariable=self.help_text, bg="#c9efd3", font=("Verdana", "16"),
                             fg="#029D8A")
        # self.help.place(x=150, y=720)
        self.help.grid(column=2, row=10)

        self.ai_button = tk.Button(self, text="Add AI bot", command=self.add_ai_player)

        self.ai_button.grid(column=2, row=8, pady=5)

        for index in range(5):
            self.grid_columnconfigure(index, minsize=100)


    def add_ai_player(self):
        sio.call(event='add_bot', data=player_dict_get('room_name'))

    def remove_player(self, index):
        print(index)
        sio.call(event='remove_player', data=[player_dict_get('room_name'), index])

    def init_update(self):
        print("Hi you're in lobby right now!")
        # Update room name title and lobby status
        self.lobby_title_text.set('Room: ' + player_dict_get('room_name'))
        self.in_lobby = True

        # If player is not vip hide start game button
        if not player_dict_get('vip'):

            self.lobby_title.grid_remove()
            self.help.grid_remove()
            self.wait.grid_remove()

            self.lobby_title.place(x=633, y=0)
            self.update()
            self.lobby_title.place(x=633-self.lobby_title.winfo_width()/2, y=0)

            self.wait.place(x=400, y=600)
            self.help.place(x=340, y=650)

            for index, label in enumerate(self.current_lobby_list):
                self.player_list_frame[index].grid_remove()
                self.player_list_frame[index].place(x=440, y=65*(index+2))

            self.start_the_game.grid_remove()
            self.ai_button.grid_remove()
            self.help_text.set("The first player to join has the ability to start the game.")
        else:
            self.wait.grid_remove()
            self.help_text.set("Since you are the first player to join, you are the VIP player. " \
                               "Press the Start Game button \nonce all the players have joined.")

        self.updates()

    def updates(self):
        if player_dict_get('running'):
            if self.in_lobby:
                self.handle_submit()
            return
        if self.in_lobby:
            if sio.connected:
                    # Change title of lobby once
                    if not self.changed_title:
                        self.lobby_title_text.set('Room: ' + player_dict_get('room_name'))
                        self.changed_title = True

                    # Update list of room members and room list widgets
                    update_room_list()

                    # Hide room list buttons and labels based on amount of players in lobby
                    print(player_dict_get('room_list_len'))
                    for index in range(6):
                        if player_dict_get('vip') is False or index > player_dict_get('room_list_len') - 1:
                            self.remove_player_list[index].grid_remove()
                        else:
                            self.remove_player_list[index].grid()

                    # Start game wait animation loop
                    if self.wait_tracker % 4 == 0:
                        self.wait_tracker = 0
                        self.wait_text.set("Waiting on the first player to start the game")
                    elif self.wait_tracker % 4 == 1:
                        self.wait_text.set("Waiting on the first player to start the game.")
                    elif self.wait_tracker % 4 == 2:
                        self.wait_text.set("Waiting on the first player to start the game..")
                    elif self.wait_tracker % 4 == 3:
                        self.wait_text.set("Waiting on the first player to start the game...")
                    self.wait_tracker += 1
            else:
                print("You're in the lobby but you're disconnected")
                self.back_to_menu()

        print("label width", self.lobby_title.winfo_width())

        # Call this function again in three seconds
        self.after(2000, self.updates)

    def handle_submit(self):
        if player_dict_get('room_list_len') < 2:
            print("Too few players")
            messagebox.showerror("Error: Not enough players",
                                 "Please have two players in the lobby, then try again!")
            return

        self.in_lobby = False
        sio.emit('start_game', player_dict_get('room_name'))
        self.controller.show_frame(Game)

    def back_to_menu(self):
        self.in_lobby = False

        # Grid everything that could've been forgotten
        self.start_the_game.grid()
        self.ai_button.grid()
        self.wait.grid()

        sio.disconnect()
        sio.wait()
        self.controller.show_frame(MainMenu)


class Game(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.con = controller
        self.config(bg="#008040")
        self.message_label_color = "#a56f22"

        self.back_to_home = tk.Button(self, text="Back to Main Menu",
                                      command=self.back_button_submit)
        self.back_to_home.place(x=0, y=0)

        # Player and Balance declarations
        # OUR PLAYER IS AT INDEX 0
        self.pl_list = []
        self.pl_text = [tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar()]
        self.bal_text = [tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar()]
        self.inv_text = [tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar()]

        for t in self.pl_text:
            t.set('')

        self.running = True

        self.pl_name = ["", "", "", "", "", ""]  # UNUSED ?????
        self.pl_label = [0, 0, 0, 0, 0, 0]
        self.bal_label = [0, 0, 0, 0, 0, 0]
        self.inv_label = [tk.Label(self, textvariable=self.inv_text[i], font=("Verdana", "11")) for i in range(6)]

        self.pl_label[0] = tk.Label(self, textvariable=self.pl_text[0], font=("Verdana", "11"))
        self.pl_label[1] = tk.Label(self, textvariable=self.pl_text[1], font=("Verdana", "11"))
        self.pl_label[2] = tk.Label(self, textvariable=self.pl_text[2], font=("Verdana", "11"))
        self.pl_label[3] = tk.Label(self, textvariable=self.pl_text[3], font=("Verdana", "11"))
        self.pl_label[4] = tk.Label(self, textvariable=self.pl_text[4], font=("Verdana", "11"))
        self.pl_label[5] = tk.Label(self, textvariable=self.pl_text[5], font=("Verdana", "11"))

        self.bal_label[0] = tk.Label(self, textvariable=self.bal_text[0], font=("Verdana", "11"))
        self.bal_label[1] = tk.Label(self, textvariable=self.bal_text[1], font=("Verdana", "11"))
        self.bal_label[2] = tk.Label(self, textvariable=self.bal_text[2], font=("Verdana", "11"))
        self.bal_label[3] = tk.Label(self, textvariable=self.bal_text[3], font=("Verdana", "11"))
        self.bal_label[4] = tk.Label(self, textvariable=self.bal_text[4], font=("Verdana", "11"))
        self.bal_label[5] = tk.Label(self, textvariable=self.bal_text[5], font=("Verdana", "11"))

        # Card Back
        self.card_back_image = Image.open(game_info_get('cwd') + "/res/back.png")
        self.card_back_image = ImageTk.PhotoImage(self.card_back_image)
        self.card_back_label = tk.Label(self, image=self.card_back_image, bg="#008040")

        # List of cards to be displayed on the board
        self.board_card_image = [self.card_back_image, self.card_back_image, self.card_back_image, self.card_back_image,
                                 self.card_back_image]
        self.board_card_label = [0, 0, 0, 0, 0]
        self.card1_image = 0
        self.card1_label = 0
        self.card1_displayed = False
        self.card2_label = 0
        self.card2_image = 0
        self.card2_displayed = False
        self.pot_label = 0

        self.min_bet_text = tk.StringVar()
        self.min_bet_label = 0

        self.small_blind_text = tk.StringVar()
        self.small_blind_label = 0

        self.big_blind_text = tk.StringVar()
        self.big_blind_label = 0

        self.dealer_text = tk.StringVar()
        self.dealer_label = 0

        self.round_num_text = tk.StringVar()
        self.round_num_label = 0

        self.won_the_pot_text = tk.StringVar()
        self.won_the_pot_label = 0

        # Board card positions
        self.board_card_x = [210, 410, 610, 810, 1010]
        self.board_card_y = [335] * 5

        # player positions. OUR PLAYER IS AT INDEX 0
        self.pl_x = [870, 65, 330, 600, 870, 1137]
        self.pl_y = [670, 130, 50, 20, 50, 130]

        # Blinds positions
        self.blind_x = [815, 5, 270, 540, 810, 1082]
        self.blind_y = [675, 135, 55, 25, 55, 135]

        # Dealer position
        self.d_x = [905, 95, 460, 730, 1000, 1167]
        self.d_y = [732, 195, 55, 25, 55, 195]

        # Import blind and dealer tokens
        self.bb_token_image = ImageTk.PhotoImage(Image.open(game_info_get('cwd') + "/res/bb_token.png"))
        self.bb_token = tk.Label(self, image=self.bb_token_image, bg="#008040")

        self.sb_token_image = ImageTk.PhotoImage(Image.open(game_info_get('cwd') + "/res/sb_token.png"))
        self.sb_token = tk.Label(self, image=self.sb_token_image, bg="#008040")

        self.dealer_token_image = ImageTk.PhotoImage(Image.open(game_info_get('cwd') + "/res/d_token.png"))
        self.dealer_token = tk.Label(self, image=self.dealer_token_image, bg="#008040")

        # Import table bet
        self.table_bet_image = ImageTk.PhotoImage(Image.open(game_info_get('cwd') + "/res/table_bet.png"))
        self.table_bet_label = tk.Label(self, image=self.table_bet_image, bg="#008040").place(x=240, y=135)
        self.table_bet_name = tk.StringVar()
        self.table_bet_name.set('Current Table Bet')
        self.table_bet_name_label = tk.Label(self, textvariable=self.table_bet_name, bg="#008040",
                                             font=("Verdana", "12", "bold"))
        self.table_bet_name_label.place(x=255, y=305)

        # Import pot
        self.pot_image = ImageTk.PhotoImage(Image.open(game_info_get('cwd') + "/res/poker_chips.png"))
        self.pot_label = tk.Label(self, image=self.pot_image, bg="#008040").place(x=900, y=160)
        # self.pot_label = tk.Label(self, image=self.pot_image, bg="#008040").place(x=855,y=120)

        # Hand Rankings Image
        image = Image.open(game_info_get('cwd') + "/res/Rankings.png")
        image = image.resize((700, 900), Image.ANTIALIAS)

        self.hand_rankings_image = ImageTk.PhotoImage(image)

        self.hand_rankings_label = tk.Label(self, image=self.hand_rankings_image, bg="#008040")

        # Button that starts the game on the client side.
        self.button = tk.Button(self, text="Start Game", bg="#72f122", activebackground="#55c90d",
                                highlightbackground="black", width=25, command=self.start_up)
        self.button.place(x=1026, y=640)

        # Button that displays on winning screen to take back to menu
        self.winning_button = tk.Button(self, text="Exit to Main Menu", bg="#72f122", activebackground="#55c90d",
                                        highlightbackground="black", width=25,
                                        command=self.exit)

        # Rules tab open button
        self.show_rules_button = tk.Button(self, text="Show Hand Rankings", bg="#ffcf2b", activebackground="#dab22a",
                                            highlightbackground="black", width=25,
                                            command=self.show_rules)

        self.close_rules_button = tk.Button(self, text="Close Hand Rankings", bg="#ffcf2b", activebackground="#dab22a",
                                             highlightbackground="black", width=25,
                                             command=self.close_rules)


        self.pl_label_width = 122
        self.bal_label_width = 50

        # raise amount slider
        self.raise_slider = tk.Scale(self, from_=0, to=200, orient='horizontal', state='disabled', bg="#ffcf2b", activebackground="#dab22a",
                                     command=self.set_raise_val)
        self.raise_slider.place(x=1026, y=680, width=230, height=40)
        # self.raise_slider.pack()

        # # TODO Color for current turn
        # self.curr_player_text = tk.StringVar()
        # self.curr_player_label = tk.Label(self, textvar=self.curr_player_text, bg = "#008040").place(x=0, y=500, height=25)

        # Key
        self.key_image = ImageTk.PhotoImage(Image.open(game_info_get('cwd') + "/res/Key.png"))
        self.key_label = tk.Label(self, bg = "#008040", image = self.key_image).place(x = 10, y = 530)

        # Buttons for call/check, fold, and raise
        self.fold_button = tk.Button(self, text='Fold', state='disabled', bg = "#ffcf2b", activebackground = "#dab22a",
                                     command=lambda: [player_dict_set('choice', '2'), game_info_set('up', True)])

        # Make buttons initially disabled
        self.call_check_text = tk.StringVar()
        self.call_check_text.set(player_dict_get('checkOrCall'))
        self.call_check_button = tk.Button(self, textvar=self.call_check_text, state='disabled', bg = "#ffcf2b", activebackground = "#dab22a",
                                           command=lambda: [player_dict_set('choice', '1'), game_info_set('up', True)])

        self.raise_button = tk.Button(self, text='Raise', state='disabled', bg = "#ffcf2b", activebackground = "#dab22a",
                                      command=lambda: [player_dict_set('choice', '3'), game_info_set('up', True)])

        self.fold_button.place(x=1026, y=730, height=40, width=70)
        self.call_check_button.place(x=1106, y=730, height=40, width=70)
        self.raise_button.place(x=1186, y=730, height=40, width=70)

        # Label under the cards that signify your hand
        self.your_hand_label = tk.Label(self, text="Your hand", bg="#a56f22", height=2, width=15).place(x=510, y=740)

        # TODO Add message bar
        self.game_actions_label = tk.Label(self, text="Game Actions", fg="black", bg="#008040",
                                           font=("Verdana", "18")).place(x=555,y=105)
        self.message_text = tk.StringVar()
        self.message_label = tk.Label(self, textvar=self.message_text, fg="black", bg=self.message_label_color, width=27, height=2,
                                      font=("Verdana", "18"))
        self.message_label.place(x=440, y=155)

        #Initialize all the labels
        for i in range(6):
            self.pl_label[i].place(x=self.pl_x[i], y=self.pl_y[i],
                                   width=self.pl_label_width, height=20)
            # Adjust balance position
            self.bal_label[i].place(x=self.pl_x[i], y=self.pl_y[i] + 20,
                                    width=self.pl_label_width, height=20)
            self.inv_label[i].place(x=self.pl_x[i], y=self.pl_y[i] + 40,
                                    width=self.pl_label_width, height=20)
            # TODO Initial label colors
            self.pl_label[i].config(bg="gray")
            self.bal_label[i].config(bg="gray")
            self.inv_label[i].config(bg="gray")

        # self.reset_round()

    # Calculates the relative position from our player based on their absolute position
    def _relative_position(self, my_position, absolute_position):
        if absolute_position >= my_position:
            return absolute_position - my_position
        else:
            return 6 - my_position + absolute_position

    def _place_tokens(self):
        self.pl_list = sio.call(event='active_player_list', data=player_dict_get('room_name'))
        indices = {'my_index': None, 'd_rel_index': None, 'bb_rel_index': None, 'sb_rel_index': None}
        # print("Player list: ", self.pl_list)
        for i, p in enumerate(self.pl_list):
            if p['_client_number'] == sio.sid:
                indices['my_index'] = i

        for i, p in enumerate(self.pl_list):
            if p['_client_number'] == game_info_get('dealer'):
                indices['d_rel_ind'] = self._relative_position(indices['my_index'], i)

            if p['_client_number'] == game_info_get('big_blind'):
                indices['bb_rel_ind'] = self._relative_position(indices['my_index'], i)

            if p['_client_number'] == game_info_get('small_blind'):
                indices['sb_rel_ind'] = self._relative_position(indices['my_index'], i)

        self.bb_token.place(x=self.blind_x[indices['bb_rel_ind']], y=self.blind_y[indices['bb_rel_ind']])
        self.sb_token.place(x=self.blind_x[indices['sb_rel_ind']], y=self.blind_y[indices['sb_rel_ind']])
        self.dealer_token.place(x=self.d_x[indices['d_rel_ind']], y=self.d_y[indices['d_rel_ind']])

    def reset_round(self):
        print("the round is reset")
        self.card1_displayed = False
        self.card2_displayed = False

        for i in range(5):
            # self.board_card_image[i]
            self.card_back_label = tk.Label(self, image=self.card_back_image,
                                            bg="black", fg="black").place(x=self.board_card_x[i],
                                                                          y=self.board_card_y[i])
        # Card 1 display
        if player_dict_get("card1") != "" and not self.card1_displayed:
            temp = player_dict_get("card1").split()
            temp_s = temp[1] + " " + temp[3].lower()

            self.card1_image = self._load_card_image(temp_s)
            self.card1_label = tk.Label(self, image=self.card1_image, bg="white")

            self.card1_label.place(x=445, y=550)
            self.card1_displayed = True

        # Card 2 Displayed
        if player_dict_get("card2") != "" and not self.card2_displayed:
            temp = player_dict_get("card2").split()
            temp_s = temp[1] + " " + temp[3].lower()
            self.card2_image = self._load_card_image(temp_s)
            self.card2_label = tk.Label(self, image=self.card2_image, bg="white")
            self.card2_label.place(x=580, y=550)
            self.card2_displayed = True
        self.update()

    def init_update(self):
        if game_info_get('reset_round'):
            self.reset_round()
            game_info_set('reset_round', False)
        if game_info_get('update_tokens'):
            self._place_tokens()
            game_info_set('update_tokens', False)
        # Check to display winning button
        if game_info_get('game_ended'):
            self.winning_button.place(x=550, y=250)

        if game_info_get('message_received'):
            game_info_set('message_received', False)
            self.message_text.set(game_info_get('display_message'))



    def set_raise_val(self, val):
        player_dict_set('raise_amount', val)
        game_info_set('up', True)

    """
        Function that runs the game and checks if it's the player's turn ?
    """

    def start_up(self):
        self.running = True
        while self.running:
            # self.update_players()
            if game_info_get('up'):
                self.update_players()
                game_info_set('up', False)
            else:
                self.update()
            # print(player_dict_get("card1"))

    def back_button_submit(self):
        if messagebox.askyesno("Back to Main Menu", "You will be unable to reconnect to this game. Are you sure?"):
            self.exit()

    def exit(self):
        player_dict_set('running', False)
        self.running = False
        self.winning_button.place_forget()
        sio.disconnect()
        self.con.show_frame(MainMenu)

    #Function that shows and closes the HandRankings Rules:
    def show_rules(self):
        win = tk.Toplevel()
        win.geometry("700x900")
        win.wm_title("Hand Rankings")

        l = tk.Label(win, image=self.hand_rankings_image, bg="#008040")
        l.place(x=0, y=0)


        game_info_set('showing_rules', True)

    def close_rules(self):

        game_info_set('showing_rules', False)


    """
    Function that sets the name and balance for different players.
    """

    def _set_player_name_balance(self, absolute_position, relative_position):

        # Current Player
        if self.pl_list[absolute_position]['_client_number'] == game_info_get('curr_turn'):
            # TODO Add current player color bg = background, fg = font
            self.pl_label[relative_position].config(bg="#89EBC4", fg="black")
            self.bal_label[relative_position].config(bg="#89EBC4", fg="black")
            self.inv_label[relative_position].config(bg="#89EBC4", fg="black")
        # Inactive players
        elif (self.pl_list[absolute_position]['_balance'] == 0 and
            self.pl_list[absolute_position]['_investment'] == 0) or self.pl_list[absolute_position]['_isFolded']:
            self.pl_label[relative_position].config(bg="gray", fg="black")
            self.bal_label[relative_position].config(bg="gray", fg="black")
            self.inv_label[relative_position].config(bg="gray", fg="black")
        # Active players
        else:
            self.pl_label[relative_position].config(bg="white", fg="black")
            self.bal_label[relative_position].config(bg="white", fg="black")
            self.inv_label[relative_position].config(bg="white", fg="black")

        self.pl_text[relative_position].set(self.pl_list[absolute_position]['_name'])
        self.bal_text[relative_position].set("Balance: " + str(self.pl_list[absolute_position]['_balance']))
        _inv = "Investment: " + str(self.pl_list[absolute_position]['_investment'])
        self.inv_text[relative_position].set(_inv)

        # self.pl_label[relative_position].place(x=self.pl_x[relative_position], y=self.pl_y[relative_position],
        #                                        width=self.pl_label_width, height=20)
        #
        # self.bal_label[relative_position].place(x=self.pl_x[relative_position], y=self.pl_y[relative_position] + 20,
        #                                         width=self.bal_label_width, height=20)

    """
    Function that loads card images and returns image object
    Parameters: Card Suit, Ex: Heart 10
    """

    def _load_card_image(self, temp):
        temp = temp.split()
        try:
            if temp[1] == "11":
                temp[1] = "jack"
            if temp[1] == "12":
                temp[1] = "queen"
            if temp[1] == "13":
                temp[1] = "king"
            if temp[1] == "14":
                temp[1] = "ace"

            path = game_info_get('cwd') + "/res/" + temp[1] + "_of_" + temp[0].lower() + "s.png"
            return ImageTk.PhotoImage(Image.open(path))
        # Sometimes we try to load in a card to early before we received it which causes an Index Error
        except IndexError:
            pass

    """
    Function that places a card on the board
    parameters: position (0-4)
    """

    def _place_card(self, position):
        # Display cards on the board
        self.board_card_image[position] = self._load_card_image(game_info['board'][position])
        c = tk.Label(self, image=self.board_card_image[position], bg="white")
        c.place(x=self.board_card_x[position], y=self.board_card_y[position])

    """
        Function that renders a players screen
    """

    # reset cards at the end of the round
    def update_players(self):
        # Disable start
        self.button.config(state='disabled')

        # # Check to display winning button
        # if game_info_get('game_ended'):
        #     self.winning_button.place(x=550, y=250)

        # Check to see if HandRankings is open
        if game_info_get('showing_rules') is False:
            self.show_rules_button.place(x=5, y=746)

        # self.pl_list = sio.emit('active_player_list', '1')
        self.pl_list = sio.call(event='active_player_list', data=player_dict_get('room_name'))
        min_bet = int(player_dict_get('minimumBet'))

        bal = int(player_dict_get('balance'))
        inv = int(player_dict_get('investment'))

        # Adjusting the raise slide based on certain factors
        if bal + inv <= min_bet:
            self.raise_slider.config(from_=int(0))
            self.raise_slider.config(to=int(0))
        else:
            # If we constraint from to min_bet in cases w
            self.raise_slider.config(from_=int(1))
            self.raise_slider.config(to=int(bal - (min_bet - inv)))

        # Enable the buttons only if it is our turn
        if player_dict_get('my_turn'):

            self.raise_button["state"] = 'normal'
            self.fold_button["state"] = 'normal'
            self.call_check_button["state"] = 'normal'
            self.raise_slider["state"] = 'normal'
        else:
            self.raise_button["state"] = 'disabled'
            self.fold_button["state"] = 'disabled'
            self.call_check_button["state"] = 'disabled'
            self.raise_slider["state"] = 'disabled'

        # set the display names and balances depending on the player
        # pl_list is absolute, every client receives exact copy.
        if self.pl_list is not None:

            # Find out the index our client player is at in the pl_list
            my_index = 0
            for ind, p in enumerate(self.pl_list):
                if p['_client_number'] == sio.sid:
                    my_index = ind
            # placing our player at the main spot, bottom of the screen.
            self._set_player_name_balance(my_index, 0)

            # Positioning other players based on their relative position to us
            # pl_text is positioned relatively
            # placement_index is for relative positioning
            placement_index = 1
            # Loop to position people to the left of us (after us in the main list)
            # i is the index in the main list
            for i in range(my_index + 1, len(self.pl_list)):
                self._set_player_name_balance(i, placement_index)
                placement_index += 1

            # Loop to position people up to the right of us (before us in the main list
            placement_index = 6 - my_index
            for i in range(0, my_index):
                self._set_player_name_balance(i, placement_index)
                placement_index += 1

        # pot total
        p = 0
        for pl in self.pl_list:
            p += pl['_investment']
        game_info_set('pot', p)
        pot_string = "Total Pot amount: " + str(game_info_get('pot'))

        self.pot_label = tk.Label(self, text=pot_string,
                                  bg="#008040", font=("Verdana", "12", "bold"))
        # self.pot_label.place(x=740, y=260, width=180, height=20)
        self.pot_label.place(x=890, y=300)

        self.min_bet_text.set(str(player_dict_get('minimumBet')))
        self.min_bet_label = tk.Label(self, textvariable=self.min_bet_text, bg="#FFFFFF", font=("Verdana", "35"))
        self.min_bet_label.place(x=280, y=190)

        self.round_num_text.set('Round: ' + str(game_info_get('round_num')))
        self.round_num_label = tk.Label(self, textvariable=self.round_num_text, bg="#008040",
                                        font=("Verdana", "20", "bold"))
        self.round_num_label.place(x=1130, y=10, width=130, height=35)

        # # WIN THE GAME LABEL
        # self.won_the_pot_text.set(game_info_get('won_message'))
        # self.won_the_pot_label = tk.Label(self, textvariable=self.won_the_pot_text, )
        # self.won_the_pot_label.place(x=0, y=560, height=20)

        # Update player turn
        # self.curr_player_text.set("Waiting on: " + game_info_get('curr_turn'))

        # Update call/check text
        self.call_check_text.set(player_dict_get('checkOrCall'))
        if self.call_check_text.get() == "Call":
            call_amount = str(int(player_dict_get("minimumBet")) - int(player_dict_get("investment")))
            self.call_check_text.set("Call " + call_amount)

        if game_info_get('flop'):
            game_info_set('flop', False)
            for i in range(3):
                self._place_card(i)

        if game_info_get('turn'):
            game_info_set('turn', False)
            self._place_card(3)

        if game_info_get('river'):
            game_info_set('river', False)
            self._place_card(4)

        self.con.show_frame(Game)

# def update():
#     print("hi")


def main():
    def on_closing():
            if messagebox.askokcancel("Close GatorHoldEm", "Do you want to quit GatorHoldEm?"):
                if sio.connected:
                    sio.disconnect()
                app.destroy()
                sys.exit()

    # Start main loop
    app = GatorHoldEm()
    app.protocol("WM_DELETE_WINDOW", on_closing)
    app.mainloop()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt as e:
        sys.exit(0)
