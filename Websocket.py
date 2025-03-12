import network
import time
import socket
import dht
import machine
import ssd1306
import json
from machine import Pin, I2C
from neopixel import NeoPixel

# Initialize DHT11 Sensor
dht_sensor = dht.DHT11(Pin(4))

def dht_measure():
    try:
        dht_sensor.measure()
        return dht_sensor.temperature(), dht_sensor.humidity()
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
    lines = message.split('\\n')
    for i, line in enumerate(lines):
        oled.text(line, 0, i * 10)
    oled.show()

# WiFi Station Setup
sta = network.WLAN(network.STA_IF)
sta.active(True)
sta.connect("HackerMan", "HackerMan1100")

for _ in range(10):
    if sta.isconnected():
        print("Connected to WiFi!\nIP Address:", sta.ifconfig()[0])
        break
    time.sleep(1)
else:
    raise Exception("WiFi connection failed")

# Access Point Setup
ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid="ESP32_K", password="12345678", authmode=network.AUTH_WPA2_PSK)
print("Access Point Active\nAP IP Address:", ap.ifconfig()[0])

# Web Server Function
def web_page():
    html = """
<!DOCTYPE html>
<html>
<head>
    <title>ESP32 Web Server</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {
            background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
            background-size: 400% 400%;
            animation: gradient 15s ease infinite;
            color: white;
            padding: 20px;
            font-family: Arial, sans-serif;
        }
        @keyframes gradient {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        h1, h2 { text-align: center; margin-bottom: 20px; }
        .flex-container {
            display: flex;
            flex-wrap: wrap;
            gap: 20px;
            justify-content: center;
        }
        .control-box {
            flex: 1;
            min-width: 300px;
            background-color: rgba(0, 0, 0, 0.5);
            border-radius: 10px;
            padding: 20px;
            text-align: center;
        }
        .button-group { display: flex; justify-content: center; margin-top: 10px; }
        .button {
            padding: 10px 15px;
            margin: 5px;
            border-radius: 5px;
            color: white;
            background-color: #333;
            text-decoration: none;
            transition: all 0.3s ease;
            display: inline-block;
        }
        .button:hover {
            transform: scale(1.1);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
            cursor: pointer;
        }
        .red { background-color: #e74c3c; }
        .green { background-color: #2ecc71; }
        .blue { background-color: #3498db; }
        .submit-btn { background-color: #9b59b6; }
        .submit-btn:hover {
            transform: scale(1.1);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
        }
        input[type="number"], input[type="text"] {
            padding: 8px;
            margin: 5px;
            border-radius: 4px;
        }
        input[type="submit"] {
            padding: 10px 15px;
            border: none;
            border-radius: 5px;
        }
        #sensorData {
            text-align: center;
            padding: 20px;
            background-color: rgba(0, 0, 0, 0.5);
            border-radius: 10px;
            max-width: 500px;
            margin: 20px auto;
        }
        form { display: flex; flex-direction: column; align-items: center; }
        .rgb-controls { display: flex; justify-content: center; }
        .rgb-input { margin: 0 5px; }
        @media (max-width: 768px) {
            .flex-container { flex-direction: column; }
            .control-box { min-width: 100%; }
            .rgb-controls { flex-direction: column; }
        }
    </style>
</head>
<body>
    <h1>ESP32 Control Panel</h1>
    <div class="flex-container">
        <div class="control-box">
            <h2>RGB LED Control</h2>
            <div class="button-group">
                <a href="/red" class="button red">RED</a>
                <a href="/green" class="button green">GREEN</a>
                <a href="/blue" class="button blue">BLUE</a>
            </div>
        </div>
        <div class="control-box">
            <h2>Custom RGB Color</h2>
            <form action="/custom-rgb" method="POST">
                <div class="rgb-controls">
                    <div class="rgb-input">
                        <label>R:</label>
                        <input type="number" name="r" min="0" max="255" value="0">
                    </div>
                    <div class="rgb-input">
                        <label>G:</label>
                        <input type="number" name="g" min="0" max="255" value="0">
                    </div>
                    <div class="rgb-input">
                        <label>B:</label>
                        <input type="number" name="b" min="0" max="255" value="0">
                    </div>
                </div>
                <input type="submit" value="Set LED Color" class="button submit-btn">
            </form>
        </div>
        <div class="control-box">
            <h2>OLED Display</h2>
            <form action="/text" method="POST">
                <input type="text" name="message" maxlength="20" placeholder="Text for OLED">
                <input type="submit" value="Display" class="button submit-btn">
            </form>
        </div>
    </div>
    <div id="sensorData">
        <h2>Sensor Data</h2>
        <h3>Temperature: <span id="temp">Reading...</span>&#8451;</h3>
        <h3>Humidity: <span id="humidity">Reading...</span>%</h3>
    </div>
    <script>
        function updateSensorData() {
            var xhr = new XMLHttpRequest();
            xhr.open('GET', '/sensor-data', true);
            xhr.onreadystatechange = function() {
                if (xhr.readyState == 4 && xhr.status == 200) {
                    var data = JSON.parse(xhr.responseText);
                    document.getElementById('temp').textContent = data.temp;
                    document.getElementById('humidity').textContent = data.humidity;
                }
            };
            xhr.send();
            setTimeout(updateSensorData, 2000);
        }
        window.onload = updateSensorData;
    </script>
</body>
</html>"""
    return html

# Socket Setup
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((sta.ifconfig()[0], 80))
s.listen(5)
print("Socket bound to port 80")

while True:
    conn, addr = s.accept()
    print("Connection from:", addr)
    request = conn.recv(1024).decode()

    if "GET /sensor-data" in request:
        temp, humidity = dht_measure()
        sensor_data = {"temp": temp if temp is not None else "N/A", "humidity": humidity if humidity is not None else "N/A"}
        conn.send("HTTP/1.1 200 OK\nContent-Type: application/json\nConnection: close\n\n".encode())
        conn.send(json.dumps(sensor_data).encode())

    elif "GET /red" in request:
        neo[0] = (255, 0, 0)
        neo.write()
        conn.send("HTTP/1.1 303 See Other\nLocation: /\n\n".encode())

    elif "GET /green" in request:
        neo[0] = (0, 255, 0)
        neo.write()
        conn.send("HTTP/1.1 303 See Other\nLocation: /\n\n".encode())

    elif "GET /blue" in request:
        neo[0] = (0, 0, 255)
        neo.write()
        conn.send("HTTP/1.1 303 See Other\nLocation: /\n\n".encode())

    elif "POST /custom-rgb" in request:
        form_data = request.split("\r\n\r\n")[1]
        r_val = g_val = b_val = 0
        for param in form_data.split("&"):
            key, val = param.split("=")
            if key == "r": r_val = max(0, min(255, int(val)))
            elif key == "g": g_val = max(0, min(255, int(val)))
            elif key == "b": b_val = max(0, min(255, int(val)))
        neo[0] = (r_val, g_val, b_val)
        neo.write()
        conn.send("HTTP/1.1 303 See Other\nLocation: /\n\n".encode())

    elif "POST /text" in request:
        form_data = request.split("\r\n\r\n")[1]
        message = form_data.split("message=")[1].split("&")[0].replace("+", " ").replace("%0A", "\\n")
        update_oled(message)
        conn.send("HTTP/1.1 303 See Other\nLocation: /\n\n".encode())

    else:
        conn.send("HTTP/1.1 200 OK\nContent-Type: text/html\nConnection: close\n\n".encode())
        conn.send(web_page().encode())

    conn.close()