from table import Table
from player import Player


class Room:
    def __init__(self, room_id):
        self.allow_connect = True
        self.room_id = room_id
        self._players = []
        self._table = Table(self._players)
    
    def add_player(self, player):
        self._players.append(player)

    def remove_player(self, player):
        self._players.remove(player)

    def get_player_list(self):
        return self._players


    def player_present_sid(self, sid):
        for player in self._players:
            if player.get_client_number() == sid:
                return True
        return False
# This import the table.py and should have the list of players
# Adding of player should be implemented here, initialize Player()
