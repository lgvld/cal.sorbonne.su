#!/usr/bin/env python3

import re


def infos_from_event(event):

    infos = {
        "begin": event.begin,
        "location": event.location,
        "name": event.name
    }

    return infos
