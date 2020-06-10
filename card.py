class Card:

    suits = ("Heart", "Diamond", "Club", "Spade")
    def __init__(self, number, suit):
        if self.suits.__contains__(suit):
            self.suit = suit
        self.number = number
