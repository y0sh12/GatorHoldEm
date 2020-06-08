import json
class Player:
    def __init__(self, client_number):
        self.balance = 500
        self.client_number = client_number
        self.name = "Gator"

    def __init__(self, client_number, name, ai_bot_bool):
        self.balance = 500
        self.client_number = client_number
        self.name = name
        self.AI = ai_bot_bool

    def get_balance(self):
        return self.balance

    def increase_balance(self, gains):
        self.balance = self.balance + int(gains)

    def __str__(self):
        return json.dumps(self.__dict__)

