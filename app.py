
from flask import Flask, render_template, request, redirect, url_for, jsonify
from chesslogic import get_board_state, movePiece, get_current_player, reset_game

app = Flask(__name__)

@app.route('/')
def root():
    return redirect(url_for('drag_ui'))

@app.route('/text', methods=['GET', 'POST'])
def text_ui():
    message = None
    if request.method == 'POST':
        move = request.form.get('move')
        result = movePiece(move)
        if result:
            message = result
        else:
            message = f"Move successful! Now it's {get_current_player()}'s turn."
    board = get_board_state()
    current_player = get_current_player()
    return render_template('index.html', board=board, message=message, current_player=current_player)

@app.route('/drag')
def drag_ui():
    board = get_board_state()
    current_player = get_current_player()
    return render_template('drag.html', board=board, current_player=current_player)

@app.route('/api/move', methods=['POST'])
def api_move():
    data = request.get_json(silent=True) or {}
    source = data.get('from')  # e.g., 'e2'
    target = data.get('to')    # e.g., 'e4'
    piece_letter = data.get('piece')  # optional override

    if not source or not target:
        return jsonify({"error": "Missing from/to"}), 400

    board_state = get_board_state()
    try:
        s_file = ord(source[0].lower()) - ord('a')
        s_rank = int(source[1])
        row = 8 - s_rank
        col = s_file
        sprite = board_state[row][col]
        if sprite == '0':
            return jsonify({"error": "No piece at source"}), 400
        inferred_letter = sprite[1]
        piece_letter = piece_letter or inferred_letter
    except Exception:
        return jsonify({"error": "Invalid coordinates"}), 400

    move_str = f"{piece_letter.upper()},{source},{target}"
    result = movePiece(move_str)

    board = get_board_state()
    message = result or "OK"
    is_checkmate = isinstance(result, str) and result.startswith("Checkmate!")
    response = {
        "board": board,
        "current_player": get_current_player(),
        "message": message,
        "checkmate": is_checkmate
    }
    status = 200 if result is None or (isinstance(result, str) and result.startswith("Check")) else 400
    return jsonify(response), status

@app.route('/reset', methods=['POST'])
def reset():
    reset_game()
    return jsonify({
        "board": get_board_state(),
        "current_player": get_current_player()
    })

if __name__ == '__main__':
    app.run(debug=True)
