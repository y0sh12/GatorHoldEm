import socketio

# standard Python
sio = socketio.Client()
# Test comment by Azhar

name = ""


@sio.event
def connect():
    print("Welcome", name + "!")
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
    sio.emit('my_name', (name, room))
    print(message)


def main():
    global name
    name = input("What is your name?\n")
    sio.connect('http://localhost:5000')
    # sio.connect('http://172.105.150.126:5000')
    print('Your sid is', sio.sid)
    print("You are now in the lobby")
    room = input("What room would you like to join?\n")
    sio.emit('goto_room', room)


if __name__ == '__main__':
    main()