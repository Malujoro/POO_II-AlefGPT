import socket
import threading

# Define o endereço e porta do servidor
HOST = '127.0.0.1'
PORT = 7000
ADDR = (HOST, PORT)

# Define um dicionário com o IP e Porta dos clientes
clientes = {}

# Função para gerenciar cada cliente em uma thread
def handle_client(con, nome):
    print(f"Cliente {nome} conectado.")

    try:
        while True:
            dados = con.recv(1024).decode()
            if(not dados):
                break

            if(':' not in dados):
                con.send("Formato inválido. Use 'destino:mensagem'.".encode())
                continue
            
            destino, mensagem = dados.split(':', 1)

            # Envia a mensagem ao destino
            if(destino in clientes):
                clientes[destino][0].send(f"Mensagem de {nome}: {mensagem}".encode())
                con.send("Mensagem enviada com sucesso.".encode())
            else:
                con.send("Destinatário não encontrado.".encode())

            print(f"Mensagem de {nome} para {destino}: {mensagem}")

    finally:
        del clientes[nome]
        con.close()
        print(f"Cliente {nome} desconectado.")

# Função para iniciar o servidor
def iniciar_servidor():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(ADDR)
    server_socket.listen(3)
    print(f"Servidor rodando na porta {PORT}")

    while True:
        con, endereco = server_socket.accept()
        nome_usuario = con.recv(1024).decode()
        clientes[nome_usuario] = (con, endereco)
        thread = threading.Thread(target=handle_client, args=(con, nome_usuario))
        thread.start()

iniciar_servidor()