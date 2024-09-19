import RPi.GPIO as GPIO  
import time  

TOUCH_PIN = 8 


GPIO.setmode(GPIO.BCM)


GPIO.setup(TOUCH_PIN, GPIO.IN)

try:
    while True:
        if GPIO.input(TOUCH_PIN) == GPIO.HIGH: 
            print("touch")
        else:
            print("no touch")
        time.sleep(0.5)
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
