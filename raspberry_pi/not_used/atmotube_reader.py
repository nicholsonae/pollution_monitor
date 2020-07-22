
import time
import asyncio
from time import strftime,localtime
from bleak import discover
from bleak import BleakClient

address = "c5:dd:46:d6:f5:65"
SGPC3 =                     "db450002-8e9a-4818-add7-6ed94a328ab4"
temp_humidity_pressure =    "db450003-8e9a-4818-add7-6ed94a328ab4"
battery_info =              "db450004-8e9a-4818-add7-6ed94a328ab4"
pm_chars =                  "db450005-8e9a-4818-add7-6ed94a328ab4"

TX_service = "6e400003-b5a3-f393-e0a9-e50e24dcca9e"

async def run(address, loop, info_toget):
	async with BleakClient(address, loop=loop) as client:
		dat = await client.read_gatt_char(info_toget)
		return(dat)
		
loop = asyncio.get_event_loop()
SGPC3_dat = loop.run_until_complete(run(address, loop,SGPC3))
thp_dat = loop.run_until_complete(run(address, loop, temp_humidity_pressure))
#bat_dat = loop.run_until_complete(run(address, loop, battery_info))
pm_dat  = loop.run_until_complete(run(address, loop, pm_chars))
TX = loop.run_until_complete(run(address, loop, TX_service))

if pm_dat == bytearray(b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'): #error
	exit();


TVOC  = int.from_bytes(SGPC3_dat[0:2], byteorder='little')/1000.0
PM1   = int.from_bytes(pm_dat[0:3], byteorder='little')/100.0
PM25  = int.from_bytes(pm_dat[3:6], byteorder='little')/100.0
PM10  = int.from_bytes(pm_dat[6:9], byteorder='little')/100.0
PM4   = int.from_bytes(pm_dat[9:12], byteorder='little')/100.0
T     = int.from_bytes(thp_dat[6:8], byteorder='little')/100.0
H     = int.from_bytes(thp_dat[0:1], byteorder='little')
P     = int.from_bytes(thp_dat[2:6], byteorder='little')/100.0
#info = int.from_bytes(bat_dat[1:2], byteorder='little')
#bat  = int.from_bytes(bat_dat[0:1], byteorder='little')

timeofreading = strftime("%Y-%m-%d %H:%M:%S", localtime())

f = open('atmotube_reading.txt','w')
to_write = str(timeofreading)+","+str(TVOC)+","+str(T)+","+str(H)+","+str(P)+","+str(PM1)+","+str(PM25)+","+str(PM10)+","+str(PM4);

f.write(to_write)

f.close()

import os
from datetime import datetime
from pijuice import PiJuice

time_now    = datetime.now().time()
night_start = datetime.strptime('2020-06-03 23:00:00', '%Y-%m-%d %H:%M:%S').time()
night_end   = datetime.strptime('2020-06-04 05:00:00', '%Y-%m-%d %H:%M:%S').time()

t = open('../testing.txt','r')
testing = t.read()[0]
t.close()

if time_now > night_start and testing == '0':
	fg = open('shutdown_times.txt','a')
	fg.write('shutting down - night mode activated. '+str(time_now))
	fg.close()
	time.sleep(100)
	pj=PiJuice(1, 0x14)
	pj.power.SetPowerOff(30)
	os.system("sudo shutdown now")



str(binascii.unhexlify(t))[2:-1]

RN2483
4294967245


time_now    = datetime.now().time()
night_start = datetime.strptime('2020-06-03 23:00:00', '%Y-%m-%d %H:%M:%S').time()
night_end   = datetime.strptime('2020-06-04 05:00:00', '%Y-%m-%d %H:%M:%S').time()

t = open('../testing.txt','r')
testing = t.read()[0]
t.close()

if (time_now > night_start or time_now < night_end) and testing == '0':
        fg = open('shutdown_times.txt','a')
        fg.write('shutting down - night mode. '+str(time_now))
        fg.close()
        time.sleep(100)
        pj=PiJuice(1, 0x14)
        pj.power.SetPowerOff(30)
        os.system("sudo shutdown now")
