import os

atmo_names = []
atmo_users = []
ip_address = []
data_filename = 'atmotube_reading.txt' #the name of the file stored on the raspberry pi

filename = "../data/atmotube_data_" #form of the filename where all data is stored for each atmotube locally
filetype = ".csv"

g = open('../atmotube_info/atmotube2ip.txt','r')
g_lines = g.readlines()
for i in range(1,len(g_lines)):
	line = g_lines[i].split()
	atmo_names.append(line[0])
	atmo_users.append(line[1])
	ip_address.append(line[2])

g.close()


for j in range(0,len(atmo_names)):
	os.system('scp '+atmo_users[j]+'@'+ip_address[j]+':/home/pi/atmotube-readings/'+data_filename+' ../data/atmodata_currentreading_'+atmo_names[j]+'.txt')
	a = open('../data/atmodata_currentreading_'+atmo_names[j]+'.txt','r')
	a_data = a.readlines()[-1]
	write_header = False;  # do we need to write the header?
	got_data = False;      # do we already have this data?
	if not os.path.isfile(filename+atmo_names[j]+filetype): write_header = True;
	else: 
		o = open(filename+atmo_names[j]+filetype,'r')
		last_line = o.readlines()[-1]
		if last_line.split(",")[0] == a_data.split(",")[0]: got_data = True; #already have recorded this data
	b = open(filename+atmo_names[j]+filetype,'a')
	if write_header: b.write('Date,VOC (ppm), Temperature (C), Humidity (%),Pressure (hPa),PM1,PM2.5,PM10,PM4\n');
	if not got_data: b.write(a_data+'\n')
	b.close()
	a.close()




