from heroes import SuperHero, Superman, ChuckNorris
from places import Place, Tokyo, Kostroma
from antagonistfinder import AntagonistFinder
from massmedia import MassMedia


def save_the_place(hero: SuperHero, place: Place, massmedia: MassMedia):
    hero.find(place)
    hero.attack()
    if hero.can_use_ultimate_attack:
        hero.ultimate()
    massmedia.create_news(hero, place)


if __name__ == '__main__':
    massmedia = MassMedia()

    save_the_place(Superman(), Kostroma(), massmedia)
    print('-' * 20)
    save_the_place(ChuckNorris(), Tokyo(), massmedia)
