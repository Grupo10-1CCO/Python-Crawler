import json
import requests
import database
import psutil
import os
from datetime import datetime
from time import sleep


def captura():

    url = "http://192.168.18.4:8080/data.json"

    r = requests.get(url)
    jsonFile= r.text.encode("utf8")
    data = json.loads(jsonFile)

    # Formatando o JSON e transformando em inteiro (int)
    temperatura = int(data["Children"][0]["Children"][0]["Children"][1]["Children"][0]["Value"][:2])

    #CPU
    cpu = psutil.cpu_percent()

    #RAM
    ram = round(psutil.virtual_memory().total / 1024 / 1024 / 1024 ,2)

    #Disco
    particoes = []
    for part in psutil.disk_partitions(all=False): # identificando partições
        if part[0] == "F:\\":
            break
        elif part[0] == "E:\\":
            break
        else:
            particoes.append(part[0])

            # Coletando o uso em cada partição 
        porcentagemOcupados = [] 
        for j in particoes:
            porcentagemOcupados.append(psutil.disk_usage(j).percent)

    disco = porcentagemOcupados[0]



    #os.system("cls")
    #print("CPU: {}\nRAM: {}\nDisco: {}\nTemperatura: {}".format(cpu,ram,disco,temperatura))

    #Capturando a data atual e horas
    dataAtual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    #query = "INSERT INTO [dbo].[Dados] (registro,momento,fkComponente) VALUES ({},'{}',205)".format(temperatura,dataAtual)

    #database.insert(query)

    #Armazenando o apenas a data (dd/mm/yyyy)
    hoje = datetime.now().date()

    #Gerando um arquivo CSV com os dados de maquina. O nome arquivo é a data de hoje
    with open('{}.csv'.format(hoje),'a') as file:
        file.write(f'{cpu},{temperatura},{ram},{disco}\n')
    
    return temperatura