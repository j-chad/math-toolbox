# The University Toolbox
Just a little something I decided to make during my studies (1st year engineering). 

Currently only contains a vector library but hopefully more will be added throughout.

## Contributing
If you would like to contribute or have any ideas please email me (address is on my profile.) or raise an issue. Pull requests are welcome!

## Usage
Tested on python 3.7.2. May or may not work on other 3.x.x releases.
```python
>>> from toolbox.vectors import Vector

# create a vector
>>> u = Vector(1, 2)
>>> v = Vector(1, 2, 3)

# reference components
>>> v.x
1
>>> v.y
2
>>> v.z
3
>>> v.components
(1, 2, 3)

# magnitude
>>> u.magnitude
2.236...

# angle (relative to x axis)
>>> u.angle
0.463...

# scalar multiplication
>>> u * 3
Vector(x=3, y=6)

# dot product
>>> u * Vector(7, 3)
13
# or
>>> dot(u, Vector(7, 3))
13

# cross product
>>> a = Vector(4, 7, 2)
>>> b = Vector(2, 8, 1)
>>> a.cross(b)
Vector(x=-9, y=0, z=18)

```