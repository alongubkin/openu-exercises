from entities.entity import Entity


class RobotEntity(Entity):
  TYPE = "ROBOT"
  
  def __init__(self, position, path=[]):
    super(RobotEntity, self).__init__(RobotEntity.TYPE, position, walkable=True)
    self.path = path

  def update(self, grid):
    if len(self.path) == 0:
      return False
    
    grid.move_entity(self, self.path[0])
    self.path = self.path[1:]

    return True

  def serialize(self):
    return super(RobotEntity, self)._serialize({
      'path': self.path,
    })
  
  @staticmethod
  def deserialize(data):
    return RobotEntity(tuple(data['position']), 
      [tuple(point) for point in data['path']]) 