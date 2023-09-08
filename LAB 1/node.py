import socket
import sys
import random

# Dirección IP y puerto del cliente
client_server_ip = "localhost" #vacío para localhost
client_server_port = 5001

# Dirección IP y puerto del servidor host
host_server_ip = "" #vacío para localhost
host_server_port = 5001

def connect_to_client(client_address):
    node_to_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        node_to_client_socket.connect(client_address)
    except socket.error as message:
        print("Error al conectar al cliente en la dirección:", client_address)
        print(message)
        sys.exit()
    
    print("Conectado al cliente en la dirección:", client_address)
    
    return node_to_client_socket

def send_message(socket, message):
    socket.send(message.encode())
    return


def receive_message(socket):
    message = socket.recv(1024)
    message = message.decode()
    return message

def connect_to_connecta4_server(connecta4_server_address):
    # Implementa aquí el código para establecer la conexión UDP con el Servidor Conecta4
    pass

def main():
    intermediary_server_address = (host_server_ip, host_server_port)
    intermediary_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    intermediary_server_socket.bind(intermediary_server_address)
    intermediary_server_socket.listen(1)
    print("Esperando conexiones de clientes...")
    
    while True:
        client_socket, client_address = intermediary_server_socket.accept()
        print("Conexión establecida con el cliente:", client_address)

        # Conexion con el conecta4 server
        '''
        connecta4_server_address = ('connecta4_server_ip', client_server_port)
        connecta4_server_socket = connect_to_connecta4_server(connecta4_server_address)
        '''
        randint = random.randint(0, 1)
        if randint == 0:
            menssage = "NO"

        else:
            menssage = "OK"

        send_message(client_socket, menssage)
        print("respuesta de disponibilidad:", menssage)
        
        #Cerrar la conexión con el cliente y cerrar el servidor
        if menssage == "NO":
            client_socket.close()
            print("Conexión con el cliente cerrada.")
            break
        
        elif menssage == "OK":
            print("Jugando...")
            print("Jugando...")
            print("Jugando...")


        client_socket.close()
        print("Conexión con el cliente cerrada.")
        break


    intermediary_server_socket.close()
    print("Servidor cerrado.")
    return


if __name__ == "__main__":
    main()