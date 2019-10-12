class Entity:
  def __init__(self, entity_type, position):
    self.entity_type = entity_type
    self.position = position

  def update(self, grid):
    """Returns whether there will be another step for this entity, so we can know when to
    end the simulation."""
    return False

  def serialize(self):
    raise NotImplementedError()

  def _serialize(self, data):
    """Helper method for inherited entities"""
    return {
      **{ 'type': self.entity_type, 'position': self.position },
      **data,
    }