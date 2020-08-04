import copy
import sys
import os
import eventlet
import socketio
import pathlib
from .player import Player
from .room import Room
from .table import Table
from .ai import AI
import time
import random
import string
import math

roomList = []


sio = socketio.Server()
app = socketio.WSGIApp(sio)


@sio.event
def connect(sid, environ):
    print(sid, "in lobby")


@sio.on('active_player_list')
def on_event(sid, room_id):
    room = next((room for room in roomList if room.room_id == room_id), None)
    if room is None:
        print("room does not exist")
        return None
    pl_list = []
    for pl in room.get_player_list():
        if pl.AI:
            temp_pl = Player(pl._client_number, False, pl.get_name(), True)
            temp_pl._isFolded = pl.isFolded
            temp_pl._investment = pl.investment
            temp_pl._bankrupt = pl.bankrupt
            temp_pl._balance = pl.balance
        else:
            temp_pl = copy.deepcopy(pl)

        temp_pl.hand = []
        pl_list.append(temp_pl.__dict__)
    return pl_list


@sio.on('in_room')
def in_room(sid, data):
    name = data[0]
    room_id = data[1]
    room = next((room for room in roomList if room.room_id == room_id), None)
    player_list = room.get_player_list()
    player = next((player for player in player_list if player.get_name() == name), None)
    if player is None:
        return False
    else:
        return True


# gui should make sure that only vip players can do this action
# pass the room object not the room_id
@sio.on('add_bot')
def add_bot(sid, room_id):
    room = next((room for room in roomList if room.room_id == room_id), None)
    sample = string.ascii_lowercase + string.digits
    ai_code = ''.join(random.choice(sample) for i in range(32))
    ai_player = AI(ai_code, False, "AI BOT", True)
    ai_player._connected = False
    room.add_player(ai_player)
    sio.emit('ai_joined', room=room.room_id)


@sio.event
def disconnect(sid):
    # If everyone disconnects empty the room of players and delete room for roomList
    room = find_room(sid)
    if room is not None:
        player_list = room.get_player_list()
        player = next((player for player in player_list if player.get_client_number() == sid), None)

        player._balance = 0
        player._investment = 0
        player.declare_bankrupt()
        player._connected = False

        # If game in progress, just make sure that there are at least two active players
        if room.game_in_progress:
            pass
            # room.game_in_progress = False
            connected_players = sum([1 for p in room.get_player_list() if p._connected])
            # O human player, deleted the room
            if connected_players == 0:
                room.game_in_progress = False
                for p in room.get_player_list()[:]:
                    room.remove_player(p)
                roomList.remove(room)
                return
            ai_num = sum([1 for p in room.get_player_list() if p.AI == True])
            # If one human player,
            if connected_players + ai_num <= 1:
                sio.emit('game_ended', "The game has ended.", room=room.room_id)
                room.game_in_progress = False

        else:
            # We are in lobby
            # print("We are not in a game")
            is_vip_ = player.is_vip
            # Remove diconnecting player
            room.remove_player(player)

            # count ai players in room
            ai_players = sum([1 for p in room.get_player_list() if p.AI == True])


            # If player disconnecting is vip
            if is_vip_:
                # Set VIP to other person not AI
                for p in room.get_player_list():
                        if not p.AI:
                            p.is_vip = True
                            # print("We have a new vip: ", p)
                            sio.emit('vip', room=p.get_client_number())
                            break

        ai_players = sum([1 for p in room.get_player_list() if p.AI == True])
        # No players in room or all players in room are AI
        if len(room.get_player_list()) == 0 or ai_players == len(room.get_player_list()):
            roomList.remove(room)


        print('disconnect', sid)


@sio.on('remove_player')
def remove_player(sid, data):
    room_id = data[0]
    index = data[1]
    room = next((room for room in roomList if room.room_id == room_id), None)
    if room is not None:
        player_list = room.get_player_list()
        player = player_list[index]
        if player is not None:
            if player.AI is False:
                client_id = player.get_client_number()
                if client_id == sid:
                    return True
                else:
                    sio.disconnect(client_id)
                    return False
            else:
                room.remove_player(player)
                return False


@sio.on('my_name')
def on_event(sid, name, room_id):
    room = next((room for room in roomList if room.room_id == room_id), None)
    if len(room.get_player_list()) == 0:
        print("vip")
        room.add_player(Player(sid, True, name))
        sio.emit('vip', room=sid)
    else:
        room.add_player(Player(sid, False, name))

    sio.emit('user_connection', (name + " has joined the room!"), room=room_id, skip_sid=sid)


@sio.event
def goto_room(sid, room_id):
    find_room = next((room for room in roomList if room.room_id == room_id), None)
    if find_room is None:
        roomList.append(Room(room_id))
        find_room = roomList[-1]

    if len(find_room.get_player_list()) < 6 and find_room.game_in_progress is False:
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


