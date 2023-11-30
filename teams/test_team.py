from teams.team import Team
from players.test_player import TestPlayer

class TestTeam(Team):
    counter = 0

    def __init__(self, num_players, team_id):
        Team.__init__(self, num_players, team_id)
        TestTeam.counter += 1
        self.team_name = f'test_team_{TestTeam.counter}'
    def getFormation(self, player_id):
        return (0, float(player_id))
    def setPlayer(self, player_id):
        self.players[player_id] = TestPlayer(f'{self.team_name}.{player_id}')
        return
