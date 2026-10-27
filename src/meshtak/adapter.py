import asyncio, threading
import meshtak.tak_server as tak_server, meshtak.receiving_node as receiving_node

def start_adapter():
    tak_thread = threading.Thread(target=start_tak_server, daemon=True)
    tak_thread.start()
    receiving_thread = threading.Thread(target=start_receiver_node, daemon=True)
    receiving_thread.start()

    try:
        tak_thread.join()
        receiving_thread.join()

    except KeyboardInterrupt:
        print("Shutting down...")

def start_tak_server():
    print("Starting TAK server...")
    try:
        asyncio.run(tak_server.start())
    except Exception as e:
        print(f"TAK server error: {e}")

def start_receiver_node():
    receiving_node.start()