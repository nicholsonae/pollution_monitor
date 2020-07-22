#!/usr/bin/python3
# This script is started at reboot by cron
# Since the start is very early in the boot sequence we wait for the i2c-1 device

import pijuice, time, os
from datetime import datetime

while not os.path.exists('/dev/i2c-1'):
    time.sleep(0.1)

pj = pijuice.PiJuice(1, 0x14)

pj.power.SetWakeUpOnCharge(False)
chargeLevel = pj.status.GetChargeLevel()['data']

f = open('wakeup_time_charge.txt','w')
f.write(str(datetime.now().time())+' '+str(chargeLevel)+'\n')
f.close()

pj.rtcAlarm.SetAlarm({'second': 0, 'minute_period': 20, 'hour': 'EVERY_HOUR', 'day': 'EVERY_DAY'})

if chargeLevel <= 5:
   time_now = datetime.now().time()
   fg = open('shutdown_onwakeup_times.txt','w')
   fg.write(str(time_now)+" "+str(chargeLevel))
   fg.close()
   pj.rtcAlarm.SetWakeupEnabled(False);
   pj.power.SetWakeUpOnCharge(20)
   pj.power.SetPowerOff(60)
   os.system("sudo shutdown now")
   exit() 

while not pj.rtcAlarm.GetControlStatus()['data']['alarm_wakeup_enabled']:
   pj.rtcAlarm.SetWakeupEnabled(True)
