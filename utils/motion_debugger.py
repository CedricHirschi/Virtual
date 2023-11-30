#!/usr/bin/env python
import sys
import time
import pybullet
import pybullet_data

# from simulation.resources.motions import Motions

sys.path.append('.')

from qibullet import SimulationManager
from resources.motions import Motions

from absl import flags
from absl import app

FLAGS = flags.FLAGS

flags.DEFINE_string('motion', 'Forwards', 'Target motion to debug')


def main(argv):
    # Launch simulation
    manager = SimulationManager()
    client = manager.launchSimulation(gui=True, auto_step=False)

    robot = manager.spawnNao(client, [0, 0, 0], [0, 0, 0, 1], spawn_ground_plane=True)

    time.sleep(1.0)

    poses = Motions.getMotion(FLAGS.motion)
    poseSlider = pybullet.addUserDebugParameter("pose", 1, len(poses), 1)

    try:
        while True:
            i = pybullet.readUserDebugParameter(poseSlider)
            timing, pose = poses[int(i) - 1]

            robot.setAngles(list(pose.keys()), list(pose.values()), 1.0)
            manager.stepSimulation(client)

    except KeyboardInterrupt:
        manager.stopSimulation(client)


if __name__ == "__main__":
    app.run(main)
