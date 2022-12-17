import RPi.GPIO as GPIO
from adafruit_dht import DHT22
import board
import time
from ..config import SENSOR_TEMPERATURA, IP_SERVIDOR_CENTRAL, INPUTS_PIN, my_import, IP_SERVIDOR_DISTRIBUIDO, OUTPUTS_PIN, PORTA_SERVIDOR_CENTRAL, PORTA_SERVIDOR_DISTRIBUIDO, DHT22_PIN

# print('outputs_pin: ', outputs_pin)
# function to set up the GPIO pins
def setup():
    # global dht22_pin
    #Set warnings to false
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(list(OUTPUTS_PIN.values()), GPIO.OUT)
    GPIO.setup(list(INPUTS_PIN.values()), GPIO.IN)
    GPIO.setup(list(SENSOR_TEMPERATURA.values()), GPIO.IN)
    # concatenate the pin number to the string 'board.D'
    # dht22_pin = '.D'.join(['board', str(list(SENSOR_TEMPERATURA.values())[0])])
 
# set the output pins to the desired state
def set_output_pins(state, pin_num):
    if state == 1:
        GPIO.output(pin_num, GPIO.HIGH)
    elif state == 0:
        GPIO.output(pin_num, GPIO.LOW)
    else:
        print("Invalid state. Please check the configuration file.")

# read the input pins
def read_input_pins(pin_num):
    return GPIO.input(pin_num)

# read the temperature sensor
def read_temp():
    # global dht22_pin
    pin = my_import(DHT22_PIN)
    dht = DHT22(pin, use_pulseio=False)
    
    # loop to read temp
    while True:
        print("Temperatura: "+str(dht.temperature)+"C")
        print("Humidade: "+str(dht.humidity)+"%")
        time.sleep(2)

# check alarm
def check_alarm():
    pass

# read the configuration file
setup()

# set L_01 to high
set_output_pins(1, OUTPUTS_PIN['Lâmpada 01'])

#read the temperature
read_temp()

