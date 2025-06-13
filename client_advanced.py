import socket
import threading
import time

def receber_mensagens(socket_client):
    while True:
        try:
            mensagem = socket_client.recv(1024).decode('utf-8')
            if not mensagem:
                print('\nConexão encerrada pelo servidor.')
                break
            print("\n" + mensagem + "\nDigite mensagem: ", end="")
        except:
            print('\nConexão com o servidor perdida')
            break

def iniciar_cliente():
    HOST = '127.0.0.1'
    PORTA = 2323

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((HOST, PORTA))

            # Autenticação
            print(s.recv(1024).decode('utf-8'), end="")  # Solicita usuário
            usuario = input()
            s.sendall(usuario.encode('utf-8'))

            print(s.recv(1024).decode('utf-8'), end="")  # Solicita senha
            senha = input()
            s.sendall(senha.encode('utf-8'))

            resposta = s.recv(1024).decode('utf-8')
            if not resposta.startswith('AUTENTICACAO OK'):
                print("\nFalha na autenticação, tente novamente")
                time.sleep(1)
                return

            print("\n" + resposta)
            print('\nComandos disponíveis:')
            print('HORA   - Solicitar a hora atual')
            print('DATA   - Solicitar a data atual')
            print('LISTAR - Ver usuários conectados')
            print('@usuario mensagem - Enviar mensagem privada')
            print('SAIR   - Encerrar conexão')

            # Thread para receber mensagens
            thread_receber = threading.Thread(target=receber_mensagens, args=(s,))
            thread_receber.daemon = True
            thread_receber.start()

            # Envio de mensagens
            while True:
                mensagem = input('Digite sua mensagem: ')
                if mensagem.lower() == 'sair':
                    print("Desconectando do servidor...")
                    break
                s.sendall(mensagem.encode('utf-8'))

        except ConnectionRefusedError:
            print("Não foi possível conectar ao servidor.")
        except Exception as e:
            print(f"Ocorreu um erro: {e}")

if __name__ == '__main__':
    iniciar_cliente()
