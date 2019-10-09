import matplotlib.pyplot as plt
from cellular_automata import CellularAutomata2D, CellularAutomataEntity
from visualizer import CellularAutomataVisualizer
import random
from statistics import mean
import math

OPPOSITE_SEX = {
  'M': 'F',
  'F': 'M',
}


OPPOSITE_DIRECTION = {
  'left': 'right',
  'top_left': 'bottom_right',
  'bottom_left': 'top_right',
  'top': 'bottom',
  'bottom': 'top',
  'right': 'left',
  'top_right': 'bottom_left',
  'bottom_right': 'top_left',
}

MATRIX_SIZE = 20
TOTAL_COUPLES = 50
MINIMUM_BREAKUP_SCORE_DIFF = 15
BREAKUP_PROBABILITY_COEFFICIENT = 0.142
INITIAL_CYCLES = 3000
UNMARRIED_SCORE = 20
MAXIMUM_SCORE = 100

class Person(CellularAutomataEntity):
  def __init__(self, name, gender, score=0, direction=None, 
               married_to=None, breakups=None, disappear=False, total_breakups=0):
    self.name = name
    self.gender = gender
    self.score = score
    self.direction = direction
    self.married_to = married_to
    self.breakups = [] if breakups is None else breakups
    self.disappear = disappear
    self.total_breakups = total_breakups

  def get_color(self):
    if self.gender == 'M':
      return (30, 144, 255)
    elif self.gender == 'F':
      return (255, 105, 180)
  
  def add_breakup(self, name):
    self.breakups.insert(0, name)

    if len(self.breakups) > 3:
      self.breakups = self.breakups[0:3]

    self.total_breakups += 1

  def __copy__(self):
    return Person(self.name, self.gender, self.score, self.direction, self.married_to, 
      self.breakups, self.disappear, self.total_breakups)

class Spot(CellularAutomata2D):
  def __init__(self, walkable_from=None):
    self.walkable_from = walkable_from
  
  def get_color(self):
    return (255, 255, 255)

  def __copy__(self):
    return Spot(self.walkable_from)

