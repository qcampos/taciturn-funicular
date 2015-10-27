from game import *
from players import *

import time

def timefunc(f):
    def f_timer(*args, **kwargs):
        start = time.time()
        result = f(*args, **kwargs)
        end = time.time()
        print(f.__name__, 'took', end - start, 'time')
        return result
    return f_timer


@timefunc
def playGame(player1, player2, printBoard=False):
    players = {CROSS:player1, CIRCLE:player2}
    game = Game()

    if printBoard: print(game)

    while game.winner() == NONE:
        player = players[game.player]
        bPos, mPos = player.getMove(game)

        d = {(0,0):7, (0,1):8, (0,2):9,
             (1,0):4, (1,1):5, (1,2):6,
             (2,0):1, (2,1):2, (2,2):3}

        
        game.play(bPos, mPos)
        if printBoard:
            print("Played", d[bPos], d[mPos])
            print(game)

    print("Winner", valToPlayer(game.winner()))
    return game.winner()



p1 = MinMaxPlayer(CROSS)
p2 = AlphaBetaPlayer(CIRCLE, 3)
rand = RandomPlayer(CROSS)
human = ConsoleHumanPlayer(CROSS)
for i in range(10):
    playGame(rand, p2, printBoard=False)
