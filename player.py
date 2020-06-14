import json


class Player:
    def __init__(self, client_number, name="Gator", ai_bot_bool=False):
        self._balance = 500
        self._client_number = client_number
        self._name = name
        self._AI = ai_bot_bool
        self._hand = []
        self._isFolded = False
        self._investment = 0

    # investment is amount currently in pot
    @property
    def investment(self):
        return self._investment

    def reset_investment(self):
        self._investment = 0
    
    def add_investment(self, amnt):
        self._investment = self._investment + amnt

    @property
    def balance(self):
        return self._balance
    
    @property 
    def name(self):
        return self._name
    
    @property
    def hand(self):
        return self._hand

    def change_balance(self, gains):
        self._balance = self._balance + int(gains)

    def fold(self):
        self._isFolded = True

    def reset_fold(self):
        self._isFolded = False

    @property
    def isFolded(self):
        return self._isFolded
    
    
    # Receives a single card that gets added to hand
    def deal(self, card):
        self._hand.append(card)

    def get_client_number(self):
        return self._client_number


    def get_name(self):
        return self._name


    def __str__(self):
        return self._name

    def __eq__(self, obj):
        return isinstance(obj, Player) and obj._client_number  == self._client_number
