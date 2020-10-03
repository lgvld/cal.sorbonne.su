#!/usr/bin/env python3

import logging
import os
import sys
import urllib.request


DIR_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
DIR_DATA = os.path.join(DIR_ROOT, "data")
DIR_ICS = os.path.join(DIR_DATA, "ics")
DIR_STATIC = os.path.join(DIR_ROOT, "static")

MASTERS_YML = os.path.join(DIR_DATA, "masters.yml")


logging.basicConfig(
    datefmt="%Y-%m-%d %H:%M:%S",
    # format="%(asctime)s %(levelname)-8s %(message)s",
    format="%(asctime)s %(levelname)s %(message)s",
    level=logging.DEBUG,
    stream=sys.stdout
)

# Disable logging for disturbing modules (when setting logging level to DEBUG).
logging.getLogger("requests").setLevel(logging.WARNING)


CALDAV_URL = "https://cal.ufr-info-p6.jussieu.fr:443/caldav.php/"
CALDAV_USERNAME = "student.master"
CALDAV_PASSWORD = "guest"


# configuration of urllib.request (CalDavZAP requires basic authentification).
password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()
password_mgr.add_password(None,
                          CALDAV_URL,
                          CALDAV_USERNAME,
                          CALDAV_PASSWORD)
handler = urllib.request.HTTPBasicAuthHandler(password_mgr)
opener = urllib.request.build_opener(handler)
urllib.request.install_opener(opener)


TIME_BETWEEN_UPDATES = 2 * 60 * 60

TIME_BEFORE_OUTDATED = 4 * 60 * 60


NAME = "cal.sorbonne.su"

ROOT_URL = "https://cal.sorbonne.su/"

DEFAULT_URL = "https://cal.sorbonne.su/M1+M2"


# ATTRIBUTES = (
#     'name',
#     'begin',
#     'end',
#     'duration',
#     'uid',
#     'description',
#     'created',
#     'last_modified',
#     'location',
#     'url',
#     'transparent',
#     'alarms',
#     'attendees',
#     'categories',
#     'status',
#     'organizer',
#     'geo',
#     'classification'
# )
