from machine import Pin
import time
import wifi  
from umqtt.simple import MQTTClient

# === Configuración de WiFi ===
wifi.conectar()  

# === Configuración MQTT ===
MQTT_BROKER = "192.168.166.46"  # IP de la Raspberry Pi con Mosquitto
MQTT_PORT = 1883
MQTT_CLIENT_ID = "esp32_led_client"
MQTT_TOPIC_LED = b"micro/led/control"  

# === Configuración del pin del LED ===
led = Pin(15, Pin.OUT)  

# === Función de callback para manejar mensajes MQTT ===
def control_led_callback(topic, msg):
    print(f"Mensaje recibido en {topic}: {msg}")
    if msg == b"ON":
        led.value(1)
        print("💡 LED ENCENDIDO")
    elif msg == b"OFF":
        led.value(0)
        print("💡 LED APAGADO")
    else:
        print("Mensaje no reconocido")

# === Conectar al broker MQTT ===
client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, port=MQTT_PORT)
client.set_callback(control_led_callback)
client.connect()
client.subscribe(MQTT_TOPIC_LED)

print("Conectado al broker MQTT y suscrito al topic de control del LED")

# === Bucle principal ===
while True:
    client.check_msg()
    time.sleep(0.1)  