import json
from random import choice
from time import sleep
import paho.mqtt.client as mqtt
import logging
import Station

logging.basicConfig(
    level=logging.INFO,  # Set the logging level to INFO
    format='%(asctime)s - %(levelname)s - %(message)s',  # Customize the log message format
    datefmt='%Y-%m-%d %H:%M:%S'  # Set the date and time format
)

def connect():
    client = mqtt.Client("DeviceSimulator")
    client.connect("localhost")
    client.loop_start()
    logging.info("Connected to MQTT Broker")
    return client

def disconnect(client):
    client.disconnect()
    logging.info("Disconnected from MQTT Broker")
    client.loop_stop()

def main():
    client = connect()
    device1 = Station.Station("Device1")
    device2 = Station.Station("Device2")
    device3 = Station.Station("Device3")
    devices = [device1, device2, device3]
    while True:
        for device in devices:
            device.get_values()
            values = device.get_values()
            payload = json.dumps(values)
            client.publish(f"UPB/{device.name}", payload)
            logging.info(f"Published values for {device.name}")
        sleep(10)
        try:
            pass
        except KeyboardInterrupt:
            break
            
    disconnect(client)

if __name__ == "__main__":
    main()
