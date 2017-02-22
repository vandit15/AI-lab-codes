from arff import load
import pickle
import sys
import matplotlib.pyplot as plt
import numpy as np
def train():
    file='data1.arff'
    dataset=load(open(file,'rb'))
    dataset = dataset[u'data']
    ##print dataset
    alpha = 0.001
    epochs = 200000
    cost = 0.0
    #for row in dataset:
    #    row[3] = float(row[3])
    mins = []
    maxs = []
    temp = []
    sums = []
    length = len(dataset[0])
    size = len(dataset)
    for i in range(length):
        temp = []
        for j in range(size):
            temp.append(dataset[j][i])
        mins.append(min(temp))
        maxs.append(max(temp))
        sums.append(sum(temp))
    #normalize
    for i in range(len(dataset[0])-1):
        for j in range(len(dataset)):
            dataset[j][i] = (dataset[j][i]-(sums[i]/float(size)))/(float(maxs[i]-mins[i]))
    thetas = []
    tempthetas = []
    derivative = []
    for i in range(length):
        thetas.append(0.0)
    for i in range(epochs):
        cost=0.0
        for row in dataset:
            hx = thetas[0]
            for k in range(length-1):
                hx = hx + row[k]*thetas[k+1]
            error = hx - row[-1]
            thetas[0] = thetas[0] - alpha*error/size
            for k in range(length-1):
                thetas[k+1] = thetas[k+1] - alpha*error*row[k]/size
            cost += error**2
        cost = cost/(2*size)
        print("epoch number %d : cost = %f ")%(i+1,cost)
    print thetas
    picklefile = open('sirkaregpicklefile.txt','wb')
    pickle.dump(thetas,picklefile)
    picklefile.close()

def test():
    picklefile  = open("sirkaregpicklefile.txt",'rb')
    thetas = pickle.load(picklefile)
    file='data1.arff'
    dataset=load(open(file,'rb'))
    dataset = dataset[u'data']
    #for row in dataset:
    #    row[3] = float(row[3])
    length = len(dataset[0])
    size = len(dataset)
    mins = []
    maxs = []
    temp = []
    sums = []
    for i in range(length):
        temp = []
        for j in range(size):
            temp.append(dataset[j][i])
        mins.append(min(temp))
        maxs.append(max(temp))
        sums.append(sum(temp))
    #normalize

    temp1 = []
    for j in range(size):
        temp1.append(float(dataset[j][0]))
    print temp1
    for i in range(len(dataset[0])-1):
        for j in range(len(dataset)):
            dataset[j][i] = (dataset[j][i]-(sums[i]/float(size)))/(float(maxs[i]-mins[i]))
    for row in dataset:
        hx = thetas[0]
        for i in range(len(dataset[0])-1):
            hx += thetas[i+1]*row[i]
        print("Actual %f predicted %f")%(row[-1],hx)
    list = []
    for i in range(size):
        list.append(thetas[1]*temp1[i] + thetas[0])
    fig,ax = plt.subplots()
    ax.plot(temp1,list,color='red')
    print temp
    temp = np.array(temp)
    temp1 = np.array(temp1)
    ax.scatter(temp1,temp)
    #plt.plot(temp1,temp)
    plt.show()

arg = sys.argv[1]
if arg == "-train":
    train()
else:
    test()
