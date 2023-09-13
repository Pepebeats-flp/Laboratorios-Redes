import socket
import sys

intermediary_ip = "localhost"
intermediary_port = 5001

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
    return

def modify_board(board,col,player):
    col-=1
    done = False
    while not done:
        if(board[0][col] != " "):
            print("Columna llena, seleccione otra.")
            col = int(input(">>"))-1
            continue
        i = len(board[0])
        while i:
            if(board[i-1][col] == " "):
                board[i-1][col] = player
                break
            i-=1
        done = True
    return board,col

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

def disconnect_to_server(socket):
    socket.close()
    return

def send_message(socket, message):
    socket.send(message.encode())
    return

def receive_message(socket):
    message = socket.recv(1024)
    message = message.decode()
    return message

def game(intermediary_socket):
    win = False
    lose = False
    tie = False
    my_board = create_board(6,6)
    
    #First turn
    print("------ Mi tablero ------")
    print_board(my_board)
    print("Ingrese columna:")
    column = input(">>")

    my_board,column = modify_board(my_board,int(column),"X")
    
    #Send play to intermediary server
    send_message(intermediary_socket,str(column))
    
    while not win and not tie and not lose:
        #receive status and bot play
        print("A")
        response = receive_message(intermediary_socket)
        print("B")
        response = response.split(",")
        print(response)
        status = response[0]
        bot_play = response[1]
        print("C")
        
        #Update board with bot play
        my_board,bot_play = modify_board(my_board,bot_play,"O")
        
        if status == "Bot wins":
            lose = True
            break
        elif status == "Tie":
            tie = True
            break
        
        #Client turn
        print("------ Mi tablero ------")
        print_board(my_board)
        print("Ingrese columna:")
        column = input(">>")
        my_board,column = modify_board(my_board,int(column),"X")
        
        #Send play to intermediary server
        send_message(intermediary_socket,column)
        
        #Receive status
        status = receive_message(intermediary_socket)
        
        if status == "You win":
            win = True
        elif status == "Tie":
            tie = True
        
    print("------ Mi tablero ------")
    print_board(my_board)
    
    if win:
        print("¡Ganaste!")
    elif lose:
        print("Bot gana")
    elif tie:
        print("Empate")
    
    return

def main():
    try:
        while True:
            print("- - - - - - - - Bienvenido al Juego - - - - - - - -")
            print("- Seleccione una opción:")
            print("1-Jugar")
            print("2-Salir")
            
            choice = input(">>")
            
            if choice == "1": #Jugar
                #Connect to intermediary server
                intermediary_address = (intermediary_ip,intermediary_port)
                intermediary_socket = connect_to_server(intermediary_address)
                
                #Request to start the game
                send_message(intermediary_socket, "Iniciar juego")
                
                #Get response from server
                response = receive_message(intermediary_socket)
                
                if response == "Ok":
                    #Game logic
                    print("Iniciando juego...")
                    game(intermediary_socket)
                    break
                
                elif response == "No":
                    print("Servidor no disponible. Inténtelo más tarde.")
                    break
                
            elif choice == "2":#Salir
                break
            else:
                print("Entrada incorrecta, inténtelo nuevamente.")
        
        print("Saliendo del juego...")
        
        #Send message of game end to server
        send_message(intermediary_socket,"Terminar")
        
        #Receive response from server
        response = (intermediary_socket)
        
        if response == "Terminar":
            disconnect_to_server(intermediary_socket)
    
    except Exception as e:
        print("Error al conectar con el servidor:", e)
        sys.exit()
        
    return


if __name__ == "__main__":
    main()