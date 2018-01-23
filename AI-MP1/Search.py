from collections import deque
import Utilities
import time
import string
import heapq
import cProfile
'''
Node class to represent different nodes in the maze
'''
class Node:
    def __init__(self, x, y, cost, parent, heuristic = 1, visitedGoals = 0):
        self.x = x
        self.y = y
        self.cost = cost
        self.heuristic = heuristic
        self.parent = parent
        self.visitedGoals = visitedGoals

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.cost == other.cost and self.heuristic == other.heuristic and self.visitedGoals == other.visitedGoals


'''
Implementation of breadth-first search. Takes a 2D maze, start position and goal position as input and
returns a Node representing the goal state once it is reached.
'''
def BFS(maze, start, goal):
    visited = []
    frontier = deque()
    expanded = 0
    visited.append(start)
    s = Node(start[0], start[1], 0, None)
    frontier.append(s)

    while frontier:
        print("Expanded: " + str(expanded) + "\n")
        current = frontier.popleft()
        expanded+=1
        if current.x == goal[0] and current.y == goal[1]:
            return current, expanded
        for adjacent in Utilities.getAdjacentNodes(maze, (current.x, current.y)):
            if adjacent not in visited:
                visited.append(adjacent)
                frontier.append(Node(adjacent[0], adjacent[1], 1 + current.cost, current))

'''
Implementation of depth-first search. Takes a 2D maze, start position and goal position as input and
returns a Node representing the goal state once it is reached.
'''
def DFS(maze, start, goal):
    visited = []
    frontier = []
    expanded = 0
    visited.append(start)
    s = Node(start[0], start[1], 0, None)
    frontier.append(s)

    while frontier:
        print("Expanded: " + str(expanded) + "\n")
        current = frontier.pop()
        expanded+=1
        if current.x == goal[0] and current.y == goal[1]:
            return current, expanded
        for adjacent in Utilities.getAdjacentNodes(maze, (current.x, current.y)):
            if adjacent not in visited:
                visited.append(adjacent)
                frontier.append(Node(adjacent[0], adjacent[1], 1 + current.cost, current))


'''
Implementation of greedy best first search. Takes a 2D maze, start position and goal position as input and
returns a Node representing the goal state once it is reached.
'''
def GBFS(maze, start, goal):
    visited = []
    frontier = []
    expanded = 0
    visited.append(start)
    s = Node(start[0], start[1], 0, None, Utilities.getManhattanDistance(start, goal))
    frontier.append(s)

    while frontier:
        print("Expanded: " + str(expanded) + "\n")
        current = Utilities.getLowestHeuristicNode(frontier)
        frontier.remove(current)
        expanded+=1
        if current.x == goal[0] and current.y == goal[1]:
            return current, expanded
        for adjacent in Utilities.getAdjacentNodes(maze, (current.x, current.y)):
            if adjacent not in visited:
                visited.append(adjacent)
                frontier.append(Node(adjacent[0], adjacent[1], 1 + current.cost, current, Utilities.getManhattanDistance(adjacent, goal)))

'''
Implementation of A* search. Takes a 2D maze, start position and goal position as input and
returns a Node representing the goal state once it is reached. Next node chosen is based on lowest
heuristic for A*
'''
def a_star1(maze, start, goal):
    visited = []
    frontier = []
    expanded = 0
    visited.append(start)
    s = Node(start[0], start[1], 0, None, Utilities.getManhattanDistance(start, goal))
    frontier.append(s)

    while frontier:
        print("Expanded: " + str(expanded) + "\n")
        current = Utilities.getLowestHeuristicNode_astar(frontier)
        frontier.remove(current)
        expanded+=1
        if current.x == goal[0] and current.y == goal[1]:
            return current, expanded
        for adjacent in Utilities.getAdjacentNodes(maze, (current.x, current.y)):
            if adjacent not in visited:
                visited.append(adjacent)
                frontier.append(Node(adjacent[0], adjacent[1], 1 + current.cost, current, Utilities.getManhattanDistance(adjacent, goal)))

