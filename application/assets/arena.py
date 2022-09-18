import abc
from typing import Optional
from application.assets.characters import BaseUnit


class Singleton(abc.ABC):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super().__new__(cls)
        return cls.instance


class Arena(Singleton):
    STAMINA_PER_ROUND = 3
    player = None
    enemy = None
    game_is_running = False
    battle_result = ""

    def start_game(self, player: BaseUnit, enemy: BaseUnit) -> None:
        self.player = player
        self.enemy = enemy
        self.game_is_running = True

    def _stamina_regeneration(self) -> None:
        # если текущая + восстановленная выносливость за раунд превышают максимальную,
        # то устанавливаем максимальное значение выносливости
        for unit in (self.player, self.enemy):
            if unit.stamina + self.STAMINA_PER_ROUND > unit.unit_class.max_stamina:
                unit.stamina = unit.unit_class.max_stamina
            else:
                unit.stamina += self.STAMINA_PER_ROUND

    def _check_players_hp(self) -> Optional[str]:
        if self.player.hp == self.enemy.hp == 0:
            self.battle_result = f'Здоровье у {self.player.name} и {self.enemy.name} закончилось. Ничья!'

        elif self.player.hp > 0 and self.enemy.hp <= 0:
            self.battle_result = f'Победил {self.player.name}. У {self.enemy.name} закончилось здоровье!'

        elif self.player.hp <= 0 and self.enemy.hp > 0:
            self.battle_result = f'К сожалению, ваш герой {self.player.name} проиграл'

        return self.battle_result

    def next_turn(self) -> str:
        if self._check_players_hp():
            return self.battle_result
        else:
            self._stamina_regeneration()
            return self.enemy.hit(self.player)

    def player_hit(self) -> tuple[str, str]:
        hit_result = self.player.hit(self.enemy)
        next_turn_result = self.next_turn()  # может быть или результатом о финальном исходе, если ХП у одного
        # из игроков кончилось, или результатом с ударом опонента
        return hit_result, next_turn_result

    def player_use_skill(self) -> tuple[str, str]:
        skill_result = self.player.use_skill(self.enemy)
        next_turn_result = self.next_turn()
        return skill_result, next_turn_result

    def _end_game(self) -> str:
        self.game_is_running = False
        if not self.battle_result:
            return "Игра прервана, победитель не выявлен"
        else:
            return self.battle_result
