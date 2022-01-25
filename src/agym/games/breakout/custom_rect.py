import pygame

class Rect:
    def __init__(self, rect):
        self._w = rect.w
        self._h = rect.h
        self.center = list(map(float, rect.center))

    def as_rect(self):
        rect = pygame.Rect(self.left, self.top, self.w, self.h)
        return rect

    def copy(self):
        rect = Rect(self)
        return rect

    def __str__(self):
        result = "(({}, {}), ({}, {}))".format(
            self._w, self._h, *self.center)
        return result

    # top
    @property
    def top(self):
        return self.center[1] - self._h / 2

    @top.setter
    def top(self, top):
        self.center[1] = top + self._h / 2

    # bottom
    @property
    def bottom(self):
        return self.center[1] + self._h / 2

    @bottom.setter
    def bottom(self, bottom):
        self.center[1] = bottom - self._h / 2

    # left
    @property
    def left(self):
        return self.center[0] - self._w / 2

    @left.setter
    def left(self, left):
        self.center[0] = left + self._w / 2

    # right
    @property
    def right(self):
        return self.center[0] + self._w / 2

    @right.setter
    def right(self, right):
        self.center[0] = right - self._w / 2

    # w
    @property
    def w(self):
        return self._w

    @w.setter
    def w(self, w):
        self._w = w

    # h
    @property
    def h(self):
        return self._h

    @h.setter
    def h(self, h):
        self._h = h

    # centerx
    @property
    def centerx(self):
        return self.center[0]

    @centerx.setter
    def centerx(self, centerx):
        self.center[0] = centerx

    # centery
    @property
    def centery(self):
        return self.center[1]

    @centery.setter
    def centery(self, centery):
        self.center[1] = centery
