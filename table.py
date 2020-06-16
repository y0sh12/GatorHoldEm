from deck import Deck
from player import Player
from collections import defaultdict
from itertools import combinations

# who will initialize minimum bet? and starting amount?
# changing minimum bet?


class Table:

    theRound = 0
    card_order_dict = {2:2, 3:3, 4:4, 5:5, 6:6, 7:7, 8:8, 9:9, 10:10,11:11, 12:12, 13:13, 14:14}
    hand_dict = {10: "royal-flush", 9:"straight-flush", 8:"four-of-a-kind", 7:"full-house", 6:"flush", 5:"straight", 4:"three-of-a-kind", 3:"two-pairs", 2:"one-pair", 1:"highest-card"}


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
            player.reset_all()
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


    def check_hand(self, hand):
        if self.check_royal_flush(hand):
            return 10
        elif self.check_straight_flush(hand):
            return 9
        elif self.check_four_of_a_kind(hand):
            return 8
        elif self.check_full_house(hand):
            return 7
        elif self.check_flush(hand):
            return 6
        elif self.check_straight(hand):
            return 5
        elif self.check_three_of_a_kind(hand):
            return 4
        elif self.check_two_pair(hand):
            return 3
        elif self.check_one_pair(hand):
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
            return True
        return False

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
        # rank_values = [Table.card_order_dict[i] for i in values]
        rank_values = [i for i in values]
        value_range = max(rank_values) - min(rank_values)
        if len(set(value_counts.values())) == 1 and (value_range == 4):
            return True
        else:
            if(set(values)) == set([14, 2, 3, 4, 5]):
                return True
        if(set(values)) == set([11, 12, 13, 14, 2]):
            return False
        return False

    def check_three_of_a_kind(self, hand):
        values = [card.rank for card in hand]
        value_counts = defaultdict(lambda:0)
        for v in values:
            value_counts[v] += 1
        if set(value_counts.values()) == set([3, 1]):
            return True
        else:
            return False

   
    def check_two_pair(self, hand):
        values = [card.rank for card in hand]
        value_counts = defaultdict(lambda:0)
        for v in values:
            value_counts[v] += 1
        if sorted(value_counts.values()) == [1, 2, 2]:
            return True
        else:
            False
    
    def check_one_pair(self, hand):
        values = [card.rank for card in hand]
        value_counts = defaultdict(lambda:0)
        for v in values:
            value_counts[v] += 1
        if 2 in value_counts.values():
            return True
        else:
            return False

    def play(self, cards):
        best_hand = 0
        combination = combinations(cards, 5)
        for i in combination:
            hand_value = self.check_hand(list(i))
            if hand_value > best_hand:
                best_hand = hand_value
    
        return best_hand

    def show(self):
        for player in self._players:
            if player.isFolded:
                continue
            else:
                print(player.name, "'s cards: ",end = "")
                for card in player.hand:
                    print(card, end = ",")
                print()
                player.set_best_hand(self.play(player.hand + self._visible_cards))
                print("Best hand:", player.best_hand)
        max_combination = max([player.best_hand for p in self._players])

        ties_with_max = [p for p in self._players if p.best_hand == max_combination]

        if len(ties_with_max) == 1: # if one player wins whole pot, no ties
            player.change_balance(self.pot)
            print(player.name, "has won the pot:", self.pot)
        else:
            # TODO BE MODIFIED TO CHECK FOR TIE BREAKERS
            split = self.pot / len(ties_with_max)
            for p in ties_with_max:
                p.change_balance(split)
                print(p, "has won a split of the pot:", split)

# Old big blind will become small blind, i.e., game goes clockwise
# 