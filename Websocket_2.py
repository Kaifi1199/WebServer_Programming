import network
import time
import socket
from machine import Pin, I2C
import ssd1306
# WiFi Station Configuration
ssid_st = "Abdullah123"
password_st = "Abdullah70"
print("Connecting to WiFi", end="")
sta = network.WLAN(network.STA_IF)
sta.active(True)
sta.connect("Abdullah123", "Abdullah70")
# Wait for connection
for _ in range(10):
    if sta.isconnected():
        break
    time.sleep(1)
    print(".", end="")
if sta.isconnected():
    print("\nConnected to WiFi!")
    print("IP Address as station:", sta.ifconfig()[0])
else:
    print("\nFailed to connect")
# Access Point Configuration
ssid_ap = "ESP32_K"
password_ap = "12345678"  # Minimum 8 characters
auth_mode = network.AUTH_WPA2_PSK  # Secure mode (recommended)
# Create an Access Point
ap = network.WLAN(network.AP_IF)
ap.active(True)  # Activate AP mode
ap.config(essid=ssid_ap, password=password_ap, authmode=auth_mode)  # Set SSID and password
print("Access Point Active")
print("AP IP Address:", ap.ifconfig()[0])
# Initialize OLED Display
i2c = I2C(scl=Pin(9), sda=Pin(8))  # Adjust pins based on your setup
oled = ssd1306.SSD1306_I2C(128, 64, i2c)
def display_on_oled(text):
    oled.fill(0)  # Clear the display
    oled.text(text, 0, 0)  # Display text at (x=0, y=0)
    oled.show()
# Web Page with Beautiful Calculator and CSS
def web_page(result=""):
    html = """<!DOCTYPE html>
    <html>
    <head>
        <title>ESP32 Calculator</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap');
            
            body {
                font-family: 'Roboto', sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                margin: 0;
                padding: 20px;
                color: #333;
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            
            .container {
                max-width: 600px;
                width: 100%;
                background-color: rgba(255, 255, 255, 0.9);
                border-radius: 20px;
                padding: 25px;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
                transition: transform 0.3s ease;
            }
            
            .container:hover {
                transform: translateY(-5px);
            }
            
            h1 {
                color: #4a148c;
                text-align: center;
                margin-bottom: 10px;
                font-weight: 700;
                text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
            }
            
            p {
                text-align: center;
                margin-bottom: 30px;
                color: #666;
                font-size: 16px;
            }
            
            .calculator {
                background: linear-gradient(145deg, #f6f6f6, #e6e6e6);
                border-radius: 15px;
                padding: 20px;
                box-shadow: 0 8px 15px rgba(0, 0, 0, 0.1);
            }
            
            .display {
                background-color: #f8f9fa;
                border: none;
                border-radius: 10px;
                padding: 15px;
                margin-bottom: 20px;
                text-align: right;
                font-size: 28px;
                box-shadow: inset 0 2px 5px rgba(0, 0, 0, 0.1);
                height: 50px;
                overflow: hidden;
                font-weight: 500;
                color: #333;
                transition: all 0.3s ease;
            }
            
            .buttons {
                display: grid;
                grid-template-columns: repeat(4, 1fr);
                gap: 12px;
            }
            
            button {
                background: linear-gradient(145deg, #ffffff, #f0f0f0);
                border: none;
                border-radius: 50%;
                width: 60px;
                height: 60px;
                font-size: 20px;
                font-weight: 500;
                cursor: pointer;
                transition: all 0.2s ease;
                box-shadow: 5px 5px 10px #d1d1d1, -5px -5px 10px #ffffff;
                display: flex;
                align-items: center;
                justify-content: center;
                margin: 0 auto;
            }
            
            button:hover {
                transform: translateY(-3px);
                box-shadow: 7px 7px 15px #d1d1d1, -7px -7px 15px #ffffff;
            }
            
            button:active {
                transform: translateY(0);
                box-shadow: inset 3px 3px 7px #d1d1d1, inset -3px -3px 7px #ffffff;
            }
            
            .operator {
                background: linear-gradient(145deg, #3f51b5, #3949ab);
                color: white;
                font-weight: bold;
                box-shadow: 5px 5px 10px #aaa, -5px -5px 10px #fff;
            }
            
            .operator:hover {
                background: linear-gradient(145deg, #3949ab, #303f9f);
            }
            
            .equals {
                background: linear-gradient(145deg, #4caf50, #43a047);
                color: white;
                font-weight: bold;
                box-shadow: 5px 5px 10px #aaa, -5px -5px 10px #fff;
            }
            
            .equals:hover {
                background: linear-gradient(145deg, #43a047, #388e3c);
            }
            
            .clear {
                background: linear-gradient(145deg, #f44336, #e53935);
                color: white;
                font-weight: bold;
                box-shadow: 5px 5px 10px #aaa, -5px -5px 10px #fff;
            }
            
            .clear:hover {
                background: linear-gradient(145deg, #e53935, #d32f2f);
            }
            
            .hidden {
                display: none;
            }
            
            /* For the expression form */
            form {
                margin-top: 20px;
                display: flex;
                flex-direction: column;
            }
            
            input[type="text"] {
                padding: 15px;
                border: none;
                border-radius: 10px;
                font-size: 16px;
                margin-bottom: 15px;
                box-shadow: inset 0 2px 5px rgba(0, 0, 0, 0.1);
            }
            
            input[type="submit"] {
                background: linear-gradient(145deg, #3f51b5, #3949ab);
                color: white;
                border: none;
                border-radius: 10px;
                padding: 15px;
                font-size: 16px;
                font-weight: 500;
                cursor: pointer;
                transition: all 0.3s ease;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            }
            
            input[type="submit"]:hover {
                background: linear-gradient(145deg, #3949ab, #303f9f);
                transform: translateY(-2px);
                box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
            }
            
            /* Animations */
            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(10px); }
                to { opacity: 1; transform: translateY(0); }
            }
            
            @keyframes pulse {
                0% { transform: scale(1); }
                50% { transform: scale(1.05); }
                100% { transform: scale(1); }
            }
            
            /* Make buttons responsive */
            @media (max-width: 500px) {
                button {
                    width: 50px;
                    height: 50px;
                    font-size: 18px;
                }
                
                .display {
                    font-size: 24px;
                    height: 45px;
                    padding: 12px;
                }
                
                .container {
                    padding: 15px;
                }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>ESP32 Calculator</h1>
            <p>Connect to ESP32_K network to use this calculator</p>
            
            <div class="calculator">
                <div class="display" id="display"></div>
                <div class="buttons">
                    <button class="clear" onclick="clearDisplay()">C</button>
                    <button onclick="appendToDisplay('(')">(</button>
                    <button onclick="appendToDisplay(')')">)</button>
                    <button class="operator" onclick="appendToDisplay('/')">/</button>
                    
                    <button onclick="appendToDisplay('7')">7</button>
                    <button onclick="appendToDisplay('8')">8</button>
                    <button onclick="appendToDisplay('9')">9</button>
                    <button class="operator" onclick="appendToDisplay('*')">*</button>
                    
                    <button onclick="appendToDisplay('4')">4</button>
                    <button onclick="appendToDisplay('5')">5</button>
                    <button onclick="appendToDisplay('6')">6</button>
                    <button class="operator" onclick="appendToDisplay('-')">-</button>
                    
                    <button onclick="appendToDisplay('1')">1</button>
                    <button onclick="appendToDisplay('2')">2</button>
                    <button onclick="appendToDisplay('3')">3</button>
                    <button class="operator" onclick="appendToDisplay('+')">+</button>
                    
                    <button onclick="appendToDisplay('0')">0</button>
                    <button onclick="appendToDisplay('.')">.</button>
                    <button class="equals" onclick="calculate()">=</button>
                    <button onclick="backspace()">←</button>
                </div>
            </div>
            
            <form action="/" method="get" id="calc-form" class="hidden">
                <input type="text" name="expression" id="expression-field" placeholder="">
                <input type="submit" value="Calculate">
            </form>
            
        </div>

        <script>
            // JavaScript for calculator functionality
            let display = document.getElementById('display');
            let expressionField = document.getElementById('expression-field');
            let form = document.getElementById('calc-form');
            let resultDisplay = document.getElementById('result-display');
            
            function appendToDisplay(value) {
                display.textContent += value;
                animateButton(event.target);
            }
            
            function clearDisplay() {
                display.textContent = '';
                animateButton(event.target);
            }
            
            function backspace() {
                display.textContent = display.textContent.slice(0, -1);
                animateButton(event.target);
            }
            
            function calculate() {
                let expression = display.textContent;
                expressionField.value = expression;
                animateButton(event.target);
                form.submit();
            }
            
            function animateButton(button) {
                button.style.animation = 'pulse 0.3s ease-in-out';
                setTimeout(() => {
                    button.style.animation = '';
                }, 300);
            }
            
            // Add click effect for all buttons
            document.querySelectorAll('button').forEach(button => {
                button.addEventListener('mousedown', function() {
                    this.style.transform = 'scale(0.95)';
                });
                
                button.addEventListener('mouseup', function() {
                    this.style.transform = 'scale(1)';
                });
                
                button.addEventListener('mouseleave', function() {
                    this.style.transform = 'scale(1)';
                });
            });
            
            // If there's a result, show it in the display and animate result area
            let resultText = "{result}";
            if (resultText && resultText !== "" && resultText !== "{result}") {
                display.textContent = resultText;
                resultDisplay.style.animation = 'fadeIn 0.5s ease-in-out';
            }
        </script>
    </body>
    </html>"""
    return html
