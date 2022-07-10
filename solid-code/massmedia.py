from heroes import SuperHero
from places import Place


class MassMedia:
    def create_news(self, hero: SuperHero, place: Place):
        print(f'{hero.name} saved the {place.name}!')
