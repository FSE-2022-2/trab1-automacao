# Description: Interface for central server
import logging
import requests
import json
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
import csv
from colored import fg, bg, attr

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
        if self.chambers_id == []:
            fg('red')
            print('Nenhuma sala conectada')
            attr('reset')
        else:      
            chambers_id = self.chambers_id[-1]
            for chamber_id in chambers_id:
                # set color blue
                print(fg('blue'), end='')
                print(f'Sala <{chamber_id}> conectada: ', end=';')
            # reset color
            print(attr('reset'))
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
        response = requests.post(MAIN_SERVER_ADDRESS, json=data)
        return response.content

    def interface(self):
        # first load
        _ = json.loads(self.read_all('sala1'))  #default chamber
        history = FileHistory('history.csv')
        session = PromptSession(history=history)
        # get session history of commands
        while True:
            # Display menu of available commands
            #print colored header text
            print(fg('green') + 'TUI Menu' + attr('reset'))
            print('1: Selecionar sala')
            print('2: Enviar comando para ativar/desativar componente')
            print('3: Ler dados de uma sala')
            print('4: Ler dados de todas as salas conectadas')
            print('5: Obtenha o histórico de comandos salvos no log CSV')
            print(fg('red')+'q: Quit'+attr('reset'))
            command = session.prompt(
                # print temp and humidity real time'
                'Enter a command (1-5, q to quit): ',
            )
            if command == '1':
                self.chamber_id = session.prompt('Enter chamber ID(Ex: sala1, sala2): ')
            elif command == '2':
              # send command to toggle
                if self.chamber_id:
                    component = session.prompt('Enter component: ', auto_suggest=AutoSuggestFromHistory())
                    # print(self.send_toggle_command(self.chamber_id, component))
                    # dummy response
                    print(self.send_toggle_command(self.chamber_id, component))
            elif command == '3':
                data = json.loads(self.read_all(self.chamber_id))
                self.print_data(data, self.chamber_id)
            elif command == '4':
                if not self.chambers_id:
                    print('Nenhuma sala foi conectada, aguarde update...')
                    continue
                chambers_id = self.chambers_id[-1]
                for chamber_id in chambers_id:
                    data = json.loads(self.read_all(chamber_id))
                    self.print_data(data, chamber_id)
            elif command == '5':
                # Load the command history from the file in list format
                commands = history.load()
                # read history from file
                with open('history.csv', 'r') as f:
                    reader = csv.reader(f)
                    for row in reader:
                        print(row)
            elif command == 'q':
                break
            else:
                print('Invalid command')


if __name__ == '__main__':
    interface = Interface()
    interface.interface()
