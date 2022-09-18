from __future__ import annotations
import abc
import random
from typing import Optional

from application.assets.game_unit_classes import UnitClass
from application.assets.equipment import Weapon, Armor


class BaseUnit(abc.ABC):
    def __init__(self, name: str, unit_class: UnitClass):
        self.name = name
        self.unit_class = unit_class
        self._hp = unit_class.max_health
        self._stamina = unit_class.max_stamina
        self.weapon = None
        self.armor = None
        self.is_skill_used = False

    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, value):
        self._hp = round(value, 2)

    @property
    def stamina(self):
        return self._stamina

    @stamina.setter
    def stamina(self, value):
        self._stamina = round(value, 2)


    def equip_weapon(self, weapon: Weapon):
        self.weapon = weapon
        return self.weapon

    def equip_armor(self, armor: Armor):
        self.armor = armor
        return self.armor

    def _calculate_attackers_damage(self, target: BaseUnit):
        '''
        УРОН = УРОН_АТАКУЮЩЕГО - БРОНЯ_ЦЕЛИ
        Урон атакующего = урон от оружия * модификатор атаки класса,
        урон от оружия = случайное число в диапазоне min-max damage
        '''
        attackers_damage = self.weapon.calculate_damage() * self.unit_class.attack_idx
        target_armor = self._calculate_target_armor(target)

        if target_armor > attackers_damage:
            return 0
        else:
            return round(attackers_damage - target_armor, 2)

    @staticmethod
    def _calculate_target_armor(target: BaseUnit) -> float:
        if target.stamina >= target.armor.stamina_per_hit:
            target_armor = target.unit_class.armor_idx * target.armor.defence
        else:
            target_armor = 0.0
        return target_armor

    def get_damage(self, damage: int) -> float:
        # Если выносливости больше, чем требуется для брони, то снижаем выносливость из-за исопльзования брони
        # В противном случае броня не используется и выносливость не тратится
        if self.stamina >= self.weapon.stamina_per_hit:
            self.stamina -= self.weapon.stamina_per_hit

        if self.hp < damage:
            self.hp = 0
        else:
            self.hp -= damage
        return damage

    def use_skill(self, target: BaseUnit) -> str:
        if self.is_skill_used:
            return f'{self.name} пытался применить {self.unit_class.skill.name} на {target.name},' \
                   f'однако навык уже использован'
        else:
            self.is_skill_used = True
            return self.unit_class.skill.use(user=self, target=target)

    def generate_response_text(self,
                               is_stamina_enough: bool,
                               damage: float = 0.0,
                               target: Optional[BaseUnit] = None) -> str:
        if not is_stamina_enough:
            return f"{self.name} попытался использовать {self.weapon.name}, но у него не хватило выносливости."

        if damage > 0:
            return f"{self.name} используя {self.weapon.name} пробивает {target.armor.name} соперника и " \
                   f"наносит {damage} урона."

        else:
            return f"{self.name} используя {self.weapon.name} наносит удар, " \
                   f"но {target.armor.name} cоперника его останавливает."

    @abc.abstractmethod
    def hit(self, target: BaseUnit) -> str:
        if self.stamina >= self.weapon.stamina_per_hit:
            damage = self._calculate_attackers_damage(target)
            self.stamina -= self.weapon.stamina_per_hit
            target.get_damage(damage)
            response_text = self.generate_response_text(target=target, damage=damage, is_stamina_enough=True)

        else:
            response_text = self.generate_response_text(is_stamina_enough=False)

        return response_text


class PlayerUnit(BaseUnit):
    def hit(self, target: BaseUnit) -> str:
        return super().hit(target)


class EnemyUnit(BaseUnit):
    def use_skill_with_probability(self, target: BaseUnit) -> Optional[str]:
        # с 10-процентной вероятностью enemy применяет навык
        figure = random.randint(1, 10)
        if figure == 1:
            return self.use_skill(target)

    def hit(self, target: BaseUnit) -> str:
        if not self.is_skill_used:
            # Враг пытается использовать скилл  с 10-процентной вероятностью
            response_text = self.use_skill_with_probability(target)
            # Если скилл не использован, враг наносит простой удар
            if not response_text:
                response_text = super().hit(target)
        else:
            response_text = super().hit(target)

        return response_text
