from flask import Flask, render_template_string
import adafruit_dht
import board
import time
import threading

DHT_SENSOR = adafruit_dht.DHT11(board.D4)

app = Flask(__name__)

temperature = None
humidity = None

def read_sensor():
    global temperature, humidity
    while True:
        try:
            temperature = DHT_SENSOR.temperature
            humidity = DHT_SENSOR.humidity
            if temperature is not None and humidity is not None:
                temperature = round(temperature, 1)
                humidity = round(humidity, 1)
        except RuntimeError as error:
            pass  
        time.sleep(1)

html_page = '''
<!doctype html>
<html>
    <head>
        <title>Temperature and Humidity</title>
        <meta http-equiv="refresh" content="1">
    </head>
    <body>
        <h1>Temperature and Humidity</h1>
        <hr>
        <div style="padding-left:20px;">
            <h3>Temperature: {{ temperature }} &#8451;</h3>
            <h3>Humidity: {{ humidity }} %</h3>
        </div>
    </body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(html_page, temperature=temperature, humidity=humidity)

if __name__ == "__main__":
    sensor_thread = threading.Thread(target=read_sensor)
    sensor_thread.daemon = True
    sensor_thread.start()
    try:
        app.run(host='0.0.0.0', port=8080)
    except KeyboardInterrupt:
        pass
