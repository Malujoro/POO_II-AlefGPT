import socket
host = ''
port = 9000
addr = (host, port)
serv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #cria o socket
serv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #reiniciliza o socket
serv_socket.bind(addr) #define a porta e quais ips podem se conectar com o servidor
serv_socket.listen(10) #define o limite de conexoes
print ('aguardando conexao')
con1, cliente1 = serv_socket.accept()  # servidor aguardando conexao
print('cliete2')
con2, cliente2 = serv_socket.accept()  # servidor aguardando conexao
print('conectado')
print('aguardando mensagem')

while(True):
    recebe = con1.recv(1024) #define que os pacotes recebidos sao de ate 1024 bytes
    print ('mensagem recebida: '+ recebe.decode())
    con1.send('mensagem recebida '.encode())
    con2.send(recebe)

serv_socket.close()


