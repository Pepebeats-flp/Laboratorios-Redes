import socket
import sys

#Intermediary server - client address
intermediary_ip = "localhost"
intermediary_port = 5001

def send_receive_udp_message(message,server_address = ('localhost', 12345)):
    # Crear un socket UDP
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        # Enviar una solicitud inicial al servidor
        sock.sendto(message.encode(), server_address)

        # Recibir la respuesta del servidor
        data, server = sock.recvfrom(1024)

        # Decodificar y verificar la respuesta del servidor
        response = data.decode()
        print("Respuesta del servidor: {}".format(response))
    except Exception as e:
        print(e)
    finally:
        print("Cerrando conexión UDP")
        sock.close()
    return response

def disconnect(socket):
    socket.close()
    return

def send_message(socket, message):
    socket.send(message.encode())
    return

def receive_message(socket):
    message = socket.recv(1024)
    message = message.decode()
    return message

def game():
    print("jugando jaja")
    return

def main():
    intermediary_address = (intermediary_ip, intermediary_port)
    intermediary_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    intermediary_socket.bind(intermediary_address)
    intermediary_socket.listen(1)
    print("Esperando conexiones de clientes...")
    
    while True:
        client_socket, client_address = intermediary_socket.accept()
        print("Conexión establecida con el cliente:", client_address)
        
        #UDP connection with connect4_server.go
        
        #Receive message from client
        solitude = receive_message(client_socket)
        
        if solitude == "Iniciar juego":
            #Send solitude and receive response from connect4_server.go
            response = send_receive_udp_message(solitude)
            response = response.split(",")
            
            dispo = response[0]
            
            connect4_ip = response[1]
            connect4_port = response[2]
            connect4_address = (connect4_ip,connect4_port)
            
            #Send response to client
            send_message(client_socket,dispo)
            
            if dispo == "Ok":
                game()
                break
            
            elif dispo == "No":
                break
            
    #disconnect to client.py
    disconnect(client_socket)
    disconnect(intermediary_socket)
    
    return

if __name__ == "__main__":
    main()