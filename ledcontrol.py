from flask import Flask, render_template_string, url_for, redirect
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
ledPin = [18, 23, 24]
ledStates = [0, 0, 0]
GPIO.setup(ledPin[0], GPIO.OUT)
GPIO.setup(ledPin[1], GPIO.OUT)
GPIO.setup(ledPin[2], GPIO.OUT)

def updateLeds():
    for num, value in enumerate(ledStates):
        GPIO.output(ledPin[num], value)
        

html_page='''<!doctype html>
    <html>
        <head>
            <title>LED Controller</title>
        </head>
        
        <body>
            <h1> Embedded System LED Controller</h1>
            <hr>
            
            <div style="padding-left:20px;">
                <h3>LED1, LED2, LED3</h3>
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
