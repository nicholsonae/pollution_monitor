from time import strftime,localtime
from datetime import datetime, timedelta

greyMessage = "No data"
blueMessage = "Excellent air quality"
greenMessage = "Good air quality"
yellowMessage = "Moderate air quality"
orangeMessage = "Poor air quality"
redMessage = "Dangerous air quality"

tubeNames2locations = {}

f = open('../atmotube_info/atmotube2location.txt','r')
f_lines = f.readlines()
if len(f_lines) > 1:
    for i in range(1,len(f_lines)):
        dat = f_lines[i].split()
        n = dat[0]
        lat = dat[1]
        lon = dat[2]
        tubeNames2locations[n] = (lat,lon)

f.close()

tubeName2data = {}
tubeName2day = {}

random_counter = 1;


filename = "../data/atmotube_data_" #form of the filename where all data is stored for each atmotube locally
filetype = ".csv"


timenow = strftime("%Y-%m-%d %H:%M:%S", localtime())
timenowconvert = datetime.strptime(timenow,"%Y-%m-%d %H:%M:%S")
day_ago  = timenowconvert - timedelta(days  = 1)
#timenow = "2020-05-05 12:05:52"

#Date, VOC, temp, hum, press, pm1, pm2.5, pm10, pm4

for tube in tubeNames2locations:
    day_pm1   = []
    day_pm25  = []
    day_pm10  = []
    day_time  = []
    day_VOC   = []
    day_temp  = []
    day_hum   = []
    day_press = []
    d = open(filename+tube+filetype,'r')
    d_lines = d.readlines()
    if len(d_lines) > 1: #any data has been collected
        tubeName2data[tube] = []
        atmodata = [0]*7 # VOC, temperature, humidity, pressure, PM1, PM2.5, PM10
        VOC = 0;
        temperature = 0;
        humidity = 0;
        pressure = 0;
        PM1 = 0;
        PM25 = 0;
        PM10 = 0;
        num_readings = 0;
        for j in range(-1, -len(d_lines),-1):
            dat = d_lines[j].split(",")
            timeofreading =  datetime.strptime(dat[0],"%Y-%m-%d %H:%M:%S")
            if (timenowconvert - timeofreading).total_seconds() <= 3600: #data is from the past hour
                atmodata[0] += float(dat[1]) #voc
                atmodata[1] += float(dat[2]) #temp
                atmodata[2] += float(dat[3]) #hum
                atmodata[3] += float(dat[4]) #press
                atmodata[4] += float(dat[5]) #pm1
                atmodata[5] += float(dat[6]) #pm2.5
                atmodata[6] += float(dat[7]) #pm10
                num_readings += 1
            if timeofreading >= day_ago:
                day_time.append(dat[0])
                day_pm1.append(float(dat[5]))
                day_pm25.append(float(dat[6]))
                day_pm10.append(float(dat[7]))
                day_VOC.append(float(dat[1]))
                day_temp.append(float(dat[2]))
                day_hum.append(float(dat[3]))
                day_press.append(float(dat[4]))
        for i in range(0,len(atmodata)):
                if num_readings > 0: atmodata[i] = atmodata[i]/num_readings;
        tubeName2data[tube] = [timenow,atmodata[0],atmodata[1],atmodata[2],atmodata[3],atmodata[4],atmodata[5],atmodata[6]];
        tubeName2day[tube] = [day_time,day_pm1,day_pm25,day_pm10,day_VOC,day_temp,day_hum,day_press]
        random_counter += 1;

        
