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

MORSE_CODE = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
    'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
    'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
    'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
    'Y': '-.--', 'Z': '--..', '0': '-----', '1': '.----', '2': '..---',
    '3': '...--', '4': '....-', '5': '.....', '6': '-....', '7': '--...',
    '8': '---..', '9': '----.', ' ': ' '
}

def blink_neopixel(morse):
    for symbol in morse.strip():
        if symbol == '.':
            np[0] = (255, 0, 0)  # Red for dot
            np.write()
            time.sleep(0.5)      # Dot: 0.5 sec
            np[0] = (0, 0, 0)   # Off
            np.write()
            time.sleep(0.2)      # Gap
        elif symbol == '-':
            np[0] = (0, 0, 255)  # Blue for dash
            np.write()
            time.sleep(2)        # Dash: 2 sec
            np[0] = (0, 0, 0)   # Off
            np.write()
            time.sleep(0.2)      # Gap
        elif symbol == ' ':
            time.sleep(0.5)      # Space between words
    print("Neopixel sequence complete")

def text_to_morse(text):
    oled.fill(0)  # Clear OLED
    oled.text("MorseGlow", 0, 0)
    morse = ""
    for char in text.upper():
        if char in MORSE_CODE:
            morse += MORSE_CODE[char] + " "
    # Display text and morse code on OLED
    oled.text(text[:16], 0, 20)
    oled.text(morse[:16], 0, 40)
    oled.show()
    print("OLED Updated - Text:", text, "Morse:", morse)
    blink_neopixel(morse)
    return morse.strip()

def webpage(last_morse=""):
    html = """<!DOCTYPE html>
<html>
<head>
    <title>MorseGlow Transmitter</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1e3c72, #2a5298);
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            color: #fff;
            overflow: hidden;
        }
        .container {
            background: rgba(255, 255, 255, 0.1);
            padding: 30px;
            border-radius: 15px;
            width: 400px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            text-align: center;
            position: relative;
            z-index: 1;
        }
        .container::before {
            content: '';
            position: absolute;
            top: -10px;
            left: -10px;
            right: -10px;
            bottom: -10px;
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.2), rgba(255, 255, 255, 0.05));
            border-radius: 25px;
            z-index: -1;
            filter: blur(20px);
            animation: glow 3s infinite alternate;
        }
        @keyframes glow {
            0% {
                box-shadow: 0 0 20px rgba(255, 255, 255, 0.2);
            }
            100% {
                box-shadow: 0 0 40px rgba(255, 255, 255, 0.4);
            }
        }
        h1 {
            font-size: 2.5rem;
            margin-bottom: 20px;
            color: #fff;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
        }
        .input-box {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
        }
        input[type="text"] {
            flex: 1;
            padding: 12px;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            background: rgba(255, 255, 255, 0.2);
            color: #fff;
            outline: none;
            transition: background 0.3s ease;
        }
        input[type="text"]:focus {
            background: rgba(255, 255, 255, 0.3);
        }
        input[type="text"]::placeholder {
            color: rgba(255, 255, 255, 0.7);
        }
        button {
            padding: 12px 24px;
            background: #3498db;
            border: none;
            border-radius: 8px;
            color: white;
            font-size: 16px;
            cursor: pointer;
            transition: background 0.3s ease, transform 0.2s ease;
        }
        button:hover {
            background: #2980b9;
            transform: translateY(-2px);
        }
        button:active {
            transform: translateY(0);
        }
        .morse-output {
            background: rgba(255, 255, 255, 0.1);
            padding: 15px;
            border-radius: 8px;
            color: #000000;
            font-family: monospace;
            word-wrap: break-word;
            margin-top: 20px;
            animation: fadeIn 1s ease;
            font-weight: bold;
        }
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
    </style>
</head>
<body onload="document.getElementById('msgInput').value = '';">
    <div class="container">
        <h1>MorseGlow</h1>
        <form action="/" method="POST">
            <div class="input-box">
                <input type="text" id="msgInput" name="msg" placeholder="Enter your message" maxlength="20">
                <button type="submit">Transmit</button>
            </div>
        </form>
        <div class="morse-output">Last Morse Code: """ + last_morse + """</div>
    </div>
</body>
</html>"""
    return html


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