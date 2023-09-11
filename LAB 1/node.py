import socket
import sys
import random

# Dirección IP y puerto del server intermediario
node_server_ip = "localhost"
node_server_port = 5001

host_server_ip = "localhost"
host_server_port = None

def connect_to_host(host_address):
    

    pass

def send_message(socket, message):
    socket.send(message.encode())
    return


def receive_message(socket):
    message = socket.recv(1024)
    message = message.decode()
    return message

def main():
    intermediary_server_address = (node_server_ip, node_server_port)
    intermediary_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    intermediary_server_socket.bind(intermediary_server_address)
    intermediary_server_socket.listen(1)
    print("Esperando conexiones de clientes...")
    
    while True:
        client_socket, client_address = intermediary_server_socket.accept()
        print("Conexión establecida con el cliente:", client_address)

        # Datos a enviar
        message = "Hola, servidor UDP en Go!"

        # Crear un socket UDP
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Enviar una solicitud al servidor Go para obtener el puerto
        request_message = "Obtener puerto"
        host_address = (host_server_ip, None)  # None inicialmente
        udp_socket.sendto(request_message.encode(), host_address)

        # Recibir el puerto del servidor
        data, server = udp_socket.recvfrom(1024)
        host_server_port = int(data.decode())  # Actualiza el puerto recibido

        # Mensaje a enviar al servidor Go
        message = "Hola, servidor UDP en Go!"

        # Establecer la dirección del servidor con el puerto recibido
        host_address = (host_server_ip, host_server_port)

        # Enviar datos al servidor
        udp_socket.sendto(message.encode(), host_address)

        # Recibir respuesta del servidor (si es necesario)
        data, server = udp_socket.recvfrom(1024)
        print(f"Respuesta del servidor ({server}): {data.decode()}")

        # Cerrar el socket UDP
        udp_socket.close()


        print("Conexión establecida con el servidor conecta4:", host_address)

        
        if udp_socket is None:
            print("No se pudo establecer conexión con el servidor conecta4.")
            client_socket.close()
            print("Conexión con el cliente cerrada.")
            break
        else:
            print("Conexión establecida con el servidor conecta4:", host_address)


        message = receive_message(udp_socket)
        print("\n\n"+message+"\n\n")
        
        #Cerrar la conexión con el cliente y cerrar el servidor
        if message == "OK":
            print("Jugando...")
            print("Jugando...")
            print("Jugando...")        
        else:
            client_socket.close()
            print("Conexión con el cliente cerrada.")
            break


        client_socket.close()
        print("Conexión con el cliente cerrada.")
        break


    intermediary_server_socket.close()
    print("Servidor cerrado.")
    return


if __name__ == "__main__":
    main()