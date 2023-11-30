# Simple Robot Soccer Simulator

## Getting Started with the Simulator

### Requirements

The simulator requires a desktop-level computer (> 4 cores) to provide real-time simulation.

```
pip install qibullet pybullet absl-py
```

### How to run the simulator

```
python ./simulator.py
```

## Make Your Team

### Base classes

- class `Team`: Manage multiple players
- class `Player`: Represent a single palyers 

Please do not change the base classes!

### How to implement your algorithm

1. Create a new file under `players`

1. Define your own `Player` class
```python
from players.player import Player

class YourPlayer(Player)
  def behave(self):
    # Define your own algorithm 

```

3. Create a new file under `teams`

4. Define your own `Team` class in the file
```python
from teams.team import Team
from players.your_player import YourPlayer

class YourTeam(Team)
  def getFormation(self, player_id):
    # Determine the position of each player 

  def setPlayer(self, player_id):
    # Create your player object
    self.players[player_id] = YourPlayer()
```

### How to test your algorithm with the simulator

1. Import your team class in `simulator.py`
```python
from teams.your_team import YourTeam
```

2. Change the parameter of `RoboCupSimulator`
```python
  simulator = RoboCupSimulator(YourTeam, TheOtherTeam)
```
