import paho.mqtt.client as mqtt
import json
import os

# --- MQTT Broker Configuration ---
# Since Mosquitto is on your laptop, this script should also run on your laptop.
BROKER_ADDRESS = "localhost" # Assuming this script runs on the same machine as Mosquitto
BROKER_PORT = 1883           # Default MQTT port
TOPIC = "iot/sensor/data"    # The MQTT topic to subscribe to

# --- Logging Configuration ---
LOG_FILE = "iot_data_log.txt"

# --- MQTT Client Callbacks ---
def on_connect(client, userdata, flags, rc):
    """Callback function when the client connects to the MQTT broker."""
    if rc == 0:
        print(f"✅ Connected to MQTT Broker at {BROKER_ADDRESS}:{BROKER_PORT}!")
        client.subscribe(TOPIC) # Subscribe to the topic once connected
        print(f"👂 Subscribed to topic: {TOPIC}")
    else:
        print(f"❌ Failed to connect, return code {rc}\n")

def on_message(client, userdata, msg):
    """Callback function when a message is received from the subscribed topic."""
    try:
        payload = msg.payload.decode() # Decode the byte payload to a string
        # print(f"⬇️ Received: {payload} on topic {msg.topic}")

        # Try to parse as JSON (assuming the sender sends JSON)
        try:
            iot_data = json.loads(payload)
            log_entry = f"{iot_data.get('timestamp', 'N/A')} - Device {iot_data.get('device_id', 'N/A')}: Temp={iot_data.get('temperature', 'N/A')}°C, Hum={iot_data.get('humidity', 'N/A')}%"
        except json.JSONDecodeError:
            log_entry = f"RAW: {payload}" # Log raw if not JSON

        # Append received data to a text file
        with open(LOG_FILE, "a") as f:
            f.write(log_entry + "\n")
        print(f"💾 Logged: {log_entry}")

    except Exception as e:
        print(f"⚠️ Error processing message: {e}")

# --- Setup MQTT Client ---
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Connect to the broker
try:
    client.connect(BROKER_ADDRESS, BROKER_PORT, 60)
except Exception as e:
    print(f"🚨 Error connecting to MQTT broker: {e}")
    exit() # Exit if connection fails

# Start the MQTT client loop
# This is a blocking call that processes network traffic, dispatches callbacks,
# and generally keeps the client running until client.disconnect() is called
# or the program exits.
print(f"Monitoring system starting. Logging data to '{LOG_FILE}'...")
client.loop_forever()

# This part will only be reached if loop_forever() is somehow exited (e.g., forced disconnect)
print("👋 Monitoring system stopped.")
