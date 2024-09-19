import RPi.GPIO as GPIO
import adafruit_dht
import time
import board


green_led = 7    
yellow_led = 6    
red_led = 5       
trig_pin = 3     
echo_pin = 4     
touch_pin = 1


dht_device = adafruit_dht.DHT11(board.D2)


GPIO.setmode(GPIO.BCM)
GPIO.setup(green_led, GPIO.OUT)
GPIO.setup(yellow_led, GPIO.OUT)
GPIO.setup(red_led, GPIO.OUT)
GPIO.setup(trig_pin, GPIO.OUT)
GPIO.setup(echo_pin, GPIO.IN)
GPIO.setup(touch_pin, GPIO.IN)

GPIO.output(green_led, GPIO.LOW)
GPIO.output(yellow_led, GPIO.LOW)
GPIO.output(red_led, GPIO.LOW)

touch_flag = False

def get_distance():
    GPIO.output(trig_pin, True)
    time.sleep(0.00001)
    GPIO.output(trig_pin, False)

    start_time = time.time()
    stop_time = time.time()

    while GPIO.input(echo_pin) == 0:
        start_time = time.time()

    while GPIO.input(echo_pin) == 1:
        stop_time = time.time()

    time_elapsed = stop_time - start_time
    distance = (time_elapsed * 34300) / 2  
    return distance

def measure_temperature_and_humidity():
    try:
        temperature = dht_device.temperature
        humidity = dht_device.humidity

        if temperature is not None and humidity is not None:
            print(f"Temperature: {temperature:.1f}C, Humidity: {humidity:.1f}%")
        else:
            print("Failed to retrieve data from sensor")
    
    except RuntimeError as error:
        print(f"Error reading DHT11: {error.args[0]}")

try:
    while True:
        if GPIO.input(touch_pin) == GPIO.HIGH and not touch_flag:
            touch_flag = True
            print("System ON\n")
            
            measure_temperature_and_humidity()
            
            while touch_flag:     
                distance = get_distance()
                print(f"Distance is {distance:.1f} cm")

                if distance > 20:
                    GPIO.output(green_led, GPIO.HIGH)
                    GPIO.output(yellow_led, GPIO.LOW)
                    GPIO.output(red_led, GPIO.LOW)
                elif 10 < distance <= 20:
                    GPIO.output(green_led, GPIO.LOW)
                    GPIO.output(yellow_led, GPIO.HIGH)
                    GPIO.output(red_led, GPIO.LOW)
                elif distance <= 10:
                    GPIO.output(green_led, GPIO.LOW)
                    GPIO.output(yellow_led, GPIO.LOW)
                    GPIO.output(red_led, GPIO.HIGH)
                    print("Too close")

                time.sleep(1)  
                
                if GPIO.input(touch_pin) == GPIO.HIGH:
                    print("System OFF")
                    
                    measure_temperature_and_humidity()
                    
                    touch_flag = False
                    GPIO.output(green_led, GPIO.LOW)
                    GPIO.output(yellow_led, GPIO.LOW)
                    GPIO.output(red_led, GPIO.LOW)
                    time.sleep(1)

except KeyboardInterrupt:
    print("Program stopped")

finally:
    GPIO.cleanup()
    dht_device.exit()
