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


@sio.on('active_player_list')
def on_event(id):
    room = next((room for room in roomList if room.room_id == id), None)
    if room is None:
        return None

    return room.get_player_list()

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
    if room.game_in_progress is not False and len(room.get_player_list()) == 3:
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

# return True if game can still be continued
# returns False if everybody folded
def game_loop(room):
    table = room.get_Table()
    check = len(room.get_player_list())
    fold = 0
    while check > 0:
        player = table.current_player
        is_check = True if player.investment == table.minimum_bet else False
        checkOrCall = "Check" if is_check else "Call"
        info = str(player.balance), str(player.investment), str(table.minimum_bet), str(checkOrCall)
        sio.emit('which_players_turn', player.get_name(), room=room.room_id)
        try:
            option = sio.call(event='your_turn', data=info, sid=player.get_client_number())
        except e as TimeoutError:
            pass
        sio.emit('player_action', player.get_name, option, room=room.room_id)
        if int(option) == 1:
            player.change_balance(-(table.minimum_bet - player.investment))
            table.add_to_pot(table.minimum_bet - player.investment)
            player.add_investment(table.minimum_bet - player.investment)
            if is_check:
                check -=1
        if int(option) == 2:
            player.fold()
            fold += 1
            check -= 1
        if int(option) == 3:
            check = len(room.get_player_list()) - fold
            # _raise = Ask player how much raise
            ask = "By how much do you want to raise"
            _raise = sio.call(event = 'raise', data = ask, sid = player.get_client_number())
            table.change_minimum_bet(int(_raise))
            player.change_balance(-(table.minimum_bet - player.investment))
            table.add_to_pot(table.minimum_bet - player.investment)
            player.add_investment(table.minimum_bet - player.investment)
        
        
        folded = 0
        for p in room.get_player_list():
            if p.isFolded:
                folded += 1
        if len(room.get_player_list()) - folded <= 1:
            for p in room.get_player_list():
                if not p.isFolded:
                    p.change_balance(table.pot)
            return False
        table.next_player() #++player

    return True

def show(room):
    table = room.get_Table()
    for player in room.get_player_list():
        if player.isFolded:
                continue
        else:
            play = table.play(player.hand + table._visible_cards)
            player.set_best_hand(play[0])
            player.set_best_sum(play[1])
            sio.emit('message', "Your best hand: " + str(player.best_hand), room = player.get_client_number())
            sio.emit('message', "Your best sum: " + str(player.best_sum), room = player.get_client_number())
    max_combination = max(p.best_hand for p in room.get_player_list())
    max_sum = max(p.best_sum for p in room.get_player_list()if p.best_hand == max_combination)
    ties_with_max = [p for p in room.get_player_list() if p.best_hand == max_combination and p.best_sum == max_sum]

    if len(ties_with_max) == 1: # if one player wins whole pot, no ties
        ties_with_max[0].change_balance(table.pot)
        sio.emit('message', str(ties_with_max[0]) + " has won the pot: " + str(table.pot) + "\n", room = room.room_id)
    else:
        # TODO BE MODIFIED TO CHECK FOR TIE BREAKERS
        split = table.pot / len(ties_with_max)
        for p in ties_with_max:
            p.change_balance(split)
            sio.emit('message', str(p) + "has won a split of the pot: " + str(split) + "\n", room = room.room_id)

def start_game(room):
    room.game_in_progress = True
    sio.emit('message', "game starting", room=room.room_id)
    table = room.get_Table()
    
    while True:
        isBroke = 0
        for player in room.get_player_list():
            if player.balance == 0:
                isBroke += 1
        if len(room.get_player_list()) - isBroke == 1:
            break
        else :
            table.new_round()
            sio.emit('message', "Round: " + str(Table.theRound), room = room.room_id)
            table.distribute_cards()
            small_blind = str(table.small_blind) + " is the small blind"
            big_blind = str(table.big_blind) + " is the big blind"
            dealer = str(table._dealer) + " is the dealer"
            for player in room.get_player_list():
                card_string = str(player.hand[0]), str(player.hand[1])
                sio.emit('emit_hand', card_string, room=player.get_client_number())
            sio.emit('message', dealer, room=room.room_id)
            sio.emit('message', small_blind, room=room.room_id)
            sio.emit('message', big_blind, room=room.room_id)
            
            if not game_loop(room):
                continue 
            
            sio.emit('message', "---------THE FLOP----------\n", room = room.room_id)
            table._deck.pick_card() #the burn card
            table.add_to_visible_cards(table._deck.pick_card()) 
            table.add_to_visible_cards(table._deck.pick_card())   #The FLOP - three cards
            table.add_to_visible_cards(table._deck.pick_card())
            visibleCards = str(table._visible_cards[0]) + str(table._visible_cards[1]) + str(table._visible_cards[2])
            sio.emit('message', visibleCards, room = room.room_id)
            
            if not game_loop(room):
                continue
            
            sio.emit('message', "---------THE TURN----------\n", room = room.room_id)
            table._deck.pick_card() #the burn card
            table.add_to_visible_cards(table._deck.pick_card()) #The TURN - one card
            visibleCards += str(table._visible_cards[3])
            sio.emit('message', visibleCards, room = room.room_id)

            if not game_loop(room):
                continue
            
            sio.emit('message', "---------THE RIVER----------\n", room = room.room_id)
            table._deck.pick_card() #the burn card
            table.add_to_visible_cards(table._deck.pick_card()) #The RIVER - one card
            visibleCards += str(table._visible_cards[4])
            sio.emit('message', visibleCards, room = room.room_id)
            
            if not game_loop(room):
                continue
            
            show(room)


if __name__ == '__main__':
    try:
        eventlet.wsgi.server(eventlet.listen(('', 5000)), app)
    except KeyboardInterrupt as e:
        sys.exit(0)
