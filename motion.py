import numpy as np
import pandas as pd
import random
import collections
import math


# note to me we can use opo the other if we get an interaction...
class Atom:
    numeric_label = 0

    def __init__(self):
        self.location = (random.randint(-100, 100), random.randint(-100, 100))
        self.numeric_label = Atom.numeric_label
        Atom.numeric_label += 1

    def simple_random_motion(self):
        x = random.randint(-1, 1)
        y = random.randint(-1, 1)
        self.location = (self.location[0] + x, self.location[1] + y)

    def check_distance(self, other):
        return math.sqrt((((self.location[0] - other.location[0]) ** 2) + (self.location[1] - other.location[1]) ** 2))

    def force_one(self):
        pass

    @property
    def location(self):
        return self.__location

    @location.setter
    def location(self, location):
        self.__location = location


class ParticleZero(Atom):
    def __init__(self):
        Atom.__init__(self)


class Universe:
    def __init__(self, eot):
        self.zero_particles = collections.deque()
        self.one_particles = collections.deque()
        self.end_of_time = eot
        self.record_of_the_state_of_the_universe = pd.DataFrame(np.nan, index=[x for x in range(self.end_of_time)],
                                                                columns=['time', 'zero_particles', 'one_particles'])

    def bang(self, number_of_zero_particles):
        set_of_zero_changes_to_one = set()
        age_of_universe = 0

        for particle in range(number_of_zero_particles):
            self.zero_particles.append(ParticleZero())

        while age_of_universe <= self.end_of_time:

            self.record_of_the_state_of_the_universe.ix[age_of_universe, 'time'] = age_of_universe
            self.record_of_the_state_of_the_universe.ix[age_of_universe, 'zero_particles'] = len(self.zero_particles)
            self.record_of_the_state_of_the_universe.ix[age_of_universe, 'one_particles'] = len(self.one_particles)

            for p_zero_move_counter in range(len(self.zero_particles)):
                p_zero_to_observe = self.zero_particles.pop()
                p_zero_to_observe.simple_random_motion()
                for p_zero_check_proximity in self.zero_particles:
                    if p_zero_to_observe.check_distance(p_zero_check_proximity) < 1:
                        set_of_zero_changes_to_one.add(p_zero_to_observe.numeric_label)
                        set_of_zero_changes_to_one.add(p_zero_check_proximity.numeric_label)
                self.zero_particles.appendleft(p_zero_to_observe)

            for p_catagorizeing_counter in range(len(self.zero_particles)):
                p_zero_to_catagorize = self.zero_particles.pop()
                if p_zero_to_catagorize.numeric_label in set_of_zero_changes_to_one:
                    self.one_particles.append(p_zero_to_catagorize)
                else:
                    self.zero_particles.appendleft(p_zero_to_catagorize)

            age_of_universe += 1


test5 = True
if test5:
    thisUniverse = Universe(1000)
    thisUniverse.bang(1000)
    print(thisUniverse.record_of_the_state_of_the_universe)
