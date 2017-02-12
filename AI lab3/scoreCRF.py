import sys
import pandas as pd
from sklearn.metrics import confusion_matrix as cm
from sklearn.metrics import precision_recall_fscore_support as pr
from sklearn.metrics import accuracy_score as acc
from sklearn.metrics import classification_report as cr
fA = open('testAns.txt', 'r')
fO = open('prediction.txt', 'r')
ans=[]
out=[]
for line in fA:
	if not line.startswith('#'):
		l = line.split("\t")
		if not l[0] == '\n':
			s = str(l[1])
			s = s[0:len(s)-1]
			ans.append(s)
for line in fO:
	if not line.startswith('#'):
		l = line.split("\t")
		if not l[0] == '\n':
			s = str(l[1])
			s = s[0:len(s)-1]
			out.append(s)
label=pd.Series(ans).unique()
print "\nlabels:" + str(label)
prf = pr(ans,out,labels=label,beta=1,average='weighted')
print "\nPresicion:" + str(prf[0])
print "\nRecall:" + str(prf[1])
print "\nF Score:" + str(prf[2])
acp = acc(ans,out,True)
act = acc(ans,out,False)
acp = acp*100
print "\nAccuracy:"+str(acp)+"%      "+str(act)+"/"+str(len(ans))
report = cr(ans,out,label)
print str(report)
prf = pr(ans,out,labels=label,beta=1,average=None)
sc = pd.DataFrame(index=['Precision','Recall','F Score','Support'],columns=label)
sc[:]=prf[:]
sc=pd.DataFrame.transpose(sc)
print "\n\n"
print str(sc)
arr = cm(ans,out,label)
mat = pd.DataFrame(index=label,columns=label)
mat[:]=arr[:]
print "\n\n"
print u"\u2193"+"Actual/Predicted-->"
print (str(mat))
fA.close()
fO.close()

