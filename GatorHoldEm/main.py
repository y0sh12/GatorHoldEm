from room import Room
from table import Table
from deck import Deck
from player import Player
from card import Card

# TO DO
# 1.) Code for pairs, tie break
# -- Testing remaining ---- 2.) limit raise to player balance remaining
# 3.) Testing possible hands
# 4.) Twice checking should be rectified
# 5.) Give pot to player in round if all other players fold
# ----------------------- 6.) Create dict for all the players balances
# 7.) Error handling if someone leaves mid game.
# 8.) Raise 0, not possible. 
# 9.) 2 people one person goes all in, skip to show


def print_balance(room1):
    for player in room1.get_player_list():
        print("Name: ", player.name, " ")
        print("Hand: ", end="")
        for h in player.hand:
            print(h, end=" ")
            print("Balance: ", player.balance)

def game_loop(room1, num_raises=0):

    bankrupt_players = sum([1 for p in room1.get_player_list() if p.bankrupt])
    folded = 0
    check = len(room1._players) - folded - bankrupt_players
    while True:
        player = room1._table.current_player
        print("Current player is: ", player)
        print(player, "Current Balance: ", player.balance, " Current Investment: ", player.investment)
        for card in player.hand:
            print(card, end = " ")
            print() 

        print(player.name)
        print("Minimum Bet to Play:", room1._table.minimum_bet)
        is_check = True if player.investment == room1._table.minimum_bet else False
        checkOrCall = "Check" if is_check else "Call"
        if num_raises < 3:
            print("1.)", checkOrCall, "2.) Fold 3.) Raise")
        else:
            print("1.)", checkOrCall, "2.) Fold")
     

        option = int(input())
        if(option == 1):
            player.change_balance(-(room1._table.minimum_bet - player.investment))
            room1._table.add_to_pot(room1._table.minimum_bet - player.investment)
            player.add_investment(room1._table.minimum_bet - player.investment)
            # if is_check:
            #    check -=1
        if(option == 2):
            player.fold()
            # fold += 1
            # check -= 1
        if option == 3 and num_raises < 3:
            check = len(room1._players) - folded - bankrupt_players
            print("By how much?")
            _raise = int(input())
            room1._table.change_minimum_bet(_raise)
            player.change_balance(-(room1._table.minimum_bet - player.investment))
            room1._table.add_to_pot(room1._table.minimum_bet - player.investment)
            player.add_investment(room1._table.minimum_bet - player.investment)
            num_raises += 1

        # if we get to last action and we 
        # 4th person not getting an opportunity to call
        if (player == table.last_action and num_raises >= 3) and (player == table.last_action and option == 1):
            pass

        # player == table.last_action and num_raises >= 3, he has to call and check: if he folds 


        # if lastaction and ischeck and option == 1
            
        print(player, " after Balance: ", player.balance, " After Investment: ", player.investment, "\n")

        # iterate through all players, count is Folded. After if len(player) - count_isFoled == 1, call show, break
        room1._table.next_player() # ++player


        

def main():
    # room = Room()
    # test = Table(len(playerList))
    
    # playerList = []
    # playerList.append(Player(12, "Adriel"))
    # playerList.append(Player(13, "Bharat"))
    # playerList.append(Player(14, "Yosh"))
    # playerList.append(Player(15, "Azhar"))
    # test = Table(playerList)
    # test.distribute_cards(playerList)
    # for player in playerList:
    #     print("Name: ", player.name, " ")
    #     print("Hand: ", end="")= 
    #     for h in player.hand:
    #         print(h, end=" ")
    #     print("Balance: ", player.balance)

    # print(test._deck.num_cards)

    room1 = Room(123)
    room1.add_player(Player(12, "Adriel"))
    room1.add_player(Player(13, "Bharat"))
    room1.add_player(Player(14, "Yosh"))
    room1.add_player(Player(15, "Azhar"))

    print(room1._table._deck.num_cards)
    print(room1._table._players)

    # Round 1
    while(True):
        room1._table.new_round()  # New Round Starts
        print("Round:", Table.round_number)
        room1._table.distribute_cards()
        print("Current Dealer: ", room1._table._dealer)
        print("Current sb", room1._table._small_blind)
        print("Current big Blind", room1._table._big_blind)

        game_loop(room1) #pre-flop
        #plyers = 1, break

        # looping through players, when we get to last_call (player that gets to call last), we check if investment is equal to min bet AFTER the player's action.

        # player.next()

        print("Number of cards before flopping is ", room1._table._deck.num_cards)
        print("************************THE FLOP*********************")
        room1._table._deck.pick_card() #the burn card
        room1._table.add_to_visible_cards(room1._table._deck.pick_card()) 
        room1._table.add_to_visible_cards(room1._table._deck.pick_card())   #The FLOP - three cards
        room1._table.add_to_visible_cards(room1._table._deck.pick_card())
        
        print("Cards on the table: ", end=" ")
        for a in room1._table._visible_cards:
            print(a, end=" ")
        print() 
        
        # print(room1._table._deck.num_cards)
        room1._table.change_last_action()
        game_loop(room1) #pre-turn
        
        print("************************THE TURN*********************")
        room1._table._deck.pick_card() #the burn card
        room1._table.add_to_visible_cards(room1._table._deck.pick_card()) # The Turn - one card   
        print("Cards on the table: ", end=" ")
        for a in room1._table._visible_cards:
            print(a, end=" ")
        print() 

        game_loop(room1) #pre-river

        print("************************THE RIVER*********************")
        room1._table._deck.pick_card() #the burn card
        room1._table.add_to_visible_cards(room1._table._deck.pick_card()) # The River - one card
        print("Cards on the table: ", end=" ")
        for a in room1._table._visible_cards:
            print(a, end=" ")
        print() 
        
        game_loop(room1) #after River
        for a in room1._table._visible_cards:
            print(a, end=" ")
            print()
        room1._table.show()  # Show

    



    # room1._players[1].change_balance(-500)
    # Round 2
    # room1._table.new_round()
    # print("Current Dealer: ", room1._table._dealer)
    # print("Current sb", room1._table._small_blind)
    # print("Current big Blind", room1._table._big_blind)

    # Round 3
    # room1._table.new_round()
    # print("Current Dealer: ", room1._table._dealer)
    # print("Current sb", room1._table._small_blind)
    # print("Current big Blind", room1._table._big_blind)
# """            


#     sb_gen = small_blind()
#     sb = next(sb_gen)

# """     
#     """
#     # Deck test
#     deck = Deck()
#     print(deck)
#     print("Picking card: ", deck.pick_card())
#     print("Attempting reset")
#     deck.reset()
#     print("Length of the deck is ", deck.num_cards)
#     print(deck)
#     """

main()