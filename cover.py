#!/data/data/com.termux/files/usr/bin/env python
import re
import subprocess
import shlex
import requests
import sys
import json


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

    y = r'"latitude":\s*(\-?\d+(\.\d+)?)'
    x = r'"longitude":\s*(\-?\d+(\.\d+)?)'

    if "latitude" and "longitude" in str_output:
        lat = re.search(y, str_output).group(0)
        long = re.search(x, str_output).group(0)
        lat_ls = lat.split(" ")
        long_ls = long.split(" ")
        coords.append(lat_ls[1])
        coords.append(long_ls[1])
    else:
        print("Could not find location!\nExiting...")
        sys.exit()
    return coords


def resp(api_key, coordinates):
    '''
    returns the json resp of the weather
    '''
    r = requests.get(
        f"https://api.darksky.net/forecast/{api_key}/{str(coordinates[0])},{str(coordinates[1])}?exclude=currently,minutely,hourly,alerts&time=timezone").text
    return r


def notify(json_data):
    '''
    parses json obj to get tomorrow's precipType

    then displays a toast message
    '''
    data = json.loads(json_data)
    # Parse the data obj for tomorrow's PrecipType
    precip = str(data["daily"]["data"][1]["precipType"])

    if precip == "rain":
        r_args = shlex.split("termux-toast It will rain tomorrow! Put the cover on the car!")
        subprocess.run(r_args)
    elif precip == "snow":
        s_args = shlex.split("termux-toast It will snow tomorrow! Put the cover on the car!")
        subprocess.run(s_args)


api = ""
notify(resp(api, coord()))
