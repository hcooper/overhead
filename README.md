> [!WARNING]  
> Flightradar24 has changed a lot since this was written. It's quite possible, if not probable, this doesn't work anymore.

# overhead

`overhead` is a python module which pulls data from flightradar24.com. For a given area it returns a list of `Aircraft()` objects. These objects have a number of basic properties (e.g. airline, direction of flight, model, etc), which make them easily ingested by downstream services.

This library mainly exists to power `snips-skill-overhead`, which is a module for the Snips voice assistant. The skill lets you ask "What planes are flying overhead?". A number of the object properties are designed to help the Snips text-to-speech system pronounce aircraft information correctly (e.g. "seven three seven", not "seven hundred and thirty seven").

## Random Comments
 - Please don't abuse this. This is using public flightradar24.com data. They offer a great
 service, throw some cash their way (and look for real APIs) if you want to start hammering it.
 - Note the Snips skill is written using Python 3. However the public version of `hermes_python` (the library used for speaking via MQTT to Snips) is only built for Python 2. I've documented the minor tweaks needs to make Python 3 work here: https://github.com/snipsco/snips-issues/issues/26
 - I recommend a high-quality TTS service if you want the results to be spoken. I have another project which makes Snips use AWS Polly: https://github.com/hcooper/snips-tts-polly.

## Credits
The airline, airport, and plane data I've included here aren't my own work (my I've added one
or two very minor tweaks):
 - IATA airline data: https://github.com/BesrourMS/Airlines
 - IATA airport data: https://github.com/jbrooksuk/JSON-Airports
 - Plane model data: (need to find the github link)

## Example Usage

### As a module
`get_aircrafts` takes in one string, in format `lat_a,lat_b,long_y,long_z` which will form a search area of ay, az, by, bz.

```
>>> from overhead import get_aircrafts

>>> get_aircrafts("51.72,51.44,-0.59,0.34")
[<overhead.Aircraft object at 0x03D471F0>, <overhead.Aircraft object at 0x03D6C730>...]

>>> get_aircrafts("51.72,51.44,-0.59,0.34")[0].model_name
'Airbus A320'

>>> get_aircrafts("51.72,51.44,-0.59,0.34")[3].orig_speech
'London Heathrow Airport'
```

### As a script
If executed standalone, this module will produce a simple example output:

```
LHR->KEF BA800  ↓ (Airbus A320)
GOT->LHR BA803  ← (Airbus A320)
LHR->PMO BA610  ← (Airbus A320)
LHR->STR BA918  ← (Airbus A320)
LHR->MAN BA1370 → (Airbus A320)
LHR->           ↙ (Boeing 777-200)
LHR->EDI BA1434 ↖ (Airbus A320)
JFK->LHR BA116  → (Boeing 747-400)
LHR->           ↓ (Boeing 747-400)
JFK->LHR VS138  → (Airbus A330-300)
LHR->NCE BA342  → (Airbus A321)
LHR->ORD AA99   ↘ (Boeing 787-8)
LHR->BCN BA478  → (Airbus A320-neo)
LHR->           ← (Boeing 777-200)
TXL->LHR EW8460 ← (Airbus A319)
CGN->LHR EW460  ← (Airbus A320)
MAN->CIA FR3204 ↘ (Boeing 737-800)
ATL->LHR VS104  ← (Airbus A330-300)
MAN->LHR BA1385 → (Airbus A319)
CDG->LHR AF1680 ← (Airbus A320)
EMA->BRU BM1233 → (Embraer RJ145)
TXL->LHR BA981  ↓ (Airbus A321)
EDI->LHR BE2101 ↙ (De Havilland Canada DHC-8-400 Dash 8Q)
LCY->FRA LH927  → (Embraer 190)
AMS->LCY KL983  ← (Embraer 190)
MUC->LHR LH2470 ← (Airbus A320)
CPH->LHR BA811  ↑ (Airbus A319)
EDI->LCY BA8701 ← (Embraer 190)
STN->CDG QR8440 ↘ (Boeing 777-200LR)
```

### As a Snips skill

***In light of Snips being acquired, and its public services being shutdown, this plugin is no longer maintained. See https://www.home-assistant.io/blog/2019/12/03/sonos-shutting-down-local-voice-option-snips/ for more information.***

Once `action-overhead-handler.py` is running (either by yourself, or automatically by `snips-skill-server`), it will subscribe to the configured Snips action (e.g. `whatPlanesAreOverhead`). Once triggered it will respond by sending the text-to-speech service a string of text describing the aircraft it's found, in a format that's optimized for computer pronunciation:

```
I have identified 1 aircraft.

British Airways, 4 2 9.
An Airbus A 3 20. Heading East.
From "Amsterdam Schiphol", to "London Heathrow".
```

[Example output](example.mp3) using AWS Polly for TTS.
