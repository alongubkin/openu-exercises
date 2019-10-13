from entities.entity import Entity


class BrickEntity(Entity):
  TYPE = "BRICK"
  
  def __init__(self, position):
    super(BrickEntity, self).__init__(BrickEntity.TYPE, position, walkable=False)

  def serialize(self):
    return super(BrickEntity, self)._serialize({})
  
  @staticmethod
  def deserialize(data):
    return BrickEntity(tuple(data['position']))