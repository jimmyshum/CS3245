#!/usr/bin/python
import re
import nltk
import sys
import getopt

mdb = []
idb = []
tdb = []

def build_LM(in_file):
    """
    build language models for each label
    each line in in_file contains a label and an URL separated by a tab(\t)
    """
    print 'building language models...'
    # This is an empty method
    # Pls implement your code in below
    
    
    f = open(in_file, 'r')

    
    for line in f:
        lang = line.split(" ")[0]
        line = line.replace(lang+" ","")
        alpha = list(line)
        
        if lang == "malaysian":

            for i in range(0, len(alpha)-5):
                temp = []
                for j in range (i, i+4):
                    temp.append(alpha[j])
                mdb.append(temp)

        if lang == "indonesian":
            for i in range(0, len(alpha)-5):
                temp = []
                for j in range (i, i+4):
                    temp.append(alpha[j])
                idb.append(temp)
        
        if lang == "tamil":
            for i in range(0, len(alpha)-5):
                temp = []
                for j in range (i, i+4):
                    temp.append(alpha[j])
                tdb.append(temp)

        remain = line
    
    f.close()

def searchMalayDB(test):
    prob = 0.0
    match = 1
    total = len(mdb)

    for i in range(0, len(mdb)-1):
        isMatch = 1
        data = mdb[i]
        for j in range(0, 4):
            if test[j] != data[j]:
                isMatch = 0

        if isMatch == 1:
            match = match + 1
    prob = float(match)/total + 1

    #test
    #print "Malay - ",test,": ",match,"/",total," ",prob

    return prob

    
def searchIndoDB(test):
    prob = 0.0
    match = 1
    total = len(idb)

    for i in range(0, len(idb)-1):
        isMatch = 1
        data = idb[i]
        for j in range(0, 4):
            if test[j] != data[j]:
                isMatch = 0

        if isMatch == 1:
            match = match + 1
    prob = float(match)/total + 1

    #test
    #print "Indo - ",test,": ",match,"/",total," ",prob

    return prob

def searchTamilDB(test):
    prob = 0.0
    match = 1
    total = len(tdb)
    for i in range(0, len(tdb)-1):
        isMatch = 1
        data = tdb[i]
        for j in range(0, 4):
            if test[j] != data[j]:
                isMatch = 0

        if isMatch == 1:
            match = match + 1
    prob = float(match)/total + 1

    #test
    #print "Tamil - ",test,": ",match,"/",total," ",prob

    return prob
def findHighest(p1,p2,p3):
    curr = 1
    h = p1
    if(p2 > h): 
        h = p2
        curr = 2
    if(p3 > h):
        h = p3
        curr = 3
    return curr


def test_LM(in_file, out_file, LM):

    """
    test the language models on new URLs
    each line of in_file contains an URL
    you should print the most probable label for each URL into out_file
    """
    print "testing language models..."
    # This is an empty method
    # Pls implement your code in below

    inFile = open(in_file, 'r')
    outFile = open(out_file, 'w')

    for line in inFile:
        alpha = list(line)
        ttProbM = 1;
        ttProbI = 1;
        ttProbT = 1;
        isOther = 0;


        for i in range(0, len(alpha)-5):
            test = []
            
            for j in range (i, i+4):
                test.append(alpha[j])    

            probM = searchMalayDB(test)
            probI = searchIndoDB(test)
            probT = searchTamilDB(test)

            if probM == probI == probT == 0.0:
                isOther = 1
                output = 4

            ttProbM = ttProbM * probM
            ttProbI = ttProbI * probI
            ttProbT = ttProbT * probT
            
        #test
        #print ttProbM, " : ", ttProbI, " : ",ttProbT

        if isOther == 0:
            output = findHighest(ttProbM,ttProbI,ttProbT)

        if output == 1:
            outFile.write("malaysian ")
        if output == 2:
            outFile.write("indonesian ")
        if output == 3:
            outFile.write("tamil ")
        if output == 4:
            outFile.write("other ")

        outFile.write(line)

    inFile.close()
    outFile.close()


def usage():
    print "usage: " + sys.argv[0] + " -b input-file-for-building-LM -t input-file-for-testing-LM -o output-file"

input_file_b = input_file_t = output_file = None
try:
    opts, args = getopt.getopt(sys.argv[1:], 'b:t:o:')
except getopt.GetoptError, err:
    usage()
    sys.exit(2)
for o, a in opts:
    if o == '-b':
        input_file_b = a
    elif o == '-t':
        input_file_t = a
    elif o == '-o':
        output_file = a
    else:
        assert False, "unhandled option"
if input_file_b == None or input_file_t == None or output_file == None:
    usage()
    sys.exit(2)

LM = build_LM(input_file_b)
test_LM(input_file_t, output_file, LM)
