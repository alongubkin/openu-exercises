from entities import ENTITY_BY_TYPE

    
class Grid:
  def __init__(self, size):
    self.entities = {}
    self.size = size
  
  def add_entity(self, entity):
    if entity.position in self.entities:
      raise Exception('Position is already occupied.')

    self.entities[entity.position] = entity

  def get_entity(self, position):
    return self.entities[position]

  def move_entity(self, entity, position):
    assert self.entities[entity.position] == entity

    if position in self.entities:
      raise Exception('New position is already occupied.')

    self.entities[position] = entity
    del self.entities[entity.position]

    entity.position = position

  def update(self):
    done = False
    for entity in list(self.entities.values()):
      if entity.update(self):
        done = True
    
    return done
        
  def serialize(self):
    return {
      'size': self.size,
      'entities': [entity.serialize() for entity in self.entities.values()],
    }

  @staticmethod
  def deserialize(data):
    grid = Grid(data['size'])
    for entity in data['entities']:
      grid.add_entity(ENTITY_BY_TYPE[entity['type']].deserialize(entity))

    return grid