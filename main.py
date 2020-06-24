from room import Room
from table import Table
from deck import Deck
from player import Player
from card import Card

# TO DO
# 1.) Code fo pairs, tie break
# 2.) limit raise to player blance remaining
# 3.) Testing possible hands


def print_balance(room1):
    for player in room1.get_player_list():
        print("Name: ", player.name, " ")
        print("Hand: ", end="")
        for h in player.hand:
            print(h, end=" ")
            print("Balance: ", player.balance)

def game_loop(room1):
    check = len(room1._players)
    fold = 0
    while check > 0:
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
        print("1.)", checkOrCall, "2.) Fold 3.) Raise")
        option = int(input())
        if(option == 1):
            player.change_balance(-(room1._table.minimum_bet - player.investment))
            room1._table.add_to_pot(room1._table.minimum_bet - player.investment)
            player.add_investment(room1._table.minimum_bet - player.investment)
            if is_check:
                check -=1
        if(option == 2):
            player.fold()
            fold += 1
            check -= 1
        if(option == 3):
            check = len(room1._players) - fold
            print("By how much?")
            _raise = int(input())
            room1._table.change_minimum_bet(_raise)
            player.change_balance(-(room1._table.minimum_bet - player.investment))
            room1._table.add_to_pot(room1._table.minimum_bet - player.investment)
            player.add_investment(room1._table.minimum_bet - player.investment)

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
    #     print("Hand: ", end="")
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
        print("Round:", Table.theRound)
        room1._table.distribute_cards()
        print("Current Dealer: ", room1._table._dealer)
        print("Current sb", room1._table._small_blind)
        print("Current big Blind", room1._table._big_blind)

        game_loop(room1) #pre-flop
        #plyers = 1, break

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