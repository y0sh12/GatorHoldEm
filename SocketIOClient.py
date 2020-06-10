import socketio

# standard Python
sio = socketio.Client()
# Test comment by Azhar

@sio.event
def connect():
    print("I'm connected!")

@sio.event
def connect_error():
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
    name = input("What is your name?")
    sio.connect('http://localhost:5000')
    print('my sid is', sio.sid)
    sio.emit('my_name', name)


if __name__ == '__main__':
    main()