from classes.chesspiece import chessPiece
class pawn(chessPiece):
    def __init__(self,team):
        super().__init__(1,"P",team,[[1,0]])

    def legalMove(self,start,end,currentTeam,endPiece,Board):
        delta_row = end[0] - start[0]
        delta_col = end[1] - start[1]
        direction = -1 if self.team == "White" else 1  # because rows count from top
        start_rank = 6 if self.team == "White" else 1
        # forward move
        if delta_col == 0:
            if delta_row == direction and endPiece.name == "0":
                return True
            if start[0] == start_rank and delta_row == 2 * direction and endPiece.name == "0":
                between_row = start[0] + direction
                if Board[between_row][start[1]].name == "0":
                    return True
            return False
        # capture
        if abs(delta_col) == 1 and delta_row == direction and endPiece.name != "0" and endPiece.team != self.team:
            return True
        return False
