from ctypes import *
from .deck import Deck
from .table import Table
from .player import Player
from .card import Card
import timeit
from random import randint
import os
import pathlib

class AI(Player):
    def __init__(self, client_number, is_vip=False, name="AI BOT", ai_bot_bool=True):
        super(AI, self).__init__(client_number, is_vip, name, ai_bot_bool)
        self._ehs = None
        self._deck = Deck()
        self._choice = None
        self._lib = self.load_ai_lib()

    def test_lib(self):
        self._lib.InitTheEvaluator()


        #self._lib.DoSomeWork()
        #c_bench = timeit.timeit(lambda: self._lib.DoSomeWork(), number=1)
        #print(c_bench)
        
    @property
    def choice(self):
        self._choice = self.make_choice()
        return self._choice

    def EV(self, hand_strength, min_bet, pot):
         return (hand_strength * pot) - ((1-hand_strength) * min_bet)

    def make_choice(self, num_opponents, hole_cards, community_cards, pot, min_bet, investment):
        temp = os.getcwd()
        cwd = str(pathlib.Path(__file__).parent.resolve())
        os.chdir(cwd)
        self._lib.InitTheEvaluator()
        os.chdir(temp)
        self._deck.reset()

        t_hole_cards = []
        t_community_cards = []

        

        for i, h_c in enumerate(hole_cards):
            t_hole_cards.append(self.translate(h_c))
        for i, c_c in enumerate(community_cards):
            t_community_cards.append(self.translate(c_c))


        c_t_hole_cards = (c_int * len(t_hole_cards))(*t_hole_cards)
        c_t_community_cards = (c_int * len(t_community_cards))(*t_community_cards)

        print(len(t_hole_cards))

        self.set_ehs(self._lib.HandStrength(c_t_hole_cards, (len(t_hole_cards)), c_t_community_cards, len(t_community_cards), num_opponents))

        ev = self.EV(self._ehs, min_bet, pot)
        if min_bet != 0: #if someone raised before you, i.e., your total investment is NOT equal to the "minimum_Bet" variable
            if ev >= 0:
                choice = 1  #Call
            else:
                random = randint(1, 4)
                if random == 2:
                    choice  = 1 #Bluff Call
                else:
                    choice = 2 #Fold
        else:
            if self._ehs > 0.6:
                choice = 3 #Raise
            else:
                # FOR BLUFF: 1 to 3, if it lands on 2, then just choice = 3
                choice = 1 #Check


 

        return choice

    def make_raise(self, min_bet, balance):
        if self._ehs > 0.85:
            return balance
        elif self._ehs > 0.6 and self._ehs < 0.85:
            return min_bet / 2
        else:
            return min_bet / 2
    
    @property
    def deck(self):
        return self._deck
    @property
    def ehs(self):
        return self._ehs

    def set_ehs(self, ehs):
        self._ehs = ehs


    def translate(self, card):
        values = {'c':1, 'd':2, 'h':3, 's':4}
        return 4 * (card.rank - 2) + values[card.suit[0].lower()]


    def load_ai_lib(self):
        temp = os.getcwd()
        cwd = str(pathlib.Path(__file__).parent.resolve())
        os.chdir(cwd)
        lib = cdll.LoadLibrary("./libai.so")

        lib.InitTheEvaluator.restype = c_int
        lib.InitTheEvaluator.argtypes = None

        lib.DoSomeWork.restype = None
        lib.DoSomeWork.argtypes = None

        lib.GetHandValue.restype = c_int
        lib.GetHandValue.argtype = POINTER(c_int)

        lib.HandStrength.restype = c_double
        lib.HandStrength.argtype = [POINTER(c_int), c_int, POINTER(c_int), c_int, c_int]

        os.chdir(temp)
        return lib
