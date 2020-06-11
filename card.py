class Card:

    _suits = ("Heart", "Diamond", "Club", "Spade")
    _ranks = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13)
    # 1 - Ace, 11 - Jack, 12 - Queen, 13 - King

    def __init__(self, suit, rank):
        if suit in self._suits:
            self._suit = suit
        if rank in self._ranks:
            self._rank = rank

    def __str__(self):
        return "Suit: " + str(self._suit) + " Rank: " + str(self._rank)
