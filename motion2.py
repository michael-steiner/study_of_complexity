import numpy as np
import pandas as pd
import random
import collections
import math
from enum import Enum


class TypeOfParticle(Enum):
    particle_zero = 0
    particle_one = 1


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
        self.type_of_particle = TypeOfParticle.particle_zero


class ParticleOne(Atom):
    def __index__(self):
        Atom.__init__(self)
        self.type_of_particle = TypeOfParticle.particle_one


class Universe:
    def __init__(self, eot):
        self.zero_particles = collections.deque()
        self.one_particles = collections.deque()
        self.end_of_time = eot
        self.record_of_the_state_of_the_universe = pd.DataFrame(np.nan, index=[x for x in range(self.end_of_time)],
                                                                columns=['time', 'zero_particles', 'one_particles'])

    def move_class_of_particles(self):
        """ this method may be slow because we are appending on the left - consider writing the 'list' data structure"""
        set_of_particle_x_change_to_particle_y = set()

        for class_x_move_counter in range(len(self.zero_particles)):
            x_particle_to_move = self.zero_particles.pop()
            x_particle_to_move.simple_random_motion()
            for x_particle_to_check_proximity in self.zero_particles:
                if x_particle_to_move.check_distance(x_particle_to_check_proximity) < 10:
                    set_of_particle_x_change_to_particle_y.add(x_particle_to_move.numeric_label)
                    set_of_particle_x_change_to_particle_y.add(x_particle_to_check_proximity.numeric_label)
            self.zero_particles.appendleft(x_particle_to_move)

        for x_categorizing_counter in range(len(self.zero_particles)):
            x_particle_to_categorize = self.zero_particles.pop()
            if x_particle_to_categorize.numeric_label in set_of_particle_x_change_to_particle_y:
                self.one_particles.append(x_particle_to_categorize)
            else:
                self.zero_particles.appendleft(x_particle_to_categorize)

    def bang(self, number_of_zero_particles):
        age_of_universe = 0

        for particle in range(number_of_zero_particles):
            self.zero_particles.append(ParticleZero())

        while age_of_universe <= self.end_of_time:
            self.record_of_the_state_of_the_universe.ix[age_of_universe, 'time'] = age_of_universe
            self.record_of_the_state_of_the_universe.ix[age_of_universe, 'zero_particles'] = len(self.zero_particles)
            self.record_of_the_state_of_the_universe.ix[age_of_universe, 'one_particles'] = len(self.one_particles)

            self.move_class_of_particles()

            age_of_universe += 1


test5 = True
if test5:
    thisUniverse = Universe(100)
    thisUniverse.bang(100)
    print(thisUniverse.record_of_the_state_of_the_universe)
