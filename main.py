from room import Room
from table import Table
from deck import Deck


def main():
    # room = Room()
    test = Table()
    
    # Deck test
    deck = Deck()
    print(deck)
    print("Picking card: ", deck.pick_card())
    print("Attempting reset")
    deck.reset()
    print(deck)

main()
