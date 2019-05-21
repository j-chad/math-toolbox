import math
from itertools import zip_longest
from numbers import Real
from typing import Any, Union


class __Vector:
    __vector__ = True

    def __init__(self, *args: Real):
        self.components = args

    def __add__(self, other: "__Vector") -> "__Vector":
        if is_vector(other):
            return Vector(*[a + b for a, b in zip_longest(self.components, other.components, fillvalue=0)])
        return NotImplemented

    def __sub__(self, other: "__Vector") -> "__Vector":
        if is_vector(other):
            return Vector(*[a - b for a, b in zip_longest(self.components, other.components, fillvalue=0)])
        return NotImplemented

    def __mul__(self, other: Union["__Vector", Real]) -> Union[Real, "__Vector"]:
        """Defines a scalar or dot multiplication, depending on the operands"""
        if is_vector(other):
            return dot(self, other)
        elif isinstance(other, Real):
            return Vector(*[other * a for a in self.components])
        return NotImplemented

    __rmul__ = __mul__

    def __repr__(self):
        return f"Vector({', '.join(str(i) for i in self.components)})"

    def __eq__(self, other: "__Vector") -> bool:
        if is_vector(other):
            return self.components == other.components
        return NotImplemented

    @property
    def magnitude(self):
        return math.sqrt(sum([i ** 2 for i in self.components]))


class Vector(__Vector):
    def __new__(cls, *args):
        if len(args) == 2:
            return Point2D(*args)
        elif len(args) == 3:
            return Point3D(*args)
        return super().__new__(cls)


class Point2D(__Vector):
    def __init__(self, i: Real, j: Real):
        super().__init__(i, j)

    def __repr__(self):
        return f"Vector(x={self.x}, y={self.y})"

    @property
    def angle(self):
        return math.atan(self.x / self.y)

    @property
    def x(self):
        return self.components[0]

    @property
    def y(self):
        return self.components[1]


class Point3D(__Vector):
    def __init__(self, i: Real, j: Real, k: Real):
        super().__init__(i, j, k)

    def __repr__(self):
        return f"Vector(x={self.x}, y={self.y}, z={self.z})"

    @property
    def x(self):
        return self.components[0]

    @property
    def y(self):
        return self.components[1]

    @property
    def z(self):
        return self.components[2]

    def cross(self, b: "Point3D") -> "Point3D":
        return Point3D(
            ((self.y * b.z) - (self.z * b.y)),
            ((self.z * b.x) - (self.x * b.z)),
            ((self.x * b.y) - (self.y * b.x))
        )


def dot(a: __Vector, b: __Vector):
    return sum([a * b for a, b in zip_longest(a.components, b.components, fillvalue=0)])


def is_vector(a: Union[__Vector, Any]):
    return getattr(a, "__vector__", False)
