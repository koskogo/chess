from classes.chesspiece import chessPiece
class empty(chessPiece):
    def __init__(self):
        super().__init__(0, "0", "non",[[0,0]])