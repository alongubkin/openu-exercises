from entities.entity import Entity


class BrickEntity(Entity):
  def __init__(self, position):
    super(BrickEntity, self).__init__('BRICK', position)

  def serialize(self):
    return super(BrickEntity, self)._serialize({})
  
  @staticmethod
  def deserialize(data):
    return BrickEntity(tuple(data['position']))