counter = 0
numTubes = len(tubeName2data)
o = open('../atmotube_data.js','w');
o.write("var atmoData = [")
for i in tubeName2data:
    o.write('{"type": "Feature","id": "'+str(i)+'","properties": {"icon": ')
    if   tubeName2data[i][1:] == [0,0,0,0,0,0,0]: o.write('greyIcon,   "message": "'+greyMessage);
    elif (tubeName2data[i][1] <= 0.065) and (tubeName2data[i][6] <= 15)  and (tubeName2data[i][7] <= 25):  o.write('blueIcon,   "message": "'+blueMessage);
    elif (tubeName2data[i][1] <= 0.220) and (tubeName2data[i][6] <= 30)  and (tubeName2data[i][7] <= 50):  o.write('greenIcon,  "message": "'+greenMessage);
    elif (tubeName2data[i][1] <= 0.660) and (tubeName2data[i][6] <= 55)  and (tubeName2data[i][7] <= 90):  o.write('yellowIcon, "message": "'+yellowMessage);
    elif (tubeName2data[i][1] <= 2.200) and (tubeName2data[i][6] <= 110) and (tubeName2data[i][7] <= 180): o.write('orangeIcon, "message": "'+orangeMessage);
    else: o.write('redIcon, "message": "'+redMessage)
    o.write('","x_axis":')
    o.write(str(tubeName2day[i][0]))
    o.write(',"pm1":')
    o.write(str(tubeName2day[i][1]))
    o.write(',"pm25":')
    o.write(str(tubeName2day[i][2]))
    o.write(',"pm10":')
    o.write(str(tubeName2day[i][3]))
    o.write(',"VOC":')
    o.write(str(tubeName2day[i][4]))
    o.write(',"temp":')
    o.write(str(tubeName2day[i][5]))
    o.write(',"hum":')
    o.write(str(tubeName2day[i][6]))
    o.write(',"press":')
    o.write(str(tubeName2day[i][7]))
    o.write('},')
    o.write('"geometry": {"type": "Point","coordinates": [')
    o.write(tubeNames2locations[i][0]+','+tubeNames2locations[i][1]+']')
    o.write('}}')
    counter += 1;
    if counter < numTubes: o.write(',')

o.write('];')


time_now = datetime.now()
hour_ago = time_now - timedelta(hours = 1)
day_ago  = time_now - timedelta(days  = 1)

datafile = '../data/atmotube_data_atmo1'
datatype = '.csv'

day_pm1  = []
day_pm25 = []
day_pm10 = []
day_time = []
f = open(datafile+datatype,'r')
f_lines = f.readlines()
for j in range(-1,-len(f_lines),-1):
	dat = f_lines[j].split(',')
	dString = datetime.strptime(dat[0],"%Y-%m-%d %H:%M:%S")
	if dString > day_ago:
		#time_diff = (time_now - dString).total_seconds()/3600.0
		#day_time.append(-1*time_diff)
		#reduced_date = datetime(year=dString.year,month=dString.month,day=dString.day,hour=dString.hour,minute=dString.minute)
		#day_time.append(reduced_date)
		day_time.append(dat[0])
		day_pm1.append(float(dat[5]))
		day_pm25.append(float(dat[6]))
		day_pm10.append(float(dat[7]))


o.write('\n')
o.write('var trace1 = {\n')
o.write('  x: ')
o.write('[]')
o.write(',\n')
o.write('  y: ')
o.write('[]')
o.write(',\n')
o.write("  mode: 'lines+markers',\n")
o.write("  name: 'PM1'\n")
o.write('};')

o.write('\n')
o.write('var trace2 = {\n')
o.write('  x: ')
o.write('[]')
o.write(',\n')
o.write('  y: ')
o.write('[]')
o.write(',\n')
o.write("  mode: 'lines+markers',\n")
o.write("  name: 'PM2.5'\n")
o.write('};')

o.write('\n')
o.write('var trace3 = {\n')
o.write('  x: ')
o.write('[]')
o.write(',\n')
o.write('  y: ')
o.write('[]')
o.write(',\n')
o.write("  mode: 'lines+markers',\n")
o.write("  name: 'PM10'\n")
o.write('};')

o.write('\n')
o.write('var trace4 = {\n')
o.write('  x: ')
o.write('[]')
o.write(',\n')
o.write('  y: ')
o.write('[]')
o.write(',\n')
o.write("  mode: 'lines+markers',\n")
o.write("  name: 'VOC',\n")
o.write("  yaxis: 'y2'")
o.write('};')

o.write('\n')
o.write('var trace5 = {\n')
o.write('  x: ')
o.write('[]')
o.write(',\n')
o.write('  y: ')
o.write('[]')
o.write(',\n')
o.write("  mode: 'lines+markers',\n")
o.write("  name: 'Temperature',\n")
o.write("  yaxis: 'y3'")
o.write('};')

o.write('\n')
o.write('var trace6 = {\n')
o.write('  x: ')
o.write('[]')
o.write(',\n')
o.write('  y: ')
o.write('[]')
o.write(',\n')
o.write("  mode: 'lines+markers',\n")
o.write("  name: 'Humidity',\n")
o.write("  yaxis: 'y4'")
o.write('};')

o.write('\n')
o.write('var trace7 = {\n')
o.write('  x: ')
o.write('[]')
o.write(',\n')
o.write('  y: ')
o.write('[]')
o.write(',\n')
o.write("  mode: 'lines+markers',\n")
o.write("  name: 'Pressure',\n")
o.write("  yaxis: 'y5'")
o.write('};')

o.write("var timenow = '"+timenow+"';")
o.write("var timepast = '"+str(day_ago)+"';")

o.close()
