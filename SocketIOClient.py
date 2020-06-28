import tkinter as tk
import sys
import socketio
from PIL import Image, ImageTk

# Dictionary that holds general player info. Variables are type of info to store & value
player_dict = {
    'name': '',
    'room_name': '',
    'room_list': [None] * 6,
    'room_list_len': 0,
    'card1': "",
    'card2': ""
}
def player_dict_set(specifier, value):
    player_dict[specifier] = value


def player_dict_get(specifier):
    return player_dict[specifier]


# SocketIO connection calls
sio = socketio.Client()


@sio.event
def connect():
    print("Welcome", player_dict_get('name') + "!")
    print("You have successfully connected to the Gator Hold \'em server!")
    print("Good Luck!")


@sio.event
def connect_error(data):
    if str(data) == "Unauthorized":
        print("The game has started or has reached maximum player limit")
    else:
        print("The connection failed!")


@sio.event
def disconnect():
    print("You have left the game. Come back soon!")


@sio.on('user_connection')
def on_event(message):
    print(message)
    update_room_list()


@sio.on('user_disconnect')
def on_event(message):
    print(message)
    update_room_list()


@sio.on('joined_room')
def on_event(message, room):
    sio.emit('my_name', (player_dict_get('name'), player_dict_get('room_name')))
    print(message)


@sio.on('your_turn')
def on_event(balance, investment, minimumBet, checkOrCall):
    choice = input(str(
        "Your balance: " + balance + " \nYour Investment: " + investment + " \nMinimum Bet to Play: " + minimumBet + " \n1.) " + checkOrCall + " 2.) Fold 3.) Raise\n"))
    return choice


@sio.on('message')
def on_event(message):
    print(message)
    if message == "game starting":
        player_dict_set('game_starting', True)


@sio.on('emit_hand')
def on_event(card1, card2):
    print("Your hand:", card1, card2)
    player_dict_set("card1", card1)
    player_dict_set("card2", card2)


@sio.on('connection_error')
def on_event(error):
    print("The game has started or has reached maximum player limit")


@sio.on('raise')
def on_event(ask):
    howMuch = input(str(ask + "\n"))
    return howMuch


@sio.on('which_players_turn')
def on_event(data):
    print(data, 'has to go')


@sio.on('player_action')
def on_event(player, option):
    print(player, 'chose option', option)


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
        self.geometry('800x600')

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
        # Title
        self.title = tk.Label(self, font=(None, 24), text="GatorHoldEm", height=3, width=20, fg="black")
        self.title.grid(row=0, column=1, padx=100, pady=50, sticky='S')

        # Name label
        self.name_label = tk.Label(self, text="Enter your name here:", foreground="black")
        self.name_label.grid(row=1, column=0)

        # Name input
        self.name_entry = tk.Entry(self, fg="black", bg="white", width=50)
        self.name_entry.grid(row=1, column=1)

        # Room label
        self.room_label = tk.Label(self, text="Enter name of room to join:", foreground="black")
        self.room_label.grid(row=2, column=0)

        # Room input
        self.room_entry = tk.Entry(self, fg="black", bg="white", width=50)
        self.room_entry.grid(row=2, column=1)

        # Submit button
        self.submit = tk.Button(self, text="Submit", bg="blue", width=25, command=self.handle_click)
        self.submit.grid(row=3, column=1, padx=0, pady=25)

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
        sio.connect('http://localhost:5000')
        sio.emit('goto_room', player_dict_get('room_name'))

        # If successful, update room members and display lobby page
        update_room_list()

        # Start game if there are three people in the lobby, else continue to lobby
        if player_dict_get('room_list_len') == 3:
            self.controller.show_frame(Game)
        else:
            self.controller.show_frame(Lobby)


