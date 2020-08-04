from .deck import Deck
from .player import Player
from collections import defaultdict
from itertools import combinations

# who will initialize minimum bet? and starting amount?
# changing minimum bet?


class Table:

    theRound = 0
    hand_dict = {10: "royal-flush", 9:"straight-flush", 8:"four-of-a-kind", 7:"full-house", 6:"flush", 5:"straight", 4:"three-of-a-kind", 3:"two-pairs", 2:"one-pair", 1:"highest-card"}


    def __init__(self, player_list):
        self._players = player_list
        self._deck = Deck()
        self._visible_cards = []
        self._minimumBet = 50
        self._pot = 0
        self._dealer_gen_obj = self._dealer_gen()
        self._small_blind = None
        self._big_blind = None
        self._dealer = None
        self._current_player = None
        self._skip_to_show = False
        self._last_action = None
        Table.theRound = 0

    def new_round(self):

        # Resetting phase
        self._skip_to_show = False
        for player in self._players:
            player.reset_all()
        self._deck.reset()
        self._visible_cards.clear()
        self._pot = 0
        self._minimumBet = 50
        Table.theRound += 1


        #New round initialization phase    
        # Dealer and blinds pointers that change only at the end of the round
        self._dealer = next(self._dealer_gen_obj)
        self._small_blind = next(self._dealer_gen_obj)
        self._big_blind = next(self._dealer_gen_obj)
        self._last_action = self._big_blind
        print("Dealer is: ", self._dealer)
        print("Small blind is: ", self._small_blind)
        print("big blind is: ", self._big_blind)
        while True:
            pointer = next(self._dealer_gen_obj)
            if pointer == self._dealer:
                break
        
        # Taking the blind amounts
        small_blind_amount = self._minimumBet // 2
        big_blind_amount = self._minimumBet

        # If player cant pay blind take balance instead
        if small_blind_amount > self._small_blind.balance:
            small_blind_amount = self._small_blind.balance

        if big_blind_amount > self._big_blind.balance:
            big_blind_amount = self._big_blind.balance

        # Update balance and investment accordingly
        self._small_blind.change_balance(-small_blind_amount)
        self._small_blind.add_investment(small_blind_amount)

        self._big_blind.change_balance(-big_blind_amount)
        self._big_blind.add_investment(big_blind_amount)

        # Add amount to the pot
        self.add_to_pot(small_blind_amount + big_blind_amount)

        # Current player pointer
        self._current_player_gen_obj = self._current_player_gen()
        while True:
            self._current_player = next(self._current_player_gen_obj)
            if self._current_player == self._big_blind:
                break
        
        #Pre - flop point to player left of big blind
        self._current_player = next(self._current_player_gen_obj)

    # Alternative create a new table every time we have a new game.
    # Calle a new game
    def new_game(self):
        # Add function that creates a new list of players based on who's still in the room
        # Reset self._dealer_gen_obj and self._current_player_gen_obj
        # Set everyone's balance to $500
        # Set self._bankrupt = False

        self._visible_cards = []
        self._minimumBet = 50
        self._pot = 0
        self._dealer_gen_obj = self._dealer_gen()
        self._small_blind = None
        self._big_blind = None
        self._dealer = None
        self._current_player = None
        self._skip_to_show = False
        self._last_action = None
        Table.theRound = 0


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

    def change_minimum_bet(self, amount):
        self._minimumBet += amount

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

    @property
    def dealer(self):
        return self._dealer

    @property
    def skip_to_show(self):
        return self._skip_to_show

    @skip_to_show.setter
    def skip_to_show(self, _value):
        self._skip_to_show = _value
    # Deals 2 cards to each player's hand
    
    @property
    def last_action(self):
        return self._last_action
    
    # Call after flop
    def change_last_action(self):
        # If the dealer has folded pick the active palyer to the right of the dealer.
        if self._dealer.isFolded:
            previous_p = self._dealer
            current_p = next(self._dealer_gen_obj)
            while True:
                if current_p == self._dealer:
                    break
                else:
                    if not current_p.isFolded:
                        previous_p = current_p
                    current_p = next(self._dealer_gen_obj)
            self._last_action = previous_p
        else:
            self._last_action = self._dealer

    def distribute_cards(self):
        for _ in range(2):
            for p in self._players:
                if not p.bankrupt:
                    p.deal(self._deck.pick_card())
    
    def _dealer_gen(self):
        while True:
            for p in self._players:
                if p.bankrupt:
                    pass
                else:
                    yield p
    
    def _current_player_gen(self):
        while True:
            for p in self._players:
                if p.bankrupt or p.isFolded:
                    pass
                else:
                    yield p
    
    def next_player(self):
        self._current_player = next(self._current_player_gen_obj)


    def check_hand(self, hand):
        if self.check_royal_flush(hand):
            return 10
        elif self.check_straight_flush(hand):
            return 9
        elif self.check_four_of_a_kind(hand)[0]:
            return 8
        elif self.check_full_house(hand):
            return 7
        elif self.check_flush(hand):
            return 6
        elif self.check_straight(hand):
            return 5
        elif self.check_three_of_a_kind(hand)[0]:
            return 4
        elif self.check_two_pair(hand)[0]:
            return 3
        elif self.check_one_pair(hand)[0]:
            return 2
        else:
            return 1

    def check_royal_flush(self, hand):
        if self.check_straight_flush(hand):
            values = [card.rank for card in hand]
            if set(values) == set([10, 11, 12, 13, 14]):
                return True
            else:
                return False
        else:
            return False

    def check_straight_flush(self, hand):
        if self.check_flush(hand) and self.check_straight(hand):
            return True
        else:
            return False

    def check_four_of_a_kind(self, hand):
        values = [card.rank for card in hand]
        value_counts = defaultdict(lambda:0)
        for v in values:
            value_counts[v] += 1
        if sorted(value_counts.values()) == [1, 4]:
            return [True, 4 * sorted(value_counts.keys())[1]]
        return [False, None]

    def check_full_house(self, hand):
        values = [card.rank for card in hand]
        value_counts = defaultdict(lambda:0)
        for v in values:
            value_counts[v] += 1
        if sorted(value_counts.values()) == [2, 3]:
            return True
        return False
    
    def check_flush(self, hand):
        suits = [card.suit for card in hand]
        if len(set(suits)) == 1:
            return True
        else:
            return False
    
    def check_straight(self, hand):
        values = [card.rank for card in hand]
        value_counts = defaultdict(lambda:0)
        for v in values:
            value_counts[v] += 1
        rank_values = [i for i in values]
        value_range = max(rank_values) - min(rank_values)
        if len(set(value_counts.values())) == 1 and (value_range == 4):
            return True
        else:
            if set(values) == set([14, 2, 3, 4, 5]):
                return True
        if set(values) == set([11, 12, 13, 14, 2]) or set(values) == set([12, 13, 14, 2, 3]) or set(values) == set([13, 14, 2, 3, 4])  :
            return False
        return False

    def check_three_of_a_kind(self, hand):
        values = [card.rank for card in hand]
        value_counts = defaultdict(lambda:0)
        for v in values:
            value_counts[v] += 1
        if set(value_counts.values()) == set([3, 1]):
            return [True, 3 * sorted(value_counts.keys())[2]]
        else:
            return [False, None]

   
    def check_two_pair(self, hand):
        values = [card.rank for card in hand]
        value_counts = defaultdict(lambda:0)
        for v in values:
            value_counts[v] += 1
        if sorted(value_counts.values()) == [1, 2, 2]:
            return [True, 2 * (sorted(value_counts.keys())[1] + sorted(value_counts.keys())[2])]
        else:
            return [False, None]
    
    def check_one_pair(self, hand):
        values = [card.rank for card in hand]
        value_counts = defaultdict(lambda:0)
        for v in values:
            value_counts[v] += 1
        if 2 in value_counts.values():
            return [True, 2 * sorted(value_counts.keys())[3]]
        else:
            return [False, None]

    def play(self, cards):
        best_hand = 0
        best_sum = 0
        hand_sum = None
        combination = combinations(cards, 5)
        for i in combination:
            hand_value = self.check_hand(list(i))
            if hand_value > best_hand:
                best_hand = hand_value
                best_sum = sum([card.rank for card in list(i)])
                if hand_value == 2:
                    hand_sum = self.check_one_pair(list(i))[1] 
                if hand_value == 3:
                    hand_sum = self.check_two_pair(list(i))[1] 
                if hand_value == 4:
                    hand_sum = self.check_three_of_a_kind(list(i))[1] 
                if hand_value == 8:
                    hand_sum = self.check_four_of_a_kind(list(i))[1] 
            if hand_value == best_hand:
                if sum([card.rank for card in list(i)]) > best_sum:
                    best_sum = sum([card.rank for card in list(i)])
        return [best_hand, best_sum, hand_sum]

    # def show(self):
    #     for player in self._players:
    #         if player.isFolded:
    #             continue
    #         else:
    #             print(player.name, "'s cards: ",end = "")
    #             for card in player.hand:
    #                 print(card, end = ",")
    #             print()
    #             play = self.play(player.hand + self._visible_cards)
    #             player.set_best_hand(play[0])
    #             player.set_best_sum(play[1])
    #             print("Best hand:", player.best_hand)
    #             print("Best sum:", player.best_sum)
    #     max_combination = max(p.best_hand for p in self._players)
    #     max_sum = max(p.best_sum for p in self._players if p.best_hand == max_combination)
    #     print("Max sum: ", max_sum, "Max combination: ", max_combination)
    #     ties_with_max = [p for p in self._players if p.best_hand == max_combination and p.best_sum == max_sum]

    #     print(len(ties_with_max))
    #     if len(ties_with_max) == 1: # if one player wins whole pot, no ties
    #         ties_with_max[0].change_balance(self.pot)
    #         print(ties_with_max[0].name, "has won the pot:", self.pot)
    #     else:
    #         split = self.pot / len(ties_with_max)
    #         for p in ties_with_max:
    #             p.change_balance(split)
    #             print(p, "has won a split of the pot:", split)

# Old big blind will become small blind, i.e., game goes clockwise
# 