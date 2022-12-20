import json
import requests
import logging
import threading
import asyncio
import time
import random
from io import BytesIO
import RPi.GPIO as GPIO
from adafruit_dht import DHT22
import board
import time
import json
import socket
from http.server import HTTPServer, BaseHTTPRequestHandler

# TODO get this from config.json
with open('config.json') as json_data:
    data = json.load(json_data)
    HOST = data.get('ip_servidor_distribuido')
    PORT = data.get('porta_servidor_distribuido')
    MAIN_SERVER_ADDRESS = 'http://' + ':'.join([
        data.get('ip_servidor_central'),
        str(data.get('porta_servidor_central'))
    ])



def my_import(name):
    #import ipdb;ipdb.set_trace()
    components = str(name).split('.')
    mod = __import__(components[0])
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod

logging.basicConfig(level=logging.DEBUG)
# logging.setFormatter(logging.Formatter())

class DistributedServerHTTPRequestHandler(BaseHTTPRequestHandler):

    CHAMBER_ID = 'sala1'

    last_action = {}

    components = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args)

    def do_GET(self):
        self.send_response(400)
        self.end_headers()
        self.wfile.write(b'This server only accepts POST requests')

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        response_data = dict()

        try:
            response_data = self.parse_post(body)

        except Exception as err:
            response_data['status'] = 400
            response_data['response'] = str(err)

        self.send_response(response_data.get('status'))
        self.end_headers()
        response = json.dumps(response_data, indent=2).encode('utf-8')
        self.wfile.write(response)

    def update_values_on_main_server(self):
        components_json = json.dumps(self.components)
        data = {
            'chamber_id': self.CHAMBER_ID,
            'command': f'update_value:{components_json}'
        }
        response = requests.post(MAIN_SERVER_ADDRESS, json=data)
        logging.info(f'{response.status_code} - {response.content}')

    @staticmethod
    def parse_body(body):
        body_dict = json.loads(body)
        command = body_dict.get('command', '').split(':', 1)
        object = command[-1]
        action = command[0]
        return action, object

    def parse_post(self, body):
        """Parse received JSON and do what is needed"""
        action, object = self.parse_body(body)
        if not action or action not in self.allowed_commands:
            print(action)
            raise Exception('Action not in ALLOWED_COMMANDS')

        return self.allowed_commands.get(action)(object)

    def update_value(self, object):
        """
        Read status of an sensor or other part of the system
        Object must be a JSON string.
        """
        data = json.loads(object)
        self.components.update(data)
        # update values on main server
        try:
            self.update_values_on_main_server()
        except Exception as err:
            logging.error(err)
        return {
            'response': f'updated value {data} successfully',
            'status': 200
        }

    def get_action(self, *args, **kwargs):
        action = self.last_action
        if action:
            self.last_action = {}
        return {
            'response': action,
            'status': 200
        }

    def send_action(self, action):
        self.last_action = json.loads(action)
        self.save_action_to_csv_file(self.last_action)
        return {
            'response': f'{action} was sent!',
            'status': 200
        }

    def save_action_to_csv_file(self, action):
        pass

    @property
    def allowed_commands(self):
        return {
            'update_value': self.update_value,
            'get_action': self.get_action,
            'send_action': self.send_action
        }


