import unittest
from math import pi, sqrt

from toolbox.vectors import Point2D, Point3D, Vector
from toolbox.vectors._vectors import _Vector
from toolbox.vectors.shapes import VectorLine, VectorLine2D, VectorLine3D, PointIntersection


class TestVector(unittest.TestCase):
    def test_creation(self):
        self.assertIsInstance(Vector(1, 2, 3, 4), Vector)

    def test_len(self):
        u = _Vector(1, 2, 3)
        self.assertEqual(len(u), 3)

    def test_add_vectors(self):
        u = _Vector(2, 7, 4)
        v = _Vector(5, 8, 2)
        self.assertEqual(u + v, _Vector(7, 15, 6))

    def test_add_scalar(self):
        u = _Vector(2, 7, 4)
        self.assertIs(u.__add__(3), NotImplemented)

    def test_subtract_vectors(self):
        u = _Vector(2, 7, 4)
        v = _Vector(5, 8, 2)
        self.assertEqual(u - v, _Vector(-3, -1, 2))

    def test_subtract_scalar(self):
        u = _Vector(2, 7, 4)
        self.assertIs(u.__sub__(3), NotImplemented)

    def test_scalar_multiplication(self):
        u = _Vector(2, 7, 4)
        self.assertEqual(u * 3, _Vector(6, 21, 12))
        self.assertEqual(3 * u, _Vector(6, 21, 12))

    def test_scalar_division(self):
        u = _Vector(2, 8, 4)
        self.assertEqual(u / 2, _Vector(1, 4, 2))

    def test_dot_multiplication(self):
        u = _Vector(2, 7, 4)
        v = _Vector(5, 8, 2)
        self.assertEqual(u * v, 74)
        self.assertEqual(v * u, 74)

    def test_equality(self):
        self.assertEqual(_Vector(2, 7, 4), _Vector(2, 7, 4))
        self.assertEqual(_Vector(2, 7, 4) * 2, _Vector(4, 14, 8))

    def test_magnitude(self):
        self.assertEqual(_Vector(2, 3).magnitude, sqrt(13))
        self.assertEqual(_Vector(2, 1, 7).magnitude, sqrt(54))


class TestPoint2D(unittest.TestCase):
    def test_creation(self):
        self.assertIsInstance(Vector(1, 2), Point2D)

    def test_accessors(self):
        u = Point2D(x=3, y=5)
        self.assertEqual(u.x, 3)
        self.assertEqual(u.y, 5)

    def test_angle(self):
        self.assertEqual(Point2D(5, 5).angle, pi / 4)


class TestPoint3D(unittest.TestCase):
    def test_creation(self):
        self.assertIsInstance(Vector(4, 2, 9), Point3D)

    def test_accessors(self):
        u = Point3D(x=3, y=5, z=2)
        self.assertEqual(u.x, 3)
        self.assertEqual(u.y, 5)
        self.assertEqual(u.z, 2)

    def test_cross_multiply(self):
        u = Point3D(2, 7, 4)
        v = Point3D(5, 8, 2)
        self.assertEqual(u.cross(v), Point3D(x=-18, y=16, z=-19))


class TestVectorLine(unittest.TestCase):
    def test_creation(self):
        self.assertIsInstance(VectorLine(Vector(2, 7, 4, 6), Vector(5, 8, 2, 1)), VectorLine)
        self.assertIsInstance(VectorLine(Vector(2, 7, 4), Vector(5, 8, 2)), VectorLine3D)
        self.assertIsInstance(VectorLine(Vector(2, 7), Vector(5, 8)), VectorLine2D)

    def test_different_dimensions(self):
        with self.assertRaises(ValueError):
            VectorLine(Vector(2, 7, 4), Vector(5, 8))

    def test_intercept_point_on_line(self):
        u = VectorLine(Vector(1, 1), Vector(2, 0))
        v = Vector(3, -1)
        intercept = u.intersect(v)
        self.assertIsInstance(intercept, PointIntersection)
        self.assertEqual(intercept.point, Vector(3, -1))
        self.assertEqual(intercept.point, v.intersect(u).point)

    def test_intercept_point_outside_line(self):
        u = VectorLine(Vector(0, 0), Vector(2, -2))
        v = Vector(3, -1)
        self.assertIsNone(u.intersect(v))
        self.assertIsNone(v.intersect(u))

    def test_intercept_parallel_line_2d(self):
        u = VectorLine(Vector(1, 1), Vector(2, 0))
        v = VectorLine(Vector(0, 0), Vector(2, -2))
        self.assertIsNone(u.intersect(v))
        self.assertIsNone(v.intersect(u))

    def test_intercept_lines_2d(self):
        u = VectorLine(Vector(0, 3), Vector(2, -1))
        v = VectorLine(Vector(0, 0), Vector(1, -1))
        intercept = u.intersect(v)
        self.assertIsInstance(intercept, PointIntersection)
        self.assertEqual(intercept.point, Vector(3, -3))
        self.assertEqual(intercept.point, v.intersect(u).point)
