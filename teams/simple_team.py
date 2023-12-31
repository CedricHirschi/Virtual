from teams.team import Team
from players.simple_player import SimplePlayer

from math import ceil

class SimpleTeam(Team):
    def __init__(self, num_players, team_id):
        Team.__init__(self, num_players, team_id)

    def getFormation(self, player_id):
        num_players = len(self.players)

        x = 1.0 * ceil(float(player_id) / 2)
        y = 0.0

        if num_players % 2 != 0 or player_id != num_players - 1:
            y = 0.5 * ceil(float(player_id) / 2) * (player_id % 2 * 2 - 1)

        return (x, y)

    def setPlayer(self, player_id):
        self.players[player_id] = SimplePlayer()