import socketio

# standard Python
sio = socketio.Client()
# Test comment by Azhar

name = ""


@sio.event
def connect():
    print("I'm connected!")
    sio.emit('my_name', name)


@sio.event
def connect_error(data):
    if str(data) == "Unauthorized":
        print("The game has started or has reached maximum player limit")
    else:
        print("The connection failed!")


@sio.event
def disconnect():
    print("I'm disconnected!")


@sio.on('user_connection')
def on_message(data):
    print(data)


@sio.on('user_disconnect')
def on_message(data):
    print(data)


def main():
    global name
    name = input("What is your name?")
    # sio.connect('http://localhost:5000')
    sio.connect('http://172.105.150.126:5000')
    print('my sid is', sio.sid)


if __name__ == '__main__':
    main()