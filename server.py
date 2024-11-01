import socket
import threading

HOST = '127.0.0.1'
PORT = 7000
ADDR = (HOST, PORT)

PALAVROES = {'batutinha', 'prolog'}
banidos = {}
clientes = {}

def censurar_mensagem(mensagem):
    for palavra in PALAVROES:
        mensagem = mensagem.replace(palavra, '*' * len(palavra))
    return mensagem

# função que verifica banimento
def verificar_banimento(cliente, mensagem):
    if any(palavra in mensagem for palavra in PALAVROES):
        banidos[cliente] = banidos.get(cliente, 0) + 1
        if banidos[cliente] >= 3:
            return True
    return False

# função para gerenciar cada cliente em uma thread
def handle_client(con, endereco):
    print(f"Cliente {endereco} conectado.")
    clientes[endereco] = con  # armazena cada conexão do cliente

    try:
        while True:
            dados = con.recv(1024).decode()
            if not dados:
                break

            if ':' not in dados:
                con.send("Formato inválido. Use 'destino:mensagem'.".encode())
                continue
            
            destino_str, mensagem = dados.split(':', 1)
            destino = eval(destino_str)  # converte a string para tupla

            # censura e verifica banimento
            mensagem_censurada = censurar_mensagem(mensagem)
            if verificar_banimento(endereco, mensagem):
                con.send("Você foi banido por enviar mensagens proibidas.".encode())
                break

            # envia a mensagem ao destino
            if destino in clientes:
                clientes[destino].send(f"Mensagem de {endereco}: {mensagem_censurada}".encode())
                con.send("Mensagem enviada com sucesso.".encode())
            else:
                con.send("Destinatário não encontrado.".encode())

            print(f"Mensagem de {endereco} para {destino}: {mensagem_censurada}")

    finally:
        del clientes[endereco]
        con.close()
        print(f"Cliente {endereco} desconectado.")


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
