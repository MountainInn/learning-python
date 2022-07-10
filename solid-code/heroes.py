from weapons import *
from abc import ABC, abstractmethod
from antagonistfinder import AntagonistFinder


class SuperHero(ABC):

    def __init__(self, name, can_use_ultimate_attack=True):
        self.name = name
        self.can_use_ultimate_attack = can_use_ultimate_attack
        self.finder = AntagonistFinder()

    def find(self, place):
        self.finder.get_antagonist(place)

    @abstractmethod
    def attack(self):
        ...

    @abstractmethod
    def ultimate(self):
        ...


class Superman(LaserMixin, FistMixin, SuperHero):

    def __init__(self):
        super().__init__('Clark Kent', True)

    def attack(self):
        self.punch()

    def ultimate(self):
        self.incinerate_with_lasers()


class ChuckNorris(KickMixin, GunMixin, SuperHero):

    def __init__(self):
        super().__init__('Chuck Norris', False)

    def attack(self):
        self.roundhouse_kick()

    def ultimate(self):
        self.fire_a_gun()
