from PIL import Image, ImageDraw, ImageColor
import csv

xoffset = 230
zoffset = 690

with open('stations.csv') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    stations = [row for row in csv_reader]
with open('connections.csv') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    connections = [row for row in csv_reader]
	
image = Image.new('RGBA',(750,1200),(255,255,255,0))
draw = ImageDraw.Draw(image)

for station in stations:
	split = station["coords"].split('/')
	x = int(split[0]) - xoffset
	station.update({"x" : x})
	z = int(split[2]) - zoffset
	station.update({"z" : z})
	color = ImageColor.getcolor(station['line'], 'RGBA')
	draw.rectangle((x - 10, z - 10, x + 10, z + 10), fill= color)
	draw.text((x - 30, z + 20), station["station"], fill= 'black')
	
stationsdic = {(s["line"],s["station"]) : s for s in stations}

for edge in connections:
	origin = stationsdic[(edge["line"],edge["origin"])]
	dest = stationsdic[(edge["line"],edge["dest"])]
	x0,z0,x1,z1 = origin["x"],origin["z"],dest["x"],dest["z"]
	coords = [x0,z0,x0,z1,x1,z1]
	draw.line(coords, fill = edge["line"], width = 5)
	
image.save('stationsmap.png')