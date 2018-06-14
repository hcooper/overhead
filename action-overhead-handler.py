#!/usr/bin/env python3
from hermes_python.hermes import Hermes
from overhead import Aircraft, get_aircrafts


def make_speech_output(aircraft: Aircraft) -> str:
    return '{}, {}.\n{}. Heading {}.\nFrom "{}", to "{}".'.format(
        aircraft.airline,
        " ".join(aircraft.flight_no[2:]),
        aircraft.model_speech,
        aircraft.direction,
        aircraft.orig_speech,
        aircraft.dest_speech,
    )


def subscribe_intent_callback(hermes, intentMessage) -> bool:
    message = ""
    # TODO: read this from a config file
    aircrafts = get_aircrafts("47.83,47.40,-123.08,-121.48")

    if aircrafts:
        message += "I have identified {} aircraft.\n\n".format(len(aircrafts))
        for aircraft in aircrafts:
            message += make_speech_output(aircraft) + "\n\n"

    if not message:
        message = "Sorry, no aircraft found."

    return hermes.publish_end_session(intentMessage.session_id, message.encode())


with Hermes(b"localhost:1883") as h:
    h.subscribe_intent(b"coops:whatPlanesAreOverhead", subscribe_intent_callback)
    h.start()
