from random import shuffle
from card import Card


class Deck:

    def __init__(self, decks=1):
        self._decks = decks
        self._cards = []
        for r in range(2, 15):
            for s in ("Heart", "Diamond", "Club", "Spade"):
                self._cards.append(Card(s, r))
        self.shuffle(self._cards)

    # prints all the cards currently in the deck.
    def __str__(self):
        cds = ""
        for a in self._cards:
            cds += a.__str__() + "\n"
        return cds

    @property
    def num_cards(self):
        return len(self._cards)

    def shuffle(self):
        shuffle(self._cards)

    def pick_card(self):
        return self._cards.pop()