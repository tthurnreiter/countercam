#!/usr/bin/env python3

import os
import paho.mqtt.client as mqtt
import json
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    #client.subscribe("$SYS/#")
    client.subscribe(mqtt_topic)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    try:
      data = json.loads(msg.payload.decode('utf-8'))
      if(data["type"] == "end"):
        data = data["after"]
        #filtered_data = { key:value for (key,value) in data.items() if key in ["id", "label", "top_score", "end_time"] }
        influx_line=f"""traffic,label={data['label']} id="{data['id']}",score={data['top_score']},count=1 {int(data['end_time']*1e6)*1000}"""
        print(influx_line)
        influx_write_api.write(influx_bucket, influx_org, influx_line, write_options=SYNCHRONOUS)
    except Exception as ex:
      print(ex)

print("Starting...")
mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

mqtt_host = os.environ.get('MQTT_HOST') if 'MQTT_HOST' in os.environ else 'localhost'
mqtt_port = os.environ.get('MQTT_PORT') if 'MQTT_PORT' in os.environ else 1883
mqtt_topic = os.environ.get('MQTT_TOPIC') if 'MQTT_TOPIC' in os.environ else '#'
influx_host = os.environ.get('DB_HOST') if 'DB_HOST' in os.environ else 'localhost'
influx_port = os.environ.get('DB_PORT') if 'DB_PORT' in os.environ else 9999
influx_token = os.environ.get('DB_TOKEN') if 'DB_TOKEN' in os.environ else ""
influx_org = os.environ.get('DB_ORG') if 'DB_ORG' in os.environ else ""
influx_bucket = os.environ.get('DB_BUCKET') if 'DB_BUCKET' in os.environ else ""

print(f"Connecting to mqtt: {mqtt_host}:{mqtt_port}")
mqtt_client.connect(mqtt_host, int(mqtt_port), 60)

print(f"Connecting to influx: {influx_host}:{influx_port}")
influx_client = influxdb_client.InfluxDBClient(url=f"http://{influx_host}:{influx_port}", token=influx_token, org=influx_org)
influx_write_api = influx_client.write_api()

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
mqtt_client.loop_forever()
