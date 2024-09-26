from flask import Flask, render_template_string
import RPi.GPIO as GPIO
import time

TRIG = 17
ECHO = 27

GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

app = Flask(__name__)

def measure_distance():
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()

    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    return round(distance, 2)

html_page = '''
<!doctype html>
<html>
    <head>
        <title>Ultrasonic Distance Measurement</title>
        <meta http-equiv="refresh" content="1">
    </head>
    <body>
        <h1>Ultrasonic Distance Measurement</h1>
        <hr>
        <div style="padding-left:20px;">
            <h3>Measured Distance: {{ distance }} cm</h3>
        </div>
    </body>
</html>
'''

@app.route('/')
def index():
    distance = measure_distance()
    return render_template_string(html_page, distance=distance)

if __name__ == "__main__":
    try:
        app.run(host='0.0.0.0', port=8080)
    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()
