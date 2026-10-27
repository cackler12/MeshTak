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

### Executing program

```bash
pip install uv

uv run meshtak
```

## Help

## Authors

CJ Ackler - cjackler12@gmail.com

## Version History

COMING SOON

## License

This project is licensed under the Apache 2.0 License - see the LICENSE.md file for details

## Acknowledgments

* [pytak](https://github.com/snstac/pytak)
* [Meshtastic](https://github.com/meshtastic)