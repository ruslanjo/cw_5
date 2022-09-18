from __future__ import annotations
from typing import TYPE_CHECKING
import abc

if TYPE_CHECKING:
    from application.assets.characters import BaseUnit


class Skill(abc.ABC):
    user = None
    target = None

    @property
    @abc.abstractmethod
    def name(self):
        pass

    @property
    @abc.abstractmethod
    def required_stamina(self):
        pass

    @property
    @abc.abstractmethod
    def damage(self):
        pass

    @abc.abstractmethod
    def skill_effect(self):
        pass

    def _check_stamina(self, user: BaseUnit): # TODO добавить аннотация BaseUnit
        return user.stamina >= self.required_stamina

    def use(self, user: BaseUnit, target: BaseUnit): # TODO добавить аннотацию BaseUnit
        self.user = user
        self.target = target

        if self._check_stamina(user):
            return self.skill_effect()
        return f'{self.user.name} попытался использовать {self.name}, но у него не хватило выносливости.'


class FireFist(Skill):
    name = 'Огненный кулак'
    required_stamina = 5.5
    damage = 10

    def skill_effect(self) -> str:
        self.user.stamina -= self.required_stamina

        if self.target.hp < self.damage:
            self.target.hp = 0
        else:
            self.target.hp -= self.damage

        return f'{self.user.name} использует {self.name} и наносит {self.damage} урона сопернику.'


class Armageddon(Skill):
    name = 'Армагедон'
    required_stamina = 8
    damage = 18

    def skill_effect(self):
        self.user.stamina -= self.required_stamina

        if self.target.hp < self.damage:
            self.target.hp = 0
        else:
            self.target.hp -= self.damage
        return f'{self.user.name} использует {self.name} и наносит {self.damage} урона сопернику.'
