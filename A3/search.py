import re
import nltk
import sys
import getopt
import os

def search(dictionary_file,postings_file,input_file,output_file):
	inFile = open(input_file,'r')
	outFile = open(output_file,'w')
	for line in inFile:
		wordScoreList = []
		tokens = nltk.word_tokenize(line)
		for i in range(0,len(tokens)):
			word = tokens[i]
			resultList = evaluateQuery(word,dictionary_file,postings_file)
			tf_idf = calTFIDF(resultList)
			wordScore = []
			wordScore.append(word)
			wordScore.append(tf_idf)
			wordScoreList.append(wordScore)

		
		####Test 
		sorted(list(scoreList))
		for i in range(0,len(scoreList)):
			print scoreList[i] + " "

		####

		####
		for i in range(0, len(resultInnerList)-1):
			outFile.write( resultInnerList[i] + " ")
		outFile.write(resultInnerList[len(resultInnerList)-1]+"\n")
		####
	

def evaluateQuery(word,dictionary_file,postings_file):
	## term freq.[0] 
	## doc. freq.[1] 
	## N
	resultList = get_posting(postings_file, list[i], read_dictionary(dictionary_file))
	return resultList

def calTFIDF(resultList):
	tf = resultList[0]
	df = resultList[1]
	N = resultList[2]
	tf = 1 + math.log(tf,10)
	## temp 
	if df == 0:
		df = 1
	##

	if df != 0:
		idf = math.log(N/df, 10)

	return tf*idf


def read_dictionary(dictionary_file):
	dictionary = []
	line_num = 0
	dict_file = open(dictionary_file)
	for line in dict_file:
		word = line.split(" ")
		word[1] = int(word[1])
		dictionary.append(word)
		line_num = line_num + 1
	dict_file.close()
	return dictionary

def find_index(term, list):
	count = 0
	for item in list:
		if (term == item[0]):
			return count
		else:
			count = count + 1
	return -1

def get_posting(postings_file, term, dictionary):
	post_file = open(postings_file, "r+")
	# read posting and get line_offset for jumping
	line_offset =[]
	offset =0
	for line in post_file:    
		line_offset.append(offset)    
		offset += len(line)
	post_file.seek(0)

	# read target posting list from file
	dict_posit = find_index(term, dictionary)
	if (dict_posit < len(line_offset) ):
		post_file.seek(line_offset[dict_posit])
	else:
		post_file.seek(0,2)
	
	target_line = post_file.readline()
	target_line_postings = target_line.split(" ")
	target_line_postings.remove("\n")
	return target_line_postings


def getDocListLenList():
	docList = []
	path = "/Users/Jimmy/Documents/CS3245/reuters/training/"
	dirs = os.listdir( path )
	for i in range (1,len(dirs)+1):
		docList.append(i)
	return docList


def usage():
    print "usage: " + sys.argv[0]

dictionary_file = postings_file = input_file = output_file = None

try:
    opts, args = getopt.getopt(sys.argv[1:], 'd:p:q:o:')
except getopt.GetoptError, err:
    usage()
    sys.exit(2)
for o, a in opts:
    if o == '-d':
        dictionary_file = a
    elif o == '-p':
        postings_file = a
    elif o == '-q':
        input_file = a
    elif o == '-o':
    	output_file = a 
    else:
        assert False, "unhandled option"

if dictionary_file == None or postings_file == None or input_file == None or output_file == None:
    usage()
    sys.exit(2)

search(dictionary_file,postings_file,input_file,output_file)
#print "resutl" , get_posting(postings_file, "February", read_dictionary(dictionary_file))
# test()
