import xml.etree.ElementTree as ET
from pytak import W3C_XML_DATETIME
from meshtak.repository import meshtastic_id_to_uid
from uuid import uuid4
from datetime import datetime, timezone, timedelta

def translate_meshtastic_position_to_tak_track(from_id, short_name, latitude, longitude, alt_msl, timestamp):
    if from_id not in meshtastic_id_to_uid:
        meshtastic_id_to_uid[from_id] = str(uuid4())
    track_time = datetime.fromtimestamp(timestamp, timezone.utc)
    stale_time = track_time + timedelta(seconds=int(60))

    event = ET.Element(
        "event",
        {
            "version": "2.0",
            "uid": meshtastic_id_to_uid.get(from_id),
            "type": "a-f-A",
            "how": "m-g",
            "time": track_time.strftime(W3C_XML_DATETIME),
            "start": track_time.strftime(W3C_XML_DATETIME),
            "stale": stale_time.strftime(W3C_XML_DATETIME),
        },
    )

    ET.SubElement(
        event,
        "point",
        {
            "lat": str(latitude),
            "lon": str(longitude),
            # convert msl to hae
            "hae": str(alt_msl),
            "ce": "10",
            "le": "10",
        },
    )

    detail = ET.SubElement(event, "detail")

    ET.SubElement(
        detail,
        "contact",
        {"callsign": short_name},
    )

    return ET.tostring(event, encoding="utf-8")