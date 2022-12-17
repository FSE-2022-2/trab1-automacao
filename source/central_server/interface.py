# Description: Interface for central server
import requests
import json
# get local ip
import socket

# get local ip
ip = socket.gethostbyname(socket.gethostname())
# get local port
port = 10000
# set server address
SERVER_ADDRESS = f'http://{ip}:{port}'

# SERVER_ADDRESS = 'http://164.41.98.26:10000' #LATER GET THIS FROM config.json

# function for sending action signal
def send_action_signal(chamber_id, signal):
    payload = json.dumps(signal)
    requests.post(SERVER_ADDRESS, json=payload)
    print(f'Sent action signal {payload}')

# function for reading value
def read_value(chamber_id, key):
    pass
# function for updating value
def update_value(chamber_id, data):
    pass    

# function for getting log csv
def get_log_csv():
    pass

# function for dashboard
# dashboard in ascii art to show the current status and values of the chambers
def dashboard():
    pass

# function for interface /:maybe needs to show temp and humidity in this main menu, and update values after 2 seconds each time
def interface():
    print('''
    1. send action signal
    2. read value
    3. update value
    4. get log csv
    5. Dashboard
    0. exit
    ''')
    option = input('Option: ')
    if option == '1':
        chamber_id = input('Chamber ID: ')
        action = input('Action: ')
        object = input('Object: ')
        signal = f'{action}:{object}'
        send_action_signal(chamber_id, signal)
    elif option == '2':
        chamber_id = input('Chamber ID: ')
        key = input('Key: ')
        print(read_value(chamber_id, key))
    elif option == '3':
        chamber_id = input('Chamber ID: ')
        key = input('Key: ')
        value = input('Value: ')
        update_value(chamber_id, {key: value})
    elif option == '4':
        get_log_csv()
    elif option == '5':
        dashboard()
    elif option == '0':
        exit()
    else:
        print('Invalid option')
    interface()

if __name__ == '__main__':
    # loop for interface
    # {'chamber_id': 'sala1', 'action': 'update_value:{"temperature":"22"}'}
    interface()