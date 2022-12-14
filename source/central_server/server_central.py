import json
import requests
import logging
from io import BytesIO
from http.server import HTTPServer, BaseHTTPRequestHandler


# TODO get this from config.json
with open('config.json') as json_data:
    data = json.load(json_data)
    HOST = data.get('ip_servidor_central')
    PORT = data.get('porta_servidor_central')
    MAIN_SERVER_ADDRESS = 'http://' + ':'.join([
        data.get('ip_servidor_central'),
        str(data.get('porta_servidor_central'))
    ])
# HOST = '164.41.98.26'
# PORT = 10000


class MainServerHTTPRequestHandler(BaseHTTPRequestHandler):

    chambers = {}

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

    @staticmethod
    def parse_body(body):
        body_dict = json.loads(body)
        chamber_id = body_dict.get('chamber_id')
        command = body_dict.get('command', '').split(':', 1)
        object = command[-1]
        action = command[0]
        return chamber_id, action, object

    def parse_post(self, body):
        """Parse received JSON and do what is needed"""
        chamber_id, action, object = self.parse_body(body)
        if not action or action not in self.allowed_commands:
            print(action)
            raise Exception('Action not in ALLOWED_COMMANDS')

        return self.allowed_commands.get(action)(chamber_id, object)

    def update_value(self, chamber_id, object):
        """
        Read status of an sensor or other part of the system
        Object must be a JSON string.
        """
        data = json.loads(object)
        print(f'updating{chamber_id}{str(data)}')
        if self.chambers.get(chamber_id):
            self.chambers[chamber_id].update(data)
        else:
            self.chambers[chamber_id] = data
        print(self.chambers)
        #import ipdb;ipdb.set_trace()
        logging.info(f'Updated value {data} successfully from {chamber_id}')
        return {
            'response': f'updated value {data} successfully',
            'status': 200
        }

    def read_value(self, chamber_id, key):
        """Read status of an sensor or other part of the system"""
        return {
            'response': self.chambers.get(chamber_id, {}).get(key),
            'status': 200
        }

    def read_all(self, chamber_id, object):
        """Read status of an sensor or other part of the system"""
        print(self.chambers)
        logging.info(f'Read all values from {chamber_id}')
        return {
            'response': self.chambers,
            'status': 200
        }

    def send_action_signal(self, chamber_id, object):
        """
        Send signal to distributed server to make an action
        Signal must be in format `{action}:{object}`
        I.e.: {'response': 'turn_on:light_A', 'status': 200}
        """
        chamber_address = self.chambers.get(chamber_id).get('address')

        assert self.validate_action(object)

        payload = json.dumps(object)
        requests.post(chamber_address, json=payload)
        return {'response': payload, 'status': 200}

    @staticmethod
    def validate_action(object):
        return len(object.split(':')) == 2

    @property
    def allowed_commands(self):
        return {
            'update_value': self.update_value,
            'read_value': self.read_value,
            'send_action_signal': self.send_action_signal,
            'read_all': self.read_all
        }


if __name__ == '__main__':
    address = (HOST, PORT)
    httpd = HTTPServer(address, MainServerHTTPRequestHandler)
    print('Server running at http://{}:{}'.format(HOST, PORT))
    httpd.serve_forever()