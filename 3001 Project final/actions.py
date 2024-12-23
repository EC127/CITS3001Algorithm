def create_actions(red_actions, blue_actions, num_green):
    # red team actions
    red_actions.setdefault('1', {})['uncertainty'] = 9
    red_actions.setdefault('1', {})['follower_lost'] = round(0.01 * num_green)

    red_actions.setdefault('2', {})['uncertainty'] = 8
    red_actions.setdefault('2', {})['follower_lost'] = round(0.05 * num_green)

    red_actions.setdefault('3', {})['uncertainty'] = 7
    red_actions.setdefault('3', {})['follower_lost'] = round(0.07 * num_green)

    red_actions.setdefault('4', {})['uncertainty'] = 6
    red_actions.setdefault('4', {})['follower_lost'] = round(0.1 * num_green)

    red_actions.setdefault('5', {})['uncertainty'] = 5
    red_actions.setdefault('5', {})['follower_lost'] = round(0.13 * num_green)

    red_actions.setdefault('6', {})['uncertainty'] = 4
    red_actions.setdefault('6', {})['follower_lost'] = round(0.15 * num_green)

    red_actions.setdefault('7', {})['uncertainty'] = 3
    red_actions.setdefault('7', {})['follower_lost'] = round(0.17 * num_green)

    red_actions.setdefault('8', {})['uncertainty'] = 2
    red_actions.setdefault('8', {})['follower_lost'] = round(0.2 * num_green)

    red_actions.setdefault('9', {})['uncertainty'] = 1.5
    red_actions.setdefault('9', {})['follower_lost'] = round(0.4 * num_green)

    red_actions.setdefault('10', {})['uncertainty'] = 1
    red_actions.setdefault('10', {})['follower_lost'] = round(0.5 * num_green)

    # blue team actions
    blue_actions.setdefault('1', {})['uncertainty'] = 8.5
    blue_actions.setdefault('1', {})['energy_lost'] = 1

    blue_actions.setdefault('2', {})['uncertainty'] = 8
    blue_actions.setdefault('2', {})['energy_lost'] = 2

    blue_actions.setdefault('3', {})['uncertainty'] = 7.5
    blue_actions.setdefault('3', {})['energy_lost'] = 3

    blue_actions.setdefault('4', {})['uncertainty'] = 6
    blue_actions.setdefault('4', {})['energy_lost'] = 4

    blue_actions.setdefault('5', {})['uncertainty'] = 5.5
    blue_actions.setdefault('5', {})['energy_lost'] = 5

    blue_actions.setdefault('6', {})['uncertainty'] = 5
    blue_actions.setdefault('6', {})['energy_lost'] = 6

    blue_actions.setdefault('7', {})['uncertainty'] = 4.5
    blue_actions.setdefault('7', {})['energy_lost'] = 7

    blue_actions.setdefault('8', {})['uncertainty'] = 4
    blue_actions.setdefault('8', {})['energy_lost'] = 8

    blue_actions.setdefault('9', {})['uncertainty'] = 3.5
    blue_actions.setdefault('9', {})['energy_lost'] = 9

    blue_actions.setdefault('10', {})['uncertainty'] = 3
    blue_actions.setdefault('10', {})['energy_lost'] = 10