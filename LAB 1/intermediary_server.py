import socket
import sys

#Intermediary server - client address
intermediary_ip = "localhost"
intermediary_port = 5001

def create_board(rows, cols):
    board = [[' ' for _ in range(cols)] for _ in range(rows)]
    return board

def check_winner(board):
    #Verify if board is full
    full = True
    for i in range(len(board[0])):
        if board[0][i] == ' ':
            full = False
            break
        
    # Verificy horizontally
    for row in board:
        for i in range(len(row) - 3):
            if row[i] == row[i + 1] == row[i + 2] == row[i + 3] and row[i] != ' ':
                return row[i]

    # Verify vertically
    for col in range(len(board[0])):
        for i in range(len(board) - 3):
            if board[i][col] == board[i + 1][col] == board[i + 2][col] == board[i + 3][col] and board[i][col] != ' ':
                return board[i][col]

    # Verify diagonal (left to right)
    for row in range(len(board) - 3):
        for col in range(len(board[0]) - 3):
            if board[row][col] == board[row + 1][col + 1] == board[row + 2][col + 2] == board[row + 3][col + 3] and board[row][col] != ' ':
                return board[row][col]

    # Verify diagonal (right to left)
    for row in range(len(board) - 3):
        for col in range(3, len(board[0])):
            if board[row][col] == board[row + 1][col - 1] == board[row + 2][col - 2] == board[row + 3][col - 3] and board[row][col] != ' ':
                return board[row][col]

    #If board full and no winner
    if full:
        return "Tie"
    
    #If board not full and no winner
    return None

def modify_board(board,col,player):
    col-=1
    done = False
    while not done:
        i = len(board[0])
        while i:
            if(board[i-1][col] == " "):
                board[i-1][col] = player
                break
            i-=1
        done = True
    return board

def check_playable(board):
    playable = ""
    for i in range(len(board[0])):
        if board[0][i] == ' ':
            playable += "1"
        else:
            playable += "0"
            
    return playable

def send_receive_udp_message(message,server_address = ('localhost', 12345)):
    # Crear un socket UDP
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    print(message)
    try:
        # Enviar una solicitud inicial al servidor
        print("A")
        sock.sendto(message.encode(), server_address)
        print("B")

        # Recibir la respuesta del servidor
        data, server = sock.recvfrom(1024)
        print("C")

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

def game(client_socket,bot_address):
    client = False
    bot = False
    tie = False
    board = create_board(6,6)
    
    #First turn
    client_play = receive_message(client_socket)
    board = modify_board(board,int(client_play),"X")
    
    while not client and not bot and not tie:
        #Receive bot_play and bot address
        playable = check_playable(board)
        response = send_receive_udp_message(playable,bot_address)
        response = response.split(",")
        bot_play = response[0]
        bot_ip = response[1]
        bot_port = int(response[2])
        bot_address = (bot_ip,bot_port)
        
        #Apply bot_play
        board = modify_board(board,int(bot_play),"O")
        
        #Check winner
        winner = check_winner(board)
        
        if winner == "O": #Bot wins
            bot = True
            break
        elif winner == "Tie": #Tie
            tie = True
            break
        
        #Send status to client
        send_message(client_socket,"Continue,"+bot_play)
        
        #Receive client play
        client_play = receive_message(client_socket)
        board = modify_board(board,int(client_play),"X")
        
        #Check winner
        winner = check_winner(board)
        
        if winner == "X": #Client wins
            client = True
            break
        elif winner == "Tie": #Tie
            tie = True
            break
        
        #Send status to client
        send_message(client_socket,"Continue")
    
    if client:
        send_message(client_socket,"You win")
    elif bot:
        send_message(client_socket,"Bot wins")
    elif tie:
        send_message(client_socket,"Tie")
        
        
    return bot_address

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
            connect4_port = int(response[2])
            connect4_address = (connect4_ip,connect4_port)
            
            #Send response to client
            send_message(client_socket,dispo)
            
            if dispo == "Ok":
                connect4_address = game(client_socket,connect4_address)
                break
            
            elif dispo == "No":
                break
    
    #Receive game end message from client
    message = receive_message(client_socket)
    
    #Send game end message to connect4_server
    response = send_receive_udp_message(message,connect4_address)
        
    #Send game end message from client
    send_message(client_socket,response)
            
    #disconnect to client.py
    disconnect(client_socket)
    disconnect(intermediary_socket)
    
    return

if __name__ == "__main__":
    main()