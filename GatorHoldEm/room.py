from table import Table
from player import Player


class Room:
    def __init__(self, room_id):
        self.allow_connect = True
        self.game_in_progress = False
        self.room_id = room_id
        self._players = []
        self._table = Table(self._players)
    
    def add_player(self, player):
        self._players.append(player)

    def remove_player(self, player):
        # set player balance to zero and fold instead of removing to prevent program from breaking.
        if self.game_in_progress:
            player.fold()
            player._balance = 0
            player.is_vip = False
            if len(self._players) > 1:
                self._players[1].is_vip = True
        else:
            self._players.remove(player)
            if len(self._players) > 0:
                self._players[0].is_vip = True

    def get_player_list(self):
        return self._players

    def set_player_list(self, players):
        self._players = players

    def get_Table(self):
        return self._table

    def player_present_sid(self, sid):
        for player in self._players:
            if player.get_client_number() == sid:
                return True
        return False

# This import the table.py and should have the list of players
# Adding of player should be implemented here, initialize Player()
