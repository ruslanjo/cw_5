import dataclasses
from application.configs.game_units_config import WARRIOR_CONFIG, THIEF_CONFIG
from application.assets.skills import Skill


@dataclasses.dataclass
class UnitClass:
    name: str
    max_health: float
    max_stamina: float
    attack_idx: float
    stamina_idx: float  # модификатор выносливости
    armor_idx: float
    skill: Skill


warrior_class = UnitClass(**WARRIOR_CONFIG)
thief_class = UnitClass(**THIEF_CONFIG)

unit_classes = {warrior_class.name: warrior_class,
                thief_class.name: thief_class}
