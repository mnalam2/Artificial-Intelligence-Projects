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
        newImages.append(images[i:(i+28)])
        i+= 28
    return newImages


def createLabelMap(images, labels):
    imageDict = {}
    for i in range(10):
        imageDict[i] = []
    for i in range(len(labels)):
        imageDict[labels[i]].append(images[i])

    return imageDict


def countFeaturesMap (imageDict):
    featuresDict = {}
    for d in range(10):
        featuresDict[d] = {}
        for l in range (len(imageDict[d])):
            for i in range(28):
                for j in range(28):
                    if((i,j) not in featuresDict[d]):
                        featuresDict[d][(i,j)] = [0,0]
                    if(imageDict[d][l][i][j] == '+' or imageDict[d][l][i][j] == '#'):
                        featuresDict[d][(i,j)][1] += 1
                    else:
                        featuresDict[d][(i,j)][0] += 1
    return featuresDict


def featureLikelihoods (featuresDict, smoothingFactor):
    featureLikelihoodDict = {}
    for d in range(10):
        featureLikelihoodDict[d] = {}
        for i in range(28):
            for j in range(28):
                if ((i, j) not in featureLikelihoodDict[d]):
                    featureLikelihoodDict[d][(i, j)] = [0.0, 0.0]
                for v in range(2):
                    featureLikelihoodDict[d][(i,j)][v] = ((float(featuresDict[d][(i,j)][v]) + float(smoothingFactor)) / (float(featuresDict[d][(i,j)][0]) + float(featuresDict[d][(i,j)][1]) + float(smoothingFactor*2.0)))

    return featureLikelihoodDict


def getPriors(imagesDict):
    priors = []
    for i in range(10):
        priors.append((float(len(imagesDict[i])))/ 5000.0)
    return priors

def maximumAPosteriori(featureLikelihoods, priors, testImages):
    estimatedLabels = []
    for l in range(len(testImages)):
        posteriorProbabilites = [np.log(prior) for prior in priors]
        for d in range(10):
            for i in range(28):
                for j in range(28):
                    if(testImages[l][i][j] == "+" or testImages[l][i][j] == "#"):
                        posteriorProbabilites[d] += np.log(featureLikelihoods[d][(i,j)][1])
                    else:
                        posteriorProbabilites[d] += np.log(featureLikelihoods[d][(i,j)][0])
        estimatedLabels.append((np.argmax(np.array(posteriorProbabilites)), np.max(np.array(posteriorProbabilites))))

    return estimatedLabels


def getAccuracy(estimatedLabels, testLabels):
    sumMatrix = np.zeros((10,10))
    for i in range(len(testLabels)):
        sumMatrix[estimatedLabels[i][0]][testLabels[i]] += 1.0


    print(sumMatrix[0])

    confusionMatrix = np.zeros((10,10))
    for i in range(10):
        for j in range(10):
            confusionMatrix[i][j] = round((sumMatrix[i][j] / float(np.sum(sumMatrix[j]))), 3)
    return confusionMatrix


def getMostPrototypical(estimatedLabels, testLabels, testImages, digit):
    classifieds = []
    for i in range(len(testLabels)):
        if(estimatedLabels[i][0] == testLabels[i] and testLabels[i] == digit):
            classifieds.append((i, estimatedLabels[i][1]))

    mostPrototypical = []
    mostPrototypicalProbability = -np.inf

    for classified in classifieds:
        if(classified[1] > mostPrototypicalProbability):
            mostPrototypicalProbability = classified[1]
            mostPrototypical = testImages[classified[0]]

    return mostPrototypical, mostPrototypicalProbability


def getLeastPrototypical(estimatedLabels, testLabels, testImages, digit):
    classifieds = []
    for i in range(len(testLabels)):
        if (estimatedLabels[i][0] == testLabels[i] and testLabels[i] == digit):
            classifieds.append((i, estimatedLabels[i][1]))

    leastPrototypical = []
    leastPrototypicalProbability = np.inf

    for classified in classifieds:
        if (classified[1] < leastPrototypicalProbability):
            leastPrototypicalProbability = classified[1]
            leastPrototypical = testImages[classified[0]]

    return leastPrototypical, leastPrototypicalProbability



def getPrototypicals(estimatedLabels, testLabels, testImages):
    mostPrototypicals = []
    leastPrototypicals = []

    for digit in range(10):
        mostPrototypical, mostPrototypicalProbability = getMostPrototypical(estimatedLabels, testLabels, testImages, digit)
        leastPrototypical, leastPrototypicalProbability = getLeastPrototypical(estimatedLabels, testLabels, testImages, digit)
        mostPrototypicals.append((digit, mostPrototypical, mostPrototypicalProbability))
        leastPrototypicals.append((digit, leastPrototypical, leastPrototypicalProbability))

    return mostPrototypicals, leastPrototypicals


def getOddsRatio(digit1, digit2, featureLikelihoods):
    odds = np.zeros((28,28))
    for i in range (28):
        for j in range(28):
            odds[i][j] = (np.log(featureLikelihoods[digit1][(i,j)][1] / featureLikelihoods[digit2][(i,j)][1]))
    return odds


def getFeatureImage(digit):
    img = np.zeros((28,28))
    for i in range(28):
        for j in range(28):
            img[i][j] = (featureLikelihoodDict[digit][(i,j)][1])
    return img






def writeImageToFile(image, fileName):
    np.savetxt(fileName, np.array(image), fmt = '%s', delimiter = '')

np.set_printoptions(suppress=True)
k = 0.1
images = parseFile("trainingimages.txt")
labels = list(map(lambda x: int(x[0]), parseFile("traininglabels.txt")))
images = splitImages(images)
imageDict = createLabelMap(images, labels)
priors = getPriors(imageDict)
featuresDict = countFeaturesMap(imageDict)
#print(featuresDict)
featureLikelihoodDict = featureLikelihoods(featuresDict, k)
#print(featureLikelihoodDict)

testImages = parseFile("testimages.txt")
testImages = splitImages(testImages)
testLabels = list(map(lambda x: int(x[0]), parseFile("testlabels.txt")))

estimatedLabels = maximumAPosteriori(featureLikelihoodDict, priors, testImages)

prototypicals = getPrototypicals(estimatedLabels, testLabels, testImages)

#print(prototypicals[0])
#print(prototypicals[1])

num = 9
writeImageToFile(prototypicals[0][num][1], "mostPrototypicalImage.txt")
writeImageToFile(prototypicals[1][num][1], "leastPrototypicalImage.txt")
#print(estimatedLabels)

print((getAccuracy(estimatedLabels, testLabels)))

digit1 = 9
digit2 = 4
odds = getOddsRatio(digit1, digit2, featureLikelihoodDict)
img1 = getFeatureImage(digit1)
img2 = getFeatureImage(digit2)
#print (odds)

plt.figure(0)
plt.imshow(img1, cmap = "RdYlBu")
plt.colorbar()

plt.show()

plt.figure(1)
plt.imshow(img2, cmap = "RdYlBu")
plt.colorbar()

plt.show()

plt.figure(2)
plt.imshow(odds, vmin = -3, vmax = 1, cmap = "RdYlBu")
plt.colorbar()

plt.show()

