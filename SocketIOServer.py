import socketio
import eventlet
from player import Player

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
    sio.emit('user_disconnect', (str(sid) + " has left!"))

@sio.on('my_name')
def on_message(sid, name):
    playerList.append(Player(sid, name, False))
    sio.emit('user_connection', (name + " has joined!"))

if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)


# sio.emit('my event', {'data': 'foobar'}, room=user_sid)
