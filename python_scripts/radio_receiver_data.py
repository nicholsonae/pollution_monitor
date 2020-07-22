#!/usr/bin/env python3
import time
import sys
import serial
import argparse
import binascii
import os

#time_now = time.time();
#time_end = time_now + 60*9.5;

from serial.threaded import LineReader, ReaderThread

parser = argparse.ArgumentParser(description='LoRa Radio mode receiver.')
parser.add_argument('port', help="Serial port descriptor")
args = parser.parse_args()

header_text = 'Date,VOC (ppm), Temperature (C), Humidity (%),Pressure (hPa),PM1,PM2.5,PM10,PM4\n'
filename = "../data/atmotube_data_" #form of the filename where all data is stored for each atmotube locally
filetype = ".csv"

class PrintLines(LineReader):

    def connection_made(self, transport):
        print("connection made")
        self.transport = transport
        self.send_cmd('sys get ver')
        self.send_cmd('mac pause')
        self.send_cmd('radio set pwr 10')
        self.send_cmd('radio rx 0')
        self.send_cmd("sys set pindig GPIO10 0")

    def handle_line(self, data):
        if data == "ok" or data == 'busy':
            return
        if data == "radio_err":
            self.send_cmd('radio rx 0')
            return
        
        self.send_cmd("sys set pindig GPIO10 1", delay=0)
        d = str(data)
        if d.split()[0] == 'radio_rx' and len(d.split()) > 1:
            c_data = str(binascii.unhexlify(str.encode(d.split()[1])))[2:-1]
            atmoname = c_data.split()[0]
            if atmoname[0:4] == 'atmo':
               write_header = False;
               got_data = False;
               data_to_write = c_data.split()[1]+" "+c_data.split()[2]
               if not os.path.isfile(filename+atmoname+filetype): write_header = True;
               else:
                  o = open(filename+atmoname+filetype,'r')
                  last_line = o.readlines()[-1][0:-1]
                  o.close()
                  if last_line == data_to_write: got_data = True;
               print(c_data)
               b = open(filename+atmoname+filetype,'a')
               if write_header: b.write(header_text)
               if not got_data: b.write(data_to_write+'\n')
               #g = open('../data/atmodata_lostick_reading_'+atmoname+'.txt','w')
               #g.write(data_to_write)
               #g.close()
               #exit()
            else: print(atmoname)
        time.sleep(.1)
        self.send_cmd("sys set pindig GPIO10 0", delay=1)
        self.send_cmd('radio rx 0')

    def connection_lost(self, exc):
        if exc:
            print(exc)
        print("port closed")

    def send_cmd(self, cmd, delay=.5):
        a = ('%s\r\n' % cmd).encode('UTF-8')
        #g = open('testingthis.txt','w')
        #g.write(a)
        #g.close()
        self.transport.write(a)
        time.sleep(delay)

ser = serial.Serial(args.port, baudrate=57600)
with ReaderThread(ser, PrintLines) as protocol:
    #while time.time() < time_end:
    while(1):
        #print('Am I doing anything?')
        pass
