from room import Room
from table import Table
from deck import Deck
from player import Player

def print_balance(room1):
    for player in room1.get_player_list():
        print("Name: ", player.name, " ")
        print("Hand: ", end="")
        for h in player.hand:
            print(h, end=" ")
            print("Balance: ", player.balance)
        

def main():
    room1 = Room(123)
    room1.add_player(Player(12, "Adriel"))
    room1.add_player(Player(13, "Bharat"))
    room1.add_player(Player(14, "Yosh"))
    room1.add_player(Player(15, "Azhar"))
    room1._table.distribute_cards()


    print(room1._table._deck.num_cards)
    print(room1._table._players)

    # Round 1
    room1._table.new_round()
    print("Current Dealer: ", room1._table._dealer)
    print("Current sb", room1._table._small_blind)
    print("Current big Blind", room1._table._big_blind)

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


    # while check > 0
    # folds = 0
    # if folded, fold += 1
    # check = len(players)
    # if raise, check = len(players) - folds
    # if check, check -= 1

    check = len(room1._players)
    fold = 0
    while check > 0:
        player = room1._table.current_player
        print("Current player is: ", player)
        print(player, "Current Balance: ", player.balance, " Current Investment: ", player.investment)
        if player.isFolded:
            print("_____________________________________________________________________")
            continue   
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
            # print("Your Balance: ", player.balance)
        if(option == 2):
            # print("Your Balance: ", player.balance)
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
        room1._table.next_player() # ++player

    
    
    room1._table._deck.pick_card() #the burn card
    room1._table.add_to_visible_cards(room1._table._deck.pick_card()) 
    room1._table.add_to_visible_cards(room1._table._deck.pick_card())   #The FLOP - three cards
    room1._table.add_to_visible_cards(room1._table._deck.pick_card()) 
    print(room1._table._visible_cards)
    





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