'''
Possible implementation of A* with multiple goal nodes with an admissible heuristic
'''
def a_star4(maze, start, goals):
    visited = {}
    frontier = []
    expanded = 0
    numGoals = len(goals)
    # At first, no goals are visited and is represented by a bit array of all 0s
    startVisitedGoals = 0

    # An array for comparison that indicates all goals have been visited
    allVisitedGoals = pow(2, numGoals) - 1

    goalBinaries = {}
    for i in range(numGoals):
        goalBinaries[goals[i]] = pow(2, numGoals - i - 1)

    heuristicStorage = {}

    shortestPaths = getShortestPaths(goals, goalBinaries)

    d = getMinDist(start, startVisitedGoals, goals, goalBinaries, shortestPaths)
    heuristicStorage[start, startVisitedGoals] = d
    s = Node(start[0], start[1], 0, None, d, startVisitedGoals)
    frontier.append((d,s))

    visited[start] = []
    visited[start].append(startVisitedGoals)

    #print(goals)

    while frontier:
        #print("Expanded: " + str(expanded) + "\n")
        current = heapq.heappop(frontier)[1]
        #frontier.remove(current)
        expanded+=1


        # Additional check to make sure that we've reached a goal and all goals have been visited
        if (((current.x, current.y) in goals) and current.visitedGoals == allVisitedGoals):
            return current, expanded
        for adjacent in Utilities.getAdjacentNodes(maze, (current.x, current.y)):

            visitedGoals = current.visitedGoals

            # Check if this adjacent node is a goal node and modify visitedGoals based on that

            visitedGoals = visitedGoals  | goalBinaries.get(adjacent, 0)

            notExists = False
            if(adjacent not in visited):
                notExists = True

            if (notExists or (visitedGoals not in visited[adjacent])):

                if(notExists):
                    visited[adjacent] = []


                minDist = heuristicStorage.get((adjacent, visitedGoals), getMinDist(adjacent, visitedGoals, goals, goalBinaries, shortestPaths))
                heuristicStorage[(adjacent, visitedGoals)] = minDist


                #print(notExists)
                visited[adjacent].append(visitedGoals)
                heapq.heappush(frontier, (1 + current.cost + minDist, Node(adjacent[0], adjacent[1], 1 + current.cost, current, minDist, visitedGoals)))


'''
Given a list of goals and a dictionary mapping goals to integers whose binary represtentation denote that if the ith bit is 1 then the ith goal has been
visited, get the length of the shortest Manhattan path for each goal for all possible states and memoize it in a dictionary
'''
def getShortestPaths(goals, goalBinaries):

    n = len(goals)
    allVisited = pow(2, n) - 1
    shortestPaths = {}

    for i in range(n):
        shortestPaths[(goals[i], allVisited)] = 0

    for v in range(allVisited - 1, 0, -1):
        for i in range(n):
            visitedGoalsStr = (str(bin(v)))[2:].rjust(n, '0')
            unvisitedGoals = [goals[j] for j in range(n) if visitedGoalsStr[j] == '0']
            arr = [Utilities.getManhattanDistance(goals[i], g) + shortestPaths[(g, v | goalBinaries[g])] for g in unvisitedGoals]
            shortestPaths[(goals[i], v)] = min (arr)

    return shortestPaths

'''
Finds the length of the shortest path from the current node to a configuration where all goal nodes have been explored.
'''
def getMinDist(current, visitedGoals, goals, goalBinaries, shortestPaths):

    n = len(goals)
    return min ([Utilities.getManhattanDistance(current, goals[i]) + shortestPaths[goals[i], visitedGoals | goalBinaries[goals[i]]] for i in range(n)])


'''
Implementation of A* search. Takes a 2D maze, start position and multiple goal positions as input and
returns a Node representing the goal state once it is reached. Next node chosen is based on lowest
heuristic for A*
'''
def a_star_subopt(maze, start, goals):
    currents, expandeds = [],[]
    order = 1
    orders = [-1]*len(goals)
    temp_goals = goals[:]
    while len(temp_goals) > 0:
        nearest = Utilities.getClosestGoal(start, temp_goals)
        for i in range(len(goals)):
            if goals[i]==nearest:
                orders[i] = order
                order += 1
        current, expanded = a_star1(maze, start, nearest)
        currents.append(current)
        expandeds.append(expanded)
        temp_goals.remove(nearest)
        start = nearest
    return currents, expandeds, orders              
                
                
