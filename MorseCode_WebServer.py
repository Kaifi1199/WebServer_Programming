import network
import socket
import machine
import ssd1306
import time
import neopixel

# WiFi Configuration
SSID = "HackerMan"
PASSWORD = "HackerMan1100"

sta = network.WLAN(network.STA_IF)
sta.active(True)
sta.connect(SSID, PASSWORD)

while not sta.isconnected():
    time.sleep(1)
print("Connected! Station IP:", sta.ifconfig()[0])

ssid_ap = "ESP32_K"
password_ap = "12345678"
auth_mode = network.AUTH_WPA2_PSK

ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid=ssid_ap, password=password_ap, authmode=auth_mode)
print("Access Point Active, IP:", ap.ifconfig()[0])

# OLED Setup
i2c = machine.SoftI2C(scl=machine.Pin(9), sda=machine.Pin(8))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# Neopixel
np = neopixel.NeoPixel(machine.Pin(48), 1)
np[0] = (0, 0, 0)
np.write()



# Initialize socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((sta.ifconfig()[0], 80))
s.listen(5)

oled_message = "Waiting..."
last_morse = ""  # Variable to store the last Morse code

while True:
    conn, addr = s.accept()
    print('Got connection from', addr)
    request = conn.recv(1024).decode()
    print("Request Received:\n", request)

    if "favicon.ico" in request:
        conn.close()
        continue

    # Default message
    message = oled_message
    morse_output = ""

    # Handle POST request (form submission)
    if "POST /" in request:
        try:
            # Extract the body of the POST request
            body = request.split('\r\n\r\n')[1]
            pairs = body.split('&')
            for pair in pairs:
                key, value = pair.split('=')
                if key == 'msg' and value:  # Only process if msg has a value
                    message = value.replace('+', ' ')[:20]
                    morse_output = text_to_morse(message)
                    oled_message = message
                    last_morse = morse_output  # Update the last Morse code

            # Redirect to the same page after processing the POST request
            conn.send('HTTP/1.1 303 See Other\r\nLocation: /\r\n\r\n')
            conn.close()
            continue
        except Exception as e:
            print("Error parsing request:", e)

    # Send the web page response
    response = webpage(last_morse)  # Pass the last Morse code to the webpage
    conn.send('HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n')
    conn.send(response)
    conn.close()