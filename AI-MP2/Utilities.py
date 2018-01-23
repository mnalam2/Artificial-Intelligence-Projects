import numpy as np
import random

'''
Creates a 2D array of characters to represent the puzzle extracted from fileName
'''
def parseArray(fileName):
    path = './' + fileName
    with open(path) as file:
        array = [[c for c in line.strip()] for line in file]
    return array


'''
Writes a 2D array of characters representing the puzzle to fileName
'''
def writeArrayToFile(array, fileName):
    np.savetxt(fileName, np.array(array), fmt = '%s', delimiter = '')


'''
Gets the domain of possible colors in the puzzle
'''
def getDomain(array):
    domain = []
    for i in range(len(array)):
        for j in range(len(array[0])):
            if array[i][j] != "_" and array[i][j] not in domain:
                domain.append(array[i][j])
    return domain

'''
Gets the source coordinates
'''
def getSources(array):
    sources = []
    for i in range(len(array)):
        for j in range(len(array[0])):
            if array[i][j] != "_":
                sources.append((i,j))
    return sources

'''
Gets a random unassigned value found in the puzzle
'''
def getRandomUnassignedIndex(array):
    unassignedIndices = []
    for i in range(len(array)):
        for j in range(len(array[0])):
            if array[i][j] == "_":
               unassignedIndices.append((i, j))
    if unassignedIndices == []:
        return None
    else:
        return random.choice(unassignedIndices)

'''
Gets all unassigned grids neighboring an assigned grid
'''
def getAllUnassignedIndexNearColored(array):
    unassignedIndices = []
    for i in range(len(array)):
        for j in range(len(array[0])):
            if array[i][j] != "_":
                neighbors = getValidNeighbors(i, j, array)
                for neighbor in neighbors:
                    if array[neighbor[0]][neighbor[1]] == "_":
                        unassignedIndices.append(neighbor)
    return unassignedIndices

'''
Gets most constrained unassigned grid
'''
def getMostConstrainedVariable(indexes,domain,assignment,sources):
    if len(indexes) == 0:
        return None
    curr_mcv = None
    least_count = 100
    for idx in indexes:
        curr_count = 0
        for value in domain:
            if isValueConsistent(idx,value,assignment,sources):
                curr_count += 1
        if curr_count < least_count:
            least_count = curr_count
            curr_mcv = idx
    return curr_mcv

'''
Gets a random unassigned grid that neighbors an assigned grid
'''
def getUnassignedIndexNearColored(array):
    unassignedIndices = []
    for i in range(len(array)):
        for j in range(len(array[0])):
            if array[i][j] != "_":
                neighbors = getValidNeighbors(i,j, array)
                for neighbor in neighbors:
                    if array[neighbor[0]][neighbor[1]] == "_":
                        unassignedIndices.append(neighbor)
    if unassignedIndices == []:
        return None
    else:
        return random.choice(list(set(unassignedIndices)))

'''
Checks if a value assignment violates any constraints
'''
def isValueConsistent(index, value, assignment, sources):
    x = index[0]
    y = index[1]

    #print("Trying assignment: " + value + " to " + "(" + str(index[0]) + ", " + str(index[1]) + ")\n")
    assignment[x][y] = value
    neighbors = getValidNeighbors(x, y, assignment)
    b = True
    for neighbor in neighbors:
        if(not isVariableConsistent(neighbor[0], neighbor[1], assignment, sources)):
            b = False
            break
    assignment[x][y] = "_"
    return b

'''
Checks if a variable assignment violates any constraints
'''
def isVariableConsistent(x, y, assignment, sources):
    countSameColorNeighs = countSameColorNeighbors(x, y, assignment)
    countUnassignedNeighs = countNeighborsWithValue(x, y, assignment, )
    if(assignment[x][y] != "_"):
        if (x,y) in sources:
            if((countSameColorNeighs > 1) or (countUnassignedNeighs < ( 1 - countSameColorNeighs))):
                    return False
        else:
            if((countSameColorNeighs > 2) or (countUnassignedNeighs < ( 2 - countSameColorNeighs))):
                    return False
    return True

'''
Checks if puzzle is complete and no constraints violated
'''
def isAssignmentValid(assignment, sources):
    for x in range(len(assignment)):
        for y in range(len(assignment[0])):
            countSameColorNeighs = countSameColorNeighbors(x, y, assignment)
            if (x,y) in sources:
                if(countSameColorNeighs != 1):
                    return False
            else:
                if(countSameColorNeighs != 2):
                    return False
    return True

'''
number of neighbors with a specific value
'''
def countNeighborsWithValue(x, y, assignment, value = "_"):
    count = 0
    neighbors = getValidNeighbors(x, y, assignment)
    for neighbor in neighbors:
        neighborX = neighbor[0]
        neighborY = neighbor[1]
        if (assignment[neighborX][neighborY] == value):
            count += 1
    return count

'''
Counts the neighbors that have the same color as the cell specified
'''
def countSameColorNeighbors(x, y, assignment):
    count = 0
    neighbors = getValidNeighbors(x, y, assignment)
    for neighbor in neighbors:
        neighborX = neighbor[0]
        neighborY = neighbor[1]
        if(assignment[neighborX][neighborY] == assignment[x][y]):
            count += 1
    return count
'''
Takes a list of potential neighbors and an array and finds valid neighbors
'''
def getValidNeighbors(x,y, assignment):
    array = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
    validNeighbors = []
    cols = len(assignment)
    rows = len(assignment[0])
    for neighbor in array:
        x = neighbor[0]
        y = neighbor[1]
        if x >= 0 and y >= 0 and x < cols and y < rows:
            validNeighbors.append(neighbor)
    return validNeighbors
