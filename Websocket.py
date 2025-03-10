print("Hello, ESP32-S3!")

import network
import time
import socket
import dht
import machine
import ssd1306
from machine import Pin, I2C
from neopixel import NeoPixel

# Initialize DHT11 Sensor
DHT_PIN = 4
dht_sensor = dht.DHT11(machine.Pin(DHT_PIN))

def dht_measure():
    dht_sensor.measure()
    time.sleep(0.2)
    temp = dht_sensor.temperature()
    humidity = dht_sensor.humidity()
    return temp, humidity

# Initialize NeoPixel LED
neo = NeoPixel(Pin(48, Pin.OUT), 1)

# Initialize OLED Display (I2C)
i2c = I2C(0, scl=Pin(9), sda=Pin(8))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

def update_oled(message):
    oled.fill(0)
    oled.text(message, 0, 0)  # Display message at the top
    oled.show()

# WiFi Station Credentials
ssid_st = "HackerMan"
password_st = "HackerMan1100"

print("Connecting to WiFi", end="")
sta = network.WLAN(network.STA_IF)
sta.active(True)
sta.connect(ssid_st, password_st)

# Wait for connection
for _ in range(10):
    if sta.isconnected():
        break
    time.sleep(1)

if sta.isconnected():
    print("Connected to WiFi!")
    print("IP Address as station:", sta.ifconfig()[0])
else:
    print("Failed to connect")

# Create Access Point
ssid_ap = "ESP32_AP"
password_ap = "12345678"
ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid=ssid_ap, password=password_ap, authmode=network.AUTH_WPA2_PSK)

print("Access Point Active")
print("AP IP Address:", ap.ifconfig()[0])

# Web Server Function
def web_page():
    temp, humidity = dht_measure()
    html = f"""<!DOCTYPE html>
    <html>
    <head><title>ESP32 Web Server</title></head>
    <body>
    <h1>ESP32 RGB LED Control</h1>
    <p><a href="/?RGB=red"><button>Turn RGB RED</button></a></p>
    <p><a href="/?RGB=green"><button>Turn RGB GREEN</button></a></p>
    <p><a href="/?RGB=blue"><button>Turn RGB BLUE</button></a></p>
    <br>
    <h1>Temperature and Humidity</h1>
    <h2>Temp: {temp} &#8451;</h2>
    <h2>Humidity: {humidity}%</h2>
    <br>
    <h2>OLED Text Display</h2>
    <form action="/" method="GET">
        <input type="text" name="message" placeholder="Enter text">
        <input type="submit" value="Display on OLED">
    </form>
    </body>
    </html>"""
    return html

# Start Web Server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("0.0.0.0", 80))
s.listen(5)

while True:
    conn, addr = s.accept()
    print("Connection from:", addr)
    request = conn.recv(1024).decode()
    print("Request:", request)
    
    if "/?RGB=red" in request:
        neo[0] = (255, 0, 0)  # Set NeoPixel to red
        neo.write()
    elif "/?RGB=green" in request:
        neo[0] = (0, 255, 0)  # Set NeoPixel to green
        neo.write()
    elif "/?RGB=blue" in request:
        neo[0] = (0, 0, 255)  # Set NeoPixel to blue
        neo.write()
    
    # Extract message from URL
    if "?message=" in request:
        msg_start = request.find("?message=") + 9
        msg_end = request.find(" ", msg_start)
        message = request[msg_start:msg_end] if msg_end != -1 else request[msg_start:]
        message = message.replace("+", " ")  # Replace '+' with spaces
        message = message[:20]  # Limit to 20 characters
        print("Message to OLED:", message)
        oled.fill(0)
        oled.text(message, 0, 0)  # Display at the top instead of center
        oled.show()
    
    response = web_page()
    conn.send("HTTP/1.1 200 OK\nContent-Type: text/html\n\n".encode())
    conn.send(response.encode())
    conn.close()