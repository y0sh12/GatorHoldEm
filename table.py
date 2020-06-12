from deck import Deck
from player import Player

# who will initialize minimum bet? and starting amount?
# changing minimum bet?


class Table:

    def __init__(self, numOfPlayers):
        self._deck = Deck()
        self._visible_cards = []
        self._minimumBet = 50
        self._pot = 0
        self._small_blind = 1 
        self._big_blind = 0
        self._numPlayers = numOfPlayers

    def new_round(self):
        self._deck.reset()
        self._pot = 0
        self._minimumBet = 50
        if (self._big_blind + 1) > (self._numPlayers - 1):
            self._big_blind = 0
        else:
            self._big_blind += 1
        
        if (self._small_blind + 1) > (self._numPlayers - 1):
            self._small_blind = 0
        else:
            self._small_blind += 1
    
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
    
    @property
    def small_blind(self):
        return self._small_blind

    @property
    def big_blind(self):
        return self._big_blind

    # TODO Test Card distribution
    # Deals 2 cards to each player's hand

    def distribute_cards(self, players):
        for _ in range(2):
            for p in players:
                p.deal(self._deck.pick_card())
