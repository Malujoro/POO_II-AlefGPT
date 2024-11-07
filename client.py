import socket

# Define o endereço e porta do servidor
HOST = "127.0.0.1" # Localhost
PORT = 7000
ADDR = (HOST, PORT)

# Efetua a conexão com o servidor
nome = input("Seu nome de usuário: ")
print("Conectando ao servidor...")
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(ADDR)
client_socket.send(nome.encode())

# Função para receber mensagens
def escutar_mensagens():
    try:
        dados = client_socket.recv(1024).decode()
        nome_remetente, mensagem = dados.split(":", 1)
        print(f"\nMensagem recebida de {nome_remetente}: {mensagem}\n")
        return True
    except KeyboardInterrupt:
        print("\nEspera cancelada")
    except ValueError:
        print(f"\n{dados.upper()}")
    except:
        print("\nErro ao receber mensagem.")
        return True
    return False

def enviar_msg():
    nome = input("Digite o nome do destinatário: ")
    msg = input("Digite a mensagem: ")
    client_socket.send(f"{nome}:{msg}".encode())

def menu():
    while True:
        print("\nMenu")
        print("1 - Enviar mensagem")
        print("2 - Escutar mensagem")
        print("3 - Enviar mensagem e esperar resposta")
        print("4 - Apenas escutar")
        print("0 - Sair")

        opcao = input("Escolha uma opção: ")

        if(opcao == "1"):
            enviar_msg()
        elif(opcao == "2"):
            escutar_mensagens()
        elif(opcao == "3"):
            enviar_msg()
            escutar_mensagens()
        elif(opcao == "4"):
            while escutar_mensagens():
                continue
                
        elif(opcao == "0"):
            print("Saindo...")
            client_socket.close()
            break
        else:
            print("Opção inválida")

menu()