# Evaluate Mathematical Expressions
def evaluate_expression(expr):
    try:
        # Display the expression on OLED first
        display_on_oled("Expr: " + expr)
        time.sleep(2)  # Show expression for 2 seconds
        
        # Safely evaluate the expression
        result = str(eval(expr))
        display_on_oled("Result: " + result)  # Display result on OLED
        return result
    except:
        display_on_oled("Invalid Expr")  # Display error on OLED
        return "Invalid Expression"
# Setup Socket Server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("0.0.0.0", 80))
s.listen(5)
print("Web server started on http://{}:80".format(ap.ifconfig()[0]))
while True:
    conn, addr = s.accept()
    print("Connection from:", addr)
    request = conn.recv(1024).decode("utf-8")
    print("Request:", request)
    # Extract expression from the request
    expression = ""
    if "GET /?expression=" in request:
        expression = request.split("expression=")[1].split(" ")[0]
        expression = expression.replace("%2B", "+")  # Decode URL encoding for '+'
        expression = expression.replace("%2F", "/")  # Decode URL encoding for '/'
        expression = expression.replace("%28", "(")  # Decode URL encoding for '('
        expression = expression.replace("%29", ")")  # Decode URL encoding for ')'
        expression = expression.replace("%2A", "*")  # Decode URL encoding for '*'
        result = evaluate_expression(expression)
    else:
        result = ""
    # Send the web page with the result
    # Send the web page with the result
response = web_page(result)
conn.send("HTTP/1.1 200 OK\nContent-Type: text/html\n\n".encode())
conn.send(response.encode())
conn.close()