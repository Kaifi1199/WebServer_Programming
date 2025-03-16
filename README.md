# Task-1

# Web Server

A comprehensive IoT control panel running on an ESP32 microcontroller with MicroPython. This project creates a web interface to control an RGB LED, display text on an OLED screen, and monitor temperature and humidity data from a DHT11 sensor.

## Features

- **WiFi Connectivity**: Connects to your local WiFi network and creates its own access point
- **Web Interface**: Responsive web server with intuitive controls
- **RGB LED Control**: Control an RGB LED with preset colors or custom RGB values
- **OLED Display**: Send custom text messages to an OLED display
- **Temperature & Humidity Monitoring**: Real-time sensor data from a DHT11 sensor
- **Auto-updating UI**: Sensor data refreshes automatically every 2 seconds

## Hardware Requirements

- ESP32 development board
- DHT11 temperature and humidity sensor
- SSD1306 OLED display (128x64 pixels)
- WS2812B RGB LED (NeoPixel compatible)
- Jumper wires and breadboard

## Setup Instructions

1. Install MicroPython on your ESP32 board
2. Upload the main.py file to your ESP32
3. Modify the WiFi credentials in the code:
   ```python
   sta.connect("YOUR_WIFI_SSID", "YOUR_WIFI_PASSWORD")
   ```
4. Adjust the access point settings if needed:
   ```python
   ap.config(essid="ESP32_K", password="12345678", authmode=network.AUTH_WPA2_PSK)
   ```
5. Connect all components according to the pin connections chart
6. Power up the ESP32 and watch the console for connection information

## Usage

1. Connect to the ESP32's WiFi access point (default: ESP32_K, password: 12345678)
2. Open a web browser and navigate to the IP address shown on the OLED display or in the console output
3. Use the web interface to:
   - Control the RGB LED with preset colors or custom RGB values
   - Send text messages to the OLED display
   - Monitor temperature and humidity data

## Web Interface

The web interface includes:

- RGB LED control buttons for preset colors (Red, Green, Blue)
- Custom RGB color input fields
- Text input for OLED display
- Real-time temperature and humidity readings

## Customization

You can customize the code to add more features:
- Add more sensors by modifying the `dht_measure()` function
- Extend the web interface with additional controls
- Implement IoT cloud connectivity
- Add data logging capabilities

## Acknowledgments

- MicroPython community
- ESP32 developer community
- Contributors to the SSD1306 and NeoPixel libraries
