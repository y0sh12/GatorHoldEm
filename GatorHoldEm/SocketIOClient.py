import pathlib
import sys
import tkinter as tk

import socketio
from PIL import Image, ImageTk

# Dictionary that holds general player info. Variables are type of info to store & value
player_dict = {
    'name': '',
    'room_name': '',
    'in_a_room': False,
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
    'won_message': ''

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
    sio.emit('my_name', (player_dict_get('name'), player_dict_get('room_name')))
    print(message)
    game_info_set('up', True)


@sio.on('vip')
def on_event():
    print("Ayyyy you da vip")


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
    temp = flop.split()
    game_info['board'][0] = temp[1] + " " + temp[3]
    game_info['board'][1] = temp[5] + " " + temp[7]
    game_info['board'][2] = temp[9] + " " + temp[11]
    game_info_set('won_message', '')
    game_info_set('up', True)


@sio.on('turn')
def on_event(turn):
    temp = turn.split()
    game_info['board'][3] = temp[13] + " " + temp[15]
    game_info_set('up', True)


@sio.on('river')
def on_event(river):
    temp = river.split()
    game_info['board'][4] = temp[17] + " " + temp[19]
    game_info_set('up', True)


@sio.on('board_init_info')
def on_event(board_info):
    # dealer, small_blind, big_blind, min_bet
    game_info_set('dealer', board_info[0])
    game_info_set('small_blind', board_info[1])
    game_info_set('big_blind', board_info[2])
    player_dict_set('minimumBet', board_info[3])
    game_info_set('round_num', board_info[4])
    game_info_set('up', True)

    print("Called the new board_init_info function")


@sio.on('message')
def on_event(message):
    print(message)
    if message == "game starting":
        player_dict_set('running', True)

    if 'has won the pot' in message:
        game_info_set('won_message', message)

    if game_info_get('flop'):
        temp = message.split()
        print(temp)
        print(temp[0] + " " + temp[0])
        print(game_info['board'][0])
        game_info['board'][0] = temp[1] + " " + temp[3]
        game_info['board'][1] = temp[5] + " " + temp[7]
        game_info['board'][2] = temp[9] + " " + temp[11]
        game_info_set('flop', False)
    # if message == "---------THE FLOP----------\n":
    # game_info_set('flop', True)

    if game_info_get('turn'):
        temp = message.split()
        print(temp)
        game_info['board'][3] = temp[13] + " " + temp[15]
        game_info_set('turn', False)
    # if message == "---------THE TURN----------\n":
    # game_info_set('turn', True)

    if game_info_get('river'):
        temp = message.split()
        print(temp)
        game_info['board'][4] = temp[17] + " " + temp[19]
        game_info_set('river', False)
    # if message == "---------THE RIVER----------\n":
    # game_info_set('river', True)
    game_info_set('up', True)


@sio.on('emit_hand')
def on_event(card1, card2):
    print("Your hand:", card1, card2)
    player_dict_set("card1", card1)
    player_dict_set("card2", card2)
    game_info_set('up', True)


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
    curr_room_members = player_dict['room_list']
    if room_members:
        player_dict_set('room_list_len', len(room_members))
        for index, player in enumerate(curr_room_members):
            if index < len(room_members):
                curr_room_members[index].set(room_members[index]['_name'])
            else:
                curr_room_members[index].set('')
    else:
        return


class GatorHoldEm(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("GatorHoldEm")
        self.geometry('1267x781')
        self.resizable(False, False)

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
        frame.tkraise()


class MainMenu(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        # Widget declarations

        #Importing main menu background
        self.background_image = tk.PhotoImage(file=game_info_get('cwd') + "/res/main_menu.png")
        self.background_label = tk.Label(self, image=self.background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Name input
        self.name_entry = tk.Entry(self, fg="black", bg="white", width=15, font=("Helvetica", "18"))
        self.name_entry.place(x=710, y=400)

        # Room input
        self.room_entry = tk.Entry(self, fg="black", bg="white", width=15, font=("Helvetica", "18"))
        self.room_entry.place(x=710, y=575)

        # Submit button
        self.submit = tk.Button(self, activebackground='#003fa3', text="Submit", bg="#004ecc", width=10, height=2,
                                font=("Helvetica", "18"), command=self.handle_click)

        self.submit.place(x=735, y=660)

    # Event handle for submit and connecting to server
    def handle_click(self):
        # Error check for proper name and room inputs
        if self.name_entry.get() == '' or self.room_entry.get() == '':
            print("Invalid entry. Try again!")
            return

        # Set up local name and room values
        player_dict_set("name", self.name_entry.get())
        player_dict_set("room_name", self.room_entry.get())

        # Server call to create new player and join/create room, error handling
        sio.connect('http://172.105.159.124:5000')
        # sio.connect('http://localhost:5000')
        sio.emit('goto_room', player_dict_get('room_name'))
        room_members = sio.call(event='active_player_list', data=player_dict_get('room_name'))
        in_room = sio.call(event='in_room', data=[player_dict_get('name'), player_dict_get('room_name')])
        print(in_room)
        # If successful, update room members and display lobby page
        if in_room:
            update_room_list()
            self.controller.show_frame(Lobby)
        else:
            sio.disconnect()


class Lobby(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Lobby title
        self.lobby_title_text = tk.StringVar()
        self.changed_title = False
        self.lobby_title = tk.Label(self, textvariable=self.lobby_title_text)
        self.lobby_title.pack(padx=10, pady=10)

        # List of players in lobby
        self.label_list = [0] * 6
        player_list = player_dict_get('room_list')

        for index, label in enumerate(self.label_list):
            self.label_list[index] = tk.Label(self, textvariable=player_list[index]).pack(pady=5)

        # Back to home button
        self.back_to_home = tk.Button(self, text="Back to Home",
                                      command=self.leaving_lobby)
        self.back_to_home.pack(pady=10)

        # Start the game button
        self.start_the_game = tk.Button(self, text="Start the Game!",
                                        command=self.handle_submit)
        self.start_the_game.pack(pady=10)

        self.update()

    def handle_submit(self):
        sio.emit('start_game', player_dict_get('room_name'))
        player_dict_set('running', True)
        self.controller.show_frame(Game)

    def update(self):
        if sio.connected:
            # Change title of lobby once
            if player_dict_get('running'):
                self.handle_submit()

            elif not self.changed_title:
                self.lobby_title_text.set('Room: ' + player_dict_get('room_name'))
                self.changed_title = True
            # Update list of room members
            update_room_list()

        # Call this function again in three seconds
        self.after(6000, self.update)

    def leaving_lobby(self):
        sio.disconnect()
        sio.wait()
        self.controller.show_frame(MainMenu)


class Game(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.con = controller
        self.background_image = tk.PhotoImage(file=game_info_get('cwd') + "/res/felt.png")
        self.background_label = tk.Label(self, image=self.background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.back_to_home = tk.Button(self, text="Back to Lobby",
                                      command=lambda: [self.exit(), controller.show_frame(Lobby)])
        self.back_to_home.pack()
        self.pl_list = []
        self.pl_text = [tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar()]
        self.bal_text = [tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar()]

        for t in self.pl_text:
            t.set('')

        self.running = True
        self.pl_label = [0, 0, 0, 0, 0, 0]
        self.bal_label = [0, 0, 0, 0, 0, 0]
        self.pl_name = ["", "", "", "", "", ""]
        self.pl_label[0] = tk.Label(self, textvariable=self.pl_text[0])
        self.pl_label[1] = tk.Label(self, textvariable=self.pl_text[1])
        self.pl_label[2] = tk.Label(self, textvariable=self.pl_text[2])
        self.pl_label[3] = tk.Label(self, textvariable=self.pl_text[3])
        self.pl_label[4] = tk.Label(self, textvariable=self.pl_text[4])
        self.pl_label[5] = tk.Label(self, textvariable=self.pl_text[5])

        self.bal_label[0] = tk.Label(self, textvariable=self.bal_text[0])
        self.bal_label[1] = tk.Label(self, textvariable=self.bal_text[1])
        self.bal_label[2] = tk.Label(self, textvariable=self.bal_text[2])
        self.bal_label[3] = tk.Label(self, textvariable=self.bal_text[3])
        self.bal_label[4] = tk.Label(self, textvariable=self.bal_text[4])
        self.bal_label[5] = tk.Label(self, textvariable=self.bal_text[5])

        self.card_back_image = Image.open(game_info_get('cwd') + "/res/back.png")
        self.card_back_image = self.card_back_image.resize((40, 70), Image.ANTIALIAS)
        self.card_back_image = ImageTk.PhotoImage(self.card_back_image)
        self.card_back_label = tk.Label(self, image=self.card_back_image, bg="black")

        self.board_card_image = [self.card_back_image, self.card_back_image, self.card_back_image, self.card_back_image,
                                 self.card_back_image]
        self.board_card_label = [0, 0, 0, 0, 0]

        self.card1_image = 0
        self.card1_label = 0
        self.card2_label = 0
        self.card2_image = 0
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

        self.board_card_x = [220, 298, 375, 453, 530]
        self.board_card_y = [260, 260, 260, 260, 260]

        self.pl_x = [0, 300, 300, 0, -300, -300]
        self.pl_y = [540, 440, 240, 140, 240, 440]
        self.card1_x = [350, 50, 50, 350, 650, 650]
        self.card1_y = [490, 390, 190, 90, 190, 390]
        self.card2_x = [400, 100, 100, 400, 700, 700]
        self.card2_y = [490, 390, 190, 90, 190, 390]

        self.button = tk.Button(self, text="I'm ready", bg="blue", width=25, command=self.start_up)
        self.button.pack()

        self.pl_label_width = 100
        self.bal_label_width = 50

        # raise amount slider
        self.raise_slider = tk.Scale(self, from_=0, to=200, orient='horizontal', command=self.set_raise_val)
        self.raise_slider.place(x=550, y=500, width=230, height=40)
        # self.raise_slider.pack()

        # Label for current turn
        self.curr_player_text = tk.StringVar()
        self.curr_player_label = tk.Label(self, textvar=self.curr_player_text).place(x=0, y=575, height=25)

        # Buttons for call/check, fold, and raise
        self.fold_button = tk.Button(self, text='Fold',
                                     command=lambda: [player_dict_set('choice', '2'), game_info_set('up', True)])

        self.call_check_text = tk.StringVar()
        self.call_check_text.set(player_dict_get('checkOrCall'))
        self.call_check_button = tk.Button(self, textvar=self.call_check_text,
                                           command=lambda: [player_dict_set('choice', '1'), game_info_set('up', True)])

        self.raise_button = tk.Button(self, text='Raise',
                                      command=lambda: [player_dict_set('choice', '3'), game_info_set('up', True)])

        self.fold_button.place(x=550, y=550, height=40, width=70)
        self.call_check_button.place(x=630, y=550, height=40, width=70)
        self.raise_button.place(x=710, y=550, height=40, width=70)

    def set_raise_val(self, val):
        player_dict_set('raise_amount', val)
        game_info_set('up', True)

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

    def exit(self):

        self.running = False

    def update_players(self):
        # self.pl_list = sio.emit('active_player_list', '1')
        self.pl_list = sio.call(event='active_player_list', data=player_dict_get('room_name'))
        min_bet = int(player_dict_get('minimumBet'))

        bal = int(player_dict_get('balance'))
        inv = int(player_dict_get('investment'))

        if bal + inv <= min_bet:
            self.raise_slider.config(from_=int(0))
            self.raise_slider.config(to=int(0))
        else:
            # If we constraint from to min_bet in cases w
            self.raise_slider.config(from_=int(0))
            self.raise_slider.config(to=int(bal - (min_bet - inv)))

        if player_dict_get('my_turn'):
            self.raise_button["state"] = 'normal'
            self.fold_button["state"] = 'normal'
            self.call_check_button["state"] = 'normal'
        else:
            self.raise_button["state"] = 'disabled'
            self.fold_button["state"] = 'disabled'
            self.call_check_button["state"] = 'disabled'

        if self.pl_list is not None:
            for counter, pl in enumerate(self.pl_list):
                self.pl_text[counter].set(pl['_name'])
                self.bal_text[counter].set(pl['_balance'])
                # print(pl['_name'])

        for counter, t in enumerate(self.pl_text):
            x_player = 400 - self.pl_label_width / 2 - self.pl_x[counter]
            x_balance = 400 - self.bal_label_width / 2 - self.pl_x[counter]
            y_player = self.pl_y[counter]
            y_balance = self.pl_y[counter] + 20
            self.pl_label[counter].place(x=x_player, y=y_player, width=self.pl_label_width, height=20)
            self.bal_label[counter].place(x=x_balance, y=y_balance, width=self.bal_label_width, height=20)
            if t.get() == '':
                self.pl_label[counter].config(bg="gray")
                self.bal_label[counter].config(bg="gray")
            else:
                self.pl_label[counter].config(bg="white")
                self.bal_label[counter].config(bg="white")

        for counter, pl in enumerate(self.pl_list):
            if pl['_isFolded']:
                self.pl_label[counter].config(bg="gray")
                self.bal_label[counter].config(bg="gray")
            else:
                self.pl_label[counter].config(bg="white")
                self.bal_label[counter].config(bg="white")

        card1_path = ""
        if player_dict_get("card1") != "":
            temp = player_dict_get("card1").split()
            if temp[3] == "11":
                temp[3] = "jack"
            if temp[3] == "12":
                temp[3] = "queen"
            if temp[3] == "13":
                temp[3] = "king"
            if temp[3] == "14":
                temp[3] = "ace"
            card1_path = game_info_get('cwd') + "/res/" + temp[3] + "_of_" + temp[1].lower() + "s.png"
            self.card1_image = Image.open(card1_path)
            self.card1_image = self.card1_image.resize((50, 50), Image.ANTIALIAS)
            self.card1_image = ImageTk.PhotoImage(self.card1_image)
            self.card1_label = tk.Label(self, image=self.card1_image)
            seat = 0
            for counter, pl in enumerate(self.pl_list):
                if pl["_name"] == player_dict_get("name"):
                    seat = counter
            self.card1_label.place(x=self.card1_x[seat], y=self.card1_y[seat], width=50, height=50)

        p = 0
        for pl in self.pl_list:
            p += pl['_investment']
        game_info_set('pot', p)
        self.pot_label = tk.Label(self, text="Pot: " + str(game_info_get('pot')))
        self.pot_label.place(x=300, y=360, width=200, height=20)

        self.min_bet_text.set('Minimum bet: ' + str(player_dict_get('minimumBet')))
        self.min_bet_label = tk.Label(self, textvariable=self.min_bet_text)
        self.min_bet_label.place(x=300, y=380, width=200, height=20)

        self.dealer_text.set('Dealer: ' + str(game_info_get('dealer')))
        self.dealer_label = tk.Label(self, textvariable=self.dealer_text)
        self.dealer_label.place(x=300, y=400, width=200, height=20)

        self.small_blind_text.set('Small blind: ' + str(game_info_get('small_blind')))
        self.small_blind_label = tk.Label(self, textvariable=self.small_blind_text)
        self.small_blind_label.place(x=300, y=420, width=200, height=20)

        self.big_blind_text.set('Big blind: ' + str(game_info_get('big_blind')))
        self.big_blind_label = tk.Label(self, textvariable=self.big_blind_text)
        self.big_blind_label.place(x=300, y=440, width=200, height=20)

        self.round_num_text.set('Round: ' + str(game_info_get('round_num')))
        self.round_num_label = tk.Label(self, textvariable=self.round_num_text)
        self.round_num_label.place(x=700, y=0, width=100, height=20)

        self.won_the_pot_text.set(game_info_get('won_message'))
        self.round_num_label = tk.Label(self, textvariable=self.won_the_pot_text)
        self.round_num_label.place(x=0, y=560, height=20)

        card2_path = ""
        if player_dict_get("card2") != "":
            temp = player_dict_get("card2").split()
            if temp[3] == "11":
                temp[3] = "jack"
            if temp[3] == "12":
                temp[3] = "queen"
            if temp[3] == "13":
                temp[3] = "king"
            if temp[3] == "14":
                temp[3] = "ace"
            card2_path = game_info_get('cwd') + "/res/" + temp[3] + "_of_" + temp[1].lower() + "s.png"
            self.card2_image = Image.open(card2_path)
            self.card2_image = self.card2_image.resize((50, 50), Image.ANTIALIAS)
            self.card2_image = ImageTk.PhotoImage(self.card2_image)
            self.card2_label = tk.Label(self, image=self.card2_image)
            seat = 0
            for counter, pl in enumerate(self.pl_list):
                if pl["_name"] == player_dict_get("name"):
                    seat = counter
            self.card2_label.place(x=self.card2_x[seat], y=self.card2_y[seat], width=50, height=50)
        # Update player turn
        self.curr_player_text.set("Waiting on: " + game_info_get('curr_turn'))

        # Update call/check text
        self.call_check_text.set(player_dict_get('checkOrCall'))
        if self.call_check_text.get() == "Call":
            self.call_check_text.set("Call " + str(player_dict_get("minimumBet")))

        for counter, c in enumerate(self.board_card_label):
            if game_info['board'][counter] == '':
                c = tk.Label(self, image=self.card_back_image, bg="black")
                c.place(x=self.board_card_x[counter], y=self.board_card_y[counter], width=50, height=80)
            else:
                temp = game_info['board'][counter].split()
                if temp[1] == "11":
                    temp[1] = "jack"
                if temp[1] == "12":
                    temp[1] = "queen"
                if temp[1] == "13":
                    temp[1] = "king"
                if temp[1] == "14":
                    temp[1] = "ace"
                path = game_info_get('cwd') + "/res/" + temp[1] + "_of_" + temp[0].lower() + "s.png"

                self.board_card_image[counter] = Image.open(path)
                self.board_card_image[counter] = self.board_card_image[counter].resize((40, 70), Image.ANTIALIAS)
                self.board_card_image[counter] = ImageTk.PhotoImage(self.board_card_image[counter])
                c = tk.Label(self, image=self.board_card_image[counter], bg="white")
                c.place(x=self.board_card_x[counter], y=self.board_card_y[counter], width=50, height=80)

        # self.card1_image = tk.PhotoImage(file=card1_path)
        # self.card2_image = tk.PhotoImage(file=card2_path)

        self.update()

        # self.after(2000, self.update_players)


def update():
    print("hi")


def main():
    # Start main loop
    app = GatorHoldEm()
    app.mainloop()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt as e:
        sys.exit(0)
