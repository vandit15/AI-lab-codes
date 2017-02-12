import sys
import pickle

def train():
    if sys.argv[2]=="1234":
        file_name="train.txt"
    else:
        file_name=sys.argv[2]

    training_file = open(file_name,'r')
    words = set()
    tags = set()
    for lines in training_file.readlines():
        line = lines.split('\t')
        if line[0]!='\n':
            words.add(line[0])
            tags.add(line[1])
    words = list(words)
    tags = list(tags)

    # Making dictionary of words
    dictWords = {}
    dictTags = {}
    count = 0
    for i in tags:
        dictTags[i] = count
        count+=1
    count=0
    for i in words:
        dictWords[i] = count
        count+=1

    # using line proposition to set P, T, E
    tag_count = [0 for i in range(len(tags))]
    P = [0 for i in range(len(tags))]
    T = [[0 for i in range(len(tags))] for i in range(len(tags))]
    E = [[0 for i in range(len(words))] for i in range(len(tags))]


    training_file.close()
    training_file = open(file_name,'rb')
    prevTag = ''
    check = 1
    noofSen = 0
    for line in training_file.readlines():
        l = line.split('\t')
        if l[0] != '\n':
            if check==1:
                P[dictTags[l[1]]]+=1
                E[dictTags[l[1]]][dictWords[l[0]]]+=1
                tag_count[dictTags[l[1]]]+=1
                check = 0
                noofSen+=1
                prev_tag = l[1]
            else:
                try:
                    tag_count[dictTags[l[1]]]+=1
                    E[dictTags[l[1]]][dictWords[l[0]]]+=1
                    T[dictTags[prev_tag]][dictTags[l[1]]] +=1
                    prev_tag = l[1]
                except:
                    print(l)
        else:
            check = 1
    training_file.close()
    for i in range(len(tags)):
		for j in range(len(words)):
			E[i][j]=E[i][j]*1.0/tag_count[i]
    for i in range(len(tags)):
		for j in range(len(tags)):
			T[i][j]=T[i][j]*1.0/tag_count[i]
    for i in range(len(tags)):
		P[i]=P[i]*1.0/noofSen
    pickleList = [P,T,E,words,tags]
    picklefile = open('pickle.txt','wb')
    pickle.dump(pickleList,picklefile)

    for i in range(len(tags)):
        print P[i]

    for i in range(len(tags)):
        for j in range(len(tags)):
            print T[i][j], " "
        print "\n"

def test():
    testData = []
    sntnce=[]
    testfile = open(sys.argv[2],'r')
    for line in testfile.readlines():
        if line!='\n':
			sntnce.append(line[:-1])
        else:
            testData.append(sntnce)
            sntnce = []

    if sntnce:
        testData.append(sntnce)
	testfile.close()
    picklefile = open('pickle.txt','rb')
    picklelist = pickle.load(picklefile)
    P = picklelist[0]
    T = picklelist[1]
    E = picklelist[2]
    tags = picklelist[4]
    words = picklelist[3]
    dictWords = {}
    i = 0
    for word in words:
		dictWords[word]=i
		i+=1

    dictTags = {}
    i=0
    for tag in tags:
		dictTags[tag]=i
		i+=1

    prediction = open('prediction.txt','w')
    for l in testData:
        T1 = [[0 for i in range(len(l))] for j  in range(len(tags))]
        T2 = [[0 for i in range(len(l))] for j  in range(len(tags))]
        for tag in tags:
            T1[dictTags[tag]][0]=P[dictTags[tag]]*E[dictTags[tag]][dictWords[l[0]]]
            T2[dictTags[tag]][0]=0
        t=1

        while t < len(l):
            for tag in tags:
                prob = -1
                for tag_iters in tags:
                    T1[dictTags[tag]][t] = max(prob,E[dictTags[tag]][dictWords[l[t]]]*T1[dictTags[tag_iters]][t-1]*T[dictTags[tag_iters]][dictTags[tag]])
                    prob = T1[dictTags[tag]][t]
                    if T1[dictTags[tag]][t] == E[dictTags[tag]][dictWords[l[t]]]*T1[dictTags[tag_iters]][t-1]*T[dictTags[tag_iters]][dictTags[tag]]:
                        T2[dictTags[tag]][t] = dictTags[tag_iters]
            t+=1
        prob=-1
        for tag_iters in tags:
            if T1[dictTags[tag_iters]][t-1] > prob:
                prob = T1[dictTags[tag_iters]][t-1]
                z = dictTags[tag_iters]
        stack=[z]
        t=len(l)-1

        while t>0:
            z = T2[z][t]
            stack.append(z)
            t-=1
        stack.reverse()

        for i in range(len(l)):
            prediction.write(l[i]+"\t"+tags[stack[i]])
        prediction.write("\n")
    prediction.close()

if sys.argv[1] == "-train":
    train()
else:
    test()
