from classes.chesspiece import chessPiece
class bishop(chessPiece):
    def __init__(self, team):
        super().__init__(3, "B", team, [[1,1],[-1,1],[1,-1],[-1,-1]])

    def legalMove(self, start, end, currentTeam, endPiece, Board):
        delta_row = end[0] - start[0]
        delta_col = end[1] - start[1]
        if abs(delta_row) != abs(delta_col):
            return False
        step_row = 1 if delta_row > 0 else -1
        step_col = 1 if delta_col > 0 else -1
        r = start[0] + step_row
        c = start[1] + step_col
        while r != end[0] and c != end[1]:
            if Board[r][c].name != "0":
                return False
            r += step_row
            c += step_col
        # destination
        if endPiece.name == "0" or endPiece.team != self.team:
            return True
        return False