'''
Uses the output of basic search functions to print a report and print the solution
to fileName
'''
def printBasicReport(maze, goal, expanded, fileName):
    pathCost = goal.cost
    current = goal

    while (current.parent is not None):
        print("Path: (" + str(current.x) + "," + str(current.y) + ")\n")
        maze[current.x][current.y] = '.'
        current = current.parent
    Utilities.writeMazeToFile(maze, fileName)

    print("Path cost: " + str(pathCost) + "\nExpanded: " + str(expanded))

'''
Uses the output of basic search functions to print a report and print the solution
to fileName
'''
def printBasicReport_subopt(maze, goal, orders,goals,expanded, fileName):
    pathCost = goal.cost
    current = goal
    print orders
    while (current.parent is not None):
        #print("Path: (" + str(current.x) + "," + str(current.y) + ")\n")
        maze[current.x][current.y] = '.'
        current = current.parent
    Utilities.writeMazeToFile(maze, fileName)

    return pathCost, expanded

def printAdvancedReport_subopt(maze, currents, orders, goals,expandeds, fileName):
    tot_path = 0
    tot_exp = 0
    for i in range(len(currents)):
        path, expa = printBasicReport_subopt(maze,currents[i],orders[i],goals[i],expandeds[i],fileName)
        tot_path += path
        tot_exp += expa
    print "Path cost: " + str(tot_path) + " Expanded: " + str(tot_exp)
    num2alpha = dict(zip(range(1, 27), string.ascii_lowercase))

    for i in range(len(orders)):
        if orders[i] <= 9:
            maze[goals[i][0]][goals[i][1]] = orders[i]
        else:
            maze[goals[i][0]][goals[i][1]] = num2alpha[orders[i]-9]
    Utilities.writeMazeToFile(maze, fileName)


def printAdvancedReport(maze, goal, goals, expanded, fileName):
    pathCost = goal.cost
    current = goal
    count = len(goals)


    num2alpha = dict(zip(range(10,27), string.ascii_lowercase))

    while (current.parent is not None):
        print("Path: (" + str(current.x) + "," + str(current.y) + ")\n")
        if((current.x, current.y) in goals):
            if(count >= 10):
                maze[current.x][current.y] = num2alpha[count]
            else:
                maze[current.x][current.y] = count
            count -= 1
            goals.remove((current.x, current.y))
        else:
            maze[current.x][current.y] = '.'
        current = current.parent
    Utilities.writeMazeToFile(maze, fileName)

    print("Path cost: " + str(pathCost) + "\nExpanded: " + str(expanded))


'''
Helper function that executes the basic search functions. Takes mazeFileName as input maze and
writes to outputFileName as output maze
'''

def executeSearch(searchFunc, mazeFileName, outputFileName):
    if(searchFunc == BFS or searchFunc == DFS or searchFunc == GBFS or searchFunc == a_star1):
        startTime = time.time()
        maze = Utilities.parseMaze(mazeFileName)
        start = Utilities.getStartPoint(maze)
        goals = Utilities.getGoalPoints(maze)
        goal, expanded = searchFunc(maze, start, goals[0])
        printBasicReport(maze, goal, expanded, outputFileName)
        endTime = time.time()
        print("Search took " + str(endTime - startTime) + " seconds.")
    if(searchFunc == a_star4):
        startTime = time.time()
        maze = Utilities.parseMaze(mazeFileName)
        start = Utilities.getStartPoint(maze)
        goals = Utilities.getGoalPoints(maze)
        goal, expanded = searchFunc(maze, start, goals)
        printAdvancedReport(maze, goal, goals, expanded, outputFileName)
        endTime = time.time()
        print("Search took " + str(endTime - startTime) + " seconds.")
    if(searchFunc == a_star_subopt):
        startTime = time.time()
        maze = Utilities.parseMaze(mazeFileName)
        start = Utilities.getStartPoint(maze)
        goals = Utilities.getGoalPoints(maze)
        currents, expandeds, orders = searchFunc(maze, start, goals)
        printAdvancedReport_subopt(maze, currents, orders,goals, expandeds, outputFileName)
        endTime = time.time()
        print("Search took " + str(endTime - startTime) + " seconds.")


executeSearch(a_star_subopt, "mediumSearch.txt", "mediumSearchSol.txt")
