from pijuice import PiJuice
from datetime import datetime
import time

pijuice = PiJuice(1, 0x14)

time.sleep(1)

chargeLevel = pijuice.status.GetChargeLevel()['data']

now = datetime.now()
nowString = now.strftime("%d-%m-%Y %H:%M:%S")

f = open('battery_level.txt','a')
f.write(nowString+","+str(chargeLevel)+'\n')
f.close()


