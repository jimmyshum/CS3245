import re
import nltk
import sys
import getopt
import os
import math
from nltk.stem import *

# global constant N total_doc_size
total_doc_size = 7769.0
output_size = 100

def search(dictionary_file,postings_file,input_file,output_file):
	inFile = open(input_file,'r')
	outFile = open(output_file,'w')
	for line in inFile:
		tokens = nltk.word_tokenize(line)
		from collections import Counter
		queryListInfo = Counter(tokens)
		queryListDict = dict(queryListInfo)
		queryListTF = queryListInfo.values()
		queryListTF = calTFWT(queryListTF)
		queryListN = normalization(queryListTF)

		dictionary = read_dictionary(dictionary_file)

		checking_list = list( get_checking_doc_list(queryListInfo.keys(), dictionary, postings_file))
		print "checking....",checking_list
		itcinc_list= []
		for doc in checking_list:
			itc_list = get_doc_itc(queryListInfo.keys(), doc, postings_file, dictionary)
			# print "itc_list: ", itc_list
			itcinc = product(itc_list , queryListN)
			# print "itcinnnnnn",itcinc
			itcinc_list.append([itcinc,doc])

		itcinc_list.sort()
		result = itcinc_list[::-1]
		print "ANSWER:" , result
		output_size = len(result) 
		for i in range(output_size):
			if (i >= len(result)):
				break
			outFile.write(result[i][1] + " ")
		
		outFile.write("\n")
		outFile.close()
		return result
		
		

def calTFWT(qList):
	qListWT = []
	for i in range (0,len(qList)):
		tf = qList[i]
		tfwt = 1 + math.log(tf,10)
		qListWT.append(tfwt)
	return qListWT
	
def normalization(qList):
	length = len(qList)
	sqSum = 0
	nQList = []
	for i in range (0,len(qList)):
		sqSum = sqSum + qList[i]*qList[i]
	factor = math.sqrt(sqSum)

	for i in range (0,len(qList)):
		nQList.append(qList[i]/factor)
	return nQList

def product(queryListN,docListN):
	if len(queryListN) - len(docListN) != 0:
		return -1
	else:
		productList = []
		for i in range (0,len(queryListN)):
			productList.append(queryListN[i]*docListN[i])

	add_product = 0
	for item in productList:
		add_product += item
	return add_product


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
	
	term = term.lower()
	stemmer =  PorterStemmer()
	term = stemmer.stem(term)

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
	term_posting = []
	for tupple in target_line_postings:
		id_plus_freq = tupple.split(':')
		term_posting.append([id_plus_freq[0], int(id_plus_freq[1])])
	return term_posting 

def get_df(dictionary, term):
	term = term.lower()
	stemmer =  PorterStemmer()
	term = stemmer.stem(term)

	for tup in dictionary:
		if tup[0] == term:
			return tup[1]
	return 0

def get_doc_list(posting_list):
	doc_list = []
	for tupple in posting_list:
		doc_list.append(tupple[0])
	return doc_list

def get_tf_list(posting_list):
	tf_list = [] 
	for tupple in posting_list:
		tf_list.append(tupple[1])
	return tf_list


def get_raw_tf(term, doc_id, posting_file, dictionary):
	term_posting = get_posting(posting_file,term,dictionary)
	for tupple in term_posting:
		if doc_id == tupple[0]:
			return tupple[1]
	return 0

def tokenizer(input_list):
	
	token_list = nltk.word_tokenize(input_list)
	stemmer = PorterStemmer()
	
	output_list = []
	for token in token_list:
		token = token.lower()
		term = stemmer.stem(token)
		output_list.append(term)
	return output_list

def idf_from_df(df):
	if(df!=0):
		return math.log(total_doc_size/df,10)
	else:
		return 0

def tf_from_raw(raw):
	if (raw != 0):
		return 1 + math.log(raw,10)
	else:
		return 0

def get_doc_itc(term_list, doc_id, posting_file, dictionary):
	# find idf
	idf_list = []
	for term in term_list:
		df = get_df(dictionary,term)
		idf = idf_from_df(df)
		idf_list.append(idf)
	# print "idf_list", idf_list
	# find 1 + log(tf)
	tf_list = []
	for term in term_list:
		raw_tf = get_raw_tf(term, doc_id, posting_file, dictionary)
		tf = tf_from_raw(raw_tf)
		tf_list.append(raw_tf)
	# print tf_list

	i = 0
	query_size = len(term_list)
	wt_list = []
	while i< query_size:
		wt = tf_list[i] * idf_list[i]
		wt_list.append(wt)
		i+=1
	# print wt_list

	doc_length_sum= 0
	for wt in wt_list:
		doc_length_sum += wt*wt
	doc_length = math.sqrt(doc_length_sum)
	# print doc_length

	norm_list = []
	for wt in wt_list:
		if doc_length == 0:
			norm = 1
		else:
			norm = wt/doc_length
		norm_list.append(norm)

	# print norm_list
	return norm_list


def get_checking_doc_list(queryListInfo, dictionary, postings_file):
	checking_list = []
	for query_token in queryListInfo:
		token = tokenizer(query_token)
		term_posting = get_posting(postings_file,token[0],dictionary)
		checking_list = set_merge(checking_list , get_doc_list(term_posting))
	return checking_list

def set_merge(a,b):
	return set(list(a) + list(b))	

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
