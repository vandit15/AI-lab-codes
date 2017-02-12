import sys
f = open('tag.txt', 'r')
w = open('testbig.txt','w')
count = 0
for line in f:
	if not line.startswith('#'):
		l = line.split("\t")
		if l[0] == '\n':
			w.write(str(l[0]))
		else:
			s = str(l[0]).lower()+"\n"
			w.write(str(s))
w.close()
f.close()
