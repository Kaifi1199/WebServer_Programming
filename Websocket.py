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
    oled.fill(0)  # Clear the display
    
    # Split the message by newline characters
    lines = message.split('\\n')
    
    # Display each line with proper vertical spacing
    # Each character is about 8 pixels high
    for i, line in enumerate(lines):
        y_position = i * 10  # 10 pixels between lines for readability
        oled.text(line, 0, y_position)
    
    oled.show()  # Update the display

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
    print(".", end="")

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
    html = """
<!DOCTYPE html>
<html>
<head>
    <title>ESP32 Web Server</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: Arial, sans-serif;
        }
        
        body {
            background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
            background-size: 400% 400%;
            animation: gradient 15s ease infinite;
            color: white;
            padding: 20px;
            min-height: 100vh;
        }
        
        @keyframes gradient {
            0% {
                background-position: 0% 50%;
            }
            50% {
                background-position: 100% 50%;
            }
            100% {
                background-position: 0% 50%;
            }
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        
        h1 {
            text-align: center;
            margin-bottom: 30px;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
        }
        
        h2 {
            margin-bottom: 15px;
            text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.5);
            text-align: center;
        }
        
        .flex-container {
            display: flex;
            flex-wrap: wrap;
            gap: 20px;
            margin-bottom: 30px;
            justify-content: center;
        }
        
        .control-box {
            flex: 1;
            min-width: 300px;
            background-color: rgba(0, 0, 0, 0.5);
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
            position: relative;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        
        .control-box::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: linear-gradient(45deg, transparent, rgba(255, 255, 255, 0.1), transparent);
            transform: rotate(45deg);
            animation: shine 3s infinite;
            z-index: 0;
        }
        
        @keyframes shine {
            0% { left: -100%; }
            100% { left: 100%; }
        }
        
        .control-content {
            position: relative;
            z-index: 1;
            width: 100%;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        
        .button-group {
            display: flex;
            justify-content: center;
            margin-top: 10px;
            width: 100%;
        }
        
        .button {
            display: inline-block;
            padding: 10px 15px;
            margin: 5px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-weight: bold;
            transition: all 0.3s ease;
            color: white;
            background-color: #333;
            text-align: center;
        }
        
        .button:hover {
            transform: translateY(-3px);
            box-shadow: 0 6px 10px rgba(0, 0, 0, 0.3);
        }
        
        .red { background-color: #e74c3c; }
        .green { background-color: #2ecc71; }
        .blue { background-color: #3498db; }
        
        input[type="number"], input[type="text"] {
            padding: 8px;
            margin: 5px;
            border: none;
            border-radius: 4px;
            background-color: rgba(255, 255, 255, 0.9);
        }
        
        input[type="submit"] {
            background-color: #9b59b6;
            margin-top: 10px;
        }
        
        #sensorData {
            text-align: center;
            padding: 20px;
            background-color: rgba(0, 0, 0, 0.5);
            border-radius: 10px;
            margin: 0 auto;
            max-width: 500px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
        }
        
        #sensorData h3 {
            margin: 10px 0;
        }
        
        form {
            margin-top: 15px;
            width: 100%;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        
        .rgb-controls {
            display: flex;
            justify-content: center;
            margin-bottom: 10px;
            width: 100%;
        }
        
        .rgb-input {
            display: flex;
            align-items: center;
            margin: 0 5px;
        }
        
        label {
            margin-right: 5px;
            display: inline-block;
            min-width: 25px;
        }
        
        .oled-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            width: 100%;
        }
        
        /* Responsive adjustments */
        @media (max-width: 768px) {
            .flex-container {
                flex-direction: column;
            }
            
            .control-box {
                min-width: 100%;
            }
            
            .rgb-controls {
                flex-direction: column;
                align-items: center;
            }
            
            .rgb-input {
                margin: 5px 0;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>ESP32 Control Panel</h1>
        
        <div class="flex-container">
            <!-- RGB LED Control -->
            <div class="control-box">
                <div class="control-content">
                    <h2>RGB LED Control</h2>
                    <div class="button-group">
                        <a href="/red"><button class="button red">RED</button></a>
                        <a href="/green"><button class="button green">GREEN</button></a>
                        <a href="/blue"><button class="button blue">BLUE</button></a>
                    </div>
                </div>
            </div>
            
            <!-- Custom RGB Color -->
            <div class="control-box">
                <div class="control-content">
                    <h2>Custom RGB Color</h2>
                    <form action="/custom-rgb" method="POST">
                        <div class="rgb-controls">
                            <div class="rgb-input">
                                <label for="r">R:</label>
                                <input type="number" id="r" name="r" min="0" max="255" value="0">
                            </div>
                            
                            <div class="rgb-input">
                                <label for="g">G:</label>
                                <input type="number" id="g" name="g" min="0" max="255" value="0">
                            </div>
                            
                            <div class="rgb-input">
                                <label for="b">B:</label>
                                <input type="number" id="b" name="b" min="0" max="255" value="0">
                            </div>
                        </div>
                        <input type="submit" value="Set LED Color" class="button">
                    </form>
                </div>
            </div>
            
            <!-- OLED Display -->
            <div class="control-box">
                <div class="control-content">
                    <h2>OLED Display</h2>
                    <form action="/text" method="POST" class="oled-container">
                        <input type="text" name="message" maxlength="20" placeholder="Text for OLED">
                        <input type="submit" value="Display" class="button">
                    </form>
                </div>
            </div>
        </div>
        
        <!-- Sensor Data -->
        <div id="sensorData">
            <h2>Sensor Data</h2>
            <h3>Temperature: <span id="temp">Reading...</span>&#8451;</h3>
            <h3>Humidity: <span id="humidity">Reading...</span>%</h3>
        </div>
    </div>
    
    <!-- JavaScript for Live Updates -->
    <script>
        // Function to update sensor data
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
            
            // Schedule the next update
            setTimeout(updateSensorData, 2000); // Update every 2 seconds
        }
        
        // Start updating when page loads
        window.onload = function() {
            updateSensorData();
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

while True:
    conn, addr = s.accept()
    print("Connection from:", addr)
    
    try:
        request = conn.recv(1024).decode()
        print("Request:", request)
        
        # Handle sensor data endpoint for AJAX requests
        if "GET /sensor-data" in request:
            temp, humidity = dht_measure()
            if temp is None:
                temp = "N/A"
            if humidity is None:
                humidity = "N/A"
            
            # Create JSON response
            sensor_data = {"temp": temp, "humidity": humidity}
            json_response = json.dumps(sensor_data)
            
            # Send JSON response
            conn.send("HTTP/1.1 200 OK\nContent-Type: application/json\nConnection: close\n\n".encode())
            conn.send(json_response.encode())
        
        # Handle LED color control using direct paths
        elif "GET /red" in request:
            neo[0] = (255, 0, 0)  # Set NeoPixel to red
            neo.write()
            # Redirect back to the main page
            conn.send("HTTP/1.1 303 See Other\nLocation: /\n\n".encode())
        
        elif "GET /green" in request:
            neo[0] = (0, 255, 0)  # Set NeoPixel to green
            neo.write()
            # Redirect back to the main page
            conn.send("HTTP/1.1 303 See Other\nLocation: /\n\n".encode())
        
        elif "GET /blue" in request:
            neo[0] = (0, 0, 255)  # Set NeoPixel to blue
            neo.write()
            # Redirect back to the main page
            conn.send("HTTP/1.1 303 See Other\nLocation: /\n\n".encode())
        
        # Handle custom RGB color using POST method
        elif "POST /custom-rgb" in request:
            # Find the form data in the request
            form_data_pos = request.find("\r\n\r\n") + 4
            if form_data_pos < len(request):
                form_data = request[form_data_pos:]
                
                # Extract RGB values with basic parsing
                r_val = 0
                g_val = 0
                b_val = 0
                
                if "r=" in form_data:
                    r_str = form_data.split("r=")[1].split("&")[0]
                    try:
                        r_val = int(r_str)
                        r_val = max(0, min(255, r_val))  # Clamp to 0-255
                    except:
                        pass
                        
                if "g=" in form_data:
                    g_str = form_data.split("g=")[1].split("&")[0]
                    try:
                        g_val = int(g_str)
                        g_val = max(0, min(255, g_val))  # Clamp to 0-255
                    except:
                        pass
                        
                if "b=" in form_data:
                    b_str = form_data.split("b=")[1].split("&")[0]
                    try:
                        b_val = int(b_str)
                        b_val = max(0, min(255, b_val))  # Clamp to 0-255
                    except:
                        pass
                
                # Set the NeoPixel color
                neo[0] = (r_val, g_val, b_val)
                neo.write()
                print(f"LED set to RGB: {r_val}, {g_val}, {b_val}")
            
            # Redirect back to the main page
            conn.send("HTTP/1.1 303 See Other\nLocation: /\n\n".encode())
        
        # Handle OLED text using POST method
        elif "POST /text" in request:
            # Find the form data in the request
            form_data_pos = request.find("\r\n\r\n") + 4
            if form_data_pos < len(request):
                form_data = request[form_data_pos:]
                
                # Extract the message
                if "message=" in form_data:
                    message = form_data.split("message=")[1].split("&")[0]
                    # Simple URL decoding (replace + with space and %0A with \n)
                    message = message.replace("+", " ")
                    message = message.replace("%0A", "\\n")  # Handle URL-encoded newlines
                    
                    print("Message to OLED:", message)
                    update_oled(message)
            
            # Redirect back to the main page
            conn.send("HTTP/1.1 303 See Other\nLocation: /\n\n".encode())
        
        # Default: serve the main page
        else:
            response = web_page()
            conn.send("HTTP/1.1 200 OK\nContent-Type: text/html\nConnection: close\n\n".encode())
            conn.send(response.encode())
    
    except Exception as e:
        print("Error handling request:", e)
    
    finally:
        conn.close()