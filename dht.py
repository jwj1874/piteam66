import adafruit_dht
import board
import time


dht_device = adafruit_dht.DHT11(board.D4)

try:
    while True:
        try:
            
            temperature = dht_device.temperature
            humidity = dht_device.humidity
            
            
            if temperature is not None and humidity is not None:
                print(f"Temperature: {temperature:.1f}C, Humidity: {humidity:.1f}%")
            else:
                print("Failed to retrieve data from sensor")

        except RuntimeError as error:
            
            print(f"Error reading DHT11: {error.args[0]}")

        
        time.sleep(2)

except KeyboardInterrupt:
    print("Program stopped")

finally:
    dht_device.exit()
