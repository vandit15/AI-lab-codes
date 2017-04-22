f = open('input.txt','r')

sentences = []
for line in f:
    l = line.split(" ")
    temp = []
    if line.startswith('\n'):
        break
    for i in l:
        if i!="":
            temp.append(i)
    sentences.append(temp)

for i in sentences:
    s = len(i)
    i[s-1] = i[s-1][:-1]

#print sentences
stack = []
for line in sentences:
    for i in line:
        if i[0]=='(':
            stack.append('(')
            word = ""
            c = 1;
            while c < len(i):
                word += i[c]
                c+=1
            stack.append(word)

        if i[-1]==')':
            c= 0
            word = ""
            while i[c]!=')':
                word += i[c]
                c+=1
            stack.append(word)
            for x in range(c,len(i)):
                stack.append(')')


for i in stack:
    if i == ')':
            
#for ch in stack:
    #if ch =='(':
print stack
