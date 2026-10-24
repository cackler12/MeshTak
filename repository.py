from queue import Queue

track_blocking_queue = Queue()

meshtastic_id_to_uid = {} # Hashmap for fromId to CoT uid

def add_track_to_queue(track):
    track_blocking_queue.put(track)
    print(track)