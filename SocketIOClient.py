import tkinter as tk
import sys
import socketio

# Dictionary that holds general player info. Variables are type of info to store & value
player_dict = {
    'name': '',
    'room_name': ''
}


def player_dict_set(specifier, value):
    player_dict[specifier] = value


def player_dict_get(specifier):
    return player_dict[specifier]


# SocketIO connection calls
sio = socketio.Client()


@sio.event
def connect():
    print("Welcome", player_dict["name"] + "!")
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


@sio.on('user_disconnect')
def on_event(message):
    print(message)


@sio.on('joined_room')
def on_event(message, room):
    sio.emit('my_name', (player_dict["name"], player_dict["room_name"]))
    print(message)


@sio.on('your_turn')
def on_event(balance, investment, minimumBet, checkOrCall):
    choice = input(str("Your balance: " + balance + " \nYour Investment: " + investment + " \nMinimum Bet to Play: " + minimumBet + " \n1.) " + checkOrCall + " 2.) Fold 3.) Raise\n"))
    return choice


@sio.on('message')
def on_event(message):
    print(message)


@sio.on('emit_hand')
def on_event(card1, card2):
    print("Your hand:", card1, card2)


@sio.on('connection_error')
def on_event(error):
    print("The game has started or has reached maximum player limit")


class GatorHoldEm(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("GatorHoldEm")
        self.geometry('800x600')

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

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

        self.button = tk.Button(self, text="Submit", bg="blue", width=25, command=self.handle_click)
        self.button.grid(row=3, column=1, padx=0, pady=25)

    # Widget event handlers
    # def handle_keypress(self, event):
    #     print(event.char)

    def handle_click(self):
        # Error check for proper name and room inputs
        if self.name_entry.get() == '' or self.room_entry.get() == '':
            print("Invalid entry. Try again!")
            return

        player_dict_set("name", self.name_entry.get())
        player_dict_set("room_name", self.room_entry.get())
        print(player_dict_get('room_name'))

        # Server call to create new player and join/create room, error handling
        sio.connect('http://localhost:5000')
        sio.emit('goto_room', player_dict_get('room_name'))

        # If successful, proceed to lobby page
        self.controller.show_frame(Lobby)


class Lobby(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.label = tk.Label(self, text='Lobby')
        self.label.pack(padx=10, pady=10)

        self.back_to_home = tk.Button(self, text="Back to Home",
                                      command=lambda: controller.show_frame(MainMenu))
        self.back_to_home.pack()

        self.back_to_home = tk.Button(self, text="Start the Game!",
                                      command=lambda: controller.show_frame(Game))
        self.back_to_home.pack()


class Game(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.label = tk.Label(self, text="Game page!!")
        self.label.pack(padx=10, pady=10)

        self.back_to_home = tk.Button(self, text="Back to Home",
                                      command=lambda: controller.show_frame(MainMenu))
        self.back_to_home.pack()


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
