import time
import asyncio
from time import strftime,localtime
from bleak import discover
from bleak import BleakClient
import os
from datetime import datetime
from pijuice import PiJuice

n = open('../name.txt','r')
device_name = n.readlines()[0][0:-1] 
n.close()

address = "c5:dd:46:d6:f5:65"
SGPC3 = "db450002-8e9a-4818-add7-6ed94a328ab4"
temp_humidity_pressure = "db450003-8e9a-4818-add7-6ed94a328ab4"
battery_info = "db450004-8e9a-4818-add7-6ed94a328ab4"
pm_chars = "db450005-8e9a-4818-add7-6ed94a328ab4"


print('started data collection script')

async def run(address, loop, info_toget):
	async with BleakClient(address, loop=loop) as client:
		dat = await client.read_gatt_char(info_toget)
		return(dat)
	
print('about to set up loop')	
loop = asyncio.get_event_loop()
print('set up loop')
pm_dat  = loop.run_until_complete(run(address, loop, pm_chars))

time_now = time.time()
end_time = time_now + 360 # try for 6 minutes to take a reading
attempt_num = 0
print('time start and time now: ',time_now,time.time())
while pm_dat == bytearray(b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff') and time.time() < end_time: #error
	pm_dat  = loop.run_until_complete(run(address, loop, pm_chars))
	attempt_num += 1;
	print('attempt number:',attempt_num,datetime.now())
	time.sleep(10)

if pm_dat == bytearray(b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'):
	print('could not take atmotube reading \n')
	exit()

SGPC3_dat = loop.run_until_complete(run(address, loop,SGPC3))
thp_dat = loop.run_until_complete(run(address, loop, temp_humidity_pressure))
#bat_dat = loop.run_until_complete(run(address, loop, battery_info)

TVOC = int.from_bytes(SGPC3_dat[0:2], byteorder='little')/1000.0
PM1  = int.from_bytes(pm_dat[0:3], byteorder='little')/100.0
PM25 = int.from_bytes(pm_dat[3:6], byteorder='little')/100.0
PM10 = int.from_bytes(pm_dat[6:9], byteorder='little')/100.0
PM4  = int.from_bytes(pm_dat[9:12], byteorder='little')/100.0
T    = int.from_bytes(thp_dat[6:8], byteorder='little')/100.0
H    = int.from_bytes(thp_dat[0:1], byteorder='little')
P    = int.from_bytes(thp_dat[2:6], byteorder='little')/100.0

timeofreading = strftime("%Y-%m-%d %H:%M:%S", localtime())

pj = PiJuice(1, 0x14)
chargeLevel = pj.status.GetChargeLevel()['data']

f = open('atmotube_reading_for_lostick.txt','w')
to_write = str(device_name)+" "+str(timeofreading)+","+str(TVOC)+","+str(T)+","+str(H)+","+str(P)+","+str(PM1)+","+str(PM25)+","+str(PM10)+","+str(PM4)+" "+str(chargeLevel);
print(to_write)
f.write(to_write)
print(to_write)
f.close()

