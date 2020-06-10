import socketio
import eventlet
from player import Player

# installing the libraries above
# pip install "python-socketio[client]"
# pip install python-socketio
# pip install eventlet

playerList = []
# create a Socket.IO server
sio = socketio.Server()
app = socketio.WSGIApp(sio)

@sio.event
def connect(sid, environ):
    print('connect ', sid)


@sio.event
def disconnect(sid):
    print('disconnect', sid)
    playerLeft = next((player for player in playerList if player.client_number == sid), None)
    sio.emit('user_disconnect', (str(playerLeft.name) + " has left!"))

@sio.on('my_name')
def on_message(sid, name):
    playerList.append(Player(sid, name, False))
    sio.emit('user_connection', (name + " has joined!"))

if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)


# sio.emit('my event', {'data': 'foobar'}, room=sid)
