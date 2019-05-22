import unittest
from math import pi, sqrt

from toolbox import vectors


class TestVector(unittest.TestCase):
    def test_creation(self):
        self.assertIsInstance(vectors.Vector(1, 2, 3, 4), vectors.Vector)

    def test_len(self):
        u = vectors._Vector(1, 2, 3)
        self.assertEqual(len(u), 3)

    def test_add_vectors(self):
        u = vectors._Vector(2, 7, 4)
        v = vectors._Vector(5, 8, 2)
        self.assertEqual(u + v, vectors._Vector(7, 15, 6))

    def test_add_scalar(self):
        u = vectors._Vector(2, 7, 4)
        self.assertIs(u.__add__(3), NotImplemented)

    def test_subtract_vectors(self):
        u = vectors._Vector(2, 7, 4)
        v = vectors._Vector(5, 8, 2)
        self.assertEqual(u - v, vectors._Vector(-3, -1, 2))

    def test_subtract_scalar(self):
        u = vectors._Vector(2, 7, 4)
        self.assertIs(u.__sub__(3), NotImplemented)

    def test_scalar_multiplication(self):
        u = vectors._Vector(2, 7, 4)
        self.assertEqual(u * 3, vectors._Vector(6, 21, 12))
        self.assertEqual(3 * u, vectors._Vector(6, 21, 12))

    def test_dot_multiplication(self):
        u = vectors._Vector(2, 7, 4)
        v = vectors._Vector(5, 8, 2)
        self.assertEqual(u * v, 74)
        self.assertEqual(v * u, 74)

    def test_equality(self):
        self.assertEqual(vectors._Vector(2, 7, 4), vectors._Vector(2, 7, 4))
        self.assertEqual(vectors._Vector(2, 7, 4) * 2, vectors._Vector(4, 14, 8))

    def test_magnitude(self):
        self.assertEqual(vectors._Vector(2, 3).magnitude, sqrt(13))
        self.assertEqual(vectors._Vector(2, 1, 7).magnitude, sqrt(54))


class TestPoint2D(unittest.TestCase):
    def test_creation(self):
        self.assertIsInstance(vectors.Vector(1, 2), vectors.Point2D)

    def test_accessors(self):
        u = vectors.Point2D(x=3, y=5)
        self.assertEqual(u.x, 3)
        self.assertEqual(u.y, 5)

    def test_angle(self):
        self.assertEqual(vectors.Point2D(5, 5).angle, pi / 4)


class TestPoint3D(unittest.TestCase):
    def test_creation(self):
        self.assertIsInstance(vectors.Vector(4, 2, 9), vectors.Point3D)

    def test_accessors(self):
        u = vectors.Point3D(x=3, y=5, z=2)
        self.assertEqual(u.x, 3)
        self.assertEqual(u.y, 5)
        self.assertEqual(u.z, 2)

    def test_cross_multiply(self):
        u = vectors.Point3D(2, 7, 4)
        v = vectors.Point3D(5, 8, 2)
        self.assertEqual(u.cross(v), vectors.Point3D(x=-18, y=16, z=-19))


class TestVectorLine(unittest.TestCase):
    def test_creation(self):
        self.assertIsInstance(vectors.VectorLine(vectors.Vector(2, 7, 4, 6), vectors.Vector(5, 8, 2, 1)), vectors.VectorLine)
        self.assertIsInstance(vectors.VectorLine(vectors.Vector(2, 7, 4), vectors.Vector(5, 8, 2)), vectors.VectorLine3D)
        self.assertIsInstance(vectors.VectorLine(vectors.Vector(2, 7), vectors.Vector(5, 8)), vectors.VectorLine2D)

    def test_different_dimensions(self):
        with self.assertRaises(ValueError):
            vectors.VectorLine(vectors.Vector(2, 7, 4), vectors.Vector(5, 8))
