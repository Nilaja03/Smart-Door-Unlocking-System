import dht
import machine
from machine import Pin
import network
import time
import urequests

#replace with your WiFi credentials
WIFI_SSID = "OPPO A74 5G"
WIFI_PASSWORD = "g7paDbgW"

#replace with your ThingSpeak API key
THINGSPEAK_API_KEY = "5GXT4AB3L0Q5F26O"

#GPIO pin where the DHT11 sensor is connected
DHT_PIN = 0
buz = Pin(33, Pin.OUT)
SERVO_PIN = 15
servo = machine.PWM(machine.Pin(SERVO_PIN), freq=50)

def unlock_door():
    # Rotate servo to unlock the door
    servo.duty(30)  # Adjust duty cycle based on your servo
def lock_door():
    # Rotate servo to lock the door
    servo.duty(130)  # Adjust duty cycle based on your servo
    
def connect_to_wifi():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print("Connecting to Wifi...")
        sta_if.active(True)
        sta_if.connect(WIFI_SSID, WIFI_PASSWORD)
        while not sta_if.isconnected():
            pass
    #print("Connected to WiFi: ",sta_if.ifconfig())
    print("Connected to WiFi.")

def read_dht11():
    dht_sensor = dht.DHT11(machine.Pin(DHT_PIN))
    #try to read from the sensor up to 3 times
    for _ in range(3):
        try:
            dht_sensor.measure()
            temperature = dht_sensor.temperature()
            humidity = dht_sensor.humidity()
            
            if temperature>20:
                buz.on()
                unlock_door()
                print("Fire Detected. Door unlocked.")
            else:
                buz.off()
                lock_door()
            
            return temperature, humidity
        except Exception as e:
            print("Error reading DHT11:",e)
            time.sleep(2) #wait for 2 seconds before retrying
    print("Failed to read from DHT11 after multiple attempts.")
    return None, None
            
def send_to_thingspeak(humidity, temperature):
    api_url = "http://api.thingspeak.com/update"
    data = {"api_key": THINGSPEAK_API_KEY, "field1": humidity, "field2": temperature}
    response = urequests.post(api_url, json=data)
    print("ThingSpeak response:", response.text)
    response.close()

def main():
    #
    connect_to_wifi()
    while True:
        #servo.duty(0)
        temperature, humidity = read_dht11()
        print("Temperature:{}°C, Humidity: {}%".format(temperature, humidity))
        send_to_thingspeak(humidity, temperature)
        #upload data every 15 seconds (adjust as needed)
        time.sleep(10)
if __name__ == "__main__":
    servo.duty(130)
    main()