from game import *
import random



class ConsoleHumanPlayer():
    """ Read on stdin the values.
    """
    def __init__(self, color=NONE):
        pass
    def getMove(self, game):
        d = {7:(0,0), 8:(0,1), 9:(0,2),
              4:(1,0), 5:(1,1), 6:(1,2),
              1:(2,0), 2:(2,1), 3:(2,2)}
        board, move = [int(t) for t in input("Coup : ").split()]
        xB, yB = d[board]
        x, y = d[move]
        if not game.canPlayAt((xB, yB), (x,y)):
            return self.getMove(game)
        return ((xB, yB), (x,y))

class RandomPlayer():
    """ Player that plays random moves.
    """
    def __init__(self, color=NONE):
        pass
    def getMove(self, game):
        moves = game.allowedMoves()
        return random.choice(moves)

class MinMaxPlayer():
    """ Min-max algorithme for playing
    """

    WIN = 100
    LOSE = -100
    NUL = 0
    
    def __init__(self, color, depth=3):
        self.depth = depth
        self.color = color
        if self.color == CROSS:
            self.opponent = CIRCLE
        else:
            self.opponent = CROSS
            
    def getMove(self, game):
        """ Min max algorithme for player. """
        moves = game.allowedMoves()
        if not moves:
            raise RuntimeError("Player have no allowed moves")
        # Start of the tree computation
        bestVal = self.LOSE
        bestMove = moves[0]
        for boardPos, movePos in moves:
            # Play the move
            oldBoards = game.allowedBoards.copy()
            game.play(boardPos, movePos)
            # Get the best returned value
            val = self.__min(game, 0)
            if val > bestVal:
                bestVal = val
                bestMove = (boardPos, movePos)
            # Undo the move
            game.unplay(boardPos, movePos, oldBoards)
        # Return the best move founded
        return bestMove

    def __min(self, game, depth):
        # Check if the game is over
        if depth >= self.depth or game.winner() != NONE:
            return self.evaluate(game)
        # Look for the best move for second player
        minVal = self.WIN
        for boardPos, movePos in game.allowedMoves():
            # Play the move
            oldBoards = game.allowedBoards.copy()
            game.play(boardPos, movePos)
            # Check the value recursively
            val = self.__max(game, depth + 1)
            if val < minVal:
                minVal = val
            # Undo the move
            game.unplay(boardPos, movePos, oldBoards)
        # Return the opponent best move
        return minVal


    def __max(self, game, depth):
        # Check if the game is over
        if depth >= self.depth or game.winner() != NONE:
            return self.evaluate(game)
        # Look for the current player best move
        maxVal = self.LOSE
        for boardPos, movePos in game.allowedMoves():
            # Play the move
            oldBoards = game.allowedBoards.copy()
            game.play(boardPos, movePos)
            # Check the value recursively
            val = self.__min(game, depth + 1)
            if val > maxVal:
                maxVal = val
            # Undo the move
            game.unplay(boardPos, movePos, oldBoards)
        # Return the current player best move
        return maxVal
    
    def evaluate(self, game):
        w = game.winner()
        # Player win
        if w == self.color:
            return 100
        # Nul match
        elif w == BOTH:
            return 0
        # Not finished yet
        elif w == NONE:
            return self.evaluateBoard(game)
            raise NotImplementedError("The evaluation for the board is not implemented.")
        # Player lose
        else:
            return -100

    def evaluateBoard(self, game):
        wCount = [t for p in game.winners for t in p].count(self.color)
        lCount = [t for p in game.winners for t in p].count(self.opponent)
        return wCount - lCount




class AlphaBetaPlayer():
    """ Alpha-beta algorithme for playing
    """

    WIN = 100
    LOSE = -100
    NUL = 0
    
    def __init__(self, color, depth=3):
        self.depth = depth
        self.color = color
        if self.color == CROSS:
            self.opponent = CIRCLE
        else:
            self.opponent = CROSS
            
    def getMove(self, game):
        """ Min max algorithme for player. """
        moves = game.allowedMoves()
        if not moves:
            raise RuntimeError("Player have no allowed moves")
        # Start of the tree computation
        bestVal = self.LOSE
        bestMove = moves[0]
        moves.sort(key=lambda x:self.evaluateMove(game, x), reverse=True)
        for boardPos, movePos in moves:
            # Play the move
            oldBoards = game.allowedBoards.copy()
            game.play(boardPos, movePos)
            # Get the best returned value
            val = self.__min(game, 0, self.LOSE, self.WIN)
            if val > bestVal:
                bestVal = val
                bestMove = (boardPos, movePos)
            # Undo the move
            game.unplay(boardPos, movePos, oldBoards)
        # Return the best move founded
        return bestMove

    def __min(self, game, depth, alpha, beta):
        # Check if the game is over
        if depth >= self.depth or game.winner() != NONE:
            return self.evaluate(game)
        # Look for the best move for second player
        minVal = self.WIN
        moves = game.allowedMoves()
        moves.sort(key=lambda x:self.evaluateMove(game, x), reverse=False)
        for boardPos, movePos in moves:
            # Play the move
            oldBoards = game.allowedBoards.copy()
            game.play(boardPos, movePos)
            # Check the value recursively
            val = self.__max(game, depth + 1, alpha, beta)
            minVal = min(minVal, val)
            # Alpha-cutting immediatly
            if alpha >= minVal:
                game.unplay(boardPos, movePos, oldBoards)
                return minVal
            beta = min(beta, minVal)
            # Undo the move
            game.unplay(boardPos, movePos, oldBoards)
        # Return the opponent best move
        return minVal


    def __max(self, game, depth, alpha, beta):
        # Check if the game is over
        if depth >= self.depth or game.winner() != NONE:
            return self.evaluate(game)
        # Look for the current player best move
        maxVal = self.LOSE
        moves = game.allowedMoves()
        moves.sort(key=lambda x:self.evaluateMove(game, x), reverse=True)
        for boardPos, movePos in moves:
            # Play the move
            oldBoards = game.allowedBoards.copy()
            game.play(boardPos, movePos)
            # Check the value recursively
            val = self.__min(game, depth + 1, alpha, beta)
            maxVal = max(maxVal, val)
            # Beta-cutting immediatly
            if maxVal >= beta:
                game.unplay(boardPos, movePos, oldBoards)
                return maxVal
            # Update alpha
            alpha = max(alpha, maxVal)
            # Undo the move
            game.unplay(boardPos, movePos, oldBoards)
        # Return the current player best move
        return maxVal
    
    def evaluate(self, game):
        w = game.winner()
        # Player win
        if w == self.color:
            return 100
        # Nul match
        elif w == BOTH:
            return 0
        # Not finished yet
        elif w == NONE:
            return self.evaluateGame(game)
            raise NotImplementedError("The evaluation for the board is not implemented.")
        # Player lose
        else:
            return -100

    def evaluateGame(self, game):
        wCount = [t for p in game.winners for t in p].count(self.color)
        lCount = [t for p in game.winners for t in p].count(self.opponent)
        return wCount - lCount


    def evaluateMove(self, game, move):
        # Play the move
        boardPos, movePos = move
        oldBoards = game.allowedBoards.copy()
        game.play(boardPos, movePos)
        # Get the evaluation
        value = self.evaluate(game)
        # Undo the move
        game.unplay(boardPos, movePos, oldBoards)
        return value

