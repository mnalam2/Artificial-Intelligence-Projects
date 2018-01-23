import numpy as np
import random
import copy
import time
import multiprocessing


'''
Implementation of minimax. Returns the state of the board that will be the result of the minimax player's next move and tje number of expanded nodes on the way.
'''
def miniMax(node, depth, heuristic, isMax, player, expanded):
    if depth == 0:
        return node, heuristic(getOpponent(player), node), expanded

    if isMax:
        bestVal = -np.inf
        bestChild = []
        for child in getAllPossibleMoves(player, node):
            expanded+=1
            n, u, e = miniMax(child, depth - 1, heuristic, False, getOpponent(player), 0)
            expanded+= e
            if u > bestVal:
                bestVal = u
                bestChild = child

        return bestChild, bestVal, expanded

    else:
        bestVal = np.inf
        bestChild = []
        for child in getAllPossibleMoves(player, node):
            expanded+=1
            n, u, e= miniMax(child, depth - 1, heuristic, False, getOpponent(player), 0)
            expanded+=e
            if u < bestVal:
                bestVal = u
                bestChild = child

        return bestChild, bestVal,expanded

'''
Implementation of Alpha-Beta search. Returns the state of the board that will be the result of the Alpha-Beta player's next move and tje number of expanded nodes on the way.
'''
def alphaBeta(node, depth, heuristic, alpha, beta, isMax, player, expanded):
    if depth == 0:
        return node, heuristic(getOpponent(player), node), expanded
    if isMax:
        u = -np.inf
        bestChild = None
        for child in getAllPossibleMoves(player, node):
            expanded+=1
            n, v, e = alphaBeta(child, depth - 1, heuristic, alpha, beta, False, getOpponent(player), 0)
            expanded+=e
            if(v > u):
                u = v
                bestChild = child
            if u >= beta:
                return bestChild, u, expanded
            alpha = max (alpha, u)
        return bestChild, u, expanded

    else:
        u = np.inf
        bestChild = None
        for child in getAllPossibleMoves(player, node):
            expanded+=1
            n, v, e = alphaBeta(child, depth - 1, heuristic, alpha, beta, True, getOpponent(player), 0)
            expanded+=e
            if(v < u):
                u = v
                bestChild = child
            if u <= alpha:
                return bestChild, u, expanded
            beta = min (beta, u)
        return bestChild, u, expanded

'''
Helper function that runs minimax with a depth of 3
'''
def miniMax3(node, heuristic, player):
    return miniMax(node, 3, heuristic, True, player, 0)

'''
Helper function that runs Alpha-Beta with a depth of 4
'''
def alphaBeta4(node, heuristic, player):
    return alphaBeta(node, 4, heuristic, -np.inf, np.inf, True, player, 0)

'''
Helper function that runs Alpha-Beta with a depth of 3
'''
def alphaBeta3(node, heuristic, player):
    return alphaBeta(node, 3, heuristic, -np.inf, np.inf, True, player, 0)

'''
Gets all the possible final board states that result from player making each available move on the specified board
'''
def getAllPossibleMoves(player , board):

    allPossibleMoves = []
    positions = getPositions(board)
    playerPositions = []
    if player == "W":
        playerPositions = positions[0]
    else:
        playerPositions = positions[1]

    for position in playerPositions:
        moves = getValidMoves(position, board)
        for move in moves:
            b = makeMove(position, move, copy.deepcopy(board))
            allPossibleMoves.append(b)


    return allPossibleMoves

'''
Sets up the inital board as a 2D array of characters with 'W' to represent the white player and 'B' to represent the black player
'''
def createInitialBoard():
    board = [['B'] * 8]
    board.append(['B']*8)
    board.append([' '] * 8)
    board.append([' '] * 8)
    board.append([' '] * 8)
    board.append([' '] * 8)
    board.append(['W'] * 8)
    board.append(['W'] * 8)
    return board


'''
Given a player, get his oppoenent.
'''
def getOpponent(player):
    if player == "W":
        return "B"
    else: return "W"


'''
Get a pair of lists (whitePositions and blackPositions) where each list contains the indices of all its colored pieces
'''
def getPositions(board):

    blackPositions = []
    whitePositions = []

    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 'W':
                whitePositions.append((i,j))
            elif board[i][j] == 'B':
                blackPositions.append((i, j))

    return whitePositions, blackPositions


