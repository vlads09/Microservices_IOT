import datetime
from json import loads
import logging
from os import getenv
from re import match
from influxdb_client import InfluxDBClient, Point, WriteOptions
import paho.mqtt.client as mqtt
from dotenv import load_dotenv

load_dotenv('adapter.env')

influx_client = None

# Configure the logger globally
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO
)
log = logging.getLogger(__name__)

# InfluxDB connection details
INFLUXDB_URL = getenv('INFLUXDB_URL')
INFLUXDB_TOKEN = getenv('INFLUXDB_TOKEN')
INFLUXDB_ORG = getenv('INFLUXDB_ORG')
INFLUXDB_BUCKET = getenv('INFLUXDB_BUCKET')

# MQTT Broker details
MQTT_BROKER = getenv('MQTT_BROKER')
MQTT_PORT = int(getenv('MQTT_PORT'))
MQTT_TOPIC = getenv('MQTT_TOPIC')

def set_log_level():
    """Set the log level dynamically based on the environment variable."""
    debug_data_flow = getenv('DEBUG_DATA_FLOW', 'false').lower()
    log.setLevel(logging.INFO if debug_data_flow == 'true' else logging.ERROR)

def on_connect(client, userdata, flags, rc):
    """Callback function to handle the connection to the MQTT Broker."""
    if rc == 0:
        log.info("Connected to MQTT Broker")
        client.subscribe(MQTT_TOPIC)
    else:
        log.error(f"Failed to connect to MQTT Broker. Return code: {rc}")

def _on_message(client, args, message):
    """Callback function to handle the incoming messages."""
    global influx_client 
    if not match(r'^[^/]+/[^/]+$', message.topic):
        return

    log.info(f"Received a message by topic |{message.topic}|")

    data = loads(message.payload)
    location, station = message.topic.split('/')
    timestamp = datetime.datetime.now().astimezone().strftime('%Y-%m-%dT%H:%M:%S%z')
    log.info(f"Data timestamp is: {timestamp}")
    write_api = influx_client.write_api(write_options=WriteOptions(batch_size=1))

    for sensor, value in data.items(): # Iterate over the sensors and their values
        if not isinstance(value, (int, float)): # Check if the value is a number
            log.error(f"Invalid value for {sensor}")
            continue
        
        # Create a new data point
        point = Point(f"{station}.{sensor}") \
                .tag("location", location) \
                .tag("station", station) \
                .field("value", float(value)) \
                .time(timestamp)

        # Write the data point to InfluxDB
        write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=point)
        log.info(f"{location}.{station}.{sensor} {value}")

def main():
    global influx_client  # Initialize the global client
    
    set_log_level()
 
    influx_client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
    
    mqtt_client = mqtt.Client("DataLogger")
    mqtt_client.on_connect = on_connect
    mqtt_client.message_callback_add(MQTT_TOPIC, _on_message)
    mqtt_client.connect(MQTT_BROKER, MQTT_PORT)
    mqtt_client.loop_forever()

if __name__ == "__main__":
    main()
