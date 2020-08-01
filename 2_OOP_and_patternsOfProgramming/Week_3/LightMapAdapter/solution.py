from abc import ABC, abstractmethod


class LightIntensityCalc(ABC):
    @abstractmethod
    def lighten(self, geo_plan):
        pass


class MappingAdapter(LightIntensityCalc):
    def __init__(self, adaptee):
        self.adaptee = adaptee

    def lighten(self, geo_plan):
        dim = (len(geo_plan[0]), len(geo_plan))
        self.adaptee.set_dim(dim)

        lights = []
        obstacles = []

        for i in range(len(geo_plan)):
            for j in range(len(geo_plan[0])):
                if geo_plan[i][j] == 1:
                    lights.append((j, i))
                if geo_plan[i][j] == -1:
                    obstacles.append((j, i))

        self.adaptee.set_lights(lights)
        self.adaptee.set_obstacles(obstacles)
        result = self.adaptee.generate_lights()
        return result
