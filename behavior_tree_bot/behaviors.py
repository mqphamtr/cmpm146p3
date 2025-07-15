import sys
sys.path.insert(0, '../')
from planet_wars import issue_order


def attack_weakest_enemy_planet(state):
    # (1) If we currently have a fleet in flight, abort plan.
    if len(state.my_fleets()) >= 1:
        return False

    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda t: t.num_ships, default=None)

    # (3) Find the weakest enemy planet.
    weakest_planet = min(state.enemy_planets(), key=lambda t: t.num_ships, default=None)

    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        return False
    else:
        # (4) Send half the ships from my strongest planet to the weakest enemy planet.
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, strongest_planet.num_ships / 2)


def spread_to_weakest_neutral_planet(state):
    # Only proceed if we have both planets to act on
    if not state.my_planets() or not state.neutral_planets():
        return False

    # Choose planets
    strongest_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)
    weakest_planet = min(state.neutral_planets(), key=lambda p: p.num_ships, default=None)

    if not strongest_planet or not weakest_planet:
        return False

    # Don't act if we don't have enough ships to spare
    if strongest_planet.num_ships < 50:
        return False

    # Issue order
    #return issue_order(state, strongest_planet.ID, weakest_planet.ID, strongest_planet.num_ships / 2)
    return issue_order(state, strongest_planet.ID, weakest_planet.ID, strongest_planet.num_ships / 2)


def reinforce_weakest_friendly_planet(state):
    planets = state.my_planets()
    if len(planets) < 2:
        return False

    source = max(planets, key=lambda p: p.num_ships)
    dest = min(planets, key=lambda p: p.num_ships)

    if source.ID == dest.ID or source.num_ships < 10:
        return False

    return issue_order(state, source.ID, dest.ID, source.num_ships / 2)


def attack_closest_enemy_planet(state):
    my_planets = state.my_planets()
    enemy_planets = state.enemy_planets()
    if not my_planets or not enemy_planets:
        return False

    source = max(my_planets, key=lambda p: p.num_ships)
    closest = min(enemy_planets, key=lambda e: state.distance(source.ID, e.ID))

    if source.num_ships < 10:
        return False

    return issue_order(state, source.ID, closest.ID, source.num_ships / 2)
