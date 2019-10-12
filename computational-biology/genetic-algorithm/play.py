import pygame
import sys
import json
from grid_environment import Grid
from entities import RobotEntity, BrickEntity


def play(grid):
  pygame.init()

  screen = pygame.display.set_mode((grid.size * 32, grid.size * 32))

  robot = pygame.image.load('robot.png').convert()
  brick = pygame.image.load('brick.png').convert()

  pygame.display.set_icon(robot)
  pygame.display.set_caption('Robot with Genetic Algorithm')
    
    
  while True:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        return
    
    screen.fill((255, 255, 255))

    for entity in grid.entities.values():
      x, y = entity.position
      
      if isinstance(entity, RobotEntity):
        screen.blit(robot, (x * 32, y * 32))
      elif isinstance(entity, BrickEntity):
        screen.blit(brick, (x * 32, y * 32))
        
    grid.update()

    pygame.display.update()
    pygame.time.delay(100)
         

def main():
  try:
    _, game_path = sys.argv
  except:
    print('USAGE: play.py <game-path>')
    return

  with open(game_path, 'r') as game_file:
    grid = Grid.deserialize(json.loads(game_file.read()))

  play(grid)

if __name__== '__main__':
  main()