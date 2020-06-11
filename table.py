from deck import Deck
from player import Player


class Table:

    def __init__(self):
        self._players = []
        self._deck = Deck()
        self._visible_cards = []
        pass

    def add_player(self, player):
        self._players.append(player)

    @property
    def visible_cards(self):
        return self._visible_cards

    # TODO Test Card distribution
    # Deals 2 cards to each player's hand
    def distribute_cards(self):
        for _ in range(2):
            for p in self._players:
                p.Deal(self._deck.pick_card())