'''
Get all valid moves for a specific piece of the board and return a list of final positions after each move
'''
def getValidMoves(index, board):
    x = index[0]
    y = index[1]

    moves = []

    if(board[x][y] ==  " "):
        return None
    elif(board[x][y] == "B"):
        if((x + 1) < 8):
            if((y - 1) >= 0):
                if(board[x + 1][y - 1] != "B"):
                    moves.append((x + 1, y - 1))
            if((y + 1) < 8):
                if (board[x + 1][y + 1] != "B"):
                    moves.append((x + 1, y + 1))
            if board[x + 1][y] == " ":
                moves.append((x + 1, y))

    elif(board[x][y] == "W"):
        if((x - 1) >= 0):
            if((y - 1) >= 0):
                if (board[x - 1][y - 1] != "W"):
                    moves.append((x - 1, y - 1))
            if((y + 1) < 8):
                if (board[x - 1][y + 1] != "W"):
                    moves.append((x - 1, y + 1))
            if board[x - 1][y] == " ":
                moves.append((x - 1, y))

    return moves


'''
Makes a move from a starting index to a final index and gets the resulting board state
'''
def makeMove(idx,finidx,board):
    curr = board[idx[0]][idx[1]]
    board[idx[0]][idx[1]] = " "
    board[finidx[0]][finidx[1]] = curr
    return board

'''
Implementation of offensive heuristic 1
'''
def off_heur(player,board):
    positions = getPositions(board)
    if player == 'W':
        return 2.0*(30-len(positions[1])) + random.random()
    if player == 'B':
        return 2.0*(30-len(positions[0])) + random.random()

'''
Implementation of defensive heuristic 1
'''
def def_heur(player,board):
    positions = getPositions(board)
    if player == 'W':
        return 2.0*len(positions[0]) + random.random()
    if player == 'B':
        return 2.0*len(positions[1]) + random.random()

'''
Gets the average distance required to win for the player by checking how far each of player's pieces are from the opponent's side of the board
'''
def getAvgDistToWin(player, board, positions):
    if(player == "W"):
        sumDist = 0.0
        for y in range(8):
            for x in range(8):
                if(board[y][x]) == "W":
                    sumDist += float(y)
        return sumDist/float(len(positions[0]))
    else:
        sumDist = 0.0
        for y in range(7, -1, -1):
            for x in range(7, -1, -1):
                if(board[y][x]) == "B":
                    sumDist+= float(7 - y)
        return sumDist/float(len(positions[1]))

'''
Gets the minimum distance to win for the player by checking how far the closest piece to the opponent's side is
'''
def getDistToWin(player, board):
    if(player == "W"):
        for y in range(8):
            for x in range(8):
                if(board[y][x]) == "W":
                    return y
        return 7
    else:
        for y in range(7, -1, -1):
            for x in range(7, -1, -1):
                if(board[y][x]) == "B":
                    return 7 - y
        return 7


def getMaxDistToWin(player, board):
    if(player == "W"):
        for y in range(7, -1, -1):
            for x in range(7, -1, -1):
                if(board[y][x]) == "W":
                    return y

    else:
        for y in range(8):
            for x in range(8):
                if(board[y][x]) == "B":
                    return 7 - y

    return 7

'''
Implementation of offensive heuristic 2 - Prioritizes having a lower average distance to win while aggressive moves are a bonus
'''
def off_heur2(player, board):
    positions = getPositions(board)
    dist = getAvgDistToWin(player, board, positions)
    #dist = getDistToWin(player, board)
    #dist = getMaxDistToWin(player, board)
    if player == 'W':
        return 0.3*(30 - len(positions[1])) + 3.0*(20 - dist) + random.random()
    else:
        return 0.3*(30 - len(positions[0])) + 3.0*(20 - dist) + random.random()

'''
Implementation of defensive heuristic 2 - Prioritizes having a lower average to distance to win while moves that prevent ally pieces from being captured are a bonus
'''
def def_heur2(player, board):
    positions = getPositions(board)
    dist = getAvgDistToWin(player, board, positions)
    #theirDist = getDistToWin(getOpponent(player), board)
    #myDist = getDistToWin(player, board)
    #dist = getMaxDistToWin(player, board)
    if player == 'W':
        return 3*(20 - dist) + 0.3 * len(positions[0]) + random.random()
    else:
        return 3*(20 - dist) + 0.3 * len(positions[1]) + random.random()

'''
Checks the state of the board to see if the game is over. If the game is over return True, else return False
'''
def isGameOver(board):
    positions = getPositions(board)
    if len(positions[0]) == 0 or len(positions[1]) == 0:
        return True

    for x  in board[0]:
        if x == "W":
            return True
    for x in board[7]:
        if x == "B":
            return True



    return False

'''
Plays a specific game where each player will use a search strategy and a heuristic and outputs statistics of the game
'''
def playGame(searches, heuristics):
    board = createInitialBoard()


    turn = 0
    player = ["W", "B"]
    expanded = [0, 0]
    turns = [0, 0]
    times = [0.0, 0.0]
    while(not isGameOver(board)):
        #print(player[turn % 2])
        start = time.time()
        b, v, e = searches[turn % 2](board, heuristics[turn % 2], player[turn % 2])
        end = time.time()
        times[turn % 2] += (end - start)
        board = b
        expanded[turn % 2] += e
        turns[turn % 2] += 1
        #print(np.array(board))
        #time.sleep(1)
        turn+=1

    winner = player[(turn -1) % 2]
    times = [times[0]/(float(turns[0])), times[1]/(float(turns[1]))]
    averageExpanded = [float(expanded[0]) / float(turns[0]), float(expanded[1]) / float(turns[1])]
    return winner, board, expanded, averageExpanded, turns, times


