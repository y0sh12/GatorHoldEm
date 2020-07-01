import sys
import socketio
import eventlet
from room import Room
from player import Player
from table import Table
import copy

roomList = []
sio = socketio.Server()
app = socketio.WSGIApp(sio)


@sio.event
def connect(sid, environ):
    print(sid, "in lobby")


# sio.call(event='active_player_list', data=room.room_id)
@sio.on('active_player_list')
def on_event(sid, room_id):
    room = next((room for room in roomList if room.room_id == room_id), None)
    if room is None:
        print("room does not exist")
        return None
    print(room.get_player_list())
    pl_list = []
    for pl in room.get_player_list():
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


@sio.event
def disconnect(sid):
    room = find_room(sid)
    if room is not None:
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
    print("Current Players in room are: ", end='')
    for p in room.get_player_list():
        print(p, end=' ')
    sio.emit('user_connection', (name + " has joined the room!"), room=room_id, skip_sid=sid)


@sio.event
def goto_room(sid, room_id):
    find_room = next((room for room in roomList if room.room_id == room_id), None)
    if find_room is None:
        roomList.append(Room(room_id))
        find_room = roomList[-1]
    print(find_room.room_id)
    print(find_room.get_player_list())
    # temporary code to only have a max of 3 ppl per room
    if len(find_room.get_player_list()) < 6:
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
    if room.game_in_progress:
        return

    room.game_in_progress = True
    sio.emit('message', "game starting", room=room.room_id)
    table = room.get_Table()

    balance_dict = {p.get_client_number(): p.balance for p in room.get_player_list()}

    while True:
        isBroke = 0
        for player in room.get_player_list():
            if player.balance == 0:
                isBroke += 1
        if len(room.get_player_list()) - isBroke == 1:
            break
        else:
            table.new_round()
            sio.emit('new_hand')
            sio.emit('message', "Round: " + str(Table.theRound), room=room.room_id)
            table.distribute_cards()
            """
                SHOW TEST
                players[0] = [Card()]
                players[1]

                Comment out 
                table.distribute_cards()

            """
            small_blind = str(table.small_blind)
            big_blind = str(table.big_blind)
            dealer = str(table.dealer)
            min_bet = str(table.minimum_bet)
            round_num = str(Table.theRound)

            for player in room.get_player_list():
                card_string = str(player.hand[0]), str(player.hand[1])
                sio.emit('emit_hand', card_string, room=player.get_client_number())
            # sio.emit('message', dealer, room=room.room_id)
            # sio.emit('message', small_blind, room=room.room_id)
            # sio.emit('message', big_blind, room=room.room_id)
            # sio.emit('message', minbet, room=room.room_id)
            sio.emit('board_init_info', [dealer, small_blind, big_blind, min_bet, round_num], room=room.room_id)

            if not game_loop(room):
                continue

            sio.emit('message', "---------THE FLOP----------\n", room=room.room_id)
            """
            SHOW TEST
            table.add_to_visible_cards(Card())
            table.skip_to_show = True

            Comment out below code
            """
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

            sio.emit('message', "---------THE TURN----------\n", room=room.room_id)
            table._deck.pick_card()  # the burn card
            table.add_to_visible_cards(table._deck.pick_card())  # The TURN - one card
            visibleCards += " " + str(table._visible_cards[3])
            sio.emit('turn', visibleCards, room=room.room_id)

            if not table.skip_to_show:
                if not game_loop(room):
                    continue

            sio.emit('message', "---------THE RIVER----------\n", room=room.room_id)
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
    sio.emit('message', str(winner) + " HAS WON THE GAME AND HAS EARNED $" + str(winner.balance) + "!",
             room=room.room_id)


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
    while True:
        player = table.current_player
        is_check = True if player.investment == table.minimum_bet else False
        checkOrCall = "Check" if is_check else "Call"
        info = str(player.balance), str(player.investment), str(table.minimum_bet), str(checkOrCall)
        sio.emit('which_players_turn', [player.get_name(), str(table.minimum_bet)], room=room.room_id)
        try:
            option = sio.call(event='your_turn', data=info, sid=player.get_client_number())
        except e as TimeoutError:
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
            # if is_check:
            check -= 1

        if int(option) == 2:
            # if last action player's last action is to fold we should end the round there.
            # 2 active players??

            # -TO-DO- change_last_action player, point to previous person before dealer if dealer folds
            # -TO-DO- after flop, if last_action player folds on his last action.

            # If there are only 2 other active players remaining then code should not run

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
            folded += 1
            check -= 1
        if int(option) == 3:
            # _raise = Ask player how much raise

            #             ask = "By how much do you want to raise"
            #             _raise = sio.call(event='raise', data=ask, sid=player.get_client_number())
            #             table.change_minimum_bet(int(_raise))
            #             player.change_balance(-(table.minimum_bet - player.investment))
            #             table.add_to_pot(table.minimum_bet - player.investment)
            #             player.add_investment(table.minimum_bet - player.investment)

            #         # Check if everybody is folded
            #         folded = 0
            #         for p in room.get_player_list():
            #             if p.isFolded:
            #                 folded += 1
            #         if len(room.get_player_list()) - folded <= 1:
            #             for p in room.get_player_list():
            #                 if not p.isFolded:
            #                     p.change_balance(table.pot)
            #                     sio.emit('message', str(p) + " has won the pot: " + str(table.pot), room = room.room_id)
            #             return False
            #         table.next_player()  # ++player

            error = 0
            while error < 3:
                ask = "By how much do you want to raise"
                _raise = sio.call(event='raise', data=ask, sid=player.get_client_number())
                if int(_raise) > player.balance:
                    sio.emit('message', "You ain't a millionaire, try a smaller raise", room=player.get_client_number())
                    error += 1
                else:
                    table.change_minimum_bet(int(_raise))
                    player.change_balance(-(table.minimum_bet - player.investment))
                    table.add_to_pot(table.minimum_bet - player.investment)
                    player.add_investment(table.minimum_bet - player.investment)
                    check = len(room.get_player_list()) - folded - bankrupt_players
                    break
            if error == 4:
                player.fold()
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
                    sio.emit('message', str(p) + " has won the pot: " + str(table.pot), room=room.room_id)
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

        if check <= 1 and player == table.last_action:
            if last_action_was_fold:
                table._last_action = prev
            table.next_player()
            break

        table.next_player()  # ++player

    return True


def show(room):
    sio.emit('message', 'THE FINAL SHOWDOWN', room=room.room_id)
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
            sio.emit('message', "Your best hand: " + str(player.best_hand), room=player.get_client_number())
            sio.emit('message', "Your best sum: " + str(player.best_sum), room=player.get_client_number())
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
        sio.emit('message', str(ties_with_max[0]) + " has won the pot: " + str(table.pot), room=room.room_id)
    else:
        # TODO BE MODIFIED TO CHECK FOR TIE BREAKERS
        split = table.pot / len(ties_with_max)
        for p in ties_with_max:
            p.change_balance(split)
            sio.emit('message', str(p) + "has won a split of the pot: " + str(split) + "\n", room=room.room_id)


if __name__ == '__main__':
    try:
        eventlet.wsgi.server(eventlet.listen(('', 5000)), app)
    except KeyboardInterrupt as e:
        sys.exit(0)