class MarriageGame(CellularAutomata2D):
  def __init__(self, matrix_size, total_people):
    super(MarriageGame, self).__init__(matrix_size)

    # Generate 50 men and 50 women in random places in the center of the matrix.
    area = matrix_size
    people = 0

    positions = list(range(area * area))
    random.shuffle(positions)

    for position in positions:
      if people >= total_people:
        continue

      x = int(position / area)
      y = int(position % area)

      self.add_entity((x, y), Person(
        name=position, 
        gender='M' if people % 2 == 0 else 'F',
        score=random.randint(0, MAXIMUM_SCORE + 1),
      ))
      
      people += 1

    print('Added {}/{} people.'.format(people, total_people))

    # Add spots in the empty places
    for y in range(self.size):
      for x in range(self.size):
        if self.matrix[y][x] is None:
          self.add_entity((x, y), Spot())


  def _walk_transition(self, entity, neighborhood):
    if isinstance(entity, Spot) and entity.walkable_from is None:
      for direction, neighbor in neighborhood.items():
        if isinstance(neighbor, Person) and neighbor.direction == OPPOSITE_DIRECTION[direction]:
          entity.walkable_from = direction
          return entity

    elif isinstance(entity, Spot) and entity.walkable_from is not None:
      person = neighborhood[entity.walkable_from]
      if isinstance(person, Person) and person.direction == OPPOSITE_DIRECTION[entity.walkable_from]:
        return person
      else:
        entity.walkable_from = None
        return entity
          
    elif isinstance(entity, Person) and entity.direction is not None:
      spot = neighborhood[entity.direction]
      if isinstance(spot, Spot) and spot.walkable_from == OPPOSITE_DIRECTION[entity.direction]:
        return Spot()

  def _marry_transition(self, entity, neighborhood):
    if not isinstance(entity, Person):
      return None

    partner = neighborhood['right' if entity.gender == 'M' else 'left']
    if not isinstance(partner, Person):
      return None

    if entity.married_to is None:
      if partner.gender == OPPOSITE_SEX[entity.gender] and partner.married_to is None:
        if partner.name in entity.breakups:
          # Can't marry, forget oldest breakup.
          entity.add_breakup(None)
        else:
          entity.married_to = partner.name
          entity.direction = None
          
        return entity

  def _male_attraction_transition(self, entity, neighborhood):
    MALE_ATTRACTION = {
      'bottom_right': ['bottom'],
      'top_right': ['top'],
      'bottom_left': ['left'],
      'top_left': ['left'],
      'right': ['bottom_left', 'top_left', 'bottom', 'top'],
      'bottom': ['bottom_left', 'left'],
      'left': ['top_left', 'bottom_left', 'top', 'bottom'],
      'top': ['top_left', 'left'],
    }

    if not isinstance(entity, Person) or not entity.gender == 'M':
      return None
      
    if entity.married_to is not None:
      return None
    
    # Make a list of the most attractive women.
    women = [direction for direction, neighbor in neighborhood.items() if isinstance(neighbor, Person)
      and neighbor.gender == 'F' and neighbor.married_to is None and neighbor.name not in entity.breakups]
    women.sort(key=lambda direction: abs(neighborhood[direction].score - entity.score))

    if len(women) == 0:
      return None

    # Go to the best direction according to the priority in MALE_ATTRACTION.
    directions = [direction for direction in MALE_ATTRACTION[women[0]] 
      if isinstance(neighborhood[direction], Spot)]

    if len(directions) > 0:
      entity.direction = directions[0]
      return entity

  def _female_attraction_transition(self, entity, neighborhood):
    if not isinstance(entity, Person) or not entity.gender == 'F':
      return None
      
    if entity.married_to is not None:
      return None

    for neighbor in neighborhood.values():
      if not isinstance(neighbor, Person):
        continue

      if neighbor.gender != OPPOSITE_SEX[entity.gender] or neighbor.married_to is not None:
        continue

      if neighbor.name in entity.breakups:
        continue

      entity.direction = None
      return entity

  def _walk_randomly_transition(self, entity, neighborhood):
    if not isinstance(entity, Person) or entity.married_to is not None:
      return None

    directions = [direction for direction in OPPOSITE_DIRECTION.keys() 
      if isinstance(neighborhood[direction], Spot)]

    if len(directions) > 0:
      entity.direction = random.choice(directions)
      return entity

  def _breakup_randomly_transition(self, entity, neigborhood):
    if not isinstance(entity, Person) or entity.married_to is None:
      return None

    partner = neigborhood['right' if entity.gender == 'M' else 'left']
    if not isinstance(partner, Person) or partner.married_to != entity.name:
      return None

    score_diff = abs(partner.score - entity.score)
    if score_diff <= MINIMUM_BREAKUP_SCORE_DIFF:
      return None
    
    if random.random() > 1.0 / math.pow(score_diff, BREAKUP_PROBABILITY_COEFFICIENT):
      entity.add_breakup(entity.married_to)
      entity.married_to = None
      return entity

  def _update_breakup_status_transition(self, entity, neighborhood):
    if not isinstance(entity, Person) or entity.married_to is None:
      return None

    partner = neighborhood['right' if entity.gender == 'M' else 'left']
    if not isinstance(partner, Person) or partner.married_to != entity.name:
      entity.add_breakup(entity.married_to)
      entity.married_to = None
      return entity

  def transition(self, entity, neighborhood):
    result = self._walk_transition(entity, neighborhood)
    if result is not None:
      return result
    
    result = self._marry_transition(entity, neighborhood)
    if result is not None:
      return result
    
    result = self._male_attraction_transition(entity, neighborhood)
    if result is not None:
      return result   
   
    result = self._female_attraction_transition(entity, neighborhood)
    if result is not None:
      return result

    result = self._walk_randomly_transition(entity, neighborhood)
    if result is not None:
      return result   

    result = self._breakup_randomly_transition(entity, neighborhood)
    if result is not None:
      return result 

    result = self._update_breakup_status_transition(entity, neighborhood)
    if result is not None:
      return result   

    return entity

  def stats(self):
    scores = []

    for y in range(self.size):
      for x in range(self.size):
        if not isinstance(self.matrix[y][x], Person):
          continue
        
        person = self.matrix[y][x]

        if person.gender == 'F' and person.married_to is not None:
          partner = self.matrix[y][x - 1]
          if not isinstance(self.matrix[y][x-1], Person) or partner.gender != 'M':
            continue

          if person.married_to == partner.name:
            scores.append(abs(partner.score - person.score))
          
    married_couples = len(scores)

    scores += [UNMARRIED_SCORE] * (TOTAL_COUPLES - len(scores))
    return married_couples, 1.0 - (mean(scores) if len(scores) > 0 else 0) / MAXIMUM_SCORE


def main():
  ca = MarriageGame(matrix_size=MATRIX_SIZE, total_people=TOTAL_COUPLES * 2)
  
  # Run initial cycles
  print('Running initial cycles...')
  for _ in range(INITIAL_CYCLES):
    ca.step()

  # Show real-time visualization
  visualizer = CellularAutomataVisualizer(ca)
  visualizer.update()

  while True:
    ca.step()

    visualizer.update()
    
    married_couples, hapiness = ca.stats()
    print('Married couples: {}/{}, hapiness: {:.2f}%'.format(married_couples, TOTAL_COUPLES, hapiness * 100))

    plt.pause(0.5)


if __name__ == "__main__":
  main()