import Utilities
import time
import numpy as np

#opens attempts file
file = open("num_attempts.txt",'w')

'''
Dumb algorithm implementation
'''
def recursiveBacktracking(assignment, domain, sources):
    #gets random unassigned grid
    index = Utilities.getUnassignedIndexNearColored(assignment)
    #print(index)
    #if all grids assigned
    if(index is None):
        if(Utilities.isAssignmentValid(assignment, sources)):
            #if puzzle is full and correct, return
            file.close()
            return assignment
        return None

    #for each color
    for value in domain:
        #if value doesn't violate constraints
        if Utilities.isValueConsistent(index, value, assignment, sources):
            #increment attempts
            file.write('attempt\n')
            #print("Assigning " + value + " to " + "(" + str(index[0]) + ", " + str(index[1]) + ")\n")
            #assign grid that value
            assignment[index[0]][index[1]] = value
            #print(np.array(assignment))
            #recursively search
            result = recursiveBacktracking(assignment, domain, sources)
            if result is not None:
                return result
            assignment[index[0]][index[1]] = "_"
    return None

'''
Smart algorithm implementation
'''
def recursiveBacktracking_mcv(assignment, domain, sources):
    #gets all unassigned grids neighboring a colored grid
    indexes = Utilities.getAllUnassignedIndexNearColored(assignment)
    #gets most constrained grid
    index = Utilities.getMostConstrainedVariable(indexes,domain,assignment,sources)
    #print(index)
    #if all grids assigned
    if(index is None):
        if(Utilities.isAssignmentValid(assignment, sources)):
            #if puzzle is full and correct, return
            file.close()
            return assignment
        return None

    #for each color
    for value in domain:
        #if value doesn't violate constraints
        if Utilities.isValueConsistent(index, value, assignment, sources):
            #print("Assigning " + value + " to " + "(" + str(index[0]) + ", " + str(index[1]) + ")\n")
            #increment attempts
            file.write('attempt\n')
            #assign grid that value
            assignment[index[0]][index[1]] = value
            #print(np.array(assignment))
            #recursively search
            result = recursiveBacktracking_mcv(assignment, domain, sources)
            if result is not None:
                return result
            assignment[index[0]][index[1]] = "_"

    return None

#start timing
startTime = time.time()
#initialize array, domain, sources
array = Utilities.parseArray("input991.txt")
domain = Utilities.getDomain(array)
sources = Utilities.getSources(array)
#solve puzzle
result = recursiveBacktracking_mcv(array, domain, sources)
#print and save solution
print(np.array(result))
Utilities.writeArrayToFile(result, "output991.txt")
#end timing
endTime = time.time()
print("Search took " + str(endTime - startTime) + " seconds.")
#print number of value assignments attempted
file = open('num_attempts.txt','r')
print("Values attempted: " + str(len(file.readlines())))
file.close()
