#!/usr/bin/env python

# Be in these groups if you don't want to be root:
# video input gpio i2c

from sense_hat import SenseHat

raw_low = 28.577
raw_high = 29.67
raw_range = raw_high - raw_low
ref_low = 25.22
ref_high = 27.11
ref_range = ref_high - ref_low

sense = SenseHat()
t0 = sense.get_temperature()
t1 = sense.get_temperature_from_pressure()

def correct(t):
	return (t - raw_low) * ref_range / raw_range + ref_low

print('{0:.2f} ({1:.2f})'.format(correct(t0), t0))
print('{0:.2f} ({1:.2f})'.format(correct(t1), t1))
print('{0:.2f}%'.format(sense.get_humidity()))
