from grid_environment import Grid
from entities import RobotEntity, BrickEntity
import json


def main():
  grid = Grid(size=10)
  grid.add_entity(RobotEntity((1,1), path=[
    (1,2), (1,3), (1,4)
  ]))
  grid.add_entity(BrickEntity((3, 1)))
  grid.add_entity(BrickEntity((3, 2)))
  grid.add_entity(BrickEntity((3, 3)))
  grid.add_entity(BrickEntity((3, 4)))

  with open('example_grid.json', 'w') as grid_file:
    grid_file.write(json.dumps(grid.serialize()))


if __name__ == '__main__':
  main()