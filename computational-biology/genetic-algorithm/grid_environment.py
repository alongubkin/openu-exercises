from entities import ENTITY_BY_TYPE

LEGAL_MOVES = [
  (0, -1),  # Up
  (0, 1),   # Down
  (-1, 0),  # Left
  (1, 0),   # Right
]

class Grid:
  def __init__(self, size):
    self.entities = {}
    self.size = size
  
  def add_entity(self, entity):
    assert self._verify_position(entity.position)

    if entity.position not in self.entities:
      self.entities[entity.position] = []

    if not all(entity.walkable for entity in self.entities[entity.position]):
      raise Exception('Entity position is not walkable.')

    self.entities[entity.position].append(entity)

  def get_all_entities(self):
    """Returns all entities"""
    for entities in self.entities.values():
      for entity in entities:
        yield entity

  def get_entities(self, position):
    """Returns all entities in a specific position"""
    return self.entities.get(position, [])

  def find_entity(self, entity_class):
    """Finds the first entity of a specific type"""
    for entity in self.get_all_entities():
      if entity.TYPE == entity_class.TYPE:
        return entity
        
  def move_entity(self, entity, position):
    """Move an entity to a specific position. If an entity is already there, it must be walkable."""
    assert entity in self.entities[entity.position]
    assert self._verify_position(position)

    if position not in self.entities:
      self.entities[position] = []

    if not all(entity.walkable for entity in self.entities[position]):
      raise Exception('New position is not walkable.')

    self.entities[position].append(entity)
    self.entities[entity.position].remove(entity)

    entity.position = position

  def update(self):
    done = False
    for entity in list(self.get_all_entities()):
      if entity.update(self):
        done = True
    
    return done
  
  def _verify_position(self, position):
    x, y = position
    return (x >= 0 and x < self.size) and (y >= 0 and y < self.size)

  def get_legal_moves(self, position):
    for delta_x, delta_y in LEGAL_MOVES:
      x, y = position
      potential_position = (x + delta_x, y + delta_y)

      if not self._verify_position(potential_position):
        continue

      if not all(entity.walkable for entity in self.get_entities(potential_position)):
        continue
    
      yield potential_position

  def serialize(self):
    return {
      'size': self.size,
      'entities': [entity.serialize() for entity in self.get_all_entities()],
    }

  @staticmethod
  def deserialize(data):
    grid = Grid(data['size'])
    for entity in data['entities']:
      grid.add_entity(ENTITY_BY_TYPE[entity['type']].deserialize(entity))

    return grid

  def __copy__(self):
    return self.deserialize(self.serialize())