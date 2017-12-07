from display import *

class Card(object):
    def __init__(self, name):
        pass

class PrismCard(Card):
    pass

class PyramidCard(Card):
    pass

class Polyhedron(Card):
    pass

class SphereCard(Card):
    pass

class Surface3DCard(Card):
    def __init__(self, arg):
        super().__init__()
        self.arg = arg

class Curve3DCard(Card):
    pass

class Custom(Card):
    pass
        