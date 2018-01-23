
import numpy as np

'''
Creates a 2D array of characters to represent the maze extracted from fileName
'''
def parseMaze(fileName):
    path = './' + fileName
    with open(path) as file:
        maze = [[c for c in line.strip()] for line in file]
    return maze

'''
Writes a 2D array of characters representing a maze to fileName
'''
def writeMazeToFile(maze, fileName):
    np.savetxt(fileName, np.array(maze), fmt = '%s', delimiter = '')


'''
Gets the coordinates of the starting point of the maze as a pair (x,y)
'''
def getStartPoint(maze):
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] == "P":
                return i, j
    return None

'''
Gets a list of goal points in the maze as pairs (x,y)
'''
def getGoalPoints(maze):
    goalPoints = []
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] == ".":
                goalPoints.append((i, j))
    return goalPoints

'''
Gets a list of walkable adjacent nodes to the specified node
'''
def getAdjacentNodes(maze, node):
    adjacentNodes = []
    x = node[0]
    y = node[1]
    allAdjNodes = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
    for node in allAdjNodes:
        if(isWalkableNode(maze, node)):
            adjacentNodes.append(node)
    return adjacentNodes

'''
Checks if the specified node is a valid and walkable node in the maze
'''
def isWalkableNode(maze, node):
    cols = len(maze)
    rows = len(maze[0])
    x = node[0]
    y = node[1]
    if x >= 0 and y >=0 and x < cols and y < rows:
        if maze[x][y] != "%":
            return True
        return False
    return False

'''
Returns the Node with the lowest heuristic value from a list of Nodes
'''
def getLowestHeuristicNode(nodes):
    lowestHeuristic = nodes[0].heuristic
    lowestHeuristicNode = nodes[0]
    for node in nodes:
        h = node.heuristic
        if(h < lowestHeuristic):
            lowestHeuristic = h
            lowestHeuristicNode = node
    return lowestHeuristicNode

'''
Returns the Node with the lowest heuristic value (path cost + Manhattan distance) from a list of Nodes for A* search
'''
def getLowestHeuristicNode_astar(nodes):
    lowestHeuristic = nodes[0].heuristic + nodes[0].cost
    lowestHeuristicNode = nodes[0]
    for node in nodes:
        h = node.heuristic + node.cost
        if(h < lowestHeuristic):
            lowestHeuristic = h
            lowestHeuristicNode = node
    return lowestHeuristicNode

'''
Calculates the Manhattan Distance between 2 points
'''
def getManhattanDistance(node1, node2):
    return abs(node1[0] - node2[0]) + abs(node1[1] - node2[1])


'''
Returns the goal nearest to start
'''
def getClosestGoal(start, goals):
    dist = [getManhattanDistance(start, goal) for goal in goals]
    min = dist[0]
    closestGoal = goals[0]
    for i in range(len(dist)):
        if dist[i] < min:
            min = dist[i]
            closestGoal = goals[i]

    return closestGoal
