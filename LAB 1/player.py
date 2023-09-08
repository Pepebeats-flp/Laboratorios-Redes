import socket
import sys

# Dirección IP y puerto del servidor intermediario
intermediary_server_ip = "192.168.1.12"
intermediary_server_port = 5001


# Conecta con el servidor intermediario
def connect_to_server(server_address):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # Conectar el socket del cliente con el servidor en el puerto indicado
        client_socket.connect(server_address)
    except socket.error as message:
        print("Falló la conexión con el servidor {} por el puerto {}".format(server_address[0], server_address[1]))
        print(message)
        sys.exit()
    return client_socket


def send_message(socket, message):
    socket.send(message.encode())
    return

def receive_message(socket):
    message = socket.recv(1024)
    message = message.decode()
    return message

def disconnect_to_server(socket):
    socket.close()
    return


def menu():
    try:
        while True:
            print("- - - - - - - - Bienvenido al Juego - - - - - - - -")
            print("- Seleccione una opción:")
            print("1-Jugar")
            print("2-Salir")
            
            choice = input(">>")
            if choice == "1":
                # Iniciamos conexión con el servidor intermediario
                server_address = (intermediary_server_ip, intermediary_server_port)
                client_socket = connect_to_server(server_address)

                # Enviamos mensaje de disponibilidad
                send_message(client_socket, "disponible")

                # Recibimos respuesta de disponibilidad
                response = receive_message(client_socket)

                if response == "NO":
                    print("respuesta de disponibilidad:", response)
                    print("El servidor no está disponible. Intente más tarde.")
                    disconnect_to_server(client_socket)
                    break
                

                elif response == "OK":
                    print("respuesta de disponibilidad:", response)
                    print("- - - - - - - - Comienza el Juego - - - - - - - -")
                    print("Jugando...")
                    print("Jugando...")
                    print("Jugando...")
            
            
                    # Cerramos la conexión con el servidor
                    disconnect_to_server(client_socket)
                    print("Saliendo del juego.")
                    break

            elif choice == "2":
                print("Saliendo del juego.")
                break
                
            else:
                print("Opción inválida. Por favor, elija nuevamente.")

    except Exception as e:
        print("Error al conectar con el servidor:", e)
        sys.exit()
    return
    

def print_board(board):
    cols = len(board[0])
    col_numbers = " ".join(str(i) for i in range(1, cols + 1))
    print("  " + col_numbers)
    
    for row_number, row in enumerate(board, start=1):
        row_str = " ".join(cell for cell in row)
        print(f"{row_number}|{row_str}")
        print("-" * (cols * 2 - 1))
    return

def main():
    menu()
    return

if __name__ == "__main__":
    main()