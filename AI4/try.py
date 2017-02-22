import arff
from math import exp,log
import sys
import pickle
import matplotlib.pyplot as plt

def train():
    src='Classification_Datasets/diabetes.arff'
    dataset = arff.load(open(src,'rb'))#dataset=load_arff()
    data=dataset[u'data']
    for row in data:
        if row[-1]=="tested_positive":
            row[-1]=1
        else:
            row[-1]=0
    epochs = 50000
    length = len(data)
    l_rate = 0.009
    thetas = []
    tempthetas = []
    for i in range(len(data[0])):
        thetas.append(0.0)
        tempthetas.append(0.0)
    for i in range(epochs):
        cost=0.0
        for row in data:
            hx=float(thetas[0])
            for k in range(len(row)-1):
                hx+=float(row[k])*thetas[k+1]
            shx =  1/(1+exp(-hx))
            error = shx-float(row[-1])
            cost+=(log(1-shx))*(1-float(row[-1])) + log(shx)*float(row[-1])
            tempthetas[0] = thetas[0] - l_rate * error/length
            for k in range(len(row)-1):
                tempthetas[k + 1] = thetas[k + 1] - error*l_rate*float(row[k])/length
            for k in range(len(row)):
                thetas[k] = tempthetas[k]
        cost=-cost/length
        print("Iteration-%d : cost = %f") %(i+1,cost)
    for i in range(len(thetas)):
        print thetas[i]
    picklefile = open("pickle.txt",'wb')
    pickle.dump(thetas,picklefile)
    picklefile.close()

def test():
    picklefile = open("pickle.txt",'rb')
    thetas = pickle.load(picklefile)
    print thetas
    src = 'Classification_Datasets/diabetes.arff'
    dataset = arff.load(open(src,'rb'))
    data=dataset[u'data']
    for row in data:
        if row[-1] == "tested_positive":
            row[-1] = 1
        else:
            row[-1] = 0
    true=0
    x1 = []
    x0 = []
    x0d = []
    x1d = []
    for row in data:
        value = thetas[0]
        for k in range(len(row)-1):
            value += thetas[k+1]*row[k]
        value = 1/(1+exp(-value))
        if value > 0.5:
            x0.append(row[0])
            x1.append(row[1])
            print "1 " + str(row[-1])
            if row[-1] == 1:
                true+=1
        else:
            x0d.append(row[0])
            x1d.append(row[1])
            print "0 " + str(row[-1])
            if row[-1] == 0:
                true+=1
    print("\nAccuracy : %f") %(float(true)/float(len(data)))
    plt.plot(x0,x1,"r+",x0d,x1d,"bo")
    plt.show()


var = sys.argv[1]
if var == "-train":
    train()
else:
    test()
