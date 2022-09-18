################## Warriors' config ###############################
import application.assets.skills as skill

WARRIOR_CONFIG = {
    'name': 'Воин',
    'max_health': 50,
    'max_stamina': 20,
    'attack_idx': 5,
    'stamina_idx': 1.2,  # модификатор выносливости
    'armor_idx': 3,
    'skill': skill.FireFist()
}

################## Thief's config ###############################

THIEF_CONFIG = {
    'name': 'Вор',
    'max_health': 40,
    'max_stamina': 15,
    'attack_idx': 6,
    'stamina_idx': 1.3,  # модификатор выносливости
    'armor_idx': 2,
    'skill': skill.Armageddon()
}
