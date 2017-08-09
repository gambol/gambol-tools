#!/usr/bin/python
#coding=utf-8

import json
import requests
import time
import sys

reload(sys)   
sys.setdefaultencoding('utf8')  

nation=0
province=0
city=0
district=0


url='https://www.zhouheiya.cn/wcs/Tpl/home/default/storejson/%d-%d-%d-%d.json'

addr = ""

def fetch(u):
	r = None
	try:
		r = requests.get(u)
		if r.status_code == 404:
			return ""
		content = json.loads(r.text)
		addr = ""
		for c1 in content:
			addr = c1[2]
			print addr
	except:
		time.sleep(1)

while True:

	while True:

		while True:

			while True:
				u =  url %(nation, province, city, district)
				print u

				addr = fetch(u)
				if (addr == ""):
					break
				else:
					district = district + 1
					#print addr

			if (addr == "" and district == 0):
				break;

			district = 0
			city = city + 1
			time.sleep(1)

		if (addr == "" and city == 0):
			time.sleep(1)
			break

		district = 0
		city = 0
		province = province + 1

	if (addr == "" and province == 0):
		break

	district = 0
	city = 0
	province = 0
	nation = nation + 1




