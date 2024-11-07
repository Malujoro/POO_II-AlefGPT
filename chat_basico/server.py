import socket
from time import time

# Define o endereço e porta do servidor
HOST = "127.0.0.1" # Localhost
PORT = 7001
ADDR = (HOST, PORT)

# Define as palavras proibidas no chat
PALAVROES = ["batutinha", "prolog"]
# Define um dicionário com o Cliente e o número de banimentos
banidos = {}
# Define um dicionário com o IP e Porta dos clientes
clientes = {}


# Função para censurar uma mensagem
def censurar_mensagem(mensagem):
    mensagem = mensagem.lower()

    for palavra in PALAVROES:
        mensagem = mensagem.replace(palavra.lower(), "*" * len(palavra))
    
    return mensagem


# Função para verificar palavras proibidas na mensagem do cliente (e efetuar um banimento)
def verificar_banimento(cliente, mensagem):
    if(any(palavra in mensagem for palavra in PALAVROES)):
        banidos[cliente] = banidos.get(cliente, [])

        tempo_atual = time()
        banidos[cliente].append(tempo_atual)
        
        if(len(banidos[cliente]) >= 3):
            if(tempo_atual - banidos[cliente][0] <= 60):
                return True
            banidos[cliente].pop(0)
    return False


# Função para encaminhar as mensagens recebidas para o destinatário
def encaminhar_mensagem(conexao_remetente, nome_remetente):
    try:
        dados = conexao_remetente.recv(1024).decode()
        
        if(not dados or ":" not in dados):
            return

        nome_destino, mensagem = dados.split(":", 1)
        nome_destino = nome_destino.lower()

        # Censura e verifica banimento
        mensagem_censurada = censurar_mensagem(mensagem)
        if(verificar_banimento(nome_remetente, mensagem)):
            conexao_remetente.send("Você foi banido por enviar mensagens proibidas".encode())
            print(f"\n{nome_remetente} foi banido por enviar mensagens proibidas")
            clientes[nome_remetente][0].close()
            del clientes[nome_remetente]
            return

        # Envia a mensagem ao destino
        if(nome_destino in clientes.keys()):
            clientes[nome_destino][0].send(f"{nome_remetente}:{mensagem_censurada}".encode())

        print(f"Mensagem de [{nome_remetente}] para [{nome_destino}]: {mensagem_censurada}")
    except socket.timeout:
        print(f"\nTimeout de {nome_remetente}")


# Função para iniciar o servidor
def iniciar_servidor():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(ADDR)
    server_socket.listen(3)

    print(f"Servidor rodando na porta {PORT}")
    while True:
        try:
            server_socket.settimeout(1)
            try:
                print("\nEsperando nova conexão...")
                client_socket, endereco = server_socket.accept()

                client_socket.settimeout(1)
                nome_usuario = client_socket.recv(1024).decode().lower()
                clientes[nome_usuario] = (client_socket, endereco)
                print(f"\nCliente [{nome_usuario}] conectado.")
            except socket.timeout:
                print(f"\nTimeout de conexão")

            for nome, cliente in list(clientes.items()):
                print(f"\nVerificando se [{nome}] enviou algo")
                encaminhar_mensagem(cliente[0], nome)

        except KeyboardInterrupt:
            print()
            for nome, cliente in list(clientes.items()):
                cliente[0].close()
                print(f"Cliente [{nome}] desconectado.")

            print("\nServidor encerrado")
            server_socket.close()
            break

iniciar_servidor()