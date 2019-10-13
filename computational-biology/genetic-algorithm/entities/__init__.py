from entities.robot_entity import RobotEntity
from entities.brick_entity import BrickEntity
from entities.treasure_entity import TreasureEntity

ENTITY_BY_TYPE = {
  RobotEntity.TYPE: RobotEntity,
  BrickEntity.TYPE: BrickEntity,
  TreasureEntity.TYPE: TreasureEntity,
}
