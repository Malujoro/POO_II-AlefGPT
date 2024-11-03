import socket
import threading

# Define o endereço e porta do servidor
HOST = '127.0.0.1'
PORT = 7000
ADDR = (HOST, PORT)

# Define as palavras proibidas no chat
PALAVROES = {'batutinha', 'prolog'}
# Define um dicionário com o Cliente e o número de banimentos
banidos = {}
# Define um dicionário com o IP e Porta dos clientes
clientes = {}

# Função para censurar uma mensagem
def censurar_mensagem(mensagem):
    for palavra in PALAVROES:
        mensagem = mensagem.replace(palavra, '*' * len(palavra))
    return mensagem

# Função para verificar palavras proibidas na mensagem do cliente (e efetuar um banimento)
def verificar_banimento(cliente, mensagem):
    if(any(palavra in mensagem for palavra in PALAVROES)):
        banidos[cliente] = banidos.get(cliente, 0) + 1
        if(banidos[cliente] >= 3):
            return True
    return False

# Função para gerenciar cada cliente em uma thread
def handle_client(con, endereco):
    print(f"Cliente {endereco} conectado.")
    clientes[endereco] = con  # Armazena cada conexão do cliente

    try:
        while True:
            dados = con.recv(1024).decode()
            if(not dados):
                break

            if(':' not in dados):
                con.send("Formato inválido. Use 'destino:mensagem'.".encode())
                continue
            
            destino_str, mensagem = dados.split(':', 1)
            destino = eval(destino_str)  # Converte a string para tupla

            # Censura e verifica banimento
            mensagem_censurada = censurar_mensagem(mensagem)
            if(verificar_banimento(endereco, mensagem)):
                con.send("Você foi banido por enviar mensagens proibidas.".encode())
                break

            # Envia a mensagem ao destino
            if(destino in clientes):
                clientes[destino].send(f"Mensagem de {endereco}: {mensagem_censurada}".encode())
                con.send("Mensagem enviada com sucesso.".encode())
            else:
                con.send("Destinatário não encontrado.".encode())

            print(f"Mensagem de {endereco} para {destino}: {mensagem_censurada}")

    finally:
        del clientes[endereco]
        con.close()
        print(f"Cliente {endereco} desconectado.")

# Função para iniciar o servidor
def iniciar_servidor():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(ADDR)
    server_socket.listen(3)
    print(f"Servidor rodando na porta {PORT}")

    while True:
        con, endereco = server_socket.accept()
        thread = threading.Thread(target=handle_client, args=(con, endereco))
        thread.start()

iniciar_servidor()