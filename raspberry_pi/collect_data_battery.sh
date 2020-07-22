cd /home/pi/atmotube-readings
python3 atmotube_reader_for_lostick.py
echo 'collected atmotube data'
./radio_sender_data.py /dev/ttyUSB0
echo 'sent atmotube data'
cd /home/pi/piJuice-readings
python3 pijuice_battery_level.py
echo 'checked battery levels'
cd /home/pi
python3 wakeup_enable.py
echo 'enabled wakeup on'
cd /home/pi/auto_shutdown/
python3 auto_shutdown_battery.py
echo 'checked for shutdown event'
