from serial.tools import list_ports
import serial, time, threading
import meshtastic.serial_interface
from pubsub import pub
from meshtak.translator import translate_position_to_cot
from meshtak.repository import add_track_to_queue

def try_connect(port, result):
    try:
        result["interface"] = meshtastic.serial_interface.SerialInterface(
            devPath=port
        )
    except Exception as e:
        result["error"] = e

def find_receiver_node():
    for port in list_ports.comports():
        try:
            print(f"Trying {port.device}...")
            ser = serial.Serial(
                port=port.device,
                baudrate=115200,
                timeout=2
            )
            print("Port opened")
            ser.close()

            result = {}

            thread = threading.Thread(
                target=try_connect,
                args=(port.device, result),
                daemon=True
            )

            thread.start()
            thread.join(timeout=5)

            if thread.is_alive():
                print("Connection timed out")
            else:
                return result.get("interface")

        except Exception:
            pass
    return

def on_receive(packet, interface):
    try:
        print("Received packet:")
        decoded = packet.get("decoded", {})
        if decoded.get("portnum") == "POSITION_APP":
            pos = decoded.get("position", {})

            latitude = pos.get("latitude")
            longitude = pos.get("longitude")
            altitude = pos.get("altitude")
            time = pos.get("time")
            from_id = packet.get("fromId")

            track = translate_position_to_cot(
                lattitude=latitude, 
                longitude=longitude, 
                altitude=altitude, 
                fromId=from_id, 
                track_time=time)
            add_track_to_queue(track=track)

    except Exception as e:
        print(e)

def start():
    while True:
        try:
            interface = find_receiver_node()
            if interface == None:
                pass

            pub.subscribe(on_receive, "meshtastic.receive")

            while True:
                time.sleep(1)

        except Exception as ex:
            print(f"Connection lost: {ex}")
            time.sleep(5)