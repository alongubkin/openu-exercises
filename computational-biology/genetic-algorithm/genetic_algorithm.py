import random

def weighted_random_choice(choices):
  max = sum(value for key, value in choices)
  pick = random.uniform(0, max)
  current = 0
  for key, value in choices:
    current += value
    if current > pick:
      return key
            
class GeneticAlgorithm:
  def __init__(self, population_size, debug=None):
    self.generation = 0
    self.population_size = population_size
    self.debug = debug

  def create_population(self):
    raise NotImplementedError()

  def fitness(self, individual):
    raise NotImplementedError()

  def crossover(self, parent1, parent2):
    raise NotImplementedError()

  def mutate(self, individual):
    raise NotImplementedError()
  
  def stop_condition(self, iterations, fitness):
    raise NotImplementedError()

  def next_generation(self, current_generation):
    next_generation = []
      
    while len(next_generation) < self.population_size:
      parent1 = weighted_random_choice(current_generation)
      parent2 = weighted_random_choice(current_generation)

      offspring = self.mutate(self.crossover(parent1, parent2))
      next_generation.append(offspring)

    return next_generation

  def run(self, iterations=1000):
    population = list(self.create_population())

    for iteration in range(iterations):
      current_generation = [(individual, self.fitness(individual)) for individual in population]
      best_individual, best_individual_fitness = max(current_generation, key=lambda item: item[1])

      if self.debug is not None:
        print('[{}] Generation {}, fitness: {}, best individual: {}'.format(
          self.debug, self.generation, best_individual_fitness, best_individual))

      if self.stop_condition(iteration, best_individual_fitness):
        return best_individual

      population = self.next_generation(current_generation)
      self.generation += 1

    return best_individual



