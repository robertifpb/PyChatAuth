import socket
import threading
import time
from datetime import datetime

#Configurações globais
HOST = '127.0.0.1'
PORTA = 12345
USUARIOS = {"aluno":"alex", "admin":"alex123"}
LOGS_FILE = 'server_logs.txt'
clientes_conectados = []

def registrar_log(mensagem):
    with open(LOGS_FILE, 'a') as log_file:
        log_file.write(f'[{datetime.now()}] {mensagem}\n')

def brodcast(mensagem, origem = None):
    for cliente in clientes_conectados:
        if cliente != origem:
            try:
                cliente.sendall(mensagem.encode('utf-8'))
            except:
                clientes_conectados.remove(cliente)

def handle_cliente(conn, addr):
    try:
        #Autenticação
        conn.sendall('Digite usuário: ' .encode('utf-8'))
        usuario = conn.recv(1024).decode('utf-8').strip()
        conn.sendall('Digite senha: '.enconde('utf-8'))
        senha = conn.recv(1024).decode('utf-8').strip()

    if USUARIOS.get(usuario) !=  senha:
        conn.sendall('AUTENTICACAO FALHOU'.encode('utf-8'))
        registrar_log(f'Falha de autenticação de {addr}')
        coon.close()
        return
    
    conn.sendall('AUTENTICACAO OK'.encode('utf-8'))
    clientes_conectados.append(conn)
    registrar_log(f'Novo cliente conectado: {usuario}@{addr}')

    #Loop principal
    while True:
        dados = conn.recv(1024)
        if not dados:
            break

        mensagem = dados.decode('utf-8').strip()
        registrar_log(f'Mensegem de {usuario}: {mesangem}')

        #Protocolo de comandos
        if mensagem == 'HORA':
            None