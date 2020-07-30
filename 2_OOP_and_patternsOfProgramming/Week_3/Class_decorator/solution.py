from abc import ABC, abstractmethod


class Hero:
    def __init__(self):
        self.positive_effects = []
        self.negative_effects = []
        self.stats = {
            "HP": 128,  # health points
            "MP": 42,  # magic points,
            "SP": 100,  # skill points
            "Strength": 15,  # сила
            "Perception": 4,  # восприятие
            "Endurance": 8,  # выносливость
            "Charisma": 2,  # харизма
            "Intelligence": 3,  # интеллект
            "Agility": 8,  # ловкость
            "Luck": 1  # удача
        }

    def get_positive_effects(self):
        return self.positive_effects.copy()

    def get_negative_effects(self):
        return self.negative_effects.copy()

    def get_stats(self):
        return self.stats.copy()


class AbstractEffect(Hero, ABC):
    def __init__(self, base):
        self.base = base

    @abstractmethod
    def get_positive_effects(self):
        pass

    @abstractmethod
    def get_negative_effects(self):
        pass

    @abstractmethod
    def get_stats(self):
        pass


class AbstractPositive(AbstractEffect):
    def __init__(self, base):
        self.base = base

    @abstractmethod
    def get_positive_effects(self):
        pass

    def get_negative_effects(self):
        return self.base.get_negative_effects()

    @abstractmethod
    def get_stats(self):
        pass


class Berserk(AbstractPositive):
    def __init__(self, base):
        self.base = base

    def get_positive_effects(self):
        positive_effects = self.base.get_positive_effects()
        positive_effects.append('Berserk')
        return positive_effects

    def get_stats(self):
        stats_berserk = self.base.get_stats()
        for key in ['Strength', 'Endurance', 'Agility', 'Luck']:
            stats_berserk.update({key: stats_berserk[key] + 7})

        for key in ['Perception', 'Charisma', 'Intelligence']:
            stats_berserk.update({key: stats_berserk[key] - 3})

        stats_berserk.update({'HP': stats_berserk['HP'] + 50})
        return stats_berserk


class Blessing(AbstractPositive):
    def __init__(self, base):
        self.base = base

    def get_positive_effects(self):
        positive_effects = self.base.get_positive_effects()
        positive_effects.append('Blessing')
        return positive_effects

    def get_stats(self):
        base_qualities = ["Strength", "Perception", "Endurance", "Charisma",
                          "Intelligence", "Agility", "Luck"]
        stats_blessing = self.base.get_stats()
        for key in base_qualities:
            stats_blessing.update({key: stats_blessing[key] + 2})
        return stats_blessing


class AbstractNegative(AbstractEffect, ABC):
    def __init__(self, base):
        self.base = base

    def get_positive_effects(self):
        return self.base.get_positive_effects()

    @abstractmethod
    def get_negative_effects(self):
        pass

    @abstractmethod
    def get_stats(self):
        pass


class Weakness(AbstractNegative):
    def __init__(self, base):
        self.base = base

    def get_negative_effects(self):
        negative_effects = self.base.get_negative_effects()
        negative_effects.append('Weakness')
        return negative_effects

    def get_stats(self):
        stats_weakness = self.base.get_stats()
        for key in ['Strength', 'Endurance', 'Agility']:
            stats_weakness.update({key: stats_weakness[key] - 4})
        return stats_weakness

class EvilEye(AbstractNegative):
    def __init__(self, base):
        self.base = base

    def get_negative_effects(self):
        negative_effects = self.base.get_negative_effects()
        negative_effects.append('EvilEye')
        return negative_effects

    def get_stats(self):
        stats_evilEye = self.base.get_stats()
        stats_evilEye.update({'Luck': stats_evilEye['Luck'] - 10})
        return stats_evilEye


class Curse(AbstractNegative):
    def __init__(self, base):
        self.base = base

    def get_negative_effects(self):
        negative_effects = self.base.get_negative_effects()
        negative_effects.append('Curse')
        return negative_effects

    def get_stats(self):
        base_qualities = ["Strength", "Perception", "Endurance", "Charisma",
                          "Intelligence", "Agility", "Luck"]
        stats_curse = self.base.get_stats()
        for key in base_qualities:
            stats_curse.update({key: stats_curse[key] - 2})
        return stats_curse
