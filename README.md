# MeshTak

A lightweight microservice that converts Meshtastic protobuf messages to TAK CoT XML

## Description

Meshtastic currently allows users to configure a device to publish data to ATAK. However, I wanted to make a project that specifically translated position messages
sent from a tracker node to Tak CoT and published these messages to a Tak Server with minimal latency. If you use the Meshtastic ATAK plugin, you can only send message updates to ATAK every 30 seconds. With MeshTak, messages are translated to CoT and sent to the Tak Server as fast as they arrive! MeshTak is a peice of my rela-time tracking solution with Meshtastic and ATAK. I have also modified the Meshtastic firmware to send position updates at an increased rate in my firmware-otus repo here: https://github.com/cackler12/firmware-otus. 

## Getting Started

To build MeshTak from source, clone the repo using

```bash
git clone https://github.com/cackler12/MeshTak.git
```

### Dependencies

* Python 3.12 (!> 3.12 as meshtastic module is incompatible)
* 64-bit Debian based system (amd64 or arch64)
* Docker

### Building deb package

* First, choose the branch that matches the arch of your target system (arch/amd64 or arch/arm64)

```bash
git switch arch/amd64

./build_package.sh
```

### Installing MeshTak

Because MeshTak runs as a systemd service and adds a meshtak.service file to /etc, it is advised to move the deb package to /tmp before installing:

```bash
cp meshtak-0.1.0-amd64.deb /tmp

cd /tmp

sudo apt install ./meshtak-0.1.0-amd64.deb
```
### Configuring MeshTak

MeshTak uses port 8089 to connect to a Tak Server using TLS. In order to connect over TLS using pytak, the MeshTak container will need generated client certs and a ca.pem from the Tak Server.

#### Creating Tak Certs

On the Tak Server machine, run the following commands to create a client cert with the correct name:

```bash
sudo su tak

cd /opt/tak/certs

./makeCert.sh client meshTak
```

From here, you will need to move:
* meshTak.pem
* meshTak.key
* root-ca.pem

to the /usr/bin/meshtak/certs dir on the machine you installed meshtak on.

The docker-compose.yml file contains a line that maps this /usr/bin/meshtak/certs dir to /app/certs within the meshtak container, which is where the pytak connection looks for TLS certs. 

### Running MeshTak

To run MeshTak, use:

```bash
sudo systemctl start meshtak
```

To stop MeshTak, use:

```bash
sudo systemctl stop meshtak
```

To get logs from the meshtak container when running, use:

```bash
docker logs --follow meshtak
```

### Removing MeshTak

To remove the meshtak application, you can run:

```bash
sudo apt remove meshtak
```

This should check if the meshtak service is active, and if so will terminate the service and remove the package. 

## Help

Feel free to direct any bugs or questions to my email linked below! :)

## Authors

CJ Ackler - cjackler12@gmail.com

## Version History

0.1.0 - Beta

## License

This project is licensed under the Apache 2.0 License - see the LICENSE.md file for details

## Acknowledgments

* [pytak](https://github.com/snstac/pytak)
* [Meshtastic](https://github.com/meshtastic)