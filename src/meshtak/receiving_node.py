from pubsub import pub
import meshtastic, threading
from time import sleep
from meshtastic import serial_interface
from meshtak.translator import translate_meshtastic_position_to_tak_track
from meshtak.repository import add_track_to_queue

class RecieverNode:

    def __init__(self):
        self.__interface = None
        self.__connected = threading.Event()

        pub.subscribe(self.on_receive, "meshtastic.receive")
        pub.subscribe(self.on_connection_established, "meshtastic.connection.established")
        pub.subscribe(self.on_connection_lost, "meshtastic.connection.lost")

    def try_to_connect(self):
        if self.__interface is not None:
            return
        try:
            print("Listening for a meshtastic device...")
            self.__interface = meshtastic.serial_interface.SerialInterface()
        except Exception as e:
            print(f"Failed to connect to a meshtastic device: {e}")
            self.__interface = None
            self.__connected.clear()

    def try_to_close(self):
        interface = self.__interface

        self.__interface = None
        self.__connected.clear()

        if interface is not None:
            try:
                interface.close()
            except Exception as e:
                print(f"Error while closing interface: {e}")

    def on_receive(self, packet, interface):
        if interface is self.__interface:
            decoded = packet.get("decoded", {})
            match decoded.get("portnum"):
                case "POSITION_APP":
                    from_id = packet.get("fromId")
                    if from_id:
                        node_info = self.__interface.nodes.get(from_id)
                        if node_info:
                            user = node_info.get("user", {})
                            short_name = user.get("shortName", from_id[-4:])
                        else:
                            short_name = from_id[-4:]
                        pos = decoded.get("position", {})
                        latitude = pos.get("latitude")
                        longitude = pos.get("longitude")
                        altitude = pos.get("altitude")
                        timestamp = pos.get("time")
                        add_track_to_queue(
                            translate_meshtastic_position_to_tak_track(from_id, short_name, latitude, longitude, altitude, timestamp)
                        )
                    else:
                        print("Dropping position message, no fromId!")
                        
                case "SERIAL_APP":
                    print("Received a serial packet!")
                

    def on_connection_established(self, interface, topic=pub.AUTO_TOPIC):
        if interface is self.__interface:
            self.__connected.set()
            print("Successfully connected to meshtastic device!")

    def on_connection_lost(self, interface, topic=pub.AUTO_TOPIC):
        if interface is self.__interface:
            self.__connected.clear()
            print("Lost connection to meshtastic device!")

    def start(self):
        while True:
            try:
                if self.__interface == None:
                    self.try_to_connect()
                    if self.__interface == None:
                        print("Retrying meshtastic connection in 5 seconds...")
                        sleep(5)
                        continue
                
                if not self.__connected.wait(timeout=10):
                    print("Meshtastic connection timed out...")
                    self.try_to_close()
                    sleep(5)
                    continue
                while self.__connected.is_set():
                    sleep(1)
                self.try_to_close()
                sleep(5)
            except Exception as e:
                print("An exception occured while listening to meshtastic device, restarting in 5 seconds...")
                self.try_to_close()
                sleep(5)