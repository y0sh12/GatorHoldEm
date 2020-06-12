from room import Room
from table import Table
from deck import Deck
from player import Player


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

    room = Room(123)
    room.add_player(Player(12, "Adriel"))
    room.add_player(Player(13, "Bharat"))
    room.add_player(Player(14, "Yosh"))
    room.add_player(Player(15, "Azhar"))
    room._table.distribute_cards()
    for player in room.get_player_list():
            print("Name: ", player.name, " ")
            print("Hand: ", end="")
            for h in player.hand:
                print(h, end=" ")
                print("Balance: ", player.balance)

    print(room._table._deck.num_cards)
    print(room._table._players)
    room._table.new_round()
    print(room._table.small_blind)
    room._table.new_round()
    print(room._table.small_blind)


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
