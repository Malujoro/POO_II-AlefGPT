import socket
import time

HOST = '127.0.0.1'
PORT = 7000
ADDR = (HOST, PORT)

PALAVROES = {'batutinha', 'prolog'}
banidos = {}  

def censurar_mensagem(mensagem):
    for palavra in PALAVROES:
        mensagem = mensagem.replace(palavra, '*' * len(palavra))
    return mensagem

def verificar_banimento(cliente, mensagem):
    if any(palavra in mensagem for palavra in PALAVROES):
        banidos[cliente] = banidos.get(cliente, 0) + 1
        if banidos[cliente] >= 3:
            return True
    return False

def iniciar_servidor():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(ADDR)
    server_socket.listen(3)  
    print(f"servidor rodando na porta {PORT}")

    while True:
        con, endereco = server_socket.accept()
        print(f"cliente {endereco} conectado.")

        while True:
            msg = con.recv(1024).decode()
            if not msg:
                break

            mensagem_censurada = censurar_mensagem(msg)
            if verificar_banimento(endereco, msg):
                con.send("você foi banido por enviar mensagens proibidas.".encode())
                break
            else:
                con.send("mensagem enviada com sucesso".encode())

            print(f"mensagem de {endereco}: {mensagem_censurada}")

        con.close()
        print(f"cliente {endereco} desconectado.")

iniciar_servidor()
