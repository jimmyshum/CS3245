
import sys
import nltk
import getopt
import os 
from nltk.stem import *
import math

def usage():
    print "usage: " + sys.argv[0] + " -i directory-of-documents -d dictionary-file -p posting-file"


# main : get the input filenames and directory
d1 = d2 = None
try:
    opts, args = getopt.getopt(sys.argv[1:], 'o:t:')
except getopt.GetoptError, err:
    usage()
    sys.exit(2)
for o, a in opts:
    if o == '-o':
        d1 = a
    elif o == '-t':
        d2 = a
    else:
        assert False, "unhandled option"
if d1 == None or d2 == None :
    usage()
    sys.exit(2)

# clear content of dict and posting files
f = open(d1)
expect = []
for line in f:
    expect.append(line)
f.close()
print expect

f = open(d2)
result = []
for line in f :
    token = line.split(" ")
    result =(token)
f.close()


print result

count = 0
i = 0
for rterm in result:
    i = i +1
    for eterm in expect:
        rterm_mod = rterm[:-4] + '\r\n'
        if rterm_mod == eterm :
            count +=  1
            print i, ": ", eterm

print "count :", count, 
print "\n size =", len(result)
print "\n % = ", float (count)/len(result) 