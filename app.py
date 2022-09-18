from flask import Flask, render_template, url_for, redirect, request
from application.assets.arena import Arena
from application.assets.game_unit_classes import unit_classes
from application.assets.equipment import Equipment
from application.assets.characters import PlayerUnit, EnemyUnit

app = Flask(__name__)
heroes = {}
arena = Arena()
equipment = Equipment()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/choose-hero/', methods=['POST', 'GET'])
def choose_hero():
    if request.method == 'GET':
        result = {'header': 'Выбор героя',
                  'classes': unit_classes.keys(),
                  'weapons': equipment.get_weapons_list(),
                  'armors': equipment.get_armors_list()
                  }
        url = url_for('choose_hero')
        return render_template('hero_choosing.html', result=result, url=url), 200

    if request.method == 'POST':
        form_data = request.form
        name = form_data.get('name')
        unit_class = form_data.get('unit_class')
        weapon = form_data.get('weapon')
        armor = form_data.get('armor')

        player_unit = PlayerUnit(name=name, unit_class=unit_classes.get(unit_class))
        player_unit.equip_weapon(equipment.get_weapon(weapon_name=weapon))
        player_unit.equip_armor(equipment.get_armor(armor_name=armor))

        heroes['player'] = player_unit

        return redirect(url_for('choose_enemy'))


@app.route('/choose-enemy/', methods=['GET', 'POST'])
def choose_enemy():
    if request.method == 'GET':
        result = {'header': 'Выбор опонента',
                  'classes': unit_classes.keys(),
                  'weapons': equipment.get_weapons_list(),
                  'armors': equipment.get_armors_list()
                  }
        url = url_for('choose_enemy')

        return render_template('hero_choosing.html', result=result, url=url)

    if request.method == 'POST':
        form_data = request.form
        name = form_data.get('name')
        unit_class = form_data.get('unit_class')
        weapon = form_data.get('weapon')
        armor = form_data.get('armor')

        enemy_unit = EnemyUnit(name=name, unit_class=unit_classes.get(unit_class))
        enemy_unit.equip_weapon(equipment.get_weapon(weapon_name=weapon))
        enemy_unit.equip_armor(equipment.get_armor(armor_name=armor))

        heroes['enemy'] = enemy_unit

        return redirect(url_for('fight'))


@app.route('/fight/')
def fight():
    arena.start_game(player=heroes.get('player'), enemy=heroes.get('enemy'))
    return render_template('fight.html', heroes=heroes)


@app.route('/fight/hit/')
def hit():
    hit_result, next_turn_result = arena.player_hit()
    result = f'{hit_result}\n{next_turn_result}'
    return render_template('fight.html', heroes=heroes, result=result)


@app.route('/fight/use-skill/')
def use_skill():
    skill_result, next_turn_result = arena.player_use_skill()
    result = f'{skill_result}\n{next_turn_result}'
    return render_template('fight.html', heroes=heroes, result=result)


@app.route('/fight/pass-turn/')
def pass_turn():
    next_turn_result = arena.next_turn()
    return render_template('fight.html', heroes=heroes, result=next_turn_result)


@app.route('/fight/end-fight/')
def end_fight():
    return render_template('index.html', heroes=heroes)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)

