from arff import load
import pickle
from math import log,exp
import sys

def train():
    file='Classification_Datasets/diabetes.arff'
    dataset=load(open(file,'rb'))
    dataset = dataset[u'data']
    #print dataset[0][0]
    alpha = 0.015
    epochs = 60000
    cost = 0.0
    theta = []
    for row in dataset:
        if row[-1] == "tested_positive":
            row[-1] = 1
        else:
            row[-1] = 0
    thetas = []
    for i in range(len(dataset[0])):
        thetas.append(0.0)
    length = len(dataset[0])
    size = len(dataset)
    for i in range(len(dataset)):
        for j in range(length):
            dataset[i][j] = float(dataset[i][j])

    for k in range(epochs):
        cost = 0.0
        for row in dataset:
            hx = thetas[0]
            for i in range(length-1):
                hx = thetas[i+1]*float(row[i])
            shx = 1/(1+exp(-hx))
            error = shx - float(row[-1])
            cost  = cost + log(shx)*float(row[-1]) + (1-float(row[-1]))*(log(1-shx))
            thetas[0] = thetas[0] - alpha*error/size
            for i in range(length-1):
                thetas[i+1] = thetas[i+1] - error*alpha*float(row[i])/size
        cost=-cost/size
        print("epoch %d : cost = %f") % (k+1,cost)
    for i in range(length):
        print("theta %d:%f")%(i,thetas[i])
    picklefile = open("pickle.txt",'wb')
    pickle.load(thetas,picklefile)


var = sys.argv[1]
if var == "-train":
    train()
elif var == "-test":
    test()
