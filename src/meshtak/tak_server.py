from configparser import ConfigParser
import meshtak.repository as repository
import asyncio, pytak, time

tak_connected = False

async def connect_to_tak_server():

    try:
        config = ConfigParser()
        
        config["tak"] = {
            "COT_URL": "tls://takserver:8089",
            "PYTAK_TLS_CLIENT_CERT": "/app/certs/meshTak.pem",
            "PYTAK_TLS_CLIENT_KEY": "/app/certs/meshTak.key",
            "PYTAK_TLS_CLIENT_CAFILE": "/app/certs/root-ca.pem",
            "PYTAK_TLS_CLIENT_PASSWORD": "atakatak",
            "DEBUG": "1"
        }

        cfg = config["tak"]

        clitool = pytak.CLITool(cfg)
        await clitool.setup()
        
        clitool.add_tasks(
            {TakSender(clitool.tx_queue, cfg)}
        )

        tak_connected = True
        
        print("Connected to TAK Server")

        await clitool.run()

    except Exception as error:
        tak_connected = False
        print("Tak Server connection encountered an error: retrying in 5 seconds...")


class TakSender(pytak.QueueWorker):

    async def run(self):
        while True:

            payload = repository.track_blocking_queue.get()
            repository.track_blocking_queue.task_done()

            await self.put_queue(payload)

            await asyncio.sleep(1)

async def start():
    while (True):
        await connect_to_tak_server()
        time.sleep(5)
    
