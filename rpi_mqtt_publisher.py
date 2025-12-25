import paho.mqtt.client as mqtt
import time
import random
import json

device_id = 1
# --- MQTT Broker Configuration ---
# If Mosquitto is on your laptop, and this script runs on a Raspberry Pi,
# replace 'localhost' with your laptop's IP address (e.g., '192.168.1.100')
BROKER_ADDRESS = "192.168.3.101" # Or your laptop's IP if running on RPi
BROKER_PORT = 1883           # Default MQTT port
# TOPIC = "iot/sensor/data"    # The MQTT topic to publish data to
data_to_send = [
    ("current_output", "client_id/region_iii/district_i/water_wood/pump_station/current_output"),
    ("water_level", "client_id/region_iii/district_i/water_wood/pump_station/water_level")
]
# --- MQTT Client Callbacks ---
def on_connect(client, userdata, flags, rc,a):
    """Callback function when the client connects to the MQTT broker."""
    if rc == 0:
        print(f"✅ Connected to MQTT Broker at {BROKER_ADDRESS}:{BROKER_PORT}!")
    else:
        print(f"❌ Failed to connect, return code {rc}\n")

def on_publish(client, userdata, mid, response_code,properties):
    # print(type(client), end='')
    # print(client)
    # print(type(userdata), end='')
    # print(userdata)
    # print(type(mid), end='')
    # print(mid)
    # print(type(response_code), end='')
    # print(response_code)
    # print(type(properties), end='')
    # print(properties)
    
    """Callback function when a message is successfully published."""
    # print(f"Published message ID: {mid}")
    pass # No need to print for every message for simplicity

# --- Setup MQTT Client ---
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, "client_001")

client.username_pw_set("rpi", "Dynamic2024")
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
        
        for sensor_type, topic in data_to_send:
            # Generate some dummy IoT data
            data = None
            unit = None
            if (sensor_type == 'current_output'):
                data = round(random.uniform(0.1, 0.2), 4) # Amphere 0.1 - 0.2
                unit = "A"
            elif (sensor_type == 'water_level'):
                data = round(random.uniform(10, 20), 2) # Water Level 10 - 20 meter
                unit = "meter"
            if (data is None):
                continue
             
            iot_data =  {
                "id": 1,
                "sensor_type": sensor_type,
                "value": data,
                "unit": unit,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "device_id":device_id
            }
            
            # iot_data[sensor_type] = data
            # Convert dictionary to a JSON string for publishing
            payload = json.dumps(iot_data)

            # Publish the data to the topic
            client.publish(topic, payload)
            print(f"TOPIC:{topic}\n⬆️ Sent: {payload}")

        time.sleep(5) # Send data every 5 seconds

except KeyboardInterrupt:
    print("\n👋 Stopping IoT data publisher.")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    client.loop_stop()  # Stop the MQTT background loop
    client.disconnect() # Disconnect from the broker
