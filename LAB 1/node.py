import socket
import sys
import random

# Dirección IP y puerto del server intermediario
node_server_ip = "localhost"
node_server_port = 5001

host_server_port = random.randint(8000, 65535)

def connect_to_host(host_address):
    # Datos a enviar
    message = "Hola, servidor UDP en Go!"

    # Crear un socket UDP
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        # Enviar datos al servidor
        udp_socket.sendto(message.encode(), host_address)

        # Esperar una respuesta
        data, server = udp_socket.recvfrom(1024)
        print(f"Respuesta del servidor ({server}): {data.decode()}")
    finally:
        udp_socket.close()
    
    return data

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
    intermediary_server_address = (node_server_ip, node_server_port)
    intermediary_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    intermediary_server_socket.bind(intermediary_server_address)
    intermediary_server_socket.listen(1)
    print("Esperando conexiones de clientes...")
    
    while True:
        client_socket, client_address = intermediary_server_socket.accept()
        print("Conexión establecida con el cliente:", client_address)

        # Conexion con el conecta4 server
        connecta4_server_address = (node_server_ip,host_server_port)
        connecta4_server_socket = connect_to_connecta4_server(connecta4_server_address)

        print("Conexión establecida con el servidor conecta4:", connecta4_server_address)

        if connecta4_server_socket is None:
            print("No se pudo establecer conexión con el servidor conecta4.")
            client_socket.close()
            print("Conexión con el cliente cerrada.")
            break
        else:
            print("Conexión establecida con el servidor conecta4:", connecta4_server_address)


        
        
        #Cerrar la conexión con el cliente y cerrar el servidor
        if message == "NO":
            client_socket.close()
            print("Conexión con el cliente cerrada.")
            break
        
        elif message == "OK":
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