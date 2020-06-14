from deck import Deck
from player import Player

# who will initialize minimum bet? and starting amount?
# changing minimum bet?


class Table:

    theRound = 0

    def __init__(self, player_list):
        self._players = player_list
        self._deck = Deck()
        self._visible_cards = []
        self._minimumBet = 50
        self._pot = 0
        self._small_blind_gen_obj = self._small_blind_gen()
        self._small_blind = None # next(self._small_blind_gen_obj)
        self._big_blind = None

    def new_round(self):

        # Resetting phase
        for player in self._players:
            player.reset_investment()
            player.reset_fold()
        self._deck.reset()
        self._visible_cards.clear()
        self._pot = 0
        self._minimumBet = 50 + 25 * Table.theRound
        Table.theRound += 1


        #New round initialization phase    
        # Dealer and blinds pointers that change only at the end of the round
        self._dealer = next(self._small_blind_gen_obj)
        self._small_blind = next(self._small_blind_gen_obj)
        self._big_blind = next(self._small_blind_gen_obj)
        while True:
            pointer = next(self._small_blind_gen_obj)
            if pointer == self._dealer:
                break
        
        # Taking the blind amounts
        self._small_blind.change_balance(-self._minimumBet / 2)
        self._small_blind.add_investment(self._minimumBet / 2)

        self._big_blind.change_balance(-self._minimumBet)
        self._big_blind.add_investment(self._minimumBet)

        self.add_to_pot(1.5 * self._minimumBet)

        # Current player pointer
        self._current_player_gen_obj = self._current_player_gen()
        while True:
            self._current_player = next(self._current_player_gen_obj)
            if self._current_player == self._big_blind:
                break
        self._current_player = next(self._current_player_gen_obj)


    
    @property
    def current_player(self):
        return self._current_player

    # cards on the table 
    @property
    def visible_cards(self):
        return self._visible_cards

    def add_to_visible_cards(self, _card):
        self._visible_cards.append(_card)

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

    def change_minimum_bet(self, amount):
        self._minimumBet += amount

    # Deals 2 cards to each player's hand

    def distribute_cards(self):
        for _ in range(2):
            for p in self._players:
                p.deal(self._deck.pick_card())
    
    def _small_blind_gen(self):
        while True:
            for p in self._players:
                if p.balance == 0:
                    pass
                else:
                    yield p
    
    def _current_player_gen(self):
        while True:
            for p in self._players:
                if p.balance == 0 or p.isFolded:
                    pass
                else:
                    yield p
    
    def next_player(self):
        self._current_player = next(self._current_player_gen_obj)
   


# Old big blind will become small blind, i.e., game goes clockwise
# 