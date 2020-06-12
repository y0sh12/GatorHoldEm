from table import Table
from player import Player


class Room:
    def __init__(self):
        self._players = []
        self._table = Table()
    
    def add_player(self, player):
        self._players.append(player)
#This import the table.py and should have the list of players
# Adding of player should be implemented here, initialize Player()
