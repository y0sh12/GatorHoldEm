from random import shuffle
from .card import Card


class Deck:

    def __init__(self, decks=1):
        self._decks = decks
        self._cards = []
        self.reset()
        self.shuffle_cards()

    # prints all the cards currently in the deck.
    def __str__(self):
        cds = ""
        for a in self._cards:
            cds += a.__str__() + "\n"
        return cds

    @property
    def num_cards(self):
        return len(self._cards)

    def shuffle_cards(self):
        shuffle(self._cards)

    def pick_card(self):
        return self._cards.pop()

    
    def pick_specific_card(self, card):
        found = False
        for c in self._cards:
            if c.suit == card.suit and c.rank == card.rank:
                print(c.suit, c.rank, "found")
                found = True
                self._cards.remove(c)   
        if not found:
            print("card not found")
    
    def reset(self):
        self._cards.clear()
        for r in range(2, 15):
            for s in ("Heart", "Diamond", "Club", "Spade"):
                self._cards.append(Card(s, r))
        self.shuffle_cards()
