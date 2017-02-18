#!/usr/bin/env python

# Be in these groups if you don't want to be root:
# video input gpio i2c

from sense_hat import SenseHat
import bisect
import os
import sqlite3
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

t = astro_temp()
h = hat.get_humidity()

db = sqlite3.connect('/home/sm/dumbhome/refs.db')
db.execute('create table if not exists refs (reading real, reference real)')
db.commit()
refs = db.execute('select * from refs order by reading').fetchall()
db.close()
i = bisect.bisect_left(refs, t)
if i > 0:
	l, lref = refs[i-1]
	h, href = refs[i]
	t = (t - l) * (href - lref) / (h - l) + lref

db = sqlite3.connect('/home/sm/dumbhome/readings.db')
db.execute('create table if not exists inside (time integer, temp_c real, humidity real)')
db.execute("insert into inside values (strftime('%s', 'now'),?,?)", [t, h])
db.execute("delete from inside where time < (strftime('%s','now') - 60*60*24*7)")
db.commit()
db.close()

if t < 15.5:
	hat.load_image(imgs + '/cold.png')
elif t > 25:
	hat.load_image(imgs + '/hot.png')
else:
	hat.load_image(imgs + '/ok.png')
