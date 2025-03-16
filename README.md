# --Task-1--

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

# --Task-2--

# MorseGlow

MorseGlow is an interactive ESP32-based project that converts text messages into Morse code and displays them through an RGB LED and OLED display. This project combines WiFi connectivity, web interface control, and visual output to create an engaging way to learn and visualize Morse code.

## Features

- **WiFi Connectivity:** Connects to your local network and creates an access point
- **Web Interface:** Sleek, responsive web interface for entering messages
- **Morse Code Conversion:** Translates text to Morse code
- **Visual Output:** Displays Morse code through:
  - RGB LED (red for dots, blue for dashes)
  - OLED display showing both text and Morse code
- **Timing:** Properly timed Morse code signals (dots, dashes, and spaces)

## Hardware Requirements

- ESP32 development board
- SSD1306 OLED display (128x64 pixels)
- WS2812B RGB LED (NeoPixel compatible)
- Breadboard and jumper wires

## Setup Instructions

1. Install MicroPython on your ESP32 board
2. Upload the MorseGlow code to your ESP32
3. Update the WiFi credentials in the code:
   ```python
   sta.connect("YOUR_WIFI_SSID", "YOUR_WIFI_PASSWORD")
   ```
4. Modify the access point settings if needed:
   ```python
   ap.config(essid="ESP32_K", password="12345678", authmode=network.AUTH_WPA2_PSK)
   ```
5. Connect the OLED display and NeoPixel LED according to the pin connection chart
6. Power up the ESP32

## Usage

1. Connect to the ESP32's WiFi access point (default: ESP32_K, password: 12345678)
2. Open a web browser and navigate to the ESP32's IP address (displayed on the serial monitor)
3. Enter your message (up to 20 characters) in the web interface
4. Click "Transmit" to convert the text to Morse code
5. Watch as the RGB LED blinks the Morse code pattern:
   - Red light for dots (0.5 second)
   - Blue light for dashes (2 seconds)
   - Short pauses between elements and letters
6. The OLED display will show both your message and its Morse code representation

## Morse Code Timing

MorseGlow uses the following timing for Morse code signals:
- Dot: 0.5 seconds (red light)
- Dash: 2 seconds (blue light)
- Gap between elements: 0.2 seconds
- Gap between letters: 0.5 seconds

## Educational Value

This project serves as an engaging way to learn Morse code by providing visual feedback. It can be used as:
- An educational tool for teaching Morse code
- A fun way to send visual messages
- A starting point for more advanced communication projects

## Customization

You can extend this project by:
- Adding sound output for audible Morse code
- Implementing different color schemes for the LED
- Creating a message history feature
- Adding support for special characters
- Implementing different timing options for beginners and advanced users

## Acknowledgments

- MicroPython community
- The developers of the SSD1306 and NeoPixel libraries
- The global Morse code community for preserving this historic communication method
