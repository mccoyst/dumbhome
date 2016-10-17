#!/usr/bin/env python3
import urllib.request
import json
import sys

if len(sys.argv) < 2:
	sys.exit('I need the wunderground key pathname.')

key = open(sys.argv[1]).readline().strip()

r = urllib.request.urlopen('http://api.wunderground.com/api/' + key + '/conditions/q/03820.json')
if r.status == 200:
	j = str(r.read(), encoding='utf-8').strip()
	w = json.loads(j)
	print(w['current_observation']['weather'])
	print(w['current_observation']['temp_c'])
	print(w['current_observation']['relative_humidity'])
