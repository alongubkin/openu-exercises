from entities.entity import Entity


class TreasureEntity(Entity):
  TYPE = "TREASURE"
  
  def __init__(self, position):
    super(TreasureEntity, self).__init__(TreasureEntity.TYPE, position, walkable=True)

  def update(self, grid):
    return False

  def serialize(self):
    return super(TreasureEntity, self)._serialize({})
  
  @staticmethod
  def deserialize(data):
    return TreasureEntity(tuple(data['position'])) 