from deck import Deck
from player import Player

# who will initialize minimum bet? and starting amount?
# changing minimum bet?


class Table:

    def __init__(self, player_list):
        self._players = player_list
        self._deck = Deck()
        self._visible_cards = []
        self._minimumBet = 50
        self._pot = 0
        self._small_blind_gen_obj = self._small_blind_gen()
        self._small_blind = None # next(self._small_blind_gen_obj)
        self._big_blind = 0

    def new_round(self):
        self._deck.reset()
        self._pot = 0
        self._minimumBet = 50
        self._dealer = next(self._small_blind_gen_obj)
        self._small_blind = next(self._small_blind_gen_obj)
        self._big_blind = next(self._small_blind_gen_obj)
        
        while True:
            _ = next(self._small_blind_gen_obj)
    

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

    # Deals 2 cards to each player's hand

    def distribute_cards(self):
        for _ in range(2):
            for p in self._players:
                p.deal(self._deck.pick_card())
    
    def _small_blind_gen(self):
        while True:
            for p in self._players:
                yield p


# Old big blind will become small blind, i.e., game goes clockwise
# 