"""
from flask import Flask, render_template_string, url_for, redirect
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
touchPin = 2

touch_flag = False

GPIO.setup(touchPin, GPIO.IN)

def check_touch():
    if GPIO.input(touchPin) == GPIO.HIGH:
        touch_flag = True
    else:
        touch_flag = False


        

html_page='''<!doctype html>
    <html>
        <head>
            <title>Touch Sensor</title>
        </head>
        
        <body>
            <h1> Embedded System Touch Controller</h1>
            <hr>
            
            <div style="padding-left:20px;">
                <h3>Touch Sensor status</h3>
                <p>
                    <b>LED1: {% if ledStates[0] == 1 %} ON {% else %} OFF {%endif %}</b>
                    <a href="{{ url_for('LEDcontrol',LEDn=0,state=1)}}"><input type="button" value="ON"></a>
                    <a href="{{ url_for('LEDcontrol',LEDn=0,state=0)}}"><input type="button" value="OFF"></a>
                </p>
                <p> 
                    <b>LED2: {% if ledStates[1] == 1 %} ON {% else %} OFF {%endif %}</b>
                    <a href="{{ url_for('LEDcontrol',LEDn=1,state=1)}}"><input type="button" value="ON"></a>
                    <a href="{{ url_for('LEDcontrol',LEDn=1,state=0)}}"><input type="button" value="OFF"></a>
                </p>
                <p>
                    <b>LED3: {% if ledStates[2] == 1%} ON {% else %} OFF {%endif %}</b>
                    <a href="{{ url_for('LEDcontrol',LEDn=2,state=1)}}"><input type="button" value="ON"></a>
                    <a href="{{ url_for('LEDcontrol',LEDn=2,state=0)}}"><input type="button" value="OFF"></a>
                </p>
            </div>
        </body>
    </html>
    '''

app = Flask(__name__)

@app.route('/')
def index():
    return render_template_string(html_page, ledStates= ledStates)

@app.route('/<int:LEDn>/<int:state>')
def LEDcontrol(LEDn, state):
    ledStates[LEDn] = state
    updateLeds()
    
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(port = 8080, host ='0.0.0.0')





"""
from flask import Flask, render_template_string
import RPi.GPIO as GPIO
import time

# GPIO 설정
GPIO.setmode(GPIO.BCM)
touchPin = 2  # 터치 센서를 연결한 GPIO 핀 번호
GPIO.setup(touchPin, GPIO.IN)

app = Flask(__name__)

# HTML 템플릿
html_page = '''
<!doctype html>
<html>
    <head>
        <title>Touch Sensor Status</title>
        <meta http-equiv="refresh" content="1">
    </head>
    <body>
        <h1>Touch Sensor Status</h1>
        <hr>
        <div style="padding-left:20px;">
            <h3>Sensor Status: 
                {% if sensor_status %}
                    <span style="color:green;">Touched</span>
                {% else %}
                    <span style="color:red;">Not Touched</span>
                {% endif %}
            </h3>
        </div>
    </body>
</html>
'''

# 터치 센서 상태 확인 함수
def check_touch_sensor():
    return GPIO.input(touchPin) == GPIO.HIGH

@app.route('/')
def index():
    sensor_status = check_touch_sensor()
    return render_template_string(html_page, sensor_status=sensor_status)

if __name__ == "__main__":
    try:
        app.run(host='0.0.0.0', port=8080, debug=False)
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        GPIO.cleanup()  # GPIO 핀 설정 해제

        
