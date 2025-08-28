import paho.mqtt.client as mqtt
import time
import random
import json

# --- MQTT Broker Configuration ---
# If Mosquitto is on your laptop, and this script runs on a Raspberry Pi,
# replace 'localhost' with your laptop's IP address (e.g., '192.168.1.100')
BROKER_ADDRESS = "localhost" # Or your laptop's IP if running on RPi
BROKER_PORT = 1883           # Default MQTT port
TOPIC = "iot/sensor/data"    # The MQTT topic to publish data to

# --- MQTT Client Callbacks ---
def on_connect(client, userdata, flags, rc):
    """Callback function when the client connects to the MQTT broker."""
    if rc == 0:
        print(f"✅ Connected to MQTT Broker at {BROKER_ADDRESS}:{BROKER_PORT}!")
    else:
        print(f"❌ Failed to connect, return code {rc}\n")

def on_publish(client, userdata, mid):
    """Callback function when a message is successfully published."""
    # print(f"Published message ID: {mid}")
    pass # No need to print for every message for simplicity

# --- Setup MQTT Client ---
client = mqtt.Client()
client.on_connect = on_connect
client.on_publish = on_publish

# Connect to the broker
try:
    client.connect(BROKER_ADDRESS, BROKER_PORT, 60)
except Exception as e:
    print(f"🚨 Error connecting to MQTT broker: {e}")
    exit() # Exit if connection fails

# Start the MQTT loop in a non-blocking way
# This handles network traffic, dispatches callbacks, and keeps the connection alive
client.loop_start()

# --- Simulate IoT Data Sending ---
try:
    while True:
        # Generate some dummy IoT data
        temperature = round(random.uniform(20.0, 30.0), 2) # Celsius
        humidity = round(random.uniform(40.0, 70.0), 2)    # Percentage

        # Create a dictionary for the data
        iot_data = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "temperature": temperature,
            "humidity": humidity,
            "device_id": "rpi_sensor_001"
        }

        # Convert dictionary to a JSON string for publishing
        payload = json.dumps(iot_data)

        # Publish the data to the topic
        client.publish(TOPIC, payload)
        print(f"⬆️ Sent: {payload}")

        time.sleep(5) # Send data every 5 seconds

except KeyboardInterrupt:
    print("\n👋 Stopping IoT data publisher.")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    client.loop_stop()  # Stop the MQTT background loop
    client.disconnect() # Disconnect from the broker
