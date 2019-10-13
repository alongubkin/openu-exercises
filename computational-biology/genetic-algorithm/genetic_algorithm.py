import random

POPULATION_SIZE = 50
CROSSOVER_RATE = 0.7
MUTATION_RATE = 1.0

def weighted_random_choice(choices):
  max = sum(value for key, value in choices)
  pick = random.uniform(0, max)
  current = 0
  for key, value in choices:
    current += value
    if current > pick:
      return key
            
class GeneticAlgorithm:
  def __init__(self):
    self.generation = 0

  def create_population(self):
    raise NotImplementedError()

  def fitness(self, individual):
    raise NotImplementedError()

  def crossover(self, parent1, parent2):
    raise NotImplementedError()

  def mutate(self, individual):
    raise NotImplementedError()
  
  def _sort_population_by_fitness(self, population):
    return sorted(population, key=lambda individual: self.fitness(individual), reverse=True)

  def _f(self, population):
    return [(individual, self.fitness(individual)) for individual in population]

  def next_generation(self, population):
    current_generation = self._f(population)
    next_generation = []
      
    while len(next_generation) < POPULATION_SIZE:
      if random.random() < CROSSOVER_RATE:
        parent1 = weighted_random_choice(current_generation)
        parent2 = weighted_random_choice(current_generation)

        offspring = self.crossover(parent1, parent2)
      else:
        offspring = weighted_random_choice(current_generation)

      if random.random() < MUTATION_RATE:
       offspring = self.mutate(offspring)

      next_generation.append(offspring)

    return next_generation

  def run(self):
    population = list(self.create_population())

    for _ in range(2000):  # TODO: maximum iterations
      fittest = self._sort_population_by_fitness(population)[0]
      fitness = self.fitness(fittest)

      print('Generation {}, fitness: {}, fittest: {}'.format(self.generation, fitness, fittest))
      if fitness > 100 and fitness <= 100.1:
        print("FOUND!")
        return fittest

      population = self.next_generation(population)
      self.generation += 1

    return fittest



