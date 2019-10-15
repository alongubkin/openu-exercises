import random
from genetic_algorithm import GeneticAlgorithm
from entities import RobotEntity, TreasureEntity
from math import sqrt


def distance(pos1, pos2):
  x1, y1 = pos1
  x2, y2 = pos2
  return sqrt(abs(x1 - x2) ** 2 + abs(y1 - y2) ** 2)


class GeneticPathAlgorithm(GeneticAlgorithm):
  """Base class for the genetic pathfinder and path optimizer with common logic."""

  def __init__(self, environment, population_size, debug=False):
    super(GeneticPathAlgorithm, self).__init__(population_size, debug)
    self.environment = environment
    self.start_position = self.environment.find_entity(RobotEntity).position
    self.target_position = self.environment.find_entity(TreasureEntity).position

  def run(self, iterations=1000):
    path = super(GeneticPathAlgorithm, self).run(iterations)
    self.reset_environment(path)

    # Add start point and target point to the result if necessary
    if path[0] != self.start_position:
      path.insert(0, self.start_position)

    if path[-1] != self.target_position:
      path.append(self.target_position)

    # Remove useless points
    return self._optimize_path(path)

  def reset_environment(self, path=[]):
    robot = self.environment.find_entity(RobotEntity)
    treasure = self.environment.find_entity(TreasureEntity)

    robot.path = path

    self.environment.move_entity(robot, self.start_position)
    self.environment.move_entity(treasure, self.target_position)

  def _optimize_path(self, path):
    for _ in range(10):
      for x in range(len(path)):
        changed = False

        moves = list(self.environment.get_legal_moves(path[x]))
        for y in reversed(range(x + 2, len(path))):
          if path[y] in moves:
            path = path[0:x + 1] + path[y:]
            changed = True
            break
        
        if changed:
          break

    return path