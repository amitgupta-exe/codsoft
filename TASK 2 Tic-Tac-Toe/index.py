import tkinter as tk
import math

# Function to check for a win
def check_win(board, player):
    win_states = [
        [board[0][0], board[0][1], board[0][2]],
        [board[1][0], board[1][1], board[1][2]],
        [board[2][0], board[2][1], board[2][2]],
        [board[0][0], board[1][0], board[2][0]],
        [board[0][1], board[1][1], board[2][1]],
        [board[0][2], board[1][2], board[2][2]],
        [board[0][0], board[1][1], board[2][2]],
        [board[0][2], board[1][1], board[2][0]]
    ]
    return [player, player, player] in win_states

# Function to check for a draw
def check_draw(board):
    for row in board:
        if " " in row:
            return False
    return True

# Function to get the available moves
def get_available_moves(board):
    moves = []
    for i in range(3):
        for j in range(3):
            if board[i][j] == " ":
                moves.append((i, j))
    return moves

# Minimax algorithm with Alpha-Beta pruning
def minimax(board, depth, is_maximizing, alpha, beta):
    if check_win(board, "X"):
        return -10 + depth
    if check_win(board, "O"):
        return 10 - depth
    if check_draw(board):
        return 0

    if is_maximizing:
        max_eval = -math.inf
        for move in get_available_moves(board):
            board[move[0]][move[1]] = "O"
            eval = minimax(board, depth + 1, False, alpha, beta)
            board[move[0]][move[1]] = " "
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = math.inf
        for move in get_available_moves(board):
            board[move[0]][move[1]] = "X"
            eval = minimax(board, depth + 1, True, alpha, beta)
            board[move[0]][move[1]] = " "
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

# Function for the AI to make a move
def ai_move(board, buttons, status_label):
    best_score = -math.inf
    best_move = None
    for move in get_available_moves(board):
        board[move[0]][move[1]] = "O"
        score = minimax(board, 0, False, -math.inf, math.inf)
        board[move[0]][move[1]] = " "
        if score > best_score:
            best_score = score
            best_move = move
    board[best_move[0]][best_move[1]] = "O"
    buttons[best_move[0]][best_move[1]].config(text="O", state="disabled")
    if check_win(board, "O"):
        status_label.config(text="AI wins!")
    elif check_draw(board):
        status_label.config(text="It's a draw!")
    else:
        status_label.config(text="Your turn")

# Function for the human to make a move
def human_move(row, col, board, buttons, status_label):
    if board[row][col] == " ":
        board[row][col] = "X"
        buttons[row][col].config(text="X", state="disabled")
        if check_win(board, "X"):
            status_label.config(text="You win!")
        elif check_draw(board):
            status_label.config(text="It's a draw!")
        else:
            status_label.config(text="AI's turn")
            ai_move(board, buttons, status_label)

# Main game function to set up the GUI
def play_game():
    board = [[" " for _ in range(3)] for _ in range(3)]
    
    root = tk.Tk()
    root.title("Tic-Tac-Toe")
    
    status_label = tk.Label(root, text="Your turn", font=('Arial', 20))
    status_label.grid(row=0, column=0, columnspan=3)
    
    buttons = [[None for _ in range(3)] for _ in range(3)]
    
    for i in range(3):
        for j in range(3):
            buttons[i][j] = tk.Button(root, text=" ", font=('Arial', 40), width=5, height=2,
                                      command=lambda row=i, col=j: human_move(row, col, board, buttons, status_label))
            buttons[i][j].grid(row=i+1, column=j)
    
    root.mainloop()

play_game()
