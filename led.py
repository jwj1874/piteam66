import RPi.GPIO as GPIO
import time
ledPin = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(ledPin, GPIO.OUT, initial=GPIO.LOW)
while True:
 GPIO.output(ledPin, GPIO.HIGH)
 print('LED On')
 time.sleep(1)
 GPIO.output(ledPin, GPIO.LOW)
 print('LED Off')
 time.sleep(1)
