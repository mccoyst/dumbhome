#!/usr/bin/env python

# Be in these groups if you don't want to be root:
# video input gpio i2c

import sys
from sense_hat import SenseHat

if len(sys.argv) < 2:
        sys.exit('I need the wunderground key pathname.')

h = SenseHat()
h.set_rotation(0)
h.low_light = True
h.load_image(sys.argv[1])
