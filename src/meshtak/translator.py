import xml.etree.ElementTree as ET
import pytak
import numpy as np
import meshtak.repository as repository
from datetime import datetime, timezone, timedelta

def translate_position_to_cot(lattitude, longitude, altitude, fromId, track_time):
    if fromId not in repository.meshtastic_id_to_uid:
        repository.meshtastic_id_to_uid[fromId] = fromId[-4:]
    now = datetime.fromtimestamp(track_time, timezone.utc)
    stale_time = now + timedelta(seconds=int(60))

    event = ET.Element(
        "event",
        {
            "version": "2.0",
            "uid": repository.meshtastic_id_to_uid.get(fromId),
            "type": "a-f-A",
            "how": "m-g",
            "time": now.strftime(pytak.W3C_XML_DATETIME),
            "start": now.strftime(pytak.W3C_XML_DATETIME),
            "stale": stale_time.strftime(pytak.W3C_XML_DATETIME),
        },
    )

    ET.SubElement(
        event,
        "point",
        {
            "lat": str(lattitude),
            "lon": str(longitude),
            "hae": str(altitude),
            "ce": "10",
            "le": "10",
        },
    )

    detail = ET.SubElement(event, "detail")

    ET.SubElement(
        detail,
        "contact",
        {"callsign": repository.meshtastic_id_to_uid.get(fromId)},
    )

    return ET.tostring(event, encoding="utf-8")