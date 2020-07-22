import os
from pijuice import PiJuice
from datetime import datetime
import time

time.sleep(1)

pj=PiJuice(1, 0x14)

time_now    = datetime.now().time()
night_start = datetime.strptime('2020-06-03 22:00:00', '%Y-%m-%d %H:%M:%S').time()
night_end   = datetime.strptime('2020-06-04 05:00:00', '%Y-%m-%d %H:%M:%S').time()
chargeLevel = pj.status.GetChargeLevel()['data']

t = open('../testing.txt','r')
t_dat = t.read()[0]
testing = t_dat.split()[0]
t.close()

if (time_now > night_start or time_now < night_end or chargeLevel < 50) and testing == '0':
        fg = open('shutdown_times.txt','a')
        fg.write('shutting down - low battery mode activated. '+str(time_now)+'\n')
        fg.close()
        if chargeLevel <= 5:
             pj.rtcAlarm.SetWakeupEnabled(False);
             pj.power.SetWakeUpOnCharge(20)
        pj.power.SetPowerOff(60)
        os.system("sudo shutdown now")
