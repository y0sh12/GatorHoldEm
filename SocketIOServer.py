import sys
import socketio
import eventlet
from room import Room
from player import Player
from table import Table

roomList = []
sio = socketio.Server()
app = socketio.WSGIApp(sio)


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
    if len(player_list) == 0:
        roomList.remove(room)
    print('disconnect', sid)


@sio.on('my_name')
def on_event(sid, name, room_id):
    room = next((room for room in roomList if room.room_id == room_id), None)
    room.add_player(Player(sid, name, False))
    print(room.get_player_list())
    sio.emit('user_connection', (name + " has joined the room!"), room=room_id, skip_sid=sid)
    if room.game_in_progress == False and len(room.get_player_list()) == 3:
        start_game(room)


@sio.event
def goto_room(sid, room_id):
    find_room = next((room for room in roomList if room.room_id == room_id), None)
    if find_room is None:
        roomList.append(Room(room_id))
        find_room = roomList[-1]
    print (find_room.room_id)
    print (find_room.get_player_list())
    # temporary code to only have a max of 3 ppl per room
    if len(find_room.get_player_list()) < 3:
        sio.enter_room(sid, room_id)
        print(sid, "joined room", room_id)
        sio.emit('joined_room', ("You have successfully joined the room " + room_id, room_id), room=sid)
    else:
        sio.emit('connection_error', "Unauthorized", room=sid)



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


def start_game(room):
    room.game_in_progress = True
    sio.emit('message', "game starting", room=room.room_id)
    table = room.get_Table()
    table.new_round()
    table.distribute_cards()
    small_blind = str(table.small_blind) + " is the small blind"
    big_blind = str(table.big_blind) + " is the big blind"
    for player in room.get_player_list():
        card_string = str(player.hand[0]), str(player.hand[1])
        sio.emit('emit_hand', card_string, room=player.get_client_number())
    sio.emit('message', small_blind, room=room.room_id)
    sio.emit('message', big_blind, room=room.room_id)


if __name__ == '__main__':
    try:
        eventlet.wsgi.server(eventlet.listen(('', 5000)), app)
    except KeyboardInterrupt as e:
        sys.exit(0)
