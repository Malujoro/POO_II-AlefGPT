import socket
host = '127.0.0.1'
port = 9000
addr = (host, port)
serv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #cria o socket
serv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #reiniciliza o socket
serv_socket.bind(addr) #define a porta e quais ips podem se conectar com o servidor
serv_socket.listen(10) #define o limite de conexoes
print ('aguardando conexao')
con, cliente = serv_socket.accept()  # servidor aguardando conexao
print('conectado')
print('aguardando mensagem')

while(True):
    recebe = con.recv(1024) #define que os pacotes recebidos sao de ate 1024 bytes
    con.send('teste'.encode())
    print ('mensagem recebida: '+ recebe.decode())
serv_socket.close()
