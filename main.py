#!/usr/bin/env python3

import functools
import logging
import operator
import os
import time
import urllib.parse
import urllib.request
import sys
import time

import bottle
import ics
import yaml

import config


###############################################################################


os.makedirs(config.DIR_ICS, exist_ok=True)


# Or we could instead parse response (see `activecalendarcollections`) from:
# https://cal.ufr-info-p6.jussieu.fr/caldav.php/MasterInfo/
with open(config.MASTERS_YML, "r") as f:
    MASTERS = yaml.safe_load(f)


# We keep events in memory so they can be returned instantly (it may take more
# than a minute to parse every ICS file).
events_ = {}


###############################################################################


def ics_file_from_master_name(master):
    return os.path.join(config.DIR_ICS, master + ".ics")


def ics_file_is_outdated(ics_file):
    return not os.path.isfile(ics_file) or os.path.getmtime(ics_file) + config.TIME_BETWEEN_UPDATES <= time.time()


def fetch_ics_data(master):

    assert master in MASTERS, f"{master}: unknown master"

    URL = config.CALDAV_URL + "/" + MASTERS[master] + "/" + master

    with urllib.request.urlopen(URL) as response:
        return response.read().decode()


def update_ics_file(master):

    assert master in MASTERS, f"{master}: unknown master"

    ics_file = ics_file_from_master_name(master)

    ics_data = fetch_ics_data(master)

    with open(ics_file, "w+") as f:
        f.write(ics_data)

    logging.debug(f"[+] {ics_file}: file has been updated")


def update_events(master):

    assert master in MASTERS, f"{master}: unknown master"

    ics_file = ics_file_from_master_name(master)

    if master not in events_ or ics_file_is_outdated(ics_file):

        update_ics_file(master)

        events_[master] = []

        with open(ics_file, "r") as f:
            for event in ics.Calendar(f.read()).events:
                events_[master].append(event)

        logging.debug(f"[+] {ics_file}: found {len(events_[master])} events")

    else:

        logging.debug(f"[+] {master}: events are already up-to-date")


def get_events(masters, begin_after=time.time()):

    # first we create a big list by merging several lists of events.
    events = functools.reduce(operator.iadd, [events_[m] for m in masters], [])

    # then we remove outdated events.
    if begin_after:
        events = [e for e in events if e.begin.timestamp + config.TIME_BEFORE_OUTDATED > begin_after]

    # and finally, we sort the list by date.
    events.sort(key=lambda event: event.begin.timestamp)

    return events


###############################################################################


app = application = bottle.default_app()


@app.get("/static/<path:path>")
def static(path):
    return bottle.static_file(path, root=config.DIR_STATIC)


@app.get("/")
def default():
    bottle.redirect(config.DEFAULT_URL)


@app.get("/<str>")
def index(str=""):

    selected_masters = [m for m in str.split("+") if m in MASTERS]

    # selected_masters.sort()

    for master in selected_masters:
        update_events(master)

    events = get_events(selected_masters)

    title = f"{' + '.join(selected_masters)} @ {config.NAME}"

    return bottle.template("index",
                           events=events,
                           masters=MASTERS.keys(),
                           selected_masters=selected_masters,
                           title=title)


###############################################################################


if __name__ == "__main__":

    if len(sys.argv) == 2:

        app.run(debug=False,
                host="localhost",
                port=sys.argv[1],
                reloader=False,
                # server="gunicorn",
                workers=4)

    else:

        print(f"usage: {sys.argv[0]} port")
