# Description: Interface for central server
import logging
import requests
import json
from prompt_toolkit import PromptSession

# TODO get this from config.json
with open('config.json') as json_data:
    data = json.load(json_data)
    MAIN_SERVER_ADDRESS = 'http://' + ':'.join([
        data.get('ip_servidor_central'),
        str(data.get('porta_servidor_central'))
    ])


class Interface():
    def __init__(self):
        self.main_server_address = MAIN_SERVER_ADDRESS
        self.chambers_id = []

    def send_command(self, command):
        response = requests.post(self.main_server_address, json=command)
        return response.json()

    def read_all(self, chamber_id):
        data = {
            'chamber_id': chamber_id,
            'command': f'read_all'
        }
        response = requests.post(MAIN_SERVER_ADDRESS, json=data)
        # get all chamber ids from the response
        chambers_id = list(response.json().get('response').keys())
        if chambers_id not in self.chambers_id:
            self.chambers_id.append(chambers_id)
        print(self.chambers_id)
        logging.info(f'{response.status_code} - {response.content}')
        return response.content

    def print_data(self, data, chamber_id):
        sensor_presenca=(data.get('response').get(
            chamber_id).get('Sensor de Presença'))
        sensor_fumaca=(data.get('response').get(
            chamber_id).get('Sensor de Fumaça'))
        sensor_janela=(data.get('response').get(
            chamber_id).get('Sensor de Janela'))
        sensor_porta=(data.get('response').get(
            chamber_id).get('Sensor de Porta'))
        sensor_contagem_entrada=(data.get('response').get(chamber_id).get(
            'Sensor de Contagem de Pessoas Entrada'))
        sensor_contagem_saida=(data.get('response').get(chamber_id).get(
            'Sensor de Contagem de Pessoas Saída'))
        lamapada1=(data.get('response').get(chamber_id).get('Lâmpada 01'))
        lampada2=(data.get('response').get(chamber_id).get('Lâmpada 02'))
        projetor=(data.get('response').get(chamber_id).get('Projetor Multimidia'))
        ar=(data.get('response').get(chamber_id).get(
            'Ar-Condicionado (1º Andar)'))
        sirene=(data.get('response').get(
            chamber_id).get('Sirene do Alarme'))
        sensor_temperatura_umidade=(data.get('response').get(chamber_id).get(
            'Sensor de Temperatura e Umidade'))
        # check if sensor_temperatura_umidade is empty
        if not sensor_temperatura_umidade:
            sensor_temperatura_umidade = ['-', '-']
        # print all with the names of the components and if they are on or off
        # separate in columns of sensors, lamps, projector, air conditioner, alarm)
        print("+------------+  +------------+  +------------+  +------------+  +--------------+")
        #print chamber_id in the middle of the line
        print(f"|{chamber_id:^74}|")
        print("+------------+  +------------+  +------------+  +------------+  +--------------+")
        print("|  Sensor de |  |  Sensor de |  |  Sensor de |  |  Sensor de |  |  Contagem de |")
        print("| Presença:  |  |  Fumaça:   |  |  Janela:   |  |   Porta:   |  |    Pessoas   |")
        print(f"|  {sensor_presenca:^8}  |  |  {sensor_fumaca:^8}  |  |  {sensor_janela:^8}  |  |  {sensor_porta:^8}  |  |  {sensor_contagem_entrada:^8}    |")
        print("|            |  |            |  |            |  |            |  |              |")
        print("+------------+  +------------+  +------------+  +------------+  +--------------+")
        print("+------------+  +------------+  +------------+  +------------+  +--------------+")
        print("|  Lâmpada   |  |  Lâmpada   |  |  Projetor  |  |Ar-Condiciona|  |  Sirene do  |")
        print("|    01:     |  |    02:     |  |            |  |do (1º Andar)|  |   Alarme:   |")
        print(f"|  {lamapada1:^8}  |  |  {lampada2:^8}  |  |  {projetor:^8}  |  |  {ar:^8}   |  |  {sirene:^8}   |")
        print("|            |  |            |  |            |  |             |  |             |")
        print("+------------+  +------------+  +------------+  +-------------+  +-------------+")
        print("+------------------------------------------------------------------------------+")
        print("|  Sensor de Temperatura  |")
        print(f"|  {sensor_temperatura_umidade[0]:^11}°C          |")
        print("|  Sensor de Umidade      |")
        print(f"|  {sensor_temperatura_umidade[1]:^11}%           |")
        print("+------------------------------------------------------------------------------+")
        
    def send_toggle_command(self, chamber_id, component):
        data = {
            'chamber_id': chamber_id,
            'command': f'toggle:{component}'
        }
        # response = self.send_command(data)
        response = requests.post(MAIN_SERVER_ADDRESS, json={
                                 'command': 'send_action:{"toggle":"Lâmpada 02" }'})
        return response.content

    # def completer(self, text, state):
    #     options = ['1', '2', '3', '4', '5', 'q']
    #     return [option for option in options if option.startswith(text)]

    def interface(self):
        # get all chambers from server
        chambers = self.get_all_chambers()
        chambers = json.loads(chambers)
        chambers = chambers.get('response')
        # print chambers
        print('Chambers:')
        for chamber in chambers:
            print(chamber)
        session = PromptSession()
        while True:
            command = session.prompt(
                # print temp and humidity real time'
                'Enter a command (1-5, q to quit): ',
                # completer=self.completer
            )
            if command == '1':
                self.chamber_id = session.prompt('Enter chamber ID(Ex: sala1, sala2): ')
            elif command == '2':
              # send command to toggle
                if self.chamber_id:
                    component = session.prompt('Enter component: ')
                    # print(self.send_toggle_command(self.chamber_id, component))
                    # dummy response
                    print(self.send_toggle_command(self.chamber_id, component))
            elif command == '3':
                data = json.loads(self.read_all(self.chamber_id))
                    # parse data
                    # {'response': {self.chamber_id: {'Sensor de Presença': 0, 'Sensor de Fumaça': 0, 'Sensor de Janela': 0, 'Sensor de Porta': 0,
                    # 'Sensor de Contagem de Pessoas Entrada': 0, 'Sensor de Contagem de Pessoas Saída': 0, 'Lâmpada 01': 1, 'Lâmpada 02': 0, 'Projetor Multimidia': 1,
                    # 'Ar-Condicionado (1º Andar)': 0, 'Sirene do Alarme': 0, 'Sensor de Temperatura e Umidade': []}}, 'status': 200}
                print(data)
                self.print_data(data, self.chamber_id)
            elif command == '4':
                if self.chamber_id:
                    print(self.get_chamber_humidity(self.chamber_id))
                else:
                    print('No chamber selected')
            elif command == '5':
                if self.chamber_id:
                    print(self.get_chamber_light(self.chamber_id))
                else:
                    print('No chamber selected')
            elif command == 'q':
                break
            else:
                print('Invalid command')


if __name__ == '__main__':
    interface = Interface()
    interface.interface()
