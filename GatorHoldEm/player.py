class Player:
    def __init__(self, client_number, is_vip, name, ai_bot_bool=False):
        self._balance = 500
        self._client_number = client_number  # None = AI
        self._name = name
        self.AI = ai_bot_bool
        self._hand = []
        self._isFolded = False
        self._investment = 0
        self._best_hand = 0
        self._best_sum = 0
        self._bankrupt = False
        self._best_hand_sum = None
        self.is_vip = is_vip
        self._connected = True  #True for human players connected to server, False for AI bots

    @property
    def bankrupt(self):
        return self._bankrupt

    def declare_bankrupt(self):
        self._bankrupt = True

    # investment is amount player currently has in pot
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
    def best_hand(self):
        return self._best_hand
    
    @property
    def best_sum(self):
        return self._best_sum

    @property
    def best_hand_sum(self):
        return self._best_hand_sum
    
    @property 
    def name(self):
        return self._name
    
    @property
    def hand(self):
        return self._hand

    @hand.setter
    def hand(self, hand):
        self._hand = hand
    
    def set_best_hand(self, value):
        self._best_hand = value

    def set_best_sum(self, value):
        self._best_sum = value

    def set_best_hand_sum(self, value):
        self._best_hand_sum = value
    
    def change_balance(self, gains):
        self._balance = self._balance + int(gains)

    def fold(self):
        self._isFolded = True

    def reset_fold(self):
        self._isFolded = False

    def reset_hand(self):
        self._hand.clear()
    
    def reset_all(self):
        self.reset_investment()
        self.reset_fold()
        self.set_best_hand(0)
        self.reset_hand()
        self.set_best_sum(0)
        self.set_best_hand_sum(None)

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
