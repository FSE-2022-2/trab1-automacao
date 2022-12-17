import json

IP_SERVIDOR_CENTRAL = ""
PORTA_SERVIDOR_CENTRAL = ""
IP_SERVIDOR_DISTRIBUIDO = ""
PORTA_SERVIDOR_DISTRIBUIDO = ""
NOME = ""
DHT22_PIN = ""
SENSOR_TEMPERATURA = {}
OUTPUTS_PIN = {}
INPUTS_PIN = {}

#set gpio temp pin
def my_import(name):
    components = name.split('.')
    mod = __import__(components[0])
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod

def read_config():
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
        OUTPUTS_PIN[tag] = pin
        
    inputs_list = data["inputs"]
    for input in inputs_list:
        #get tag value
        tag = input["tag"]
        #get pin value
        pin = input["gpio"]
        #add to dictionary
        INPUTS_PIN[tag] = pin

    sensor_temperatura_list = data["sensor_temperatura"]
    
    for sensor in sensor_temperatura_list:
        #get tag value
        tag = sensor["tag"]
        #get pin value
        pin = sensor["gpio"]
        #add to dictionary
        SENSOR_TEMPERATURA[tag] = pin

    #parse variables
    IP_SERVIDOR_CENTRAL = data["ip_servidor_central"]
    PORTA_SERVIDOR_CENTRAL = data["porta_servidor_central"]
    IP_SERVIDOR_DISTRIBUIDO = data["ip_servidor_distribuido"]
    PORTA_SERVIDOR_DISTRIBUIDO = data["porta_servidor_distribuido"]
    NOME = data["nome"]
    DHT22_PIN = '.D'.join(['board', str(list(SENSOR_TEMPERATURA.values())[0])])


read_config()