class Lobby(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Lobby title
        self.lobby_title = tk.Label(self, text='Lobby')
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
                                        command=lambda: self.controller.show_frame(Game))
        self.start_the_game.pack(pady=10)

        self.update()

    def update(self):
        if sio.connected:
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
        self.background_image = tk.PhotoImage(file="./res/felt.png")
        self.background_label = tk.Label(self, image=self.background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.back_to_home = tk.Button(self, text="Back to Lobby",
                                      command=lambda: [self.exit(), controller.show_frame(Lobby)])
        self.back_to_home.pack()
        self.pl_list = []
        self.pl_text = [tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar()]
        self.bal_text = [tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar()]

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

        self.card1_image = 0
        self.card1_label = 0
        self.card2_label = 0
        self.card2_image = 0

        self.pl_x = [0, 300, 300, 0, -300, -300]
        self.pl_y = [540, 440, 240, 140, 240, 440]
        self.card1_x = [350, 50, 50, 350, 650, 650]
        self.card1_y = [490, 390, 190, 90, 190, 390]
        self.card2_x = [400, 100, 100, 400, 700, 700]
        self.card2_y = [490, 390, 190, 90, 190, 390]

        self.button = tk.Button(self, text="players", bg="blue", width=25, command=self.up)
        self.button.pack()

        self.pl_label_width = 100
        self.bal_label_width = 50


    def up(self):
        self.running = True
        while self.running:
            self.after(100, self.update_players())
            #print(player_dict_get("card1"))

    def exit(self):

        self.running = False

    def update_players(self):
        # self.pl_list = sio.emit('active_player_list', '1')
        for counter, t in enumerate(self.pl_text):
            t.set("")
            x_player = 400 - self.pl_label_width/2 - self.pl_x[counter]
            x_balance = 400 - self.bal_label_width/2 - self.pl_x[counter]
            y_player = self.pl_y[counter]
            y_balance = self.pl_y[counter]+20
            self.pl_label[counter].place(x=x_player, y=y_player, width=self.pl_label_width, height=20)
            self.bal_label[counter].place(x=x_balance, y=y_balance, width=self.bal_label_width, height=20)
        self.pl_list = sio.call(event='active_player_list', data=player_dict_get('room_name'))
        if self.pl_list is not None:
            for counter, pl in enumerate(self.pl_list):
                self.pl_text[counter].set(pl['_name'])
                self.bal_text[counter].set(pl['_balance'])
                # print(pl['_name'])
        else:
            print("empty")
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
            card1_path = "./res/" + temp[3] + "_of_" + temp[1].lower() + "s.png"
            self.card1_image = Image.open(card1_path)
            self.card1_image = self.card1_image.resize((50, 50), Image.ANTIALIAS)
            self.card1_image = ImageTk.PhotoImage(self.card1_image)
            self.card1_label = tk.Label(self, image=self.card1_image)
            seat = 0
            for counter, pl in enumerate(self.pl_list):
                if pl["_name"] == player_dict_get("name"):
                    seat = counter
            self.card1_label.place(x=self.card1_x[seat], y=self.card1_y[seat], width=50, height=50)

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
            card2_path = "./res/" + temp[3] + "_of_" + temp[1].lower() + "s.png"
            self.card2_image = Image.open(card2_path)
            self.card2_image = self.card2_image.resize((50, 50), Image.ANTIALIAS)
            self.card2_image = ImageTk.PhotoImage(self.card2_image)
            self.card2_label = tk.Label(self, image=self.card2_image)
            seat = 0
            for counter, pl in enumerate(self.pl_list):
                if pl["_name"] == player_dict_get("name"):
                    seat = counter
            self.card2_label.place(x=self.card2_x[seat], y=self.card2_y[seat], width=50, height=50)

        # self.card1_image = tk.PhotoImage(file=card1_path)
        # self.card2_image = tk.PhotoImage(file=card2_path)





        self.update()




        #self.after(2000, self.update_players)



def update():
    print("hi")


def main():
    # Start main loop
    app = GatorHoldEm()
    app.mainloop()

    # Example client code
    # global name
    # name = input("What is your name?\n")
    # sio.connect('http://localhost:5000')
    # # sio.connect('http://172.105.150.126:5000')
    # print('Your sid is', sio.sid)
    # print("You are now in the lobby")
    # room = input("What room would you like to join?\n")
    # sio.emit('goto_room', room)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt as e:
        sys.exit(0)
