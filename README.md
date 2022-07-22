# countercam

Trying to set up a system to detect road traffic, classify users (pedestrians, bikes, cars), count and summarize traffic numbers.

Traffic is detected using a cheap 1080p wireless network camera and machine learning.

Uses Frigate NVR (https://frigate.video/) for motion detection and object classification, a python script and an MQTT server to transfer the detection data into an Influx database for storage and graphing.

Currently abandoned, because the Raspberry Pi 4B that the project runs on turned out to have too little processing power to reliably detect all passing vehicles.

Possible future work:

- Replace Frigate NVR software with custom processing and detectors.
- Replace Raspberry Pi with more powerful hardware
- Extend Raspberry Pi with USB AI accelerator like coral.ai
- Add Grafana for nicer graphs
