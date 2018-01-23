import numpy as np
import matplotlib.pyplot as plt

# Opens the files
def readfiles():
    testlabels = open('./testlabels')
    testimages = open('./testimages')
    traininglabels = open('./traininglabels')
    trainingimages = open('./trainingimages')
    return testlabels, testimages, traininglabels, trainingimages

# Sets images and labels being analyzed
def setfiles(traininglabels, trainingimages):
    labels = np.empty(5000, dtype = np.uint8)
    images = np.zeros((5000, 785), dtype = np.uint8)
    for i in range(5000):
        labels[i] = int(next(traininglabels))
        for j in range(28):
            images[i, 28*j:28*(j+1)] = np.fromstring(next(trainingimages)[:-1], dtype = np.uint8)
    images = images - ord(' ')
    for i in range(5000):
        for j in range(785):
            if images[i, j] > 0 : 
                images[i, j] = 1
    return images, labels

# Training curve and accuracy on training set
def getAccuracy(images, labels):
    accy = np.empty(10)
    multi_class = np.zeros((10, 785))
    np.random.seed(0)
    #EPOCH
    for i in range(10):
        #Alpha set by decay rate and epoch
        a = float(10000) / (float(10000) + i)
        actual = 5000
        for j in np.random.permutation(5000):
            label = labels[j]
            image = images[j]
            estimatedLabel = np.argmax(np.dot(multi_class, image))
            if label != estimatedLabel:
                multi_class[estimatedLabel] = multi_class[estimatedLabel] - (image * a)
                multi_class[label] = multi_class[label] + (image * a)
                actual -= 1
        accy[i] = actual
    averageaccuracy = 0;
    for i in range(10):
        averageaccuracy += accy[i] / 5000
    averageaccuracy = averageaccuracy / 10
    print averageaccuracy
    for i in range(10):
        accy[i] = accy[i] / 500
    plt.plot(accy / 10)
    return multi_class, image, label

# Confusion Matrix and accuracy on test set 
def getConfusionMatrix(label, image, testlabels, testimages):
    confusion_matrix = np.zeros((10, 10))
    for i in range(1000):
        label = int(next(testlabels))
        for j in range(28):
            image[28*j:28*(j+1)] = np.fromstring(next(testimages)[:-1], dtype = np.uint8)
        image = image - ord(' ')
        for l in range(785):
            if image[l] > 0 : 
                image[l] = 1
        estimatedLabel = np.argmax(np.dot(multi_class, image))
        confusion_matrix[label, estimatedLabel] += 1
    sumMatrix = np.zeros((10,10))
    for i in range(10):
        sumamount = 0;
        for j in range(10):
            sumamount += confusion_matrix[i][j]
        for j in range(10):
            confusion_matrix[i][j] = round((confusion_matrix[i][j] / sumamount), 3)
    return confusion_matrix

np.set_printoptions(suppress = True)
testlabels, testimages, traininglabels, trainingimages = readfiles()
images, labels = setfiles(traininglabels, trainingimages)
multi_class, image, label = getAccuracy(images, labels)
print((getConfusionMatrix(label, image, testlabels, testimages)))
plt.show()


