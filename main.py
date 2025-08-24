from classes import *
from colorama import Fore, Back, Style
import re
import os

currentPlayer = "White"
chessBoard = [
    [rook("Black"), knight("Black"), bishop("Black"), queen("Black"), king("Black"), bishop("Black"), knight("Black"),
     rook("Black")],
    [pawn("Black"), pawn("Black"), pawn("Black"), pawn("Black"), pawn("Black"), pawn("Black"), pawn("Black"),
     pawn("Black")],
    [empty(), empty(), empty(), empty(), empty(), empty(), empty(), empty()],
    [empty(), empty(), empty(), empty(), empty(), empty(), empty(), empty()],
    [empty(), empty(), empty(), empty(), empty(), empty(), empty(), empty()],
    [empty(), empty(), empty(), empty(), empty(), empty(), empty(), empty()],
    [pawn("White"), pawn("White"), pawn("White"), pawn("White"), pawn("White"), pawn("White"), pawn("White"),
     pawn("White")],
    [rook("White"), knight("White"), bishop("White"), queen("White"), king("White"), bishop("White"), knight("White"),
     rook("White")]
]

def wrongMove():
    input("pls entere a correct move like in the example\n press enter to try again")

def isChessSquare(s):
    pieces = {"k", "q", "r", "b", "n", "p"}
    if len(s)==2:
        return bool(re.fullmatch(r"[a-h][1-8]", s.lower()))
    else:
        return len(s) == 1 and s.lower() in pieces

def fieldToIndex(Field):
    splitField = list(Field)
    splitField[0] = ord(splitField[0]) - ord("a")
    return splitField

def createBoard():
    os.system('cls')
    print(f'its {currentPlayer}s turn')
    for row in chessBoard:
        currentRow = []
        for piece in row:
            if piece.team == "White":
                currentRow.append((piece.name, Fore.BLUE))
            elif piece.team == "Black":
                currentRow.append((piece.name, Fore.GREEN))
            else:
                currentRow.append((piece.name, Fore.BLACK))
        currentRow.append(8 - (chessBoard.index(row)))

        for item in currentRow:
            if isinstance(item, tuple):
                piece, color = item
                print(color + piece + Style.RESET_ALL, end=" ")
            else:
                print(str(item), end=" ")  # print raw int or unexpected types
        print()
    labels = ["a", "b", "c", "d", "e", "f", "g", "h"]
    print(" ".join(labels))
    move = input(f'its {currentPlayer}s turn to make a move write the move in the following notation:\nLetter of piece,position of piece,position of target\nfor example P,e2,e4')
    return move

def movePiece(move):
    if not len(move) == 7:
        wrongMove()
        return 0
    splitMove = move.split(",")
    for i in splitMove:
        if not isChessSquare(i):
            wrongMove()
            return 0
    for i in range(2):
        splitMove[i+1] = fieldToIndex(splitMove[i+1])
    start1 = 8 - int(splitMove[1][1])
    start2 = int(splitMove[1][0])
    end1 = 8 - int(splitMove[2][1])
    end2 = int(splitMove[2][0])
    startField = chessBoard[start1][start2]
    endField = chessBoard[end1][end2]
    if not startField.name == splitMove[0].upper() or startField.name == "0" or not startField.team == currentPlayer or endField.team == currentPlayer:
        wrongMove()
        return 0
    if startField.legalMove([start1, start2], [end1, end2], currentPlayer, endField, chessBoard):
        chessBoard[end1][end2] = chessBoard[start1][start2]
        chessBoard[start1][start2] = empty()
    else:
        return 0



if __name__ == '__main__':
    while True:
        move=createBoard()
        x=movePiece(move)
        if x==0:
            continue
        currentPlayer = "White" if currentPlayer == "Black" else "Black"