@sio.on('start_game')
def start_game(sid, room_id):
    room = next((room for room in roomList if room.room_id == room_id), None)
    if room is not None and room.game_in_progress:
        return

    room.game_in_progress = True
    sio.emit('message', "Game Starting...", room=room.room_id)
    table = room.get_Table()

    balance_dict = {p.get_client_number(): p.balance for p in room.get_player_list()}

    while True:
        #If everyone is bakrupt get out
        isBroke = 0
        for player in room.get_player_list():
            if player.balance == 0:
                isBroke += 1
        if len(room.get_player_list()) - isBroke == 1:
            break
        else:
            table.new_round()
            sio.emit('new_hand')
            table.distribute_cards()

            small_blind = str(table.small_blind.get_client_number())
            big_blind = str(table.big_blind.get_client_number())
            dealer = str(table.dealer.get_client_number())
            min_bet = str(table.minimum_bet)
            round_num = str(Table.theRound)

            #
            for player in room.get_player_list():
                if not player.bankrupt:
                    card_string = str(player.hand[0]), str(player.hand[1])
                    sio.emit('emit_hand', card_string, room=player.get_client_number())

            sio.emit('board_init_info', [dealer, small_blind, big_blind, min_bet, round_num], room=room.room_id)
            if not game_loop(room):
                continue

            table._deck.pick_card()  # the burn card
            table.add_to_visible_cards(table._deck.pick_card())
            table.add_to_visible_cards(table._deck.pick_card())  # The FLOP - three cards
            table.add_to_visible_cards(table._deck.pick_card())
            visibleCards = str(table._visible_cards[0]) + " " + str(table._visible_cards[1]) + " " + str(
                table._visible_cards[2])
            sio.emit('flop', visibleCards, room=room.room_id)

            table.change_last_action()

            # Change the first player to player left of last action player.
            while True:
                first_player = next(table._dealer_gen_obj)
                if not first_player.isFolded:
                    while True:
                        if table.current_player == first_player:
                            break
                        else:
                            table.next_player()
                    break

            # Point dealer generator back to dealer
            while True:
                current_d = next(table._dealer_gen_obj)
                if current_d == table.dealer:
                    break

            if not table.skip_to_show:
                if not game_loop(room):
                    continue

            table._deck.pick_card()  # the burn card
            table.add_to_visible_cards(table._deck.pick_card())  # The TURN - one card
            visibleCards += " " + str(table._visible_cards[3])
            sio.emit('turn', visibleCards, room=room.room_id)

            if not table.skip_to_show:
                if not game_loop(room):
                    continue

            table._deck.pick_card()  # the burn card
            table.add_to_visible_cards(table._deck.pick_card())  # The RIVER - one card
            visibleCards += " " + str(table._visible_cards[4])
            sio.emit('river', visibleCards, room=room.room_id)

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
    sio.emit('message', str(winner) + " has won the game!",
             room=room.room_id)

    room.game_in_progress = False
    sio.emit('game_ended', "The game has ended.", room=room.room_id)



def find_room(sid):
    for room in roomList:
        if room.player_present_sid(sid):
            return room
    return None


