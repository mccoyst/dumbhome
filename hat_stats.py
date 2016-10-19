#!/usr/bin/env python

# Be in these groups if you don't want to be root:
# video input gpio i2c

from sense_hat import SenseHat
import os

raw_low = 27.7
raw_high = 29.67
raw_range = raw_high - raw_low
ref_low = 19.22
ref_high = 27.11
ref_range = ref_high - ref_low

sense = SenseHat()
t0 = sense.get_temperature()
t1 = sense.get_temperature_from_pressure()

def correct(t):
	return (t - raw_low) * ref_range / raw_range + ref_low

def correct2(t):
	cpu = os.popen('vcgencmd measure_temp').readline()
	cpu = float(cpu.replace("temp=","").replace("'C\n",""))
	return t - (cpu - t)/1.5

# https://github.com/astro-pi/watchdog/blob/master/watchdog.py#L2399
def astro_temp():
	t = sense.get_temperature()
	p = sense.get_temperature_from_pressure()
	h = sense.get_temperature_from_humidity()
	cpu = os.popen('vcgencmd measure_temp').readline()
	cpu = float(cpu.replace("temp=","").replace("'C\n",""))
	return ((t+p+h)/3) - (cpu/5)

print('{0:.2f} or {2:.2f} ({1:.2f})'.format(correct(t0), t0, correct2(t0)))
print('{0:.2f} or {2:.2f} ({1:.2f})'.format(correct(t1), t1, correct2(t1)))
print('{0:.2f}'.format(astro_temp()))
print('{0:.2f}%'.format(sense.get_humidity()))
