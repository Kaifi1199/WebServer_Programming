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
    try:
        dht_sensor.measure()
        temp = dht_sensor.temperature()
        humidity = dht_sensor.humidity()
        return temp, humidity
    except Exception as e:
        print("Failed to read DHT11:", e)
        return None, None

# Initialize NeoPixel LED
neo = NeoPixel(Pin(48, Pin.OUT), 1)

# Initialize OLED Display (I2C)
i2c = I2C(0, scl=Pin(9), sda=Pin(8))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

def update_oled(message):
    oled.fill(0)
    oled.text(message, 0, 0)
    oled.show()

# WiFi Station Credentials
ssid_st = "HackerMan"
password_st = "HackerMan1100"

print("Connecting to WiFi", end="")
sta = network.WLAN(network.STA_IF)
sta.active(True)
sta.connect("HackerMan", "HackerMan1100")

for _ in range(10):
    if sta.isconnected():
        break
    time.sleep(1)

if sta.isconnected():
    print("\nConnected to WiFi!")
    print("IP Address:", sta.ifconfig()[0])
else:
    print("\nFailed to connect")
    raise Exception("WiFi connection failed")

# Access Point Setup
ssid_ap = "ESP32_AP"
password_ap = "12345678"
ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid=ssid_ap, password=password_ap, authmode=network.AUTH_WPA2_PSK)

print("Access Point Active")
print("AP IP Address:", ap.ifconfig()[0])

# Web Server Function
def web_page():
    html = """<!DOCTYPE html>
    <html>
    <head><title>ESP32 Web Server</title></head>
    <body>
    <h1>ESP32 RGB LED Control</h1>
    <p><a href="/?RGB=red"><button>RED</button></a></p>
    <p><a href="/?RGB=green"><button>GREEN</button></a></p>
    <p><a href="/?RGB=blue"><button>BLUE</button></a></p>
    <h1>Temperature: <span id="temp">N/A</span>°C</h1>
    <h1>Humidity: <span id="humidity">N/A</span>%</h1>
    <form action="/" method="GET">
        <input type="text" name="message" maxlength="20" placeholder="Text for OLED">
        <input type="submit" value="Display">
    </form>
    <script>
        // JavaScript to handle Server-Sent Events (SSE)
        const eventSource = new EventSource("/events");
        eventSource.onmessage = function(event) {
            const data = JSON.parse(event.data);
            document.getElementById("temp").textContent = data.temp;
            document.getElementById("humidity").textContent = data.humidity;
        };
    </script>
    </body>
    </html>"""
    return html

# Create and bind socket only after WiFi is connected
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("0.0.0.0", 80))
s.listen(5)
print("Socket bound to port 80")

def send_event(conn, temp, humidity):
    try:
        # Send Server-Sent Event (SSE) to the client
        event = f"data: {{\"temp\": {temp}, \"humidity\": {humidity}}}\n\n"
        conn.send(event.encode())
    except OSError as e:
        print("Client disconnected:", e)
        raise  # Stop sending events if the client disconnects

while True:
    conn, addr = s.accept()
    print("Connection from:", addr)
    request = conn.recv(1024).decode()
    print("Request:", request)
    
    # Handle SSE requests
    if "GET /events" in request:
        print("SSE connection established")
        conn.send("HTTP/1.1 200 OK\nContent-Type: text/event-stream\n\n".encode())
        try:
            while True:
                temp, humidity = dht_measure()
                if temp is not None and humidity is not None:
                    send_event(conn, temp, humidity)
                time.sleep(1)  # Update every 1 second
        except OSError:
            print("SSE connection closed")
        finally:
            conn.close()
    
    # Handle regular HTTP requests
    elif "GET /" in request:
        # Check for RGB control
        if "/?RGB=red" in request:
            neo[0] = (255, 0, 0)  # Set NeoPixel to red
            neo.write()
        elif "/?RGB=green" in request:
            neo[0] = (0, 255, 0)  # Set NeoPixel to green
            neo.write()
        elif "/?RGB=blue" in request:
            neo[0] = (0, 0, 255)  # Set NeoPixel to blue
            neo.write()
        
        # Check for OLED message
        if "?message=" in request:
            # Extract the message from the request
            msg_start = request.find("?message=") + 9  # Start of the message
            msg_end = request.find("&", msg_start)  # Look for the next parameter (if any)
            if msg_end == -1:
                msg_end = request.find(" HTTP/", msg_start)  # If no next parameter, look for the end of the request
            if msg_end == -1:
                msg_end = len(request)  # If " HTTP/" is not found, use the end of the string
            message = request[msg_start:msg_end]
            message = message.replace("+", " ")  # Replace '+' with spaces
            message = message[:20]  # Limit to 20 characters
            print("Message to OLED:", message)
            oled.fill(0)
            oled.text(message, 0, 0)  # Display at the top
            oled.show()
        
        # Send the web page
        response = web_page()
        conn.send("HTTP/1.1 200 OK\nContent-Type: text/html\n\n".encode())
        conn.send(response.encode())
        conn.close()