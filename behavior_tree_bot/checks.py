

def if_neutral_planet_available(state):
    return any(state.neutral_planets())


def have_largest_fleet(state):
    return sum(planet.num_ships for planet in state.my_planets()) \
             + sum(fleet.num_ships for fleet in state.my_fleets()) \
           > sum(planet.num_ships for planet in state.enemy_planets()) \
             + sum(fleet.num_ships for fleet in state.enemy_fleets())

def have_more_planets_than_enemy(state):
    return len(state.my_planets()) > len(state.enemy_planets())


def is_enemy_stronger(state):
    my_power = sum(p.num_ships for p in state.my_planets()) + sum(f.num_ships for f in state.my_fleets())
    enemy_power = sum(p.num_ships for p in state.enemy_planets()) + sum(f.num_ships for f in state.enemy_fleets())
    return enemy_power > my_power


def has_idle_planet(state):
    return any(p.num_ships > 30 for p in state.my_planets())

def is_enemy_too_far(state):
    my_planets = state.my_planets()
    enemy_planets = state.enemy_planets()

    if not my_planets or not enemy_planets:
        return True

    min_dist = min(state.distance(m.ID, e.ID) for m in my_planets for e in enemy_planets
    )
    return min_dist > 10
