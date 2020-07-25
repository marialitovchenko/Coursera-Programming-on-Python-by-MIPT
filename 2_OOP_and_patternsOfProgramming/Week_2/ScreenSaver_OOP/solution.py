"""
ДОПОЛНИТЕЛЬНОЕ ЗАДАНИЕ: УСКОРЕНИЕ И ЗАМЕДЛЕНИЕ
УСКОРЕНИЕ (НА 25%): КНОПКА ВВЕРХ
ЗАМЕДЛЕНИЕ (НА 25%): КНОПКА ВНИЗ

ДОПОЛНИТЕЛЬНОЕ ЗАДАНИЕ: НЕСКОЛЬКО КРИВЫХ
НАЖМИТЕ SHIFT + N для создания новой кривой

Screensaver, realization using classes

"""

import pygame
import random
import math

SCREEN_DIM = (800, 600)


class Vec2d:
    """
    Class describing 2D vector. Beginning of the vector is always in the (0, 0)
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __sub__(self, other):
        """
        Subtraction of vectors
        :param other: a vector to be subtracted
        :return: Vec2d object
        """
        result_x = self.x - other.x
        result_y = self.y - other.y
        return Vec2d(result_x, result_y)

    def __add__(self, other):
        """
        Sum of vectors
        :param other: a vector to be added
        :return: Vec2d object
        """
        result_x = self.x + other.x
        result_y = self.y + other.y
        return Vec2d(result_x, result_y)

    def __mul__(self, k):
        """
        Scalar multiplication
        :param k: a scalar
        :return: Vec2d object
        """
        return Vec2d(k * self.x, k * self.y)

    def len(self):
        """
        Calculate length of vector
        :return: vector scalar length
        """
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def int_pair(self):
        """
        Returns a pair of coordinates of the vector
        :return: tuple of two ints
        """
        result = (int(self.x), int(self.y))
        return result


class Polyline:
    """
    Describes a curve
    """

    def __init__(self, display):
        self.points = []
        self.speeds = []
        self.display = display

    def add_point(self, point_coord, point_speed):
        """
        Adds a point to the polyline
        :param point_coord: tuple, vector of coordinates
        :param point_speed: tuple, speed vector
        :return: changes self.points and self.speeds
        """
        self.points.append(Vec2d(point_coord[0], point_coord[1]))
        self.speeds.append(Vec2d(point_speed[0], point_speed[1]))

    def draw_points(self, width=3, color=(255, 255, 255)):
        """
        Draws a point
        :param width: width of the marker
        :param color:color of the point
        :return: null
        """
        for p in self.points:
            pygame.draw.circle(self.display, color, (int(p.x), int(p.y)),
                               width)

    def set_points(self):
        """
        Recalculates coordinates of base points
        :return: null
        """
        for p in range(len(self.points)):
            self.points[p] = self.points[p] + self.speeds[p]
            if self.points[p].x > SCREEN_DIM[0] or self.points[p].x < 0:
                self.speeds[p] = Vec2d(- self.speeds[p].x, self.speeds[p].y)
            if self.points[p].y > SCREEN_DIM[1] or self.points[p].y < 0:
                self.speeds[p] = Vec2d(self.speeds[p].x, -self.speeds[p].y)


class Knot(Polyline):
    """
    Describes a curve with knots
    """

    def __init__(self, display):
        super().__init__(display)
        self.cross_points = []

    def get_point(self, anchor_points, alpha, deg=None):
        if deg is None:
            deg = len(anchor_points) - 1
        if deg == 0:
            return anchor_points[0]
        result = (anchor_points[deg] * alpha) + \
                  self.get_point(anchor_points, alpha, deg - 1) * (1 - alpha)
        return result

    def get_points(self, anchor_points, count):
        alpha = 1 / count
        res = []
        for i in range(count):
            res.append(self.get_point(anchor_points, i * alpha))
        return res

    def get_knot(self, count):
        if len(self.points) < 3:
            return []
        res = []
        for i in range(-2, len(self.points) - 2):
            ptn = []
            ptn.append((self.points[i] + self.points[i + 1]) * 0.5)
            ptn.append(self.points[i + 1])
            ptn.append((self.points[i + 1] + self.points[i + 2]) * 0.5)

            res.extend(self.get_points(ptn, count))
        return res

    def draw_points(self, width=3, color=(255, 255, 255), steps=35):
        """
        Draws a knotted line
        :param width: width of the marker
        :param color:color of the marker
        :param steps: number of steps
        :return: null
        """
        self.cross_points = self.get_knot(steps)
        for p_n in range(-1, len(self.cross_points) - 1):
            pygame.draw.line(self.display, color,
                             (int(self.cross_points[p_n].x),
                              int(self.cross_points[p_n].y)),
                             (int(self.cross_points[p_n + 1].x),
                              int(self.cross_points[p_n + 1].y)),
                             width)


def draw_help(dysplay):
    """функция отрисовки экрана справки программы"""
    display.fill((50, 50, 50))
    font1 = pygame.font.SysFont("courier", 24)
    font2 = pygame.font.SysFont("serif", 24)
    data = [["F1", "Show Help"], ["R", "Restart"], ["P", "Pause/Play"],
            ["Num+", "More points"], ["Num-", "Less points"],
            ["Up", "Increase speed by 25%"],
            ["Down", "Decrease speed by 25%"],
            ["Shift + N", "New curve"],
            [str(steps), "Current points"]]

    pygame.draw.lines(dysplay, (255, 50, 50, 255), True, [
        (0, 0), (800, 0), (800, 600), (0, 600)], 5)
    for i, text in enumerate(data):
        dysplay.blit(font1.render(
            text[0], True, (128, 128, 255)), (100, 100 + 30 * i))
        dysplay.blit(font2.render(
            text[1], True, (128, 128, 255)), (200, 100 + 30 * i))


if __name__ == "__main__":
    pygame.init()
    display = pygame.display.set_mode(SCREEN_DIM)
    pygame.display.set_caption("MyScreenSaver")

    steps = 35
    working = True
    show_help = False
    pause = True
    hue = 0

    polyline_list = [Polyline(display)]
    knot_list = [Knot(display)]

    while working:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                working = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    working = False
                if event.key == pygame.K_r:
                    polyline_list = [Polyline(display)]
                    knot_list = [Knot(display)]
                if event.key == pygame.K_p:
                    pause = not pause
                if event.key == pygame.K_KP_PLUS:
                    steps += 1
                if event.key == pygame.K_F1:
                    show_help = not show_help
                if event.key == pygame.K_KP_MINUS:
                    steps -= 1 if steps > 1 else 0
                # ДОПОЛНИТЕЛЬНОЕ ЗАДАНИЕ: БОЛЬШЕ КРИВЫХ
                if event.key == pygame.K_n and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    polyline_list.append(Polyline(display))
                    knot_list.append(Knot(display))
                # ДОПОЛНИТЕЛЬНОЕ ЗАДАНИЕ: УСКОРЕНИЕ
                if event.key == pygame.K_UP:
                    for i in range(len(polyline_list)):
                        for j in range(len(polyline_list[i].speeds)):
                            polyline_list[i].speeds[j] = polyline_list[i].speeds[j] * 1.25
                            knot_list[i].speeds[j] = knot_list[i].speeds[j] * 1.25
                # ДОПОЛНИТЕЛЬНОЕ ЗАДАНИЕ: ЗАМЕДЛЕНИЕ
                if event.key == pygame.K_DOWN:
                    for i in range(len(polyline_list)):
                        for j in range(len(polyline_list[i].speeds)):
                            polyline_list[i].speeds[j] = polyline_list[i].speeds[j] * 0.75
                            knot_list[i].speeds[j] = knot_list[i].speeds[j] * 0.75

            if event.type == pygame.MOUSEBUTTONDOWN:
                speed = (random.random() * 2, random.random() * 2)
                polyline_list[len(polyline_list) - 1].add_point(event.pos, speed)
                knot_list[len(polyline_list) - 1].add_point(event.pos, speed)

        display.fill((0, 0, 0))
        for i in range(len(polyline_list)):
            color = pygame.Color(i)
            hue = (hue + 1) % 360
            color.hsla = (hue, 100, 50, 100)
            polyline_list[i].draw_points(width=3, color=color)
            knot_list[i].draw_points(width=3, color=color, steps=steps)
            if not pause:
                polyline_list[i].set_points()
                knot_list[i].set_points()

        if show_help:
            draw_help(display)

        pygame.display.flip()

    pygame.display.quit()
    pygame.quit()
    exit(0)
