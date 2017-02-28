#!/usr/bin/env python

# Be in these groups if you don't want to be root:
# video input gpio i2c

from sense_hat import SenseHat
import os
import sqlite3
import sys

if len(sys.argv) < 2:
	print('I need the path to the db folder.')
	sys.exit(1)

if len(sys.argv) < 3:
	print('I need the reference value.')
	sys.exit(1)

imgs = sys.argv[1]
ref = float(sys.argv[2])


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
t = astro_temp()

db = sqlite3.connect(imgs+'/refs.db')
db.execute('create table if not exists refs (reading real, reference real)')
db.commit()
db.execute('insert into refs values (?,?)', [t, ref])
db.commit()
db.close()
