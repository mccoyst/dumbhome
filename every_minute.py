#!/usr/bin/env python

# Be in these groups if you don't want to be root:
# video input gpio i2c

from sense_hat import SenseHat
import os
import sys

if len(sys.argv) < 2:
	print('I need the path to the image folder.')
	sys.exit(1)

imgs = sys.argv[1]


def remove(s, r):
	return s.replace(r, '')

def cpu_temp():
	c = os.popen('vcgencmd measure_temp').readline()
	c = remove(c, "temp=")
	c = remove(c, "'C\n")
	return float(c)

# https://github.com/astro-pi/watchdog/blob/master/watchdog.py#L2399
def astro_temp():
	t = hat.get_temperature()
	p = hat.get_temperature_from_pressure()
	h = hat.get_temperature_from_humidity()
	c = cpu_temp()
	return ((t+p+h)/3) - (c/5)


hat = SenseHat()
hat.set_rotation(0)
hat.low_light = True
hat.load_image(imgs + '/choco.png')


t = astro_temp()
h = hat.get_humidity()

if t < 15.5:
	hat.load_image(imgs + '/cold.png')
elif t > 25:
	hat.load_image(imgs + '/hot.png')
else:
	hat.load_image(imgs + '/ok.png')
