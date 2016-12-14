#!/usr/bin/env python

# Be in these groups if you don't want to be root:
# video input gpio i2c

from sense_hat import SenseHat
import os

sense = SenseHat()
t0 = sense.get_temperature()
t1 = sense.get_temperature_from_pressure()

def remove(s, r):
	return s.replace(r, '')

def cpu_temp():
	c = os.popen('vcgencmd measure_temp').readline()
	c = remove(c, "temp=")
	c = remove(c, "'C\n")
	return float(c)

def correct(t):
	raw_low = 27.7
	raw_high = 29.67
	raw_range = raw_high - raw_low
	ref_low = 19.22
	ref_high = 27.11
	ref_range = ref_high - ref_low

	return (t - raw_low) * ref_range/raw_range + ref_low

def correct2(t):
	return t - (cpu_temp() - t)/1.5

# https://github.com/astro-pi/watchdog/blob/master/watchdog.py#L2399
def astro_temp():
	t = sense.get_temperature()
	p = sense.get_temperature_from_pressure()
	h = sense.get_temperature_from_humidity()
	c = cpu_temp()
	return ((t+p+h)/3) - (c/5)

print('{0:.2f}'.format(astro_temp()))
print('{0:.2f}'.format(sense.get_humidity()))
