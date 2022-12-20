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

    def send_command(self, command):
        response = requests.post(self.main_server_address, json=command)
        return response.json()

    def read_all(self, chamber_id):
        data = {
            'chamber_id': self.chamber_id,
            'command': f'read_all'
        }
        response = requests.post(MAIN_SERVER_ADDRESS, json=data)
        logging.info(f'{response.status_code} - {response.content}')
        return response.content

    def parse_data(self, data):
        sensor_presenca=(data.get('response').get(
            'sala1').get('Sensor de Presença'))
        sensor_fumaca=(data.get('response').get(
            'sala1').get('Sensor de Fumaça'))
        sensor_janela=(data.get('response').get(
            'sala1').get('Sensor de Janela'))
        sensor_porta=(data.get('response').get(
            'sala1').get('Sensor de Porta'))
        sensor_contagem_entrada=(data.get('response').get('sala1').get(
            'Sensor de Contagem de Pessoas Entrada'))
        sensor_contagem_saida=(data.get('response').get('sala1').get(
            'Sensor de Contagem de Pessoas Saída'))
        lamapada1=(data.get('response').get('sala1').get('Lâmpada 01'))
        lampada2=(data.get('response').get('sala1').get('Lâmpada 02'))
        projetor=(data.get('response').get('sala1').get('Projetor Multimidia'))
        ar=(data.get('response').get('sala1').get(
            'Ar-Condicionado (1º Andar)'))
        sirene=(data.get('response').get(
            'sala1').get('Sirene do Alarme'))
        sensor_temperatura_umidade=(data.get('response').get('sala1').get(
            'Sensor de Temperatura e Umidade'))

        # print all with the names of the components and if they are on or off
        print(f'Sensor de Presença: {sensor_presenca}')
        print(f'Sensor de Fumaça: {sensor_fumaca}')
        print(f'Sensor de Janela: {sensor_janela}')
        print(f'Sensor de Porta: {sensor_porta}')
        print(f'Sensor de Contagem de Pessoas Entrada: {sensor_contagem_entrada}')
        print(f'Sensor de Contagem de Pessoas Saída: {sensor_contagem_saida}')
        print(f'Lâmpada 01: {lamapada1}')
        print(f'Lâmpada 02: {lampada2}')
        print(f'Projetor Multimidia: {projetor}')
        print(f'Ar-Condicionado (1º Andar): {ar}')
        print(f'Sirene do Alarme: {sirene}')
        print(f'Sensor de Temperatura e Umidade: {sensor_temperatura_umidade[0]}°C {sensor_temperatura_umidade[1]}')
        
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
        session = PromptSession()
        while True:
            command = session.prompt(
                # print temp and humidity real time
                'Enter a command (1-5, q to quit): ',
                # completer=self.completer
            )
            if command == '1':
                self.chamber_id = session.prompt('Enter chamber ID: ')
            elif command == '2':
              # send command to toggle
                if self.chamber_id:
                    component = session.prompt('Enter component: ')
                    # print(self.send_toggle_command(self.chamber_id, component))
                    # dummy response
                    print(self.send_toggle_command(self.chamber_id, component))
            elif command == '3':
                if self.chamber_id:
                    data = json.loads(self.read_all(self.chamber_id))
                    # parse data
                    # {'response': {'sala1': {'Sensor de Presença': 0, 'Sensor de Fumaça': 0, 'Sensor de Janela': 0, 'Sensor de Porta': 0,
                    # 'Sensor de Contagem de Pessoas Entrada': 0, 'Sensor de Contagem de Pessoas Saída': 0, 'Lâmpada 01': 1, 'Lâmpada 02': 0, 'Projetor Multimidia': 1,
                    # 'Ar-Condicionado (1º Andar)': 0, 'Sirene do Alarme': 0, 'Sensor de Temperatura e Umidade': []}}, 'status': 200}
                    print(data)
                    self.parse_data(data)
                else:
                    print('No chamber selected')
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
