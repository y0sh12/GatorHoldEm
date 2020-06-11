from deck import Deck
from player import Player

# who will initialize minimum bet? and starting amount?
# changing minimum bet?


class Table:

    def __init__(self):
        self._deck = Deck()
        self._visible_cards = []
        self._minimumBet = 50
        self._pot = 0

    def new_round(self):
        self._deck.reset()
        self._pot = 0
        self._minimumBet = 50

    # cards on the table 
    @property
    def visible_cards(self):
        return self._visible_cards

    @property
    def minimum_bet(self):
        return self._minimumBet

    @property
    def pot(self):
        return self._pot

    def add_to_pot(self, amount):
        self._pot += amount

    # TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
# TODO Test Card distribution
    # Deals 2 cards to each player's hand
    def distribute_cards(self):
        for _ in range(2):
            for p in self._players:
                p.deal(self._deck.pick_card())
