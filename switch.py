import RPi.GPIO as GPIO
import time


button_pin = 5  
led_pin = 1     


GPIO.setmode(GPIO.BCM)
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  
GPIO.setup(led_pin, GPIO.OUT)

try:
    while True:
        if GPIO.input(button_pin) == GPIO.HIGH:
            GPIO.output(led_pin, GPIO.HIGH)  
            print("LED ON")
        else:
            GPIO.output(led_pin, GPIO.LOW)  
            print("LED OFF")

        time.sleep(0.1)

except KeyboardInterrupt:
    print("Program stopped")

finally:
    GPIO.cleanup()  
