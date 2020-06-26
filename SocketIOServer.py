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

# sio.call(event='active_player_list', data=room.room_id)
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
    if room.game_in_progress is False and len(room.get_player_list()) == 3:
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
        option = ''
        try:
            option = sio.call(event='your_turn', data=info, sid=player.get_client_number())
        except TimeoutError:
            pass
        sio.emit('player_action', (player.get_name(), option), room=room.room_id)

        if int(option) == 1:
            # Going all in because cannot match table bet
            if table.minimum_bet >= player.balance + player.investment:
                sio.emit('message', 'You are going all in!\n', room=player.get_client_number())
                table.add_to_pot(player.balance)
                player.add_investment(player.balance)
                player.change_balance(-player.balance)
            else:
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
            # _raise = Ask player how much raise
            error = 0
            while error < 3:
                ask = "By how much do you want to raise"
                _raise = sio.call(event = 'raise', data = ask, sid = player.get_client_number())
                if int(_raise) > player.balance:
                    sio.emit('message', "You ain't a millionaire, try a smaller raise", room=player.get_client_number())
                    error += 1
                else:
                    table.change_minimum_bet(int(_raise))
                    player.change_balance(-(table.minimum_bet - player.investment))
                    table.add_to_pot(table.minimum_bet - player.investment)
                    player.add_investment(table.minimum_bet - player.investment)
                    check = len(room.get_player_list()) - fold
                    break
            if error == 4:
                player.fold()
                fold += 1
                check -= 1


        # Counting not folded players
        active_players = 0
        for p in room.get_player_list():
            if not p.isFolded and not p.bankrupt:
                active_players += 1
        
        # If everyone  else is folded
        if active_players == 1:
           for p in room.get_player_list():
               if not p.isFolded:
                   p.change_balance(table.pot)
                   sio.emit('message', str(p) + " has won the pot: " + str(table.pot), room = room.room_id)
           return False

        
        sane_players = 0
        for p in room.get_player_list():
            # player is active and not all in
            if not p.bankrupt and not p.isFolded and p.balance != 0:
                sane_players += 1
        
        # Check edge case if everyone has gone all in
        if sane_players == 0:
            table.skip_to_show = True
            return True
                

        # Case to check if everyone *currently in game* is folded and there is only one player remaining.
        # if len(room.get_player_list()) - folded <= 1:
        #    for p in room.get_player_list():
        #        if not p.isFolded:
        #            p.change_balance(table.pot)
        #            sio.emit('message', str(p) + " has won the pot: " + str(table.pot), room = room.room_id)
        #    return False
        
        # count all broke players
        # broke = 0
        # for p in room.get_player_list():
        #     if p.balance == 0:
        #         broke += 1
        
        # Temporary fix
        # Check if all the not folded players are trying to go all in
        # if len(room.get_player_list()) - folded == broke:
        #     print()
            # Check if all player are broke
            # show()
            #    return False
            # Check if everybody is folded

        # TO DO
        # No distinction between someone who is bankrupt (out of the game) and someone who is all in.
        # add a boolean for players active()
        # generator instead of skipping over balance = 0 players, we can skip over active = false (and isFolded)

        table.next_player() #++player

    return True

def show(room):
    sio.emit('message', 'THE FINAL SHOWDOWN', room = room.room_id)
    table = room.get_Table()
    for player in room.get_player_list():
        if player.isFolded or player.bankrupt:
                continue
        else:
            play = table.play(player.hand + table._visible_cards)
            player.set_best_hand(play[0])
            player.set_best_sum(play[1])
            if play[2] != None:
                player.set_best_hand_sum(play[2])
            sio.emit('message', "Your best hand: " + str(player.best_hand), room = player.get_client_number())
            sio.emit('message', "Your best sum: " + str(player.best_sum), room = player.get_client_number())
    max_combination = max(p.best_hand for p in room.get_player_list())
    if max_combination == 2 or max_combination == 3 or max_combination == 4 or max_combination == 8:
        max_hand_sum = max(p.best_hand_sum for p in room.get_player_list() if p.best_hand == max_combination)
        max_sum = max(p.best_sum for p in room.get_player_list()if p.best_hand == max_combination and p.best_hand_sum == max_hand_sum)
        ties_with_max = [p for p in room.get_player_list() if p.best_hand == max_combination and p.best_sum == max_sum and p.best_hand_sum == max_hand_sum]
    else:
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
    
    balance_dict = {p.get_client_number():p.balance for p in room.get_player_list()}

    while True:

        # break out of the loop if all players (except one winner) are bankrupt
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
            minbet = "The minimum bet is " + str(table.minimum_bet)

            for player in room.get_player_list():
                card_string = str(player.hand[0]), str(player.hand[1])
                sio.emit('emit_hand', card_string, room=player.get_client_number())
            sio.emit('message', dealer, room=room.room_id)
            sio.emit('message', small_blind, room=room.room_id)
            sio.emit('message', big_blind, room=room.room_id)
            sio.emit('message', minbet, room = room.room_id)
            
            if not game_loop(room):
                continue 
            
            sio.emit('message', "---------THE FLOP----------\n", room = room.room_id)
            table._deck.pick_card() #the burn card
            table.add_to_visible_cards(table._deck.pick_card()) 
            table.add_to_visible_cards(table._deck.pick_card())   #The FLOP - three cards
            table.add_to_visible_cards(table._deck.pick_card())
            visibleCards = str(table._visible_cards[0]) + str(table._visible_cards[1]) + str(table._visible_cards[2])
            sio.emit('message', visibleCards, room = room.room_id)
            
            if not table.skip_to_show:
                if not game_loop(room):
                    continue
            
            sio.emit('message', "---------THE TURN----------\n", room = room.room_id)
            table._deck.pick_card() #the burn card
            table.add_to_visible_cards(table._deck.pick_card()) #The TURN - one card
            visibleCards += str(table._visible_cards[3])
            sio.emit('message', visibleCards, room = room.room_id)

            if not table.skip_to_show:
                if not game_loop(room):
                    continue
            
            sio.emit('message', "---------THE RIVER----------\n", room = room.room_id)
            table._deck.pick_card() #the burn card
            table.add_to_visible_cards(table._deck.pick_card()) #The RIVER - one card
            visibleCards += str(table._visible_cards[4])
            sio.emit('message', visibleCards, room = room.room_id)
            
            if not table.skip_to_show:
                if not game_loop(room):
                    continue
            
            show(room)
            
            # At the end of the round, declare players bankrupt if they are out of money
            for p in room.get_player_list():
                if p.balance <= 0:
                    p.declare_bankrupt()

    winner = None
    for player in room.get_player_list():
            if player.balance != 0:
                winner = player
    sio.emit('message', str(winner) + " HAS WON THE GAME AND HAS EARNED $" + str(winner.balance) + "!", room = room.room_id)


if __name__ == '__main__':
    try:
        eventlet.wsgi.server(eventlet.listen(('', 5000)), app)
    except KeyboardInterrupt as e:
        sys.exit(0)
