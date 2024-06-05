import machine
from mfrc522 import MFRC522
import time
from machine import Pin, I2C
from i2c_lcd import I2cLcd
from time import sleep
import random

def gen():
    characters = '0123456789ABCD'
    random_string = ''.join(random.choice(characters) for _ in range(8))
    with open("random_string.txt", "w") as file:
        file.write(random_string)
    with open("random_string.txt", "r") as file:
        retrieved_string = file.read()
    print("Retrieved String:", retrieved_string)
    return retrieved_string

LCD_I2C_ADDR = 0x27
ROW_PINS = [16, 17, 18, 19]
COL_PINS = [21, 22, 23, 2]
KEYS = [
    ['1', '2', '3', 'A'],
    ['4', '5', '6', 'B'],
    ['7', '8', '9', 'C'],
    ['*', '0', '#', 'D']
]

i2c = I2C(0, scl=Pin(5), sda=Pin(4), freq=10000)

lcd = I2cLcd(i2c, LCD_I2C_ADDR, 2, 16)
row_pins = [Pin(pin, Pin.IN, Pin.PULL_UP) for pin in ROW_PINS]
col_pins = [Pin(pin, Pin.OUT) for pin in COL_PINS]

SERVO_PIN = 15
servo = machine.PWM(machine.Pin(SERVO_PIN), freq=50)

rdr = MFRC522(14, 13, 12, 27, 26)

def stop_servo():
    # Stop the servo motor
    servo.duty(130)
    
def unlock_door():
    # Rotate servo to unlock the door
    servo.duty(30)  # Adjust duty cycle based on your servo
def lock_door():
    # Rotate servo to lock the door
    servo.duty(130)  # Adjust duty cycle based on your servo

def read_rfid():
    global uid
    while True:
        (stat, tag_type) = rdr.request(rdr.REQIDL)
        if stat == rdr.OK:
            (stat, raw_uid) = rdr.anticoll()
            if stat == rdr.OK:
                uid = "-".join(str(x) for x in raw_uid)
                print("Card UID: {}".format(uid))
                return uid

def read_key():
    for i in range(len(COL_PINS)):
        col_pins[i].value(0)
        for j in range(len(ROW_PINS)):
            if row_pins[j].value() == 0:
                return KEYS[j][i]
        col_pins[i].value(1)
    return None

entered_keys = ""
stop_servo()
k = gen()

# Take input from the keypad instead of manual input
lcd.putstr('1-RFID\n2-KEYPAD-->')
while True:
    key1 = read_key()
    if key1:
        lcd.putstr(key1)
        time.sleep(2)
        lcd.clear()
        break

if key1 == '2':
    lcd.putstr('Enter Passcode')
    time.sleep(2)
    lcd.clear()
    while True:
        key = read_key()
        
        if key:
            print("Key pressed:", key)

            if key == '#':
                print("Enter key pressed")
                stored_digits = entered_keys
                print("Stored Digits:", stored_digits)
                if stored_digits == k:
                    lcd.clear()
                    print("Access granted! Unlocking the door...")
                    lcd.putstr('Access Granted \n Unlocking Door....')
                    unlock_door()
                    time.sleep(5)  # Keep the door unlocked for 5 seconds
                    print("Locking the door...")
                    lcd.putstr("Locking Door")
                    lock_door()
                    lcd.clear()
                    k = gen()
                else:
                    lcd.clear()
                    print("Access denied. Wrong Password")
                    lcd.putstr("Access Denied")
                    sleep(2)
                    lcd.clear()    
                entered_keys = ""
            
            elif key == '*':
                print("Backspace key pressed")
                entered_keys = entered_keys[:-1]  

            else:
                entered_keys += key
            
            entered_keys = entered_keys[-8:]
            lcd.clear()
            lcd.move_to(0, 0)
            lcd.putstr(entered_keys)
            time.sleep(0.5)
        time.sleep(0.1)
else:
    try:
        for i in range(1):
            stop_servo()
            print("Place your RFID card near the reader...")
            lcd.putstr('Place Ur RFID...')
            time.sleep(2)
            lcd.clear()
            card_uid = read_rfid()

            # Check if the RFID card is authorized
            if card_uid == "96-21-144-89-188":
                print("Access granted! Unlocking the door...")
                lcd.putstr('Access Granted \n Unlocking Door....')
                unlock_door()
                time.sleep(5)  # Keep the door unlocked for 5 seconds
                print("Locking the door...")
                lcd.putstr('Locking Door....')
                lock_door()
                lcd.clear()
            else:
                print("Access denied! Unauthorized card.")
                lcd.putstr("Access Denied")  
                sleep(2)
                lcd.clear()
            time.sleep(2)  # Wait before reading the next RFID card
            stop_servo()
    except Exception as e:
        print("An error occurred: {}".format(e))
        lock_door()  # Lock the door in case of an error 