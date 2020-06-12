import json


class Player:
    def __init__(self, client_number, name="Gator", ai_bot_bool=False):
        self._balance = 500
        self._client_number = client_number
        self._name = name
        self._AI = ai_bot_bool
        self._hand = []

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



    # Receives a single card that gets added to hand
    def deal(self, card):
        self._hand.append(card)

    def get_client_number(self):
        return self._client_number


    def get_name(self):
        return self._name


    def __str__(self):
        return self._name
