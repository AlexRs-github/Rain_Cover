import re
import subprocess
import shlex
import requests


def coord():
	'''
	returns a list of latitude and longitude
	coords of the device
	'''
	coords = []

	commands = "termux-location -p network"
	args = shlex.split(commands)
	process = subprocess.Popen(args, shell=True, stdout=subprocess.PIPE)
	output, err = process.communicate()
	str_output = str(output)

	y = '"latitude":\s*(\-?\d+(\.\d+)?)'
	x = '"longitude":\s*(\-?\d+(\.\d+)?)'

	if "latitude" and "longitude" in str_output:
        	lat = re.search(y, str_output).group(0)
        	long = re.search(x, str_output).group(0)
        	lat_ls = lat.split(" ")
        	long_ls = long.split(" ")
        	coords.append(lat_ls[1])
        	coords.append(long_ls[1])
	return coords


def resp(api_key, coordinates):
	'''
	returns the json resp of the weather
	'''
	r = requests.get(f"https://api.darksky.net/forecast/{api_key}/{str(coordinates[0])},{str(coordinates[1])}?exclude=currently,minutely,hourly,alerts&time=timezone")
	resp = r.json
	return resp

api = "5cb9e64607d450474038c39e6da27694"
resp(api, coord())
'''
# create a function that
# will parse a json obj
# then notify the user
str_smpl = str(smpl)

rain = '"precipType":"rain"'
snow = '"precipType":"snow"'

if rain in str_smpl:
	r = re.findall(rain, str_smpl)
	if r[1]:
		print("it will rain tomorrow")
elif snow in str_smpl:
	s = re.findall(snow, str_smpl)
        if r[1]:
                print("it will snow tomorrow")
'''
