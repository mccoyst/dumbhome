#!/usr/bin/env python3
import urllib.request
import json
import sqlite3
import sys

if len(sys.argv) < 2:
	sys.exit('I need the wunderground key pathname.')

if len(sys.argv) < 3:
	sys.exit('I need the path to the db.')

key = open(sys.argv[1]).readline().strip()
db = sqlite3.connect(sys.argv[2]+'/readings.db')
db.execute('create table if not exists inside (time integer, temp_c real, humidity real)')
db.execute('create table if not exists outside (time integer, temp_c real, humidity real)')

r = urllib.request.urlopen('http://api.wunderground.com/api/' + key + '/conditions/q/03820.json')
if r.status == 200:
	j = str(r.read(), encoding='utf-8').strip()
	w = json.loads(j)
	t = w['current_observation']['temp_c']
	h = w['current_observation']['relative_humidity'].rstrip('%')
	if t:
		db.execute("insert into outside values (strftime('%s','now'),?,?)", [t, h])
		db.execute("delete from outside where time < (strftime('%s','now') - 60*60*24*7)")
		db.commit()

db.close()
