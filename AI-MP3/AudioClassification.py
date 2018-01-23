import numpy as np
import pprint
import matplotlib.pyplot as plt
import matplotlib.colors as colors


def parseFile(fileName):
    path = './' + fileName
    with open(path) as file:
        images = [[c for c in line[:-1]] for line in file]
    return images

def splitImages (images):
    newImages = []
    i = 0
    while ( i < len(images)):
        newImages.append(images[i:(i+25)])
        i+= 28
    return newImages


def countEnergyMap (yesImages, noImages):
    energyDict = {}
    energyDict[0] = {}
    energyDict[1] = {}

    for l in range (len(yesImages)):
        for i in range(25):
            for j in range(10):
                if((i,j) not in energyDict[0]):
                    energyDict[0][(i,j)] = [0,0]
                if(yesImages[l][i][j] == '%'):
                    energyDict[0][(i,j)][1] += 1
                else:
                    energyDict[0][(i,j)][0] += 1

    for l in range (len(noImages)):
        for i in range(25):
            for j in range(10):
                if((i,j) not in energyDict[1]):
                    energyDict[1][(i,j)] = [0,0]
                if(noImages[l][i][j] == '%'):
                    energyDict[1][(i,j)][1] += 1
                else:
                    energyDict[1][(i,j)][0] += 1
    return energyDict

def energyLikelihoods (energyDict, smoothingFactor):
    energyLikelihoodDict = {}
    for c in range(2):
        energyLikelihoodDict[c] = {}
        for i in range(25):
            for j in range(10):
                if ((i, j) not in energyLikelihoodDict[c]):
                    energyLikelihoodDict[c][(i, j)] = [0.0, 0.0]
                for v in range(2):
                    energyLikelihoodDict[c][(i,j)][v] = ((float(energyDict[c][(i, j)][v]) + float(smoothingFactor)) / (float(energyDict[c][(i, j)][0]) + float(energyDict[c][(i, j)][1]) + float(smoothingFactor * 2.0)))

    return energyLikelihoodDict


def getPriors(yesImages, noImages):
    totalSize = len(yesImages) + len(noImages)
    return [(float(len(yesImages)) / (float(totalSize))), (float(len(noImages)) / (float(totalSize)))]

def maximumAPosteriori(energyLikelihoods, priors, testImages):
    estimatedLabels = []
    for l in range(len(testImages)):
        posteriorProbabilites = [np.log(prior) for prior in priors]
        for c in range(2):
            for i in range(25):
                for j in range(10):
                    if(testImages[l][i][j] == "%"):
                        posteriorProbabilites[c] += np.log(energyLikelihoods[c][(i, j)][1])
                    else:
                        posteriorProbabilites[c] += np.log(energyLikelihoods[c][(i, j)][0])
        estimatedLabels.append((np.argmax(np.array(posteriorProbabilites)), np.max(np.array(posteriorProbabilites))))

    return estimatedLabels

def getAccuracy(estimatedLabels, testLabels):
    sumMatrix = np.zeros((2,2))
    for i in range(len(estimatedLabels)):
        sumMatrix[estimatedLabels[i][0]][testLabels[i]] += 1.0


    print(sumMatrix[0])

    confusionMatrix = np.zeros((2,2))
    for i in range(2):
        for j in range(2):
            confusionMatrix[i][j] = ((sumMatrix[i][j] / float(np.sum(sumMatrix[j]))))
    return confusionMatrix


np.set_printoptions(suppress=True)
k = 3
yesTrainingImages = splitImages(parseFile("yes_train.txt"))
noTrainingImages = splitImages(parseFile("no_train.txt"))
yesTestImages = splitImages(parseFile("yes_test.txt"))
noTestImages = splitImages(parseFile("no_test.txt"))
#print(yesTrainingImages[1])
energyDict = countEnergyMap(yesTrainingImages, noTrainingImages)
#print(energyDict)
energyLikelihoods = energyLikelihoods (energyDict, k)
#print(energyLikelihoods)
priors = getPriors(yesTrainingImages, noTrainingImages)
#print(priors)

estimatedLabels = maximumAPosteriori(energyLikelihoods, priors, yesTestImages + noTestImages)
yesLabels = [0] * len(yesTestImages)
noLabels = [1] * len(noTestImages)
testLabels = yesLabels + noLabels
confusionMatrix = getAccuracy(estimatedLabels, testLabels)
print(confusionMatrix)