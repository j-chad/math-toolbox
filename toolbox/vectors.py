import math
from dataclasses import dataclass
from itertools import zip_longest
from numbers import Real
from typing import Any, Union

from toolbox.helpers import Equation, method_dispatch

__all__ = ["Vector", "Point2D", "Point3D", "VectorLine", "dot", "is_vector"]


class _Vector:
    """The base Vector type.

    Will usually be created using the Vector class and is valid for any dimension.
    """
    __vector__ = True

    def __init__(self, *args: Real):
        self.components = args

    def __repr__(self) -> str:
        return f"Vector({', '.join(str(i) for i in self.components)})"

    def __len__(self) -> int:
        return len(self.components)

    def __add__(self, other: "_Vector") -> "_Vector":
        if is_vector(other):
            return Vector(*[a + b for a, b in zip_longest(self.components, other.components, fillvalue=0)])
        return NotImplemented

    def __sub__(self, other: "_Vector") -> "_Vector":
        if is_vector(other):
            return Vector(*[a - b for a, b in zip_longest(self.components, other.components, fillvalue=0)])
        return NotImplemented

    @method_dispatch
    def __mul__(self, other: Union[Real, "_Vector"]) -> Union[Real, "_Vector"]:
        """Defines a scalar or dot multiplication, depending on the operands."""
        if is_vector(other):
            return dot(self, other)
        elif isinstance(other, Real):
            return Vector(*[other * a for a in self.components])
        return NotImplemented

    def __rmul__(self, other: Union[Real, "_Vector"]) -> Union[Real, "_Vector"]:
        """Returns the same result as __mul__ since scalar multiplication and dot multiplication are both commutative operations"""
        return self.__mul__(other)

    def __eq__(self, other: "_Vector") -> bool:
        if is_vector(other):
            return self.components == other.components
        return NotImplemented

    @property
    def magnitude(self) -> Real:
        return math.sqrt(sum([i ** 2 for i in self.components]))


class Vector(_Vector):
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


class Point2D(_Vector):
    """A 2 dimensional vector.

    Adds niceties such as x and y accessors as well as an angle property.
    """

    def __init__(self, x: Real, y: Real):
        super().__init__(x, y)

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


class Point3D(_Vector):
    """A 3 dimensional vector.

        Adds niceties such as x, y and z accessors as well as a cross multiplication function.
    """

    def __init__(self, x: Real, y: Real, z: Real):
        super().__init__(x, y, z)

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


class _VectorLine:
    def __init__(self, a: _Vector, b: _Vector):
        self.p = a
        self.u = b - a
        self.components = self.__get_components()

    def __call__(self, t: Real):
        return self.p + self.u * t

    @method_dispatch
    def __intersect__(self, shape: Any):
        if not isinstance(shape, self.__class__):
            return NotImplemented
        else:
            if len(shape.components) != len(self.components):
                return NotImplemented

    @__intersect__.register
    def _(self, shape: _Vector):
        if len(shape.components) != len(self.components):
            return NotImplemented
        for i, b in enumerate(self.u.components):
            if b != 0:
                t = (shape.components[i] - self.p.components[i]) / b
                break
        else:
            t = 0
        point = Vector(*(i(t) for i in self.components))
        if shape == point:
            return PointIntersection(a=self, b=shape, point=point)
        else:
            return None

    def __get_components(self):
        components = []
        for a, b in zip(self.p.components, self.u.components):
            key = f"{a}{'+' if b >= 0 else '-'}{abs(b)}t"

            def closure(a: Real, b: Real):
                def value(t: Real):
                    return a + (b * t)

                return value

            value_ = closure(a, b)

            equation = Equation(key, value_)
            components.append(equation)
        return tuple(components)

    def intersects(self, shape: Any):
        intersect = self.__intersect__(shape)
        if intersect is NotImplemented:
            __r_intersect__ = getattr(shape, "__intersect__", None)
            if __r_intersect__ is None:
                raise TypeError(f"unsupported types for intersect: '{self.__class__.__name__}' and '{shape.__class__.__name__}'")
            else:
                intersect = __r_intersect__(self)
                if intersect is NotImplemented:
                    raise TypeError(f"unsupported types for intersect: '{self.__class__.__name__}' and '{shape.__class__.__name__}'")
        return intersect


class VectorLine(_VectorLine):
    def __new__(cls, a: _Vector, b: _Vector):
        if len(a) != len(b):
            raise ValueError(f"Vector dimensions are different. {len(a)} != {len(b)}")
        dimensions = len(a)

        if dimensions == 2:
            return VectorLine2D(a, b)
        elif dimensions == 3:
            return VectorLine3D(a, b)
        return super().__new__(cls)


class VectorLine2D(_VectorLine):
    # noinspection PyUnresolvedReferences
    def __repr__(self):
        equations = self._VectorLine__get_components()
        return f"VectorLine(x={equations[0]}, y={equations[1]})"


class VectorLine3D(_VectorLine):
    # noinspection PyUnresolvedReferences
    def __repr__(self):
        equations = self._VectorLine__get_components()
        return f"VectorLine(x={equations[0]}, y={equations[1]}, z={equations[2]})"


@dataclass
class PointIntersection:
    a: Any
    b: Any
    point: _Vector


def dot(a: _Vector, b: _Vector) -> Real:
    """Return the dot product of two vectors"""
    return sum([a * b for a, b in zip_longest(a.components, b.components, fillvalue=0)])


def is_vector(a: Union[_Vector, Any]) -> bool:
    """Return whether an object can be considered a vector or not."""
    return getattr(a, "__vector__", False)
