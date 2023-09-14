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
        
    # Verify horizontally
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
        sock.sendto(message.encode(), server_address)

        # Recibir la respuesta del servidor
        data, server = sock.recvfrom(1024)

        # Decodificar y verificar la respuesta del servidor
        response = data.decode()
        print("Recibido: ", response, " de ", server)
        
    except Exception as e:
        print(e)
        
    finally:
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
    client_address = client_socket.getpeername()
    print("Recibido: ", client_play, " de ", client_address)
    board = modify_board(board,int(client_play)+1,"X")
    
    while not client and not bot and not tie:
        #Receive bot_play and bot address
        playable = check_playable(board)
        response = send_receive_udp_message(playable,bot_address)
        print ("Enviado: ", playable, " a ", bot_address)
        response = response.split(",")
        bot_play = response[0]
        bot_ip = response[1]
        bot_port = int(response[2])
        bot_address = (bot_ip,bot_port)
        
        #Apply bot_play
        board = modify_board(board,int(bot_play),"O")
        
        #Check winner
        winner = check_winner(board)
        #print(winner)
        
        if winner == "O": #Bot wins
            bot = True
            break
        elif winner == "Tie": #Tie
            tie = True
            break
        
        #Send status to client
        send_message(client_socket,"Continue,"+bot_play)
        print("Enviado: Continue,",bot_play," a ",client_address)
        
        #Receive client play
        client_play = receive_message(client_socket)
        board = modify_board(board,int(client_play)+1,"X")
        
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
        print ("Enviado: ", "You win", " a ", client_address)
    elif bot:
        send_message(client_socket,"Bot wins,"+bot_play)
        print ("Enviado: ", "Bot wins,"+bot_play, " a ", client_address)
    elif tie:
        send_message(client_socket,"Tie")
        print ("Enviado: ", "Tie", " a ", client_address)
    
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
        
        #Receive message from client
        solitude = receive_message(client_socket)
        print ("Recibido: ", solitude, " de ", client_address)
        
        if solitude == "Iniciar juego":
            #Send solitude and receive response from connect4_server.go
            response = send_receive_udp_message(solitude)
            print ("Enviado: ", solitude, " a localhost:12345")
            response = response.split(",")
            
            dispo = response[0]
            
            connect4_ip = response[1]
            connect4_port = int(response[2])
            connect4_address = (connect4_ip,connect4_port)
            
            #Send response to client
            send_message(client_socket,dispo)
            print ("Enviado: ", dispo, " a ", client_address)
            
            if dispo == "Ok":
                connect4_address = game(client_socket,connect4_address)
                #Receive game end message from client
                solitude = receive_message(client_socket)
                print ("Recibido: ", solitude, " de ", client_address)
                break
            
            elif dispo == "No":
                break
        elif solitude == "Terminar":
            connect4_address = ("localhost",12345)
            break
    
    #Send game end message to connect4_server
    response = send_receive_udp_message(solitude,connect4_address)
    print ("Enviado: ", response, " a ", connect4_address)
    
    #Send game end message from client
    send_message(client_socket,response)
    print ("Enviado: ", response, " a ", client_address)
            
    #disconnect to client.py
    disconnect(client_socket)
    disconnect(intermediary_socket)
    
    return

if __name__ == "__main__":
    main()