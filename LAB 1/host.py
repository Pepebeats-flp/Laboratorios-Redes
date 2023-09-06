import socket

def create_board(rows, cols):
    board = [[' ' for _ in range(cols)] for _ in range(rows)]
    return board

def modify_board(board, col, player):
    if(board[0][col] != " "):
        print("Columna llena, seleccione otra.")
        return board,False
    i = len(board[0])
    while i:
        if(board[i][col] == " "):
            board[i][col] = player
            break
        i-=1
    return board,True

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
    
    return


if __name__ == "__main__":
    main()