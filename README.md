# trab1-automacao
Aluno: Guilherme Braz</br>
Matricula: 18/0018159

## Instruções de execução
### Servidor Central
- Copie o arquivo server_central.py e o arquivo config.json para a raspberry escolhido
- Modifique no template do config.json as varíaveis para que estejam de acordo com a raspberry escolhida
- Para rodar simplismente execute o seguinte comando:
```bash
python3 server_central.py
```
- Rode a interface gráfica do servidor central
```bash
python3 interface.py
```
### Servidor Dístribuido
- Copie o arquivo server_distributed.py e o arquivo config.json para as raspberrys escolhidas
- Modifique no template do config.json as varíaveis para que estejam de acordo com a raspberry escolhida
- Para rodar simplismente execute o seguinte comando:
```bash
python3 server_distributed.py
```

### Requisitos pra rodar o projeto
```bash
pip3 install -r requirements.txt
```
> Pode dar erro no requirements.txt, então instale manualmente a adafruit-circuitpython-dht
```bash
pip3 install adafruit-circuitpython-dht
```