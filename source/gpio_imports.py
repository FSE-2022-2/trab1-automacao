import RPi.GPIO as GPIO
from adafruit_dht import DHT22
import board
import time
import json
import sys
import socket
import threading

#set gpio temp pin
def my_import(name):
    components = name.split('.')
    mod = __import__(components[0])
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod

def read_config():
    global outputs_pin
    global inputs_pin
    global sensor_temperatura
    global ip_servidor_central
    global porta_servidor_central
    global ip_servidor_distribuido
    global porta_servidor_distribuido
    global nome

    with open(sys.argv[1]) as json_data:
        data = json.load(json_data)
    # parse the JSON data, output field = output list
    outputs_list = data["outputs"]
    outputs_pin = {}
    for output in outputs_list:
        #get tag value
        tag = output["tag"]
        #get pin value
        pin = output["gpio"]
        #add to dictionary
        outputs_pin[tag] = pin
        
    inputs_list = data["inputs"]
    inputs_pin = {}
    for input in inputs_list:
        #get tag value
        tag = input["tag"]
        #get pin value
        pin = input["gpio"]
        #add to dictionary
        inputs_pin[tag] = pin

    sensor_temperatura_list = data["sensor_temperatura"]
    sensor_temperatura = {}
    for sensor in sensor_temperatura_list:
        #get tag value
        tag = sensor["tag"]
        #get pin value
        pin = sensor["gpio"]
        #add to dictionary
        sensor_temperatura[tag] = pin

    #parse variables
    ip_servidor_central = data["ip_servidor_central"]
    porta_servidor_central = data["porta_servidor_central"]
    ip_servidor_distribuido = data["ip_servidor_distribuido"]
    porta_servidor_distribuido = data["porta_servidor_distribuido"]
    nome = data["nome"]

# print('outputs_pin: ', outputs_pin)
# function to set up the GPIO pins
def setup():
    global dht22_pin
    #Set warnings to false
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(list(outputs_pin.values()), GPIO.OUT)
    GPIO.setup(list(inputs_pin.values()), GPIO.IN)
    GPIO.setup(list(sensor_temperatura.values()), GPIO.IN)
    # concatenate the pin number to the string 'board.D'
    dht22_pin = '.D'.join(['board', str(list(sensor_temperatura.values())[0])])
 
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
    global dht22_pin
    dht22_pin = my_import(dht22_pin)
    dht = DHT22(dht22_pin, use_pulseio=False)
    print("Temperature: " + str(dht.temperature) + "C")
    print("Humidity: " + str(dht.humidity) + "%")

# read the configuration file
read_config()
setup()

# set L_01 to high
set_output_pins(1, outputs_pin['Lâmpada 01'])

#read the temperature
read_temp()

