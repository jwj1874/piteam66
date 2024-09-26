from optparse import TitledHelpFormatter
from flask import Flask, render_template_string, url_for, redirect
import RPi.GPIO as GPIO
import time
import adafruit_dht
import board
import threading

# GPIO 핀 설정
TRIG = 17
ECHO = 27
ledPin = [18, 23, 24]
touchPin = 2
DHT_SENSOR = adafruit_dht.DHT11(board.D4)



# GPIO 설정
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(ledPin[0], GPIO.OUT)
GPIO.setup(ledPin[1], GPIO.OUT)
GPIO.setup(ledPin[2], GPIO.OUT)
GPIO.setup(touchPin, GPIO.IN)

# 전역 변수 초기화
temperature = None
humidity = None
ledStates = [0, 0, 0]
auto_flag = 0  # 0 = MANUAL, 1 = AUTO

# Flask 애플리케이션
app = Flask(__name__)

# 초음파 센서로 거리 측정
def measure_distance():
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    pulse_start = 0
    pulse_end = 0

    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()

    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    return round(distance, 2)

# LED 상태 업데이트 함수
def updateLeds():
    for num, value in enumerate(ledStates):
        GPIO.output(ledPin[num], value)

# DHT11 센서로 온도와 습도 측정
def read_sensor():
    global temperature, humidity
    while True:
        try:
            temperature = DHT_SENSOR.temperature
            humidity = DHT_SENSOR.humidity
            if temperature is not None and humidity is not None:
                temperature = round(temperature, 1)
                humidity = round(humidity, 1)
            if temperature <= 18:
                ledStates[0] = 1
                ledStates[1] = 0
            elif 18 < temperature < 26:
                ledStates[0] = 0
                ledStates[1] = 0
            else:
                ledStates[0] = 0
                ledStates[1] = 1
                
            if humidity < 59:
                ledStates[2] = 0
            else:
                ledStates[2] = 1
                
        except RuntimeError as error:
            pass
        time.sleep(1)

# 터치 센서 상태 확인 및 auto_flag 토글
def toggle_auto_flag():
    global auto_flag
    if GPIO.input(touchPin) == GPIO.HIGH:
        auto_flag = 1 - auto_flag  # 0과 1로 전환 (토글)
        time.sleep(0.5)  # 디바운싱

# HTML 템플릿 (터치센서에 따른 AUTO/MANUAL 표시 추가)
html_page = '''
<!doctype html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>System Control Panel</title>
    <meta http-equiv="refresh" content="1"> <!-- 1초마다 자동 새로고침 -->
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f0f4d9;
            margin: 0;
            padding: 20px;
        }
        .container {
            max-width: 700px;
            margin: 0 auto;
            padding: 20px;
            border: 2px solid #406030;
            background-color: #e6e6d6;
        }
        .header {
            text-align: center;
            margin-bottom: 20px;
        }
        .header h1 {
            font-size: 24px;
            margin-top: 0;
        }
        .status {
            display: flex;
            justify-content: space-between;
            margin-bottom: 20px;
        }
        .status div {
            text-align: center;
            font-size: 20px;
        }
        .led-control {
            display: flex;
            justify-content: space-around;
            margin-bottom: 20px;
        }
        .led-control div {
            text-align: center;
        }
        .led-control button {
            padding: 10px 20px;
            border-radius: 10px;
            border: none;
            cursor: pointer;
        }
        .on {
            background-color: #00cc66;
            color: white;
        }
        .off {
            background-color: #ff6666;
            color: white;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>KU Embedded System Controller</h1>
        </div>

        <div class="status">
            <div>
                <p>온도: {{ temperature }} &#8451;</p>
            </div>
            <div>
                <p>습도: {{ humidity }}%</p>
            </div>
            <div>
                <p>거리: {{ distance }} cm</p>
            </div>
        </div>

        <div class="status">
            <div>
                <p>모드:
                    {% if auto_flag == 1 %}
                        <span style="color:green;">AUTO</span>
                    {% else %}
                        <span style="color:red;">MANUAL</span>
                    {% endif %}
                </p>
            </div>
        </div>

        <div class="led-control">
            <div>
                <p>LED1: {% if ledStates[0] == 1 %} ON {% else %} OFF {% endif %}</p>
                <a href="{{ url_for('LEDcontrol', LEDn=0, state=1) }}"><button class="on">ON</button></a>
                <a href="{{ url_for('LEDcontrol', LEDn=0, state=0) }}"><button class="off">OFF</button></a>
            </div>
            <div>
                <p>LED2: {% if ledStates[1] == 1 %} ON {% else %} OFF {% endif %}</p>
                <a href="{{ url_for('LEDcontrol', LEDn=1, state=1) }}"><button class="on">ON</button></a>
                <a href="{{ url_for('LEDcontrol', LEDn=1, state=0) }}"><button class="off">OFF</button></a>
            </div>
            <div>
                <p>LED3: {% if ledStates[2] == 1 %} ON {% else %} OFF {% endif %}</p>
                <a href="{{ url_for('LEDcontrol', LEDn=2, state=1) }}"><button class="on">ON"></button></a>
                <a href="{{ url_for('LEDcontrol', LEDn=2, state=0) }}"><button class="off">OFF"></button></a>
            </div>
        </div>
    </div>
</body>
</html>
'''

# 메인 페이지 라우트
@app.route('/')
def index():
    distance = measure_distance()  # 초음파 센서로 측정한 거리
    toggle_auto_flag()  # 터치 센서로 auto_flag 토글
    return render_template_string(html_page, distance=distance, temperature=temperature, humidity=humidity, auto_flag=auto_flag, ledStates=ledStates)

# LED 제어 라우트
@app.route('/<int:LEDn>/<int:state>')
def LEDcontrol(LEDn, state):
    ledStates[LEDn] = state
    updateLeds()
    return redirect(url_for('index'))

# 메인 실행
if __name__ == "__main__":
    # DHT11 센서 스레드 시작
    sensor_thread = threading.Thread(target=read_sensor)
    sensor_thread.daemon = True
    sensor_thread.start()

    try:
        app.run(host='0.0.0.0', port=8080)
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        GPIO.cleanup()
