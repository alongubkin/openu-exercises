import json
import random
from copy import copy
from genetic_algorithm import GeneticAlgorithm
from grid_environment import Grid
from entities import RobotEntity, BrickEntity, TreasureEntity
from statistics import mean
from math import sqrt

def build_environment(robot_path=[]):
  grid = Grid(size=10)

  grid.add_entity(BrickEntity((7, 3)))
  grid.add_entity(BrickEntity((7, 2)))
  grid.add_entity(BrickEntity((7, 1)))
  grid.add_entity(BrickEntity((6, 1)))
  grid.add_entity(BrickEntity((5, 1)))
  grid.add_entity(BrickEntity((4, 1)))
  grid.add_entity(BrickEntity((3, 1)))
  grid.add_entity(BrickEntity((3, 2)))
  grid.add_entity(BrickEntity((3, 3)))
  grid.add_entity(BrickEntity((3, 4)))
  grid.add_entity(BrickEntity((3, 5)))
  grid.add_entity(BrickEntity((3, 6)))
  grid.add_entity(BrickEntity((3, 7)))
  grid.add_entity(BrickEntity((3, 8)))

  grid.add_entity(RobotEntity((1, 1), robot_path))
  grid.add_entity(TreasureEntity((5, 5)))

  return grid


def manhattan(pos1, pos2):
  x1, y1 = pos1
  x2, y2 = pos2
  return sqrt(abs(x1 - x2) ** 2 + abs(y1 - y2) ** 2)


class GeneticPathfinder(GeneticAlgorithm):
  def __init__(self):
    super(GeneticPathfinder, self).__init__()
    
    self._environment = build_environment()
    self._start_position = self._environment.find_entity(RobotEntity).position
    self._target_position = self._environment.find_entity(TreasureEntity).position

  def create_population(self):
    for _ in range(20):
      path = [random.choice(list(self._environment.get_legal_moves(self._start_position)))]
      path.append(random.choice(list(self._environment.get_legal_moves(path[-1]))))

      yield path

  def fitness(self, individual):
    # Simulate environment
    env = build_environment(individual)
    while env.update():
      pass

    # Calculate distance to the final position
    robot_position = env.find_entity(RobotEntity).position
    # if manhattan(robot_position, self._target_position) == 0:
    #   return 0

    # float(self._environment.size)
    # 

    distance = manhattan(robot_position, self._target_position)
    return (1.0 / distance) if distance > 0 else (100 + (1.0 / len(individual)))

  def crossover(self, parent1, parent2):
    if parent1 == parent2:
      return self._optimize(parent1)

    intersections = [(index1, index2) for index1, point1 in enumerate(parent1) 
      for index2, point2 in enumerate(parent2) if point1 == point2]

    
    if len(intersections) == 0:
      return self._optimize(random.choice([parent1, parent2]))

    index1, index2 = random.choice(intersections)

    # Looks unnecessary.
    if parent1[-1] == self._target_position:
      if parent2[-1] != self._target_position:
        print('Noice.')
      return self._optimize(parent2[0:index2] + parent1[index1:])
    elif parent2[-1] == self._target_position:
      if parent1[-1] != self._target_position:
        print('Noice.')
      return self._optimize(parent1[0:index1] + parent2[index2:])
    

    paths = [
      # self._optimize(parent1),
      # self._optimize(parent2),
      parent1[0:index1] + parent2[index2:],
      parent2[0:index2] + parent1[index1:],
    ]

    return self._optimize(random.choice(paths))

  def _optimize(self, path):

    for _ in range(10):
      for x in range(len(path)):
        changed = False

        moves = list(self._environment.get_legal_moves(path[x]))
        for y in reversed(range(x + 2, len(path))):
          if path[y] in moves:
            path = path[0:x + 1] + path[y:]
            changed = True
            break
        
        if changed:
          break

    return path

  # def mutate(self, individual):

  #   if individual[-1] != self._target_position and random.random() <= 0.8:
  #     mutations = [move for move in self._environment.get_legal_moves(individual[-1]) 
  #       if move not in individual]
  #     if len(mutations) > 0:
  #       individual = individual + [random.choice(mutations)]
  

  #   # Modify existing
  #   if random.random() < 0.2:
  #     index = random.randrange(0, len(individual))
  #     mutations = [move for move in 
  #       self._environment.get_legal_moves(individual[index - 1] if index > 0 else self._start_position)
  #       if move not in individual] #if move != individual[index] and ]
  #     if len(mutations) > 0:
  #       individual = individual[0:index] + [random.choice(mutations)]
    
  #   return individual

  def mutate(self, individual):

    if individual[-1] != self._target_position and random.random() <= 0.8:
      mutations = [move for move in self._environment.get_legal_moves(individual[-1]) 
        if move not in individual]
      if len(mutations) > 0:
        return self._optimize(individual + [random.choice(mutations)])

  

    # Modify existing
    index = random.randrange(0, len(individual))
    mutations = [move for move in 
      self._environment.get_legal_moves(individual[index - 1] if index > 0 else self._start_position)
      if move not in individual] #if move != individual[index] and ]
    if len(mutations) == 0:
      return self._optimize(individual)

    return self._optimize(individual[0:index] + [random.choice(mutations)])

    # Merge two ?
    # return individual


def main():
  pathfinder = GeneticPathfinder()
  # print(pathfinder._optimize([(1,1), (2, 1), (2, 2), (1, 2), (1, 3), (2, 3), (2, 4), (2, 5), (2, 6), (1, 6), (1, 7), (1, 8), (1, 9), (2, 9), (3, 9), (4, 9), (4, 8), (4, 7), (4, 6), (5, 6), (5, 5)]))
  path = pathfinder.run()
  # path = [(2, 1), (2, 2), (1, 2), (1, 3), (2, 3), (2, 4), (2, 5), (2, 6), (1, 6), (1, 7), (1, 8), (1, 9), (2, 9), (3, 9), (4, 9), (4, 8), (4, 7), (4, 6), (5, 6), (5, 5)]
  with open('example_grid.json', 'w') as grid_file:
    grid_file.write(json.dumps(build_environment(path).serialize()))


if __name__ == '__main__':
  main()