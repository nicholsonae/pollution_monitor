var atmoData = [{"type": "Feature","id": "atmo1","properties": {"icon": greyIcon,   "message": "No data","x_axis":[],"pm1":[],"pm25":[],"pm10":[],"VOC":[],"temp":[],"hum":[],"press":[]},"geometry": {"type": "Point","coordinates": [51.000,-0.108]}},{"type": "Feature","id": "atmo2","properties": {"icon": greyIcon,   "message": "No data","x_axis":[],"pm1":[],"pm25":[],"pm10":[],"VOC":[],"temp":[],"hum":[],"press":[]},"geometry": {"type": "Point","coordinates": [51.001,-0.110]}}];
var trace1 = {
  x: [],
  y: [],
  mode: 'lines+markers',
  name: 'PM1'
};
var trace2 = {
  x: [],
  y: [],
  mode: 'lines+markers',
  name: 'PM2.5'
};
var trace3 = {
  x: [],
  y: [],
  mode: 'lines+markers',
  name: 'PM10'
};
var trace4 = {
  x: [],
  y: [],
  mode: 'lines+markers',
  name: 'VOC',
  yaxis: 'y2'};
var trace5 = {
  x: [],
  y: [],
  mode: 'lines+markers',
  name: 'Temperature',
  yaxis: 'y3'};
var trace6 = {
  x: [],
  y: [],
  mode: 'lines+markers',
  name: 'Humidity',
  yaxis: 'y4'};
var trace7 = {
  x: [],
  y: [],
  mode: 'lines+markers',
  name: 'Pressure',
  yaxis: 'y5'};var timenow = '2020-07-22 10:55:00';var timepast = '2020-07-21 10:55:00.427818';