# double pendulum

from joint import *
from pymunk.vec2d import Vec2d
from pymunk.shapes import Circle

r = 90

p = Vec2d(200, 190)
v = Vec2d(80, 0)
b0 = space.static_body
c = Circle(p + v, r)
PinJoint(b0, c.body, p)

c2 = Circle(p + 2 * v, r)
PinJoint(c.body, c2.body)

App().run()
