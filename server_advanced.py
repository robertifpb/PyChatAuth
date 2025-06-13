import socket
from threading import Thread
import time
from datetime import datetime

# Configurações globais
HOST = '127.0.0.1'
PORTA = 2323
USUARIOS = {
    "aluno": "aluno_ifpb",
    "professor": "professor_ifpb",
    "gabriel": "gabriel_if",
    "alex": "alex_if"
}
LOGS_FILE = 'server_logs.txt'
clientes_conectados = []  # Lista de tuplas: (conn, addr, usuario)

def registrar_log(mensagem):
    with open(LOGS_FILE, 'a') as log_file:
        log_file.write(f'[{datetime.now()}] {mensagem}\n')

def brodcast(mensagem, origem=None):
    for conn, _, _ in clientes_conectados:
        if conn != origem:
            try:
                conn.sendall(mensagem.encode('utf-8'))
            except:
                clientes_conectados.remove((conn, _, _))

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

        # Envia confirmação de autenticação
        conn.sendall('AUTENTICACAO OK'.encode('utf-8'))
        time.sleep(0.5)  # pequeno delay para evitar sobreposição com próxima mensagem
        mensagem_boas_vindas = f'Login bem-sucedido. Bem-vindo, {usuario}! Você está conectado ao servidor do IFPB.'
        conn.sendall(mensagem_boas_vindas.encode('utf-8'))

        clientes_conectados.append((conn, addr, usuario))
        registrar_log(f'Novo cliente conectado: {usuario}@{addr}')
        time.sleep(1)

        # Loop principal
        while True:
            dados = conn.recv(1024)
            if not dados:
                break

            mensagem = dados.decode('utf-8').strip()
            registrar_log(f'Mensagem de {usuario}: {mensagem}')

            # Protocolo de comandos
            if mensagem.upper() == 'HORA':
                resposta = f'HORA {datetime.now().strftime("%H:%M:%S")}'
            elif mensagem.upper() == 'DATA':
                resposta = f'DATA {datetime.now().strftime("%d/%m/%Y")}'
            elif mensagem.upper() == 'LISTAR':
                if clientes_conectados:
                    resposta = 'Usuários conectados:\n'
                    for _, addr_conectado, user_conectado in clientes_conectados:
                        resposta += f'- {user_conectado} @ {addr_conectado[0]}\n'
                else:
                    resposta = 'Nenhum usuário conectado no momento.'
            elif mensagem.startswith('@'):
                partes = mensagem.split(maxsplit=1)
                destino = partes[0][1:]
                msg = partes[1] if len(partes) > 1 else ""
                resposta = f'PRIVADO {usuario}: {msg}'
            else:
                resposta = f'{usuario}: {mensagem}'
                brodcast(resposta, conn)

            conn.sendall(resposta.encode('utf-8'))

    except Exception as e:
        registrar_log(f"Erro com {addr}: {e}")

    finally:
        for cliente in clientes_conectados:
            if cliente[0] == conn:
                clientes_conectados.remove(cliente)
                break
        conn.close()
        registrar_log(f'Conexão encerrada: {usuario}@{addr}')

def iniciar_servidor():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORTA))
        s.listen()
        registrar_log(f'Servidor iniciado em {HOST}:{PORTA}')
        print(f'Servidor aguardando conexões...')
        print(f'Servidor iniciado em {HOST}:{PORTA}')
        while True:
            conn, addr = s.accept()
            thread = Thread(target=handle_cliente, args=(conn, addr))
            thread.start()

if __name__ == '__main__':
    iniciar_servidor()
