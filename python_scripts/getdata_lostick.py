import os

atmo_names = []
data_lostick_filename = '../data/atmodata_lostick_reading_' #the name of the file stored on the raspberry pi
data_lostick_type = '.txt'

filename = "../data/atmotube_data_" #form of the filename where all data is stored for each atmotube locally
filetype = ".csv"

g = open('../atmotube_info/atmotube2location.txt','r')
g_lines = g.readlines()
for i in range(1,len(g_lines)):
	line = g_lines[i].split()
	atmo_names.append(line[0])

g.close()



for j in range(0,len(atmo_names)):
	lostick_data = ''
	if not os.path.isfile(data_lostick_filename+atmo_names[j]+data_lostick_type): continue; #no data for this atmotube
	g = open(data_lostick_filename+atmo_names[j]+data_lostick_type,'r')
	lostick_data = g.readlines()[0][0:-1]
	g.close()
	write_header = False;
	got_data = False;
	if not os.path.isfile(filename+atmo_names[j]+filetype): write_header = True;
	else: 
		o = open(filename+atmo_names[j]+filetype,'r')
		last_line = o.readlines()[-1][0:-1]
		o.close()
		#print(last_line)
		#print(lostick_data)
		if last_line == lostick_data: got_data = True; #already have recorded this data
	b = open(filename+atmo_names[j]+filetype,'a')
	if write_header: b.write('Date,VOC (ppm), Temperature (C), Humidity (%),Pressure (hPa),PM1,PM2.5,PM10,PM4\n');
	#print('got data: '+str(got_data))
	if not got_data: b.write(lostick_data+'\n')
	b.close()


