import socket
from threading import Thread
import time
from datetime import datetime

# Configurações globais
HOST = '127.0.0.1'
PORTA = 8381
USUARIOS = {"aluno": "aluno_ifpb", "professor": "professor_ifpb"}
LOGS_FILE = 'server_logs.txt'
clientes_conectados = []

def registrar_log(mensagem):
    with open(LOGS_FILE, 'a') as log_file:
        log_file.write(f'[{datetime.now()}] {mensagem}\n')

def brodcast(mensagem, origem=None):
    for cliente in clientes_conectados:
        if cliente != origem:
            try:
                cliente.sendall(mensagem.encode('utf-8'))
            except:
                clientes_conectados.remove(cliente)

def handle_cliente(conn, addr):
    try:
        # Autenticação
        conn.sendall('Digite usuário: '.encode('utf-8'))
        usuario = conn.recv(1024).decode('utf-8').strip()
        conn.sendall('Digite senha: '.encode('utf-8'))
        senha = conn.recv(1024).decode('utf-8').strip()

        if USUARIOS.get(usuario) != senha:
            conn.sendall('AUTENTICACAO FALHOU'.encode('utf-8'))
            registrar_log(f'Falha de autenticação de {addr}')
            conn.close()
            return

        conn.sendall('AUTENTICACAO OK'.encode('utf-8'))
        clientes_conectados.append(conn)
        registrar_log(f'Novo cliente conectado: {usuario}@{addr}')
        time.sleep(2)

        # Loop principal
        while True:
            dados = conn.recv(1024)
            if not dados:
                break

            mensagem = dados.decode('utf-8').strip()
            registrar_log(f'Mensagem de {usuario}: {mensagem}')

            # Protocolo de comandos
            if mensagem == 'HORA':
                resposta = f'HORA {datetime.now().strftime("%H:%M:%S")}'
            elif mensagem == 'DATA':
                resposta = f'DATA {datetime.now().strftime("%d/%m/%Y")}'
            elif mensagem.startswith('@'):
                # Mensagem privada
                partes = mensagem.split(maxsplit=1)
                destino = partes[0][1:]
                msg = partes[1] if len(partes) > 1 else ""
                resposta = f'PRIVADO {usuario}: {msg}'
            else:
                # Broadcast
                resposta = f'{usuario}: {mensagem}'
                brodcast(resposta, conn)

            conn.sendall(resposta.encode('utf-8'))

    except Exception as e:
        registrar_log(f"Erro com {addr}: {e}")

    finally:
        if conn in clientes_conectados:
            clientes_conectados.remove(conn)
        conn.close()
        registrar_log(f'Conexão encerrada: {usuario}@{addr}')

def iniciar_servidor():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORTA))
        s.listen()
        registrar_log(f'Servidor iniciado em {HOST}:{PORTA}')
        print(f'Servidor aguardando conexões...')
        #print(clientes_conectados.append)#
        while True:
            conn, addr = s.accept()
            thread = Thread(target=handle_cliente, args=(conn, addr))
            thread.start()

if __name__ == '__main__':
    iniciar_servidor()
