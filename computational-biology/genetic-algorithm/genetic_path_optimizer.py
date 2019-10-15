import random
from genetic_path_algorithm import GeneticPathAlgorithm
from entities import RobotEntity, TreasureEntity
from genetic_path_finder import GeneticPathfinder

MAX_ITERATIONS = 5
POPULATION_SIZE = 5
MUTATION_RATE = 0.5

class GeneticPathOptimizer(GeneticPathAlgorithm):
  def __init__(self, environment):
    super(GeneticPathOptimizer, self).__init__(environment, POPULATION_SIZE,
      debug="GeneticPathOptimizer")

  def create_population(self):
    for _ in range(POPULATION_SIZE):
      self.reset_environment()
      yield GeneticPathfinder(self.environment).run()

  def fitness(self, individual):
    # Reset the environment and set a new path for the robot
    self.reset_environment()
    self.environment.find_entity(RobotEntity).path = individual

    # Simulate the environment
    while self.environment.update():
      pass

    return 1.0 / len(individual)

  def stop_condition(self, iterations, fitness):
    return iterations > MAX_ITERATIONS

  def crossover(self, parent1, parent2):
    intersections = [(index1, index2) for index1, point1 in enumerate(parent1) 
      for index2, point2 in enumerate(parent2) if point1 == point2]

    if len(intersections) == 0:
      return min([parent1, parent2], key=len)

    index1, index2 = random.choice(intersections)

    return min([
      parent1,
      parent2,
      parent1[0:index1] + parent2[index2:],
      parent2[0:index2] + parent1[index1:],
    ], key=len)

  def mutate(self, individual):
    if random.random() > MUTATION_RATE:
      return individual

    point = random.randrange(0, len(individual))
    self.reset_environment()

    if random.random() <= 0.5:
      # Find an alternative path _to_ this point
      self.environment.find_entity(RobotEntity).path = individual
      return GeneticPathfinder(self.environment).run() + individual[point + 1:]
    else:
      # Find an alternative path _from_ this point
      self.environment.move_entity(self.environment.find_entity(RobotEntity), individual[point])
      return individual[0:point] + GeneticPathfinder(self.environment).run()