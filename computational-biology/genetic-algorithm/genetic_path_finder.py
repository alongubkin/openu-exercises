import random
from genetic_path_algorithm import GeneticPathAlgorithm, distance
from entities import RobotEntity, TreasureEntity

POPULATION_SIZE = 20
MUTATION_NEW_POINT_PROBABILITY = 0.8

class GeneticPathfinder(GeneticPathAlgorithm):
  def __init__(self, environment):
    super(GeneticPathfinder, self).__init__(environment, POPULATION_SIZE, 
      debug="GeneticPathFinder")

  def create_population(self):
    for _ in range(POPULATION_SIZE):
      path = [random.choice(list(self.environment.get_legal_moves(self.start_position)))]
      path.append(random.choice(list(self.environment.get_legal_moves(path[-1]))))

      yield path

  def fitness(self, individual):
    # Reset the environment and set a new path for the robot
    self.reset_environment()
    self.environment.find_entity(RobotEntity).path = individual

    # Simulate the environment
    while self.environment.update():
      pass

    # Calculate the distance between the robot to the target
    robot_position = self.environment.find_entity(RobotEntity).position
    target_distance = distance(robot_position, self.target_position)

    if target_distance == 0:
      return 1.0

    return 1.0 / target_distance

  def stop_condition(self, iterations, fitness):
    return fitness == 1.0

  def crossover(self, parent1, parent2):
    intersections = [(index1, index2) for index1, point1 in enumerate(parent1) 
      for index2, point2 in enumerate(parent2) if point1 == point2]

    if len(intersections) == 0:
      return random.choice([parent1, parent2])

    index1, index2 = random.choice(intersections)

    return random.choice([
      parent1[0:index1] + parent2[index2:],
      parent2[0:index2] + parent1[index1:],
    ])
    
  def mutate(self, individual):
    # Sometimes, add new point to the end of the path.
    if random.random() <= MUTATION_NEW_POINT_PROBABILITY:
      mutations = [move for move in self.environment.get_legal_moves(individual[-1]) 
        if move not in individual]
      if len(mutations) > 0:
        return individual + [random.choice(mutations)]

    # On other occasions, modify a middle point in the path, and delete the rest of the path.
    index = random.randrange(0, len(individual))
    mutations = [move for move in self.environment.get_legal_moves(individual[index - 1] 
      if index > 0 else self.start_position) if move not in individual]

    if len(mutations) == 0:
      return individual

    return individual[0:index] + [random.choice(mutations)]