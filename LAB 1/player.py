import socket
import sys

# Dirección IP y puerto del servidor intermediario
intermediary_server_ip = "192.168.1.12"
intermediary_server_port = 5000

def connect_to_server(server_address):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Conectar el socket del cliente con el servidor en el puerto indicado
        client_socket.connect(server_address)
        print("Mati chupame el pico")
    except socket.error as message:
        print("Falló la conexión con el servidor {} por el puerto {}".format(server_address[0], server_address[1]))
        print(message)
        sys.exit()
    return client_socket

def send_message(socket, message):
    # Enviar mensaje
    socket.send(message.encode())
    return

def receive_message(socket):
    message = socket.recv(1024)
    message = message.decode()
    return message

def disconnect_to_server(socket):
    socket.close()


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
    server_address = (intermediary_server_ip, intermediary_server_port)
    client_socket = connect_to_server(server_address)
    print("Mati chupame el pico")
    
    try:
        print("Mati chupame el pico")
        while True:
            print("- - - - - - - - Bienvenido al Juego - - - - - - - -")
            print("- Seleccione una opción:")
            print("1-Jugar")
            print("2-Salir")
            
            choice = input(">>")
            
            if choice == "1":
                connect_to_server(server_address)
                board=create_board(6,6)
                '''
                print("- - - - - - - - Comienza el Juego - - - - - - - -")
                col = int(input(">>"))
                #print("Seleccione un y:")
                #y = int(input(">>"))
                played = False
                while not played:
                    print_board(board)
                    print("Seleccione columna:")
                    board,played=modify_board(board, col, "X")
                print_board(board)
                if (check_winner(board) == True):
                    print("Ganaste")
                    '''
                pass
                
            elif choice == "2":
                print("Saliendo del juego.")
                break
                
            else:
                print("Opción inválida. Por favor, elija nuevamente.")

    except Exception as e:
        print("Error al conectar con el servidor:", e)
    
    finally:
        client_socket.close()

if __name__ == "__main__":
    main()