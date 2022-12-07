import RPi.GPIO as GPIO

#dictionary to hold the GPIO pin numbers and their names
#entries are in the form of "name": pin_number

#output pins
out_pins_conf1 = {'L_01':18, 'L_02':23, 'AC':24, 'PR':25, 'AL_BZ':8}
out_pins_conf2 = {'L_01':26, 'L_02':19, 'AC':13, 'PR':6, 'AL_BZ':5}
#input pins
in_pins_conf1 = {'Spres':7, 'SFum':1, 'SJan':12, 'SPor':16, 'SC_IN':20, 'SC_OUT':21}
in_pins_conf2 = {'Spres':0, 'SFum':11, 'SJan':9, 'SPor':10, 'SC_IN':22, 'SC_OUT':27}

#1-Wire pins (Temperature sensors)
temp_pin_conf1 = {'DHT22':4}
temp_pin_conf2 = {'DHT22':18}

# function to set up the GPIO pins
def setup(config):
#check if configuration is set to 1 or 2
#set the pins accordingly
    if config == 1:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(list(out_pins_conf1.values()), GPIO.OUT)
        GPIO.setup(list(in_pins_conf1.values()), GPIO.IN)
        GPIO.setup(list(temp_pin_conf1.values()), GPIO.IN)
    elif config == 2:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(list(out_pins_conf2.values()), GPIO.OUT)
        GPIO.setup(list(in_pins_conf2.values()), GPIO.IN)
        GPIO.setup(list(temp_pin_conf2.values()), GPIO.IN)
    else:
        print("Invalid configuration number. Please check the configuration file.")

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
def read_temp(pin_num):
    return GPIO.input(pin_num)


# set configuration to 1
# config = 1
# setup(config)

# set L_01 to high
# set_output_pins(1, out_pins_conf1['L_01'])
