#!/usr/bin/env python3
import csv
import json
import re
from typing import List

import requests


class Aircraft(object):
    """ Object to hold details of a particular aircraft """

    def __init__(self, track, model, orig, dest, flight_no):
        self.track = track
        self.model_code = model
        self.orig = orig
        self.dest = dest
        self.flight_no = flight_no

    @property
    def orig_speech(self):
        return airports.get(self.orig, " ".join(self.orig)).replace(
            " International Airport", ""
        )

    @property
    def dest_speech(self):
        return airports.get(self.dest, " ".join(self.dest)).replace(
            " International Airport", ""
        )

    @property
    def airline(self):
        return airlines.get(self.airline_code, " ".join(self.airline_code))

    @property
    def airline_code(self):
        return self.flight_no[:2]

    @property
    def model_name(self):
        return models.get(self.model_code, self.model_code)

    @property
    def direction(self):
        return track_to_direction(self.track)

    @property
    def model_speech(self):
        return model_to_speech(self.model_name)

    @property
    def direction_arrow(self):
        return track_to_direction(self.track, True)


def track_to_direction(track, arrow=False):
    """ For a heading in degrees, return a compass direction """
    if track >= 338 or track <= 22:
        return "↑" if arrow else "north"
    if track >= 23 and track <= 67:
        return "↗" if arrow else "north-east"
    if track >= 68 and track <= 112:
        return "→" if arrow else "east"
    if track >= 113 and track <= 157:
        return "↘" if arrow else "south-east"
    if track >= 158 and track <= 202:
        return "↓" if arrow else "south"
    if track >= 203 and track <= 247:
        return "↙" if arrow else "south-west"
    if track >= 248 and track <= 292:
        return "←" if arrow else "west"
    if track >= 293 and track <= 337:
        return "↖" if arrow else "north-west"


def model_to_speech(model: str) -> str:
    """ Covert the model name into a format which makes text-to-speech engines
    pronounce it realisticly, e.g.
      Boeing 737-400 --> Boeing 7 3 7 400
      Airbus A319 --> Airbus A 3 19
    """
    if model == "unmatched":
        return "Unmatched aircraft"

    if model == "De Havilland Canada DHC-8-400 Dash 8Q":
        return "Bombardier Dash 8 Q400"

    res = re.match("(.*) A?(.{3})-?(.{3})?", model)
    if res:
        if res.group(1) == "Boeing":
            resp = "A Boeing " + " ".join(res.group(2))
            if res.group(3):
                resp += " " + res.group(3)
            return resp

        if res.group(1) == "Airbus":
            resp = "An Airbus A 3 " + res.group(2)[1:]
            if res.group(3):
                resp += " " + res.group(3)
            return resp

    return model  # it's a model we don't have a custom lexicon for


def get_aircrafts(bounds: str) -> List[Aircraft]:
    url = (
        "https://data-live.flightradar24.com/zones/fcgi/feed.js?bounds={}"
        "&faa=1&mlat=1&flarm=1&adsb=1&gnd=1&air=1&vehicles=1&estimated=1&maxage=14400&gliders=1&stats=1"
    ).format(bounds)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0"
    }
    data = json.loads(requests.get(url, headers=headers).text)

    for f in ["full_count", "version", "stats"]:
        data.pop(f)  # strip unwanted fields

    return [Aircraft(v[3], v[8], v[11], v[12], v[13]) for v in data.values()]


# There's bound to be a better way to do this than using globals.
global models
models = {id2: name for name, id1, id2 in list(csv.reader(open("planes.dat")))}

global airports
airports = {a["iata"]: a["name"] for a in json.loads(open("airports.json").read())}

global airlines
airlines = {a["iata"]: a["name"] for a in json.loads(open("airlines.json").read())}


if __name__ == "__main__":
    bounds = "51.72,51.44,-0.59,0.34"  # Central London
    for aircraft in get_aircrafts(bounds):
        print(
            "{:<3}->{:<3} {:<6} {:<1} ({})".format(
                aircraft.orig,
                aircraft.dest,
                aircraft.flight_no,
                aircraft.direction_arrow,
                aircraft.model_name,
            )
        )
