import socket

# Define o endereço e porta do servidor
HOST = '127.0.0.1'
PORT = 7000
ADDR = (HOST, PORT)

# Define as palavras proibidas no chat
PALAVROES = ['batutinha', 'prolog']
# Define um dicionário com o Cliente e o número de banimentos
banidos = {}
# Define um dicionário com o IP e Porta dos clientes
clientes = {}

# Função para censurar uma mensagem
def censurar_mensagem(mensagem):
    mensagem = mensagem.lower()
    for palavra in PALAVROES:
        mensagem = mensagem.replace(palavra.lower(), '*' * len(palavra))
    return mensagem

# Função para verificar palavras proibidas na mensagem do cliente (e efetuar um banimento)
def verificar_banimento(cliente, mensagem):
    if(any(palavra in mensagem for palavra in PALAVROES)):
        banidos[cliente] = banidos.get(cliente, 0) + 1
        if(banidos[cliente] >= 3):
            return True
    return False

# Função para gerenciar cada cliente em uma thread
def encaminhar_mensagem(con, nome_remetente):
    try:
        while True:
            dados = con.recv(1024).decode()
            if(not dados):
                break

            if(':' not in dados):
                con.send("Formato inválido. Use 'destino:mensagem'.".encode())
                continue

            nome_destino, mensagem = dados.split(':', 1)
            nome_destino = nome_destino.lower()

            # Censura e verifica banimento
            mensagem_censurada = censurar_mensagem(mensagem)
            if(verificar_banimento(nome_remetente, mensagem)):
                con.send("Você foi banido por enviar mensagens proibidas.".encode())
                break

            # Envia a mensagem ao destino
            if(nome_destino in clientes.keys()):
                con.send(f"Mensagem de {nome_remetente}: {mensagem_censurada}".encode())
                con.send("Mensagem enviada com sucesso.".encode())
            else:
                con.send("Destinatário não encontrado.".encode())

            print(f"Mensagem de {nome_remetente} para {nome_destino}: {mensagem_censurada}")

    finally:
        del clientes[nome_remetente]
        # con.close()
        print(f"Cliente {nome_remetente} desconectado.")

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
                con, endereco = server_socket.accept()

                con.settimeout(2)
                nome_usuario = con.recv(1024).decode().lower()
                clientes[nome_usuario] = (con, endereco)
                print(f"Cliente {nome_usuario} conectado.")
            except socket.timeout:
                pass

            for nome, cliente in clientes.items():
                try:
                    encaminhar_mensagem(cliente[0], nome)
                except socket.timeout:
                    pass

        except KeyboardInterrupt:
            print("\nServidor encerrado")
            for client_socket in clientes:
                client_socket.close()
            server_socket.close()
            break

iniciar_servidor()