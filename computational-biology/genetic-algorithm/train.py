import sys
import json
import random
from genetic_path_finder import GeneticPathfinder
from genetic_path_optimizer import GeneticPathOptimizer
from entities import BrickEntity, RobotEntity, TreasureEntity
from grid_environment import Grid

def main():
  try:
    _, environment_path, solution_path = sys.argv
  except ValueError:
    print('USAGE: train.py <input-environment> <output-solution-environment>')
    return

  # Load the environment
  with open(environment_path, 'r') as environment_file:
    environment = Grid.deserialize(json.loads(environment_file.read()))
  
  # Find a path using genetic algorithm
  GeneticPathOptimizer(environment).run()
  
  # Save the solution
  with open(solution_path, 'w') as solution_file:
    solution_file.write(json.dumps(environment.serialize()))

if __name__ == '__main__':
  main()