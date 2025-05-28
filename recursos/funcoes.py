import os, time
import json
from datetime import datetime


def limpar_tela():
    os.system("cls")
    
def aguarde(segundos):
    time.sleep(segundos)
    
def inicializarBancoDeDados():
    # r - read, w - write, a - append
    try:
        banco = open("base.atitus","r")
    except:
        print("Banco de Dados Inexistente. Criando...")
        banco = open("base.atitus","w")
    
def escreverDados(nome, pontos):
    banco = open("base.atitus","r")
    dados = banco.read()

    if dados != "":
        dadosDict = json.loads(dados)
    else:
        dadosDict = {}
        
    data_br = datetime.now().strftime("%d/%m/%Y")
    hora = datetime.now().strftime("%H:%M:%S")
    
    dadosDict[nome] = (pontos, data_br, hora)
    
    banco = open("base.atitus","w")
    banco.write(json.dumps(dadosDict))
    banco.close()

def registrar_log(mensagem):
    agora = datetime.now().strftime("[%d/%m/%Y %H:%M:%S]")
    linha = f"{agora} {mensagem}\n"
    
    with open("recursos/log.dat", "a") as arquivo_log:
        arquivo_log.write(linha)