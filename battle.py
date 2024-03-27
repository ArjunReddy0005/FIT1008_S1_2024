from __future__ import annotations
from pokemon_base import *
from main import Trainer, PokeTeam
from typing import Tuple
from battle_mode import BattleMode
from array_sorted_list import *
from stack_adt import *
from queue_adt import *
from math import *

class Battle:

    def __init__(self, trainer_1: Trainer, trainer_2: Trainer, battle_mode: BattleMode, criterion = "health") -> None:
        self.trainer_1 = trainer_1
        self.trainer_1.pick_team("random")
        self.trainer_2 = trainer_2
        self.trainer_2.pick_team("random")
        self.battle_mode = battle_mode
        self.criterion = criterion
        # self._create_teams()
        self.both_defeated = None
        self.pk_to_add = ArrayR(2)

    def commence_battle(self) -> Trainer | None:
        if self.battle_mode.value == 0:
            return self.set_battle()
        elif self.battle_mode.value == 1:
            return self.rotate_battle()
        elif self.battle_mode.value == 2:
            return self.optimise_battle()
    def _create_teams(self) -> None:
        self.trainer_1.trainer_team.assemble_team(battle_mode=self.battle_mode, criterion=self.criterion) # going to initialise the ADT in the self.battle_team attribute
        self.trainer_2.trainer_team.assemble_team(battle_mode=self.battle_mode, criterion=self.criterion)
        if isinstance(type(self.trainer_1.trainer_team.team), type(self.trainer_2.trainer_team.team)):
            raise Exception("Pokemon should be in the same type of Data Structure to commence battle.")
        elif self.battle_mode.value == 0 and not (isinstance(self.trainer_2.trainer_team.team, ArrayStack) or isinstance(self.trainer_1.trainer_team.team, ArrayStack)):
            raise Exception("Both Teams Pokemon Must Be Stored In Stack ADTs")
        elif self.battle_mode.value == 1 and not (isinstance(self.trainer_2.trainer_team.team, CircularQueue) or isinstance(self.trainer_1.trainer_team.team, CircularQueue)):
            raise Exception("Both Teams Pokemon Must Be Stored In Circular Queue ADTs")
        elif self.battle_mode.value == 2 and not (isinstance(self.trainer_2.trainer_team.team, ArraySortedList) or isinstance(self.trainer_1.trainer_team.team, ArraySortedList)):
            raise Exception("Both Teams Pokemon Must Be Stored In Array Sorted List ADTs")
        else:
            return self.trainer_1.trainer_team, self.trainer_2.trainer_team
    # Note: These are here for your convenience
    # If you prefer you can ignore them
    def set_battle(self) -> PokeTeam | None:
        t1 = self.trainer_1
        t2 = self.trainer_2
        round = 0
        result = 3
        already_battle_poke_1 = ArrayStack(t1.trainer_team.size)
        already_battle_poke_2 = ArrayStack(t2.trainer_team.size)
        both_defeated = False
        # for i in range(t1.trainer_team.size):
        #     t2.register_pokemon(t1.trainer_team.array_team[i])
        #
        # for i in range(t2.trainer_team.size):
        #     t1.register_pokemon(t2.trainer_team.array_team[i])

        p1_score = 0
        p2_score = 0
        p1 = t1.trainer_team.team.pop()
        t2.register_pokemon(p1)
        p2 = t2.trainer_team.team.pop()
        t1.register_pokemon(p2)

        while not t1.trainer_team.team.is_empty() and not t2.trainer_team.team.is_empty():

            if p1.get_speed() > p2.get_speed():

                result = self.first_poke_attacks(p1, p2, t1, t2)

            elif p1.get_speed() < p2.get_speed():
                result = self.second_poke_attacks(p1, p2, t1, t2)
            elif p1.get_speed() == p2.get_speed():

                result = self.both_attack(p1, p2, t1, t2)

            # Don't know if the below check is needed.
            if result == 2 and self.both_defeated:
                print(f"Its a draw for round no. {round}")
                self.both_defeated = False
                p1 = t1.trainer_team.team.pop()
                t2.register_pokemon(p1)
                p2 = t2.trainer_team.team.pop()
                t1.register_pokemon(p2)
            elif result == 3 and not self.both_defeated:
                already_battle_poke_1.push(self.pk_to_add[0])
                already_battle_poke_2.push(self.pk_to_add[0])
            if result == 0:
                print(f"{p1.get_name()} won round no. {round}.")
                p1 = self.pk_to_add[0]
                p1.level += 1
                self.pk_to_add[0] = p1
                p1_score += 1
                already_battle_poke_1.push(self.pk_to_add[0])

                p2 = t2.trainer_team.team.pop()
                t1.register_pokemon(p2)

            elif result == 1:
                print(f"{p2.get_name()} won round no. {round}.")
                p2 = self.pk_to_add[1]
                p2.level += 1
                self.pk_to_add[1] = p2
                p2_score += 1
                already_battle_poke_2.push(self.pk_to_add[1])
                p1 = t1.trainer_team.team.pop()
                t2.register_pokemon(p1)
            round += 1
        while not t1.trainer_team.team.is_empty():
            already_battle_poke_2.push(t1.trainer_team.team.pop())
        while not t2.trainer_team.team.is_empty():
            already_battle_poke_1.push(t2.trainer_team.team.pop())


        replacing_array_stack_1 = ArrayStack(len(already_battle_poke_1))
        replacing_array_stack_2 = ArrayStack(len(already_battle_poke_2))
        for i in range(len(already_battle_poke_1)):
            pokemon = already_battle_poke_1.pop()
            replacing_array_stack_1.push(pokemon)

        for i in range(len(already_battle_poke_2)):
            pokemon = already_battle_poke_2.pop()
            replacing_array_stack_2.push(pokemon)


        self.trainer_1.trainer_team.team = replacing_array_stack_1
        self.trainer_2.trainer_team.team = replacing_array_stack_2
        self.trainer_1.get_pokedex_completion()
        self.trainer_2.get_pokedex_completion()
        if p1_score > p2_score:
            return self.trainer_1
        elif p2_score > p1_score:
            return self.trainer_2
        else:
            return None

    def rotate_battle(self) -> PokeTeam | None:
