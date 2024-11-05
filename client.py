import socket

# Define o endereço e porta do servidor
HOST = '127.0.0.1'
PORT = 7000
ADDR = (HOST, PORT)

# Efetua a conexão com o servidor
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(ADDR)

nome = input("Seu nome de usuário: ")
client_socket.send(nome.encode())

# Função para receber mensagens
def escutar_mensagens():
    while True:
        try:
            msg = client_socket.recv(1024).decode()
            print(f"\nMensagem recebida: {msg}\n")
        except:
            print("\nErro ao receber mensagem.")
            break

def menu():
    while True:
        print("\nMenu")
        print("1 - Enviar mensagem")
        print("0 - Sair")

        opcao = input("Escolha uma opção: ")

        if(opcao == '1'):
            nome = input("Digite o nome do destinatário: ")
            msg = input("Digite a mensagem: ")
            client_socket.send(f"{nome}:{msg}".encode())

        elif(opcao == '0'):
            print("Saindo...")
            client_socket.close()
            break

        else:
            print("Opção inválida")

menu()