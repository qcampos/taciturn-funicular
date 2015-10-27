

# Colors
NONE = 0
CROSS = 1
CIRCLE = 2
BOTH = 3

class Board():
    """ Represents a 3x3 board of classical tic-tac-toe. """
    
    def __init__(self):
        self.board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.ended = NONE


    def strLine(self, index):
        """ Get the line at the given index as a string representation.
        """
        def f(color):
            """ Map the value of the player to it's string representation.
            """
            if color == CROSS : return 'X' #u"\u274C"
            if color == CIRCLE : return 'O' #u"\u25EF"
            return "_"
        
        return ' '.join([f(i) for i in self.board[index]])

  
    def __repr__(self):
        return '\n'.join([self.strLine(i) for i in range(len(self.board))])


    def __setCell(self, x, y, color):
        """ Set a mark into the specified cell.
        """
        self.board[x][y] = color


    def winner(self):
        """ Return the winner color (CROSS, CRCLE, BOTH)
        or NONE if the game is not finished yet.
        """
        # If already computed, return the value
        if self.ended:
            return self.ended
        
        # Generate lines, columns and diagonals.
        indexes = [i for i in range(len(self.board))]
        lines = [[(i, j) for i in indexes] for j in indexes]
        colls = [[(j, i) for i in indexes] for j in indexes]
        diags = [[(i, i) for i in indexes]] + [[(i, len(indexes)-i-1) for i in indexes]]
        trios = lines + colls + diags

        # For each possible filling, check if a player fullfill it.
        for trio in trios:
            l = [self.board[a][b] for a,b in trio]
            if len(set(l)) == 1 and l[0] is not NONE:
                self.ended = l[0]
                return l[0]

        # Check if there is still an empty cell.
        l = [self.board[i][j] for i in indexes for j in indexes]
        if NONE not in l:
            self.ended = BOTH
            return BOTH
        
        return NONE


    def canPlayAt(self, x, y):
        """ Returns if the given position is empty and if a
        player can still play in this cell.
        """
        if self.ended or self.board[x][y]:
            return False
        return True


    def play(self, x, y, player):
        """ Play the given move. The current player will
        set a mark into the corresponding cell. """
        if not self.canPlayAt(x, y):
            print("ERROR", "Cell", x, y, "is already taken")
            return None

        # Effectively set the cell and compute the winner
        self.__setCell(x, y, player)
        return self.winner()

    def unplay(self, x, y):
        """ Undo the given move.
        """
        if self.canPlayAt(x, y):
            raise RuntimeError("Le mouvement n'est pas annulable")
        self.__setCell(x, y, NONE)
        self.ended = False

    def allowedMoves(self):
        indexes = [i for i in range(len(self.board))]
        l = [(a, b) for a in indexes for b in indexes if not self.board[a][b]]
        return l
        



        

class Game():

    def __init__(self, size = 3):
        self.size = size
        self.boards = {(i,j):Board() for i in range(size) for j in range(size)}
        self.allowedBoards = [(i,j) for i in range(size) for j in range(size)]
        self.player = CROSS
        self.ended = False
        self.winners = [[NONE for i in range(size)] for j in range(size)]

    def __repr__(self):

        s = ""
        for i in range(self.size):
            for k in range(3):
                for j in range(self.size):
                    s += self.boards[(i,j)].strLine(k)
                    s += '\t'
                s += '\n'
            s += '\n'
               
        return s  
        
    def __switchPlayer(self):
        if self.player == CROSS: self.player = CIRCLE
        else: self.player = CROSS

    def canPlayAt(self, boardPos, movePos):
        """ Check if the given move is legal.
        """
        # Chel if the board exists.
        if boardPos not in self.boards:
            raise RuntimeError("Cannot check if a move is legal in a non-existing board {}.".format(boardPos))
        if boardPos not in self.allowedBoards:
            ##print("Wrong playing {} @ {} when can play on {}.".format(movePos, boardPos, self.allowedBoards))
            return False

        # Get the board and position.
        board = self.boards[boardPos]
        x, y = movePos
        # Check if the move is valid for the board.
        if not board.canPlayAt(x, y):
            ##print("Board telling it can't")
            return False

        return True

    def play(self, boardPos, movePos):
        """ Play the given move in the given board of the game.
        """
        # Check if the move is legal.
        if self.ended:
            raise RuntimeError("Cannot play a move in an ended game")
        if not self.canPlayAt(boardPos, movePos):
            ##print("Moves can be played at {}".format(self.allowedBoards))
            raise RuntimeError("Illegal move {} in board {}. \n{}".format(movePos, boardPos, self))
        # Get the board and move positions.
        board = self.boards[boardPos]
        x, y = movePos
        # Play the move and switch player.
        winner = board.play(x, y, self.player)
        self.__switchPlayer()
        # If a player win on a board, check it
        xB, yB = boardPos
        self.winners[xB][yB] = winner

        # Then define which board is allowed.
        if self.boards[movePos].winner() == NONE:
            self.allowedBoards = [movePos]
        else:
            self.allowedBoards = [(i,j) for i in range(self.size) for j in range(self.size) if self.winners[i][j] == NONE]
        
        return self.winner()

    def unplay(self, boardPos, movePos, lastAllowedBoards):
        """ Undo the given moves and restore the game as it was.
        """
        if self.canPlayAt(boardPos, movePos):
            raise RuntimeError("Move {} @ {} wasn't played.".format(movePos, boardPos))

        # Undo the move
        board = self.boards[boardPos]
        x, y = movePos
        board.unplay(x, y)
        # Restore the state
        self.allowedBoards = lastAllowedBoards
        xB, yB = boardPos
        self.winners[xB][yB] = NONE
        self.ended = False
        self.__switchPlayer()
    
    def winner(self):
        """ Return the winner color (CROSS, CRCLE, BOTH)
        or NONE if the game is not finished yet.
        """
        # If already computed, return the value
        if self.ended:
            return self.ended
        
        # Generate lines, columns and diagonals.
        indexes = [i for i in range(self.size)]
        lines = [[(i, j) for i in indexes] for j in indexes]
        colls = [[(j, i) for i in indexes] for j in indexes]
        diags = [[(i, i) for i in indexes]] + [[(i, len(indexes)-i-1) for i in indexes]]
        trios = lines + colls + diags

        # For each possible filling, check if a player fullfill it.
        for trio in trios:
            l = [self.winners[a][b] for a,b in trio]
            if len(set(l)) == 1 and l[0] is not NONE:
                self.ended = l[0]
                return l[0]

        # Check if there is still an empty cell.
        l = [self.winners[i][j] for i in indexes for j in indexes]
        if NONE not in l:
            self.ended = BOTH
            return BOTH
        
        return NONE
        
        
    def allowedMoves(self):
        moves = []
        for pos in self.allowedBoards:
            moves +=  [(pos, bPos) for bPos in self.boards[pos].allowedMoves()]

        return moves




def valToPlayer(val):
    if val == NONE:
        return "NONE"
    if val == CROSS:
        return "CROSS"
    if val == CIRCLE:
        return "CIRCLE"
    return "BOTH"



