import socketio
import eventlet
from room import Room
from player import Player

# installing the libraries above
# pip install "python-socketio[client]"
# pip install python-socketio
# pip install eventlet

# ssh root@172.105.150.126
# Qwerty123
# project in root/GatorHoldEm
# Git initialized so pull when changes occur

roomList = []
sio = socketio.Server()
app = socketio.WSGIApp(sio)

allowConnections = True

@sio.event
def connect(sid, environ):
    print(sid, "in lobby")


@sio.event
def disconnect(sid):
    room = find_room(sid)
    player_list = room.get_player_list()
    player = next((player for player in player_list if player.get_client_number() == sid), None)
    if player is not None:
        room.remove_player(player)
        sio.emit('user_disconnect', (player.get_name() + " has left the room!"), room=room.room_id, skip_sid=sid)
    player_list = room.get_player_list()
    if len(player_list == 0):
        roomList.remove(room)
    print('disconnect', sid)


@sio.on('my_name')
def on_event(sid, name, room_id):
    room = next((room for room in roomList if room.room_id == room_id), None)
    room.add_player(Player(sid, name, False))
    sio.emit('user_connection', (name + " has joined the room!"), room=room_id, skip_sid=sid)


@sio.event
def goto_room(sid, room_id):
    find_room = next((room for room in roomList if room.room_id == room), None)
    if find_room is None:
        roomList.append(Room(room_id))
    sio.enter_room(sid, room_id)
    print(sid, "joined room", room_id)
    sio.emit('joined_room', ("You have successfully joined the room " + room_id, room_id), room=sid)


@sio.event
def leave_room(sid, room):
    sio.leave_room(sid, room)
    print(sid, "left room", room)

@sio.event
def leave_room(sid):
    print(sid)


def find_room(sid):
    for room in roomList:
        if room.player_present_sid(sid):
            return room
    return None

if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)


# sio.emit('my event', {'data': 'foobar'}, room=sid)
