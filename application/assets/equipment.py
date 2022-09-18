import dataclasses
import random
import json
from typing import Optional

import marshmallow
import marshmallow_dataclass
from application.constants import EQUIPMENT_DATA_PATH


@dataclasses.dataclass
class Weapon:
    name: str
    min_damage: float
    max_damage: float
    stamina_per_hit: float

    class Meta:
        unknown = marshmallow.EXCLUDE

    def calculate_damage(self) -> float:
        generated_damage: float = random.uniform(self.min_damage, self.max_damage)
        return generated_damage


@dataclasses.dataclass
class Armor:
    name: str
    defence: float
    stamina_per_hit: float

    class Meta:
        unknown = marshmallow.EXCLUDE


@dataclasses.dataclass
class EquipmentData:
    weapons_list: list
    armors_list: list


armor_schema = marshmallow_dataclass.class_schema(Armor)()
weapon_schema = marshmallow_dataclass.class_schema(Weapon)()


class Equipment:
    def __init__(self):
        json_data: dict | list = self._read_json(EQUIPMENT_DATA_PATH)
        self._equipment: EquipmentData = self._convert_json_to_dataclass(json_data)

    @property
    def equipment(self):
        return self._equipment

    @staticmethod
    def _read_json(json_path: str) -> list | dict:
        with open(json_path, 'r', encoding='utf-8') as data:
            json_data = json.load(data)
        return json_data

    @staticmethod
    def _convert_json_to_dataclass(json_data: dict):
        armor_data = json_data.get('armors')
        weapon_data = json_data.get('weapons')

        armors_list: list[Armor] = [armor_schema.load(item) for item in armor_data]
        weapons_list: list[Weapon] = [weapon_schema.load(item) for item in weapon_data]

        return EquipmentData(weapons_list=weapons_list, armors_list=armors_list)

    def get_weapon(self, weapon_name: str) -> Optional[Weapon]:
        for weapon in self.equipment.weapons_list:
            if weapon.name == weapon_name:
                return weapon

    def get_armor(self, armor_name: str) -> Optional[Armor]:
        for armor in self.equipment.armors_list:
            if armor.name == armor_name:
                return armor

    def get_weapons_list(self) -> list[Weapon]:
        return [weapon.name for weapon in self.equipment.weapons_list]

    def get_armors_list(self) -> list[Armor]:
        return [armor.name for armor in self.equipment.armors_list]