t1 = self.trainer_1
        t2 = self.trainer_2
        round = 0
        result = 3
        already_battle_poke_1 = CircularQueue(t1.trainer_team.size)
        already_battle_poke_2 = CircularQueue(t2.trainer_team.size)
        both_defeated = False
        p1_score = 0
        p2_score = 0
        while len(t1.trainer_team.team) > 0 and len(t2.trainer_team.team) > 0:
            p1 = t1.trainer_team.team.serve()
            p2 = t2.trainer_team.team.serve()

            if p1.get_speed() > p2.get_speed():

                result = self.first_poke_attacks(p1, p2, t1, t2)

            elif p1.get_speed() < p2.get_speed():

                result = self.second_poke_attacks(p1, p2, t1, t2)
            elif p1.get_speed() == p2.get_speed():

                result = self.both_attack(p1, p2, t1, t2)

            # Don't know if the below check is needed.
            if result == 2 and both_defeated:
                print(f"Its a draw for round no. {round}")
                self.both_defeated = False
            elif result == 3 and not self.both_defeated:
                t1.trainer_team.team.append(self.pk_to_add[0])
                t2.trainer_team.team.append(self.pk_to_add[1])
            if result == 0:
                print(f"{p1.get_name()} won round no. {round}.")
                p1 = self.pk_to_add[0]
                p1.level += 1
                self.pk_to_add[0] = p1
                p1_score += 1
                t1.trainer_team.team.append(self.pk_to_add[0])
                # Do we append the carcase Pokemon to its team? if not, then dont push defeated pokemon to its team.

            elif result == 1:
                print(f"{p2.get_name()} won round no. {round}.")
                p2 = self.pk_to_add[1]
                p2.level += 1
                self.pk_to_add[1] = p2
                p2_score += 1
                t2.trainer_team.team.append(self.pk_to_add[1])

            round += 1

        self.trainer_1.trainer_team.team = t1.trainer_team.team
        self.trainer_2.trainer_team.team = t2.trainer_team.team
        if len(t1.trainer_team.team) == 0 and len(t2.trainer_team.team) > 0:
            return self.trainer_2.trainer_team
        elif len(t1.trainer_team.team) > 0 and len(t2.trainer_team.team) == 0:
            return self.trainer_1.trainer_team
        else:
            return None
    def optimise_battle(self) -> PokeTeam | None:
        t1 = self.trainer_1
        t2 = self.trainer_2
        round = 0
        result = 3
        both_defeated = False
        p1_score = 0
        p2_score = 0
        i = 0
        j = 0
        p1 = t1.trainer_team.team.delete_at_index(i)
        p2 = t2.trainer_team.team.delete_at_index(i)
        while i < t1.trainer_team.size and j < t2.trainer_team.size:

            if p1.get_speed() > p2.get_speed():
                result = self.first_poke_attacks(p1, p2, t1, t2)

            elif p1.get_speed() < p2.get_speed():
                result = self.second_poke_attacks(p1, p2, t1, t2)

            elif p1.get_speed() == p2.get_speed():
                result = self.both_attack(p1, p2, t1, t2)

            if result == 2 and both_defeated:
                print(f"Its a draw for round no. {round}")
                self.both_defeated = False
            elif result == 3 and not self.both_defeated:
                t1.trainer_team.team[i] = self.pk_to_add[0]
                t2.trainer_team.team[j] = self.pk_to_add[1]
                i += 1
                j += 1
                #dont know if carcase of Pokemon gets deleted. If so then use delete_at_index()
            elif result == 0:
                print(f"{p1.get_name()} won round no. {round}.")
                p1 = self.pk_to_add[0]
                p1.level += 1
                self.pk_to_add[0] = p1
                p1_score += 1
                t1.trainer_team.team[i] = self.pk_to_add[0]
                # Do we append the carcase Pokemon to its team? if not, then dont push defeated pokemon to its team.

            elif result == 1:
                print(f"{p2.get_name()} won round no. {round}.")
                p2 = self.pk_to_add[1]
                p2.level += 1
                self.pk_to_add[1] = p2
                p2_score += 1
                t2.trainer_team.team[i] = self.pk_to_add[1]

            round += 1

        self.trainer_1.trainer_team.team = t1.trainer_team.team
        self.trainer_2.trainer_team.team = t2.trainer_team.team
        if i < j:
            return self.trainer_1.trainer_team
        elif i > j:
            return self.trainer_2.trainer_team
        else:
            return None
    def first_poke_attacks(self, p1: Pokemon, p2: Pokemon, t1: Trainer, t2: Trainer):
        attack_damage_1 = ceil(p1.attack(other_pokemon=p2) * (t1.get_pokedex_completion() / t2.get_pokedex_completion()))
        attack_damage_2 = ceil(p2.attack(other_pokemon=p1) * (t2.get_pokedex_completion() / t1.get_pokedex_completion()))
        val = None
        while True:

            p2.health -= attack_damage_1
            # Can't really have a draw.
            if p2.get_health() <= 0:
                val = 0
                break
            p1.health -= attack_damage_2
            if p1.get_health() <= 0:
                val = 1
                break
        self.pk_to_add[0] = p1
        self.pk_to_add[1] = p2
        return val

    def second_poke_attacks(self, p1: Pokemon, p2: Pokemon, t1: Trainer, t2: Trainer):
        attack_damage_1 = ceil(p1.attack(other_pokemon=p2) * (t1.get_pokedex_completion() / t2.get_pokedex_completion()))
        attack_damage_2 = ceil(p2.attack(other_pokemon=p1) * (t2.get_pokedex_completion() / t1.get_pokedex_completion()))
        val = None
        while True:

            p1.health -= attack_damage_2
            # Can't really have a draw.
            if p1.get_health() <= 0:
                val = 1
                break
            p2.health -= attack_damage_1
            if p2.get_health() <= 0:
                val = 0
                break
        self.pk_to_add[0] = p1
        self.pk_to_add[1] = p2
        return val

    def both_attack(self, p1: Pokemon, p2: Pokemon, t1: Trainer, t2: Trainer):
        attack_damage_1 = ceil(p1.attack(other_pokemon=p2) * (t1.get_pokedex_completion() / t2.get_pokedex_completion()))
        attack_damage_2 = ceil(p2.attack(other_pokemon=p1) * (t2.get_pokedex_completion() / t1.get_pokedex_completion()))
        p1.health -= attack_damage_1
        p2.health -= attack_damage_2
        val = None

        if p1.get_health() <= 0 and p2.get_health() <= 0:
            self.both_defeated = True
            val = 2

        elif p1.get_health() <= 0:
            val = 0

        elif p2.get_health() <= 0:
            val = 1

        p1.health -= attack_damage_2
        if p1.get_health() <= 0:
            val = 0

        p1.health -= 1
        p2.health -= 1
        if p1.get_health() <= 0 and p2.get_health() <= 0:
            self.both_defeated = True
            val = 2

        elif p1.get_health() <= 0:
            val = 0

        elif p2.get_health() <= 0:
            val = 1
        if p1.get_health() > 0 and p2.get_health() > 0:
            val = 3

        self.pk_to_add[0] = p1
        self.pk_to_add[1] = p2
        return val

if __name__ == '__main__':
    t1 = Trainer('Ash')
    t2 = Trainer('Gary')
    b = Battle(t1, t2, BattleMode.ROTATE)
    b._create_teams()
    winner = b.commence_battle()

    if winner is None:
        print("Its a draw")
    else:
        print(f"The winner is {winner.get_name()}")
