from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

def check_winner(board, player):
    win_combos = [
        [0,1,2], [3,4,5], [6,7,8], # rows
        [0,3,6], [1,4,7], [2,5,8], # columns
        [0,4,8], [2,4,6]           # diagonals
    ]
    for combo in win_combos:
        if all(board[i] == player for i in combo):
            return True
    return False

def computer_move(board):
    empty = [i for i, spot in enumerate(board) if spot == '']
    if empty:
        return random.choice(empty)
    return -1

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/move', methods=['POST'])
def move():
    data = request.json
    board = data['board']
    board[data['userMove']] = 'X'

    if check_winner(board, 'X'):
        return jsonify({'board': board, 'status': 'You Win!'})

    if '' not in board:
        return jsonify({'board': board, 'status': 'Draw'})

    comp_index = computer_move(board)
    if comp_index != -1:
        board[comp_index] = 'O'

    if check_winner(board, 'O'):
        return jsonify({'board': board, 'status': 'Computer Wins!'})

    if '' not in board:
        return jsonify({'board': board, 'status': 'Draw'})

    return jsonify({'board': board, 'status': 'In Progress'})

if __name__ == '__main__':
    app.run(debug=True)
