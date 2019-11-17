#!/data/data/com.termux/files/usr/bin/env python
import subprocess
import shlex
import requests
import sys
import json


def remove_all(orig, patts):
    '''
    Removes all of the patterns specified
    in a list from the original str.

    Keyword Arguments:
    orig -- The original string you want
            to have everythibg removed from

    patts -- The list of patterns you want
            to have removed from the
            original string
    '''
    for pattern in patts:
        orig = orig.replace(pattern, "")
    return orig


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
    json_output = str(output)
    if json_output is not None or json_output == "b''":
        patterns = ["b\'", "\\n  ", "\\n'", "\\n"]
        json_str = remove_all(json_output, patterns)
        data = json.loads(json_str)
        coords.append(str(data["latitude"]))
        coords.append(str(data["longitude"]))
        return coords
    else:
        print("Could not get location!\nExiting...")
        sys.exit()

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
