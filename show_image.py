#!/usr/bin/env python

# Be in these groups if you don't want to be root:
# video input gpio i2c

from sense_hat import SenseHat

h = SenseHat()
h.set_rotation(0)
h.low_light = True
h.load_image('sun-clear.png')