# return True if game can still be continued
# returns False if everybody folded
def game_loop(room, num_raises=0):
    table = room.get_Table()
    bankrupt_players = sum([1 for p in room.get_player_list() if p.bankrupt])
    folded = sum([1 for p in room.get_player_list() if p.isFolded])
    check = len(room.get_player_list()) - bankrupt_players - folded
    last_action_was_fold = False
    # number of opponents
    num_of_opponents = check - 1

    while True:
        player = table.current_player
        is_check = True if player.investment == table.minimum_bet else False
        checkOrCall = "Check" if is_check else "Call"
        info = str(player.balance), str(player.investment), str(table.minimum_bet), str(checkOrCall)
        sio.emit('which_players_turn', [player.get_client_number(), str(table.minimum_bet)], room=room.room_id)
        if player.AI:
            option = player.make_choice(num_of_opponents, player.hand, table.visible_cards, table.pot, table.minimum_bet - player.investment, player.investment)
            pass
        else:
            try:
                option = sio.call(event='your_turn', data=info, sid=player.get_client_number(), timeout = 300)
            except:
                print("Client failed to respond")
                if is_check:
                    sio.emit('message', str(player.name) + " has been forced to check", room = room.room_id)
                    option = 1
                else:
                    sio.emit('message', str(player.name) + " has been forced to fold", room = room.room_id)
                    option = 2
                sio.emit('you_timed_out')
        sio.emit('player_action', (player.get_name(), option), room=room.room_id)
        if int(option) == 1:
            # Going all in because cannot match table bet
            if table.minimum_bet >= player.balance + player.investment:
                sio.emit('message', str(player.name) + " is going all in!", room = room.room_id)
                table.add_to_pot(player.balance)
                player.add_investment(player.balance)
                player.change_balance(-player.balance)
            else:
                if is_check:
                    sio.emit('message', str(player.name) + " checked", room = room.room_id)
                else:
                    sio.emit('message', str(player.name) + " called", room = room.room_id)
                player.change_balance(-(table.minimum_bet - player.investment))
                table.add_to_pot(table.minimum_bet - player.investment)
                player.add_investment(table.minimum_bet - player.investment)
            # if is_check:
            check -= 1

        if int(option) == 2:
            if player == table.last_action:

                # modify last action to player to the right.
                prev = table.current_player
                table.next_player()
                current = table.current_player
                while True:
                    if current == player:
                        break
                    else:
                        prev = current
                        table.next_player()
                        current = table.current_player
                if not check <= 1:
                    table._last_action = prev
                else:
                    last_action_was_fold = True

            player.fold()
            sio.emit('message', str(player.name) + " has folded", room = room.room_id)
            folded += 1
            check -= 1
        if int(option) == 3:

            error = 0
            while error < 3:
                ask = "By how much do you want to raise"
                if player.AI:
                    _raise = math.floor(player.make_raise(table.minimum_bet, player.balance))
                    _raise = _raise - (_raise % 5)
                    pass  
                else:
                    _raise = sio.call(event='raise', data=ask, sid=player.get_client_number())
                if int(_raise) > player.balance:
                    # sio.emit('message', "You ain't a millionaire, try a smaller raise", room=player.get_client_number())
                    error += 1
                else:
                    sio.emit('message', str(player.name) + " has raised by $" + str(_raise), room = room.room_id)
                    table.change_minimum_bet(int(_raise))
                    player.change_balance(-(table.minimum_bet - player.investment))
                    table.add_to_pot(table.minimum_bet - player.investment)
                    player.add_investment(table.minimum_bet - player.investment)
                    check = len(room.get_player_list()) - folded - bankrupt_players
                    break
            if error == 4:
                player.fold()
                sio.emit('message', str(player.name) + " has folded", room = room.room_id)
                folded += 1
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
                    sio.emit('message', str(p) + " has won the pot: $" + str(table.pot), room=room.room_id)
            return False

        sane_players = 0
        for p in room.get_player_list():
            # player is active and not all in
            if not p.bankrupt and not p.isFolded and p.balance != 0:
                sane_players += 1

        # Check edge case if everyone has gone all in
        if sane_players <= 1:
            table.skip_to_show = True
            return True

        if check <= 1 and player == table.last_action:
            if last_action_was_fold:
                table._last_action = prev
            table.next_player()
            break

        table.next_player()  # ++player

    return True


def show(room):
    sio.emit('round_ended')

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
            sio.emit('message', "Your best hand: " + str(table.hand_dict[player.best_hand]), room=player.get_client_number())
    max_combination = max(p.best_hand for p in room.get_player_list())
    if max_combination == 2 or max_combination == 3 or max_combination == 4 or max_combination == 8:
        max_hand_sum = max(p.best_hand_sum for p in room.get_player_list() if p.best_hand == max_combination)
        max_sum = max(p.best_sum for p in room.get_player_list() if
                      p.best_hand == max_combination and p.best_hand_sum == max_hand_sum)
        ties_with_max = [p for p in room.get_player_list() if
                         p.best_hand == max_combination and p.best_sum == max_sum and p.best_hand_sum == max_hand_sum]
    else:
        max_sum = max(p.best_sum for p in room.get_player_list() if p.best_hand == max_combination)
        ties_with_max = [p for p in room.get_player_list() if p.best_hand == max_combination and p.best_sum == max_sum]

    if len(ties_with_max) == 1:  # if one player wins whole pot, no ties
        ties_with_max[0].change_balance(table.pot)
        sio.emit('message', str(ties_with_max[0]) + " has won the pot: $" + str(table.pot), room=room.room_id)
    else:
        split = table.pot / len(ties_with_max)
        for p in ties_with_max:
            p.change_balance(split)
            sio.emit('message', str(p) + "has won a split of the pot: $" + str(split) + "\n", room=room.room_id)

def main():
    try:
        temp = os.getcwd()
        cwd = str(pathlib.Path(__file__).parent.resolve())
        if not os.path.exists(cwd + "/res/HandRanks.dat"):
            os.chdir(cwd)
            os.system("python3 AiInstallation.py")

        os.chdir(temp)
        eventlet.wsgi.server(eventlet.listen(('', 5000)), app)
    except KeyboardInterrupt as e:
        sys.exit(0)


if __name__ == '__main__':
    main()
