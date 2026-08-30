import math

# Board setup
board = [" " for _ in range(9)]

def print_board():
    print()
    for i in range(3):
        print("|".join(board[i*3:(i+1)*3]))
        if i < 2:
            print("-"*5)
    print()

def check_winner(b, player):
    win_conditions = [
        [0,1,2], [3,4,5], [6,7,8],  # rows
        [0,3,6], [1,4,7], [2,5,8],  # cols
        [0,4,8], [2,4,6]            # diagonals
    ]
    for cond in win_conditions:
        if b[cond[0]] == b[cond[1]] == b[cond[2]] == player:
            return True
    return False

def is_full(b):
    return " " not in b

# Minimax Algorithm
def minimax(b, depth, is_maximizing):
    if check_winner(b, "O"):
        return 1
    if check_winner(b, "X"):
        return -1
    if is_full(b):
        return 0

    if is_maximizing:
        best = -math.inf
        for i in range(9):
            if b[i] == " ":
                b[i] = "O"
                score = minimax(b, depth + 1, False)
                b[i] = " "
                best = max(score, best)
        return best
    else:
        best = math.inf
        for i in range(9):
            if b[i] == " ":
                b[i] = "X"
                score = minimax(b, depth + 1, True)
                b[i] = " "
                best = min(score, best)
        return best

# AI move
def best_move():
    best_score = -math.inf
    move = -1
    for i in range(9):
        if board[i] == " ":
            board[i] = "O"
            score = minimax(board, 0, False)
            board[i] = " "
            if score > best_score:
                best_score = score
                move = i
    return move

# Game loop
def play():
    print("You are X, AI is O")
    print_board()

    while True:
        # Human move
        user = int(input("Enter position (1-9): ")) - 1
        if board[user] != " ":
            print("Invalid move!")
            continue
        board[user] = "X"

        if check_winner(board, "X"):
            print_board()
            print("You Win!")
            break

        if is_full(board):
            print_board()
            print("Draw!")
            break

        # AI move
        ai = best_move()
        board[ai] = "O"
        print("AI played:")
        print_board()

        if check_winner(board, "O"):
            print("AI Wins!")
            break

        if is_full(board):
            print("Draw!")
            break

# Run the game
play()