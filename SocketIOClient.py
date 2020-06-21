import sys
import socketio

sio = socketio.Client()
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


@sio.on('your_turn')
def on_event(balance, investment, minimumBet, checkOrCall):
    print("Your balance:", balance, "\nYour Investment:", investment,"\nMinimum Bet to Play:", minimumBet, "\n1.)", checkOrCall, "2.) Fold 3.) Raise")

@sio.on('message')
def on_event(message):
    print(message)

@sio.on('emit_hand')
def on_event(card1, card2):
    print("Your hand:", card1, card2)
    

@sio.on('connection_error')
def on_event(error):
    print("The game has started or has reached maximum player limit")

@sio.event
def name_(data):
    # print("name asked for")
    return data

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
    try:
        main()
    except KeyboardInterrupt as e:
        sys.exit(0)
