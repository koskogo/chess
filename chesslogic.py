from classes import *
import re
import os

currentPlayer = "White"


def create_initial_board():
    return [
        [rook("Black"), knight("Black"), bishop("Black"), queen("Black"), king("Black"), bishop("Black"), knight("Black"), rook("Black")],
        [pawn("Black"), pawn("Black"), pawn("Black"), pawn("Black"), pawn("Black"), pawn("Black"), pawn("Black"), pawn("Black")],
        [empty(), empty(), empty(), empty(), empty(), empty(), empty(), empty()],
        [empty(), empty(), empty(), empty(), empty(), empty(), empty(), empty()],
        [empty(), empty(), empty(), empty(), empty(), empty(), empty(), empty()],
        [empty(), empty(), empty(), empty(), empty(), empty(), empty(), empty()],
        [pawn("White"), pawn("White"), pawn("White"), pawn("White"), pawn("White"), pawn("White"), pawn("White"), pawn("White")],
        [rook("White"), knight("White"), bishop("White"), queen("White"), king("White"), bishop("White"), knight("White"), rook("White")]
    ]


chessBoard = create_initial_board()


def get_board_state():
    board = []
    for row in chessBoard:
        board_row = []
        for piece in row:
            if hasattr(piece, 'name'):
                if piece.name == '0':
                    board_row.append('0')
                else:
                    team_prefix = 'w' if getattr(piece, 'team', '') == 'White' else 'b'
                    board_row.append(f"{team_prefix}{piece.name}")
            else:
                board_row.append('0')
        board.append(board_row)
    return board


def wrongMove():
    return "Please enter a correct move like in the example."


def isChessSquare(s):
    pieces = {"k", "q", "r", "b", "n", "p"}
    if len(s) == 2:
        return bool(re.fullmatch(r"[a-h][1-8]", s.lower()))
    else:
        return len(s) == 1 and s.lower() in pieces


def fieldToIndex(Field):
    splitField = list(Field)
    splitField[0] = ord(splitField[0]) - ord("a")
    return splitField



def find_king(team, board):
    for r in range(8):
        for c in range(8):
            piece = board[r][c]
            if piece.name == 'K' and piece.team == team:
                return [r, c]
    return None


def is_square_attacked(target_rc, by_team, board):
    tr, tc = target_rc
    target_piece = board[tr][tc]
    for r in range(8):
        for c in range(8):
            piece = board[r][c]
            if piece.name == '0' or piece.team != by_team:
                continue
            if piece.legalMove([r, c], [tr, tc], by_team, target_piece, board):
                return True
    return False


def in_check(team, board):
    king_pos = find_king(team, board)
    if not king_pos:
        return False
    opponent = 'White' if team == 'Black' else 'Black'
    return is_square_attacked(king_pos, opponent, board)


def simulate_move_and_exposes_own_king(start_rc, end_rc, team, board):
    sr, sc = start_rc
    er, ec = end_rc
    moving_piece = board[sr][sc]
    captured = board[er][ec]
    board[er][ec] = moving_piece
    board[sr][sc] = empty()
    exposed = in_check(team, board)
    board[sr][sc] = moving_piece
    board[er][ec] = captured
    return exposed


def team_has_any_legal_move(team, board):
    for r in range(8):
        for c in range(8):
            piece = board[r][c]
            if piece.name == '0' or piece.team != team:
                continue
            for er in range(8):
                for ec in range(8):
                    end_piece = board[er][ec]
                    if end_piece.team == team:
                        continue
                    if piece.legalMove([r, c], [er, ec], team, end_piece, board):
                        if not simulate_move_and_exposes_own_king([r, c], [er, ec], team, board):
                            return True
    return False


def movePiece(move):
    global currentPlayer
    if not len(move) == 7:
        return wrongMove()
    splitMove = move.split(",")
    for i in splitMove:
        if not isChessSquare(i):
            return wrongMove()
    for i in range(2):
        splitMove[i + 1] = fieldToIndex(splitMove[i + 1])
    start1 = 8 - int(splitMove[1][1])
    start2 = int(splitMove[1][0])
    end1 = 8 - int(splitMove[2][1])
    end2 = int(splitMove[2][0])
    startField = chessBoard[start1][start2]
    endField = chessBoard[end1][end2]
    if not startField.name == splitMove[0].upper() or startField.name == "0" or not startField.team == currentPlayer or endField.team == currentPlayer:
        return wrongMove()
    if not startField.legalMove([start1, start2], [end1, end2], currentPlayer, endField, chessBoard):
        return wrongMove()

    # Disallow moves that leave or put your own king in check
    if simulate_move_and_exposes_own_king([start1, start2], [end1, end2], currentPlayer, chessBoard):
        return "Illegal move: your king would be in check."

    # Execute move
    chessBoard[end1][end2] = chessBoard[start1][start2]
    chessBoard[start1][start2] = empty()

    # Switch player
    previous_player = currentPlayer
    currentPlayer = "White" if currentPlayer == "Black" else "Black"

    # Check/checkmate evaluation for the player to move
    if in_check(currentPlayer, chessBoard):
        if not team_has_any_legal_move(currentPlayer, chessBoard):
            return f"Checkmate! {previous_player} wins."
        return f"Check! {currentPlayer} to move."

    return None


def get_current_player():
    return currentPlayer


def reset_game():
    global chessBoard, currentPlayer
    chessBoard = create_initial_board()
    currentPlayer = "White"
