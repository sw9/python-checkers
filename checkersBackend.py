def boundsCheck(f):
    
    def retfunc(*args):
        xlst = f(*args)
        
        y = []
        for x in xlst:
            x1, x2 = x
            if x1 < 8 and x1 >= 0 and x2 < 8 and x2 >= 0:
                y.append(x)
        
        return y
        
    return retfunc


@boundsCheck
def surroundings(piece, x, y, board):
    ret = []
    if (piece.king):
        ret.append((x - 1, y - 1))
        ret.append((x + 1, y + 1))
        ret.append((x + 1, y - 1))
        ret.append((x - 1, y + 1))
        return ret
    
    else:
        if (piece.color == 0):
            ret.append((x + 1, y + 1))
            ret.append((x - 1, y + 1))
            return ret
        else:
            ret.append((x - 1, y - 1))
            ret.append((x + 1, y - 1))
            return ret 


@boundsCheck
def possibleJumps(piece, x, y, board):
    positions = surroundings(piece, x, y, board)
    
    ret = []
    
    for p in positions:
        i, j = p
        if board[i][j] != None:
            if board[i][j].color != piece.color:
                ret.append((x+2*(i - x), y + 2*(j - y)))
    
    return ret

def jumpPositions(piece, x, y, board):
    positions = possibleJumps(piece, x, y, board)
    
    ret = []
    
    for p in positions:
        i, j = p

        if board[i][j] == None:
            ret.append((i, j))

    return ret

def movePositions(piece, x, y, board):
    positions = surroundings(piece, x, y, board)

    ret = []

    for p in positions:
        i, j = p
        
        if board[i][j] == None:
            ret.append((i, j))

    return ret


def initialBoard():
    ret = []
    
    for i in range(8):
        ith_row = []
        ret.append(ith_row)
        
        for j in range(8):
            ret[i].append(None)

    
    for i in range(0, 4, 2):
        for j in range(0, 7, 2):
            ret[j][i] = Piece(0)
            ret[1+j][7-i] = Piece(1)
    

    for j in range(0, 7, 2):
        ret[1+j][1] = Piece(0)
        ret[j][6] = Piece(1)

    return ret


def convertToKing(board):
    for j in range(8):
        if board[j][0] != None:
            if board[j][0].color == 1 and board[j][0].king != True:
                board[j][0].king = True
                
        if board[j][7] != None:
            if board[j][7].color == 0 and board[j][7].king != True:
                board[j][7].king = True
                
    return

def noMoveDetection(board, turn):
    ret = True

    for x in range(8):
        for y in range(8):
            if board[x][y] != None and board[x][y].color == turn:
                mvLst = movePositions(board[x][y], x, y, board)
                jmpLst = jumpPositions(board[x][y], x, y, board)
                
                if len(mvLst) == 0 and len(jmpLst) == 0:
                    pass
                else:
                    ret = False
    return ret


def noOpponentPieceDetection(board, turn):
    ret = True
    
    if turn == 0:
        opponent = 1
    else:
        opponent = 0

    for x in range(8):
        for y in range(8):
            if board[x][y] != None and board[x][y].color == opponent:
                ret = False

    return ret

def jumpDetection(board, turn):
    ret = []

    for x in range(8):
        for y in range(8):
            if board[x][y] != None and board[x][y].color == turn:
                jmpLst = jumpPositions(board[x][y], x, y, board)
                
                if len(jmpLst) == 0:
                    pass
                else:
                    ret.append((x, y))
    return ret


class Piece:
    def __init__(self, color, king = False):
        self.color = color
        self.king = king
    
    def __eq__(self, other):
        if isinstance(other, Piece):
            return (self.color == other.color) and (self.king == other.king)
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)    


    def __hash__(self):
        return hash((self.color, self.king))
