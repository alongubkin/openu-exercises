from copy import copy

def neighborhood(matrix, position):
  x, y = position

  size = len(matrix)
  assert len(matrix[0]) == size 

  return {
    # Left column
    'left': matrix[y][x - 1] if x > 0 else None,
    'top_left': matrix[y - 1][x - 1] if x > 0 and y > 0 else None,
    'bottom_left': matrix[y + 1][x - 1] if x > 0 and y + 1 < size else None,
    
    # Top and bottom
    'top': matrix[y - 1][x] if y > 0 else None,
    'bottom': matrix[y + 1][x] if y + 1 < size else None,

    # Right column
    'right': matrix[y][x + 1] if x + 1 < size else None,
    'top_right': matrix[y - 1][x + 1] if x + 1 < size and y > 0 else None,
    'bottom_right': matrix[y + 1][x + 1] if x + 1 < size and y + 1 < size else None,
  }


class CellularAutomataEntity:
  def get_color(self):
    raise NotImplementedError()


class CellularAutomata2D:
  def __init__(self, size):
    self.matrix = [[None for i in range(size)] for j in range(size)] # Initialize empty matrix
    self.size = size
    self.started = False

  def add_entity(self, position, entity):
    if self.started:
      raise Exception('You cannot add entities after the cellular automata has started!')

    x, y = position
    if self.matrix[y][x] is not None:
      raise Exception('Position is already occupied.')
    
    self.matrix[y][x] = entity
    
  def step(self):
    self.started = True

    # To emulate simultaneous update of the main matrix a temporary matrix is used.
    matrix = [[copy(item) for item in row] for row in self.matrix]

    for y in range(self.size):
      for x in range(self.size):
        # Calculate the new state of each cell based on its current state, the state of its
        # neigherhoods, and the transition rules.
        matrix[y][x] = self.transition(copy(self.matrix[y][x]), 
          neighborhood(self.matrix, (x, y)))

    # Update the main matrix.
    self.matrix = matrix

  def transition(self, entity, neighborhood):
    raise NotImplementedError()

  