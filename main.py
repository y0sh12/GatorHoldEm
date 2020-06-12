from room import Room
from table import Table
from deck import Deck
from player import Player


def main():
    # room = Room()
    # test = Table(len(playerList))
    
    playerList = []
    playerList.append(Player(12, "Adriel"))
    playerList.append(Player(13, "Bharat"))
    playerList.append(Player(14, "Yosh"))
    playerList.append(Player(15, "Azhar"))
    test = Table(len(playerList))
    test.distribute_cards(playerList)
    for player in playerList:
        print("Name: ", player.name, " ")
        print("Hand: ", end="")
        for h in player.hand:
            print(h, end=" ")
        print("Balance: ", player.balance)

    print(test._deck.num_cards)
    bigBlind = 0
    smallBlind = 1
    for index, player in range(0, len(playerList)), playerList:
        if index == test.big_blind():
            player.change_balance(-50)
        elif index == test.small_blind():
            player.change_balance(-25)
        else:
            

            

def small_blind():
    while True:
        for p in playerList:
            if p.balance <= 0:
                pass
            else:
                yield p

    sb_gen = small_blind()
    sb = next(sb_gen)
     
    """
    # Deck test
    deck = Deck()
    print(deck)
    print("Picking card: ", deck.pick_card())
    print("Attempting reset")
    deck.reset()
    print("Length of the deck is ", deck.num_cards)
    print(deck)
    """

main()
