# client.py
import socket

# Configurações do cliente
HOST = '127.0.0.1'
PORT = 7000
ADDR = (HOST, PORT)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(ADDR)

def menu():
    while True:
        print("\nMenu")
        print("1 - enviar mensagem")
        print("2 - sair")

        opcao = input("escolha uma opção: ")

        if opcao == '1':
            msg = input("digite a mensagem: ")
            client_socket.send(msg.encode())
            resposta = client_socket.recv(1024).decode()
            if resposta:
                print(f"{resposta}")
            else:
                print("Voce esta banido e não pode interagir mais no chat")


        elif opcao == '2':
            print("saindo...")
            client_socket.close()
            break

        else:
            print("opção invalida")

menu()
