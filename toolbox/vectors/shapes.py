from dataclasses import dataclass
from numbers import Real
from typing import Any, Tuple

from .helpers import Equation, method_dispatch
from .vectors import Vector, _Shape, _Vector

__all__ = ["VectorLine", "VectorLine2D", "VectorLine3D"]


class _VectorLine(_Shape):
    def __init__(self, a: _Vector, b: _Vector):
        self.p = a
        self.u = b - a
        self.components = self.__get_components()

    def __call__(self, t: Real):
        return self.p + self.u * t

    def __intersect__(self, shape: _Vector):
        if not isinstance(shape, _Vector):
            return NotImplemented

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

    def __get_components(self) -> Tuple[Equation]:
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

    @method_dispatch
    def __intersect__(self, shape: _Shape):
        if not isinstance(shape, self.__class__):
            return NotImplemented
        else:
            if len(shape.components) != len(self.components):
                return NotImplemented

            determinant = self.u.components[0] * -shape.u.components[1] - self.u.components[1] * -shape.u.components[0]

            if determinant == 0:  # Parallel Lines
                return None

            difference = (shape.p - self.p)
            determinant_a = difference.components[0] * -shape.u.components[1] - difference.components[1] * -shape.u.components[0]
            determinant_b = self.u.components[0] * difference.components[1] - self.u.components[1] * difference.components[0]
            a = determinant_a / determinant
            b = determinant_b / determinant

            x1 = self.components[0](a)
            x2 = shape.components[0](b)
            y1 = self.components[1](a)
            y2 = shape.components[1](b)

            assert x1 == x2
            assert y1 == y2

            return PointIntersection(a=self, b=shape, point=Vector(x1, y1))

    @__intersect__.register
    def _(self, shape: _Vector):
        return super().__intersect__(shape)


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