class GPIOController:

    OUTPUTS_PIN = {}
    INPUTS_PIN = {}
    SENSOR_TEMPERATURA = {}
    ALARME = False

    def __init__(self, server_address):
        self.SERVER_ADDRESS = server_address
        self.read_config()
        self.setup()


    def update_values_on_server(self):
        logging.info(f'updating values on {self.SERVER_ADDRESS}')
        updated_data = self.read_all()
        payload = {
            'command': ':'.join(['update_value', json.dumps(updated_data)])
        }
        response = requests.post(self.SERVER_ADDRESS, json=payload)
        # get only lampada 01 status
        lampada_01_status = updated_data.get('Lâmpada 01')
        logging.info(lampada_01_status)
        # logging.info(response.content)
        return response

    def get_action(self):
        response = requests.post(
            self.SERVER_ADDRESS,
            json={
                'command': 'get_action'
            }
        )
        action = json.loads(response.content)
        event = action.get('event')
        logging.info(response.content)

        if not event:
            logging.info('No action was found')
            return

        logging.info(f'event: {event}')
        target = action.get('target')
        import ipdb; ipdb.set_trace()
        self.events.get(event)(target)

    def toggle(self, target):
        # log actual value
        logging.info(f'toggling {target}')
        actual_value = self.read_input_pins(self.OUTPUTS_PIN[target])
        print(f'actual value on {target}: {actual_value}')
        ans = self.set_output_pins(not actual_value, self.OUTPUTS_PIN[target])
        #log new value
        print(f'new value on {target}: {ans}')
        print('------------------')
        logging.info(f'new value: {self.read_input_pins(self.OUTPUTS_PIN[target])}')
        import ipdb; ipdb.set_trace()

    @property
    def events(self):
        return {
            'toggle': self.toggle
        }

    def loop_data_update(self):
        while True:
            self.get_action()
            logging.info('updating data')
            self.update_values_on_server()
            time.sleep(2)



    def read_config(self):
        with open('config.json') as json_data:
            data = json.load(json_data)
        # parse the JSON data, output field = output list
        outputs_list = data["outputs"]
        for output in outputs_list:
            #get tag value
            tag = output["tag"]
            #get pin value
            pin = output["gpio"]
            #add to dictionary
            self.OUTPUTS_PIN[tag] = pin

        inputs_list = data["inputs"]
        for input in inputs_list:
            #get tag value
            tag = input["tag"]
            #get pin value
            pin = input["gpio"]
            #add to dictionary
            self.INPUTS_PIN[tag] = pin

        sensor_temperatura_list = data["sensor_temperatura"]

        for sensor in sensor_temperatura_list:
            #get tag value
            tag = sensor["tag"]
            #get pin value
            pin = sensor["gpio"]
            #add to dictionary
            self.SENSOR_TEMPERATURA[tag] = pin

        #parse variables
        self.IP_SERVIDOR_CENTRAL = data["ip_servidor_central"]
        self.PORTA_SERVIDOR_CENTRAL = data["porta_servidor_central"]
        self.IP_SERVIDOR_DISTRIBUIDO = data["ip_servidor_distribuido"]
        self.PORTA_SERVIDOR_DISTRIBUIDO = data["porta_servidor_distribuido"]
        self.NOME = data["nome"]
        self.DHT22_PIN = '.D'.join(
            [
                'board',
                str(
                    list(
                        self.SENSOR_TEMPERATURA.values()
                    )[0]
                )
            ]
        )

    def setup(self):
        global dht22_pin
        #Set warnings to false
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(list(self.OUTPUTS_PIN.values()), GPIO.OUT)
        GPIO.setup(list(self.INPUTS_PIN.values()), GPIO.IN)
        GPIO.setup(list(self.SENSOR_TEMPERATURA.values()), GPIO.IN)
        # concatenate the pin number to the string 'board.D'
        dht22_pin = '.D'.join(
            ['board', str(list(self.SENSOR_TEMPERATURA.values())[0])]
        )

    # set the output pins to the desired state
    def set_output_pins(self, high, pin_num):
        if high:
            GPIO.output(pin_num, GPIO.HIGH)
            return
        GPIO.output(pin_num, GPIO.LOW)

    # read the input pins
    def read_input_pins(self, pin_num):
        return GPIO.input(pin_num)

    # read the temperature sensor
    def read_temp(self):
        global dht22_pin
        #dht22_pin = my_import(dht22_pin)
        retries = 4
        for _ in range(retries):
            try:
                dht22_pin = board.D18
                dht = DHT22(dht22_pin, use_pulseio=False)
                ans = []
                ans.append(dht.temperature)
                ans.append(dht.humidity)
            except:
                time.sleep(1)
                continue
        return ans

    # check smoke sensor
    def check_smoke(self):
        # if the input pin is high, the alarm is on
        if self.read_input_pins(self.INPUTS_PIN['Sensor de Fumaça']) == 1:
            return 1
        else:
            return 0

    #check alarm
    def check_alarm(self):
        # if the input pin is high, the alarm is on
        if self.ALARME == 1:
            return 1
        else:
            return 0

    # read all gpio pins
    def read_all(self):
    # read all INPUTS_PIN and OUTPUTS_PIN present answer if the tag of the pin is in the list
        ans = {}
        for tag in self.INPUTS_PIN:
           # print(tag)
            ans[tag]=self.read_input_pins(self.INPUTS_PIN[tag])
        for tag in self.OUTPUTS_PIN:
            ans[tag]=self.read_input_pins(self.OUTPUTS_PIN[tag])
        # read the temperature
        ans['Sensor de Temperatura e Umidade']=self.read_temp()
        return ans

if __name__ == '__main__':
    address = (HOST, PORT)
    controller = GPIOController(server_address=f'http://{HOST}:{PORT}')
    httpd = HTTPServer(address, DistributedServerHTTPRequestHandler)

    controller_thread = threading.Thread(
        target=controller.loop_data_update, args=(), kwargs={}
    )

    controller_thread.start()

    httpd.serve_forever()
    controller_thread.join()
