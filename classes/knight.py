from classes.chesspiece import chessPiece
class knight(chessPiece):
    def __init__(self, team):
        super().__init__(3, "N", team, [[2, 1], [1, 2], [-2, 1], [-1, 2], [2, -1], [1, -2], [-2, -1], [-1, -2]])

    def legalMove(self, start, end, currentTeam, endPiece=None, Board=None):
        delta_row = end[0] - start[0]
        delta_col = end[1] - start[1]
        return [delta_row, delta_col] in self.legal