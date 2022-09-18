import dataclasses
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from application.assets.skills import Skill


@dataclasses.dataclass
class UnitClass:
    name: str
    max_health: float
    max_stamina: float
    attack: float
    stamina: float
    armor: float
    skill: Skill


class Unit




