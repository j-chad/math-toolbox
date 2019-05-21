import math
from itertools import zip_longest
from numbers import Real
from typing import Any, Union

__all__ = ["Vector", "Point2D", "Point3D", "VectorLine", "dot", "is_vector"]


class __Vector:
    """The base Vector type.

    Will usually be created using the Vector class and is valid for any dimension.
    """
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

    def __mul__(self, other: Union[Real, "__Vector"]) -> Union[Real, "__Vector"]:
        """Defines a scalar or dot multiplication, depending on the operands."""
        if is_vector(other):
            return dot(self, other)
        elif isinstance(other, Real):
            return Vector(*[other * a for a in self.components])
        return NotImplemented

    def __rmul__(self, other: Union[Real, "__Vector"]) -> Union[Real, "__Vector"]:
        """Returns the same result as __mul__ since scalar multiplication and dot multiplication are both commutative operations"""
        return self.__mul__(other)

    def __repr__(self):
        return f"Vector({', '.join(str(i) for i in self.components)})"

    def __eq__(self, other: "__Vector") -> bool:
        if is_vector(other):
            return self.components == other.components
        return NotImplemented

    @property
    def magnitude(self) -> Real:
        return math.sqrt(sum([i ** 2 for i in self.components]))


class Vector(__Vector):
    """Constructs a __Vector instance.

    If the vector is a special case, i.e. 2 dimensional, a instance will be created to reflect this.
    In all other cases a standard __Vector instance will be returned.
    """

    def __new__(cls, *args: Real):
        if len(args) == 2:
            return Point2D(*args)
        elif len(args) == 3:
            return Point3D(*args)
        return super().__new__(cls)


class Point2D(__Vector):
    """A 2 dimensional vector.

    Adds niceties such as x and y accessors as well as an angle property.
    """

    def __init__(self, i: Real, j: Real):
        super().__init__(i, j)

    def __repr__(self):
        return f"Vector(x={self.x}, y={self.y})"

    @property
    def angle(self) -> Real:
        """The angle relative to the x-axis"""
        return math.atan(self.x / self.y)

    @property
    def x(self) -> Real:
        return self.components[0]

    @property
    def y(self) -> Real:
        return self.components[1]


class Point3D(__Vector):
    """A 3 dimensional vector.

        Adds niceties such as x, y and z accessors as well as a cross multiplication function.
    """

    def __init__(self, i: Real, j: Real, k: Real):
        super().__init__(i, j, k)

    def __repr__(self):
        return f"Vector(x={self.x}, y={self.y}, z={self.z})"

    @property
    def x(self) -> Real:
        return self.components[0]

    @property
    def y(self) -> Real:
        return self.components[1]

    @property
    def z(self) -> Real:
        return self.components[2]

    def cross(self, b: "Point3D") -> "Point3D":
        """Performs vector cross multiplication on 3 dimensional vectors.

        It is important to note that this cross multiplication can only be performed on 3 dimensional vectors.
        """
        return Point3D(
            ((self.y * b.z) - (self.z * b.y)),
            ((self.z * b.x) - (self.x * b.z)),
            ((self.x * b.y) - (self.y * b.x))
        )


def dot(a: __Vector, b: __Vector) -> Real:
    """Return the dot product of two vectors"""
    return sum([a * b for a, b in zip_longest(a.components, b.components, fillvalue=0)])


def is_vector(a: Union[__Vector, Any]) -> bool:
    """Return whether an object can be considered a vector or not."""
    return getattr(a, "__vector__", False)
