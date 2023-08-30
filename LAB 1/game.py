import socket


# Dirección IP y puerto del servidor intermediario
intermediary_server_ip = "192.168.1.12"
intermediary_server_port = 5000


def connect_to_server(server_address):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(server_address)
    print("respuesta de disponibilidad: OK")
    return client_socket

def send_message(socket, message):
    # Implementa aquí el código para enviar mensajes al servidor
    pass

def receive_message(socket):
    # Implementa aquí el código para recibir mensajes del servidor
    pass

def create_board(rows, cols):
    board = [[' ' for _ in range(cols)] for _ in range(rows)]
    return board

def print_board(board):
    cols = len(board[0])
    col_numbers = " ".join(str(i) for i in range(1, cols + 1))
    print("  " + col_numbers)
    
    for row_number, row in enumerate(board, start=1):
        row_str = " ".join(cell for cell in row)
        print(f"{row_number}|{row_str}")
        print("-" * (cols * 2 - 1))

def modify_board(board, x, y, player):
    board[x-1][y-1] = player
    return board

def check_winner(board):
    for row in board:
        if row.count(row[0]) == len(row) and row[0] != ' ':
            return True

    for col in range(len(board[0])):
        check = []
        for row in board:
            check.append(row[col])
        if check.count(check[0]) == len(check) and check[0] != ' ':
            return True
        
    diagonal1 = []
    for idx, reverse_idx in enumerate(reversed(range(len(board)))):
        diagonal1.append(board[idx][reverse_idx])
    if diagonal1.count(diagonal1[0]) == len(diagonal1) and diagonal1[0] != ' ':
        return True

    diagonal2 = []
    for ix in range(len(board)):
        diagonal2.append(board[ix][ix])
    if diagonal2.count(diagonal2[0]) == len(diagonal2) and diagonal2[0] != ' ':
        return True

    return False


def main():
    server_address = (intermediary_server_ip, intermediary_server_port)
    client_socket = connect_to_server(server_address)
    try:
        while True:
            print("- - - - - - - - Bienvenido al Juego - - - - - - - -")
            print("Seleccione una opción:")
            print("1-Jugar")
            print("2-Salir")
            
            choice = input(">>")
            
            if choice == "1":
                connect_to_server(server_address)
                board=create_board(6,6)
                print("- - - - - - - - Comienza el Juego - - - - - - - -")
                print_board(board)
                print("Seleccione un x:")
                x = int(input(">>"))
                print("Seleccione un y:")
                y = int(input(">>"))
                board=modify_board(board, x, y, "X")
                print_board(board)
                if (check_winner(board) == True):
                    print("Ganaste")
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

