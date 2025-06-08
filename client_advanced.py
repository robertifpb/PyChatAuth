import socket
import threading
import time

def receber_mensagens(socket_client):
    while True:
        try:
            mensagem = socket_client.recv(1024).decode('utf-8')
            print("\n" + mensagem + "\nDigite mensagem: ", end="")
        except:
            print('\nConexão com o servidor perdida')
            time.sleep(1)
            break

def iniciar_cliente():
        HOST = '127.0.0.1'
        PORTA = 8381

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST,PORTA))

            #Autenticação
            print(s.recv(1024).decode('utf-8'), end="")
            usuario =  input()
            s.sendall(usuario.encode('utf-8'))

            print(s.recv(1024).decode('utf-8'), end="")
            senha = input()
            s.sendall(senha.encode('utf-8'))

            resposta = s.recv(1024).decode('utf-8')
            if resposta != 'AUTENTICACAO OK':
                print("Falha na autenticação, tente novamente")
                time.sleep(1)
                return
            
            print('Autenticado com sucesso! Comandos disponíveis: ')
            time.sleep(1)
            print('HORA - Solicitar a hora atual')
            print('DATA - Solicitar data atual')
            print('@usuario mensagem - Mensagem privada')

            #Thread para receber mensagens
            thread_receber = threading.Thread(target=receber_mensagens, args=(s,))
            thread_receber.start()

            #Envio de mensagens
            while True:
                mensagem = input('Digite sua mensagem: ')
                if mensagem.lower() == 'sair':
                    break
                s.sendall(mensagem.encode('utf-8'))
if __name__ == '__main__':
    iniciar_cliente()