def playMultipleGames(searches, heuristics, numGames):
    winners = {}
    winners["W"] = 0
    winners["B"] = 0
    for i in range(numGames):
        winner = playGame(searches, heuristics)
        winners[winner] +=1

    return winners

'''
A multi-process method that plays a single game and updates total statistics recorded
'''
def playGameProcess(searches, heuristics, winners, boards, expandeds, averageExpandeds, allTurns, allTimes):
    winner, board, expanded, averageExpanded, turns, times = playGame(searches, heuristics)
    winners[winner] += 1
    boards.append(board)
    expandeds.append(expanded)
    averageExpandeds.append(averageExpanded)
    allTurns.append(turns)
    allTimes.append(times)

'''
Prints the results of a specific matchup
'''
def printReport(matchup, winners, boards, expandeds, averageExpandeds, allTurns, allTimes, opponentsCaptured):
    print("--------------------\n")
    print(matchup)
    print("--------------------\n")
    print("Matchup results:\n")
    print(winners)
    print("--------------------\n")
    print("A. Final board states:\n")
    for b in boards:
        print(np.array(b))
    print("\n")
    print("--------------------\n")
    print("B. Total number of expanded nodes:\n")
    print(expandeds)
    print("--------------------\n")
    print("C. Average number of expanded nodes:\n")
    print(averageExpandeds)
    print('\n')
    print("C. Average time per move in seconds:\n")
    print(allTimes)
    print("--------------------\n")
    print("D. Numher of opponent pieces captured:\n")
    print(opponentsCaptured)
    print('\n')
    print("D. Number of turns per game:\n")
    print(allTurns)
    print("--------------------\n")

'''
Play multiple games for this matchup where each game is a separate process
'''
def playMatchupMultipleProcesses(matchup, searches, heuristics, numGames):
    manager = multiprocessing.Manager()
    winners = manager.dict()
    boards = manager.list([])
    expandeds = manager.list([])
    averageExpandeds = manager.list([])
    allTurns = manager.list([])
    allTimes = manager.list([])
    winners['W'] = 0
    winners['B'] = 0
    jobs = []
    for i in range(numGames):
        p = multiprocessing.Process(target=playGameProcess, args=(searches, heuristics, winners, boards, expandeds, averageExpandeds, allTurns, allTimes))
        jobs.append(p)
        p.start()

    for proc in jobs:
        proc.join()

    opponentsCaptured = []
    for b in boards:
        positions = getPositions(b)
        opponentsCaptured.append([16 - len(positions[1]), 16 - len(positions[0])])
    printReport(matchup, winners, boards, expandeds, averageExpandeds, allTurns, allTimes, opponentsCaptured)


'''
Main loop - Plays all the matchups and records the results
'''
if __name__ == '__main__':
    matchups = ["1. Minimax (Offensive Heuristic 1) vs Alpha-beta (Offensive Heuristic 1)", "2. Alpha-beta (Offensive Heuristic 2) vs Alpha-beta (Defensive Heuristic 1)", "3. Alpha-beta (Defensive Heuristic 2) vs Alpha-beta (Offensive Heuristic 1)", "4. Alpha-beta (Offensive Heuristic 2) vs Alpha-beta (Offensive Heuristic 1)", "5. Alpha-beta (Defensive Heuristic 2) vs Alpha-beta (Defensive Heuristic 1)", "6. Alpha-beta (Offensive Heuristic 2) vs Alpha-beta (Defensive Heuristic 2)"]
    searches = [[miniMax3, alphaBeta4], [alphaBeta4, alphaBeta4], [alphaBeta4, alphaBeta4], [alphaBeta4, alphaBeta4], [alphaBeta4, alphaBeta4], [alphaBeta4, alphaBeta4] ]
    heuristics = [[off_heur, off_heur], [off_heur2, def_heur], [def_heur2, off_heur], [off_heur2, off_heur], [def_heur2, def_heur], [off_heur2, def_heur2]]
    #matchups = ["3. Alpha-beta (Defensive Heuristic 2) vs Alpha-beta (Offensive Heuristic 1)"]

    #searches = [[alphaBeta4, alphaBeta4]]
    #heuristics = [[def_heur2, off_heur]]
    for i in range(len(matchups)):
        playMatchupMultipleProcesses(matchups[i], searches[i], heuristics[i], 10)
