import socketio
import eventlet
from player import Player

# installing the libraries above
# pip install "python-socketio[client]"
# pip install python-socketio
# pip install eventlet

# ssh root@172.105.150.126
# Qwerty123
# project in root/GatorHoldEm
# Git initialized so pull when changes occur

playerList = []
sio = socketio.Server()
app = socketio.WSGIApp(sio)

allowConnections = True

@sio.event
def connect(sid, environ):
    if len(playerList) >= 8:
        return False
    elif allowConnections:
        print('connect ', sid)
    else:
        return False

@sio.event
def disconnect(sid):
    print('disconnect', sid)
    playerLeft = next((player for player in playerList if player.client_number == sid), None)
    playerList.remove(playerLeft)
    sio.emit('user_disconnect', (str(playerLeft.name) + " has left!"))

@sio.on('my_name')
def on_event(sid, name):
    playerList.append(Player(sid, name, False))
    sio.emit('user_connection', (name + " has joined!"), skip_sid=sid)


@sio.event
def goto_room(sid, room):
    sio.enter_room(sid, room)
    print(sid, "joined room", room)


@sio.event
def leave_room(sid, room):
    sio.leave_room(sid, room)
    print(sid, "left room", room)



if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)


# sio.emit('my event', {'data': 'foobar'}, room=sid)
