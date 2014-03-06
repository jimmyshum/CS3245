# stuff to do

# read inputs from command (file position and names)

# read dictionary file (if exist) , store to memory as List
# loop all files
	# read 1 file
	# tokenizer into separated word
	# do case folding
	# sorting the terms
		# loop each terms
		# count freqency (find replicates)
		# add term to dictionary 
			# (update freqency if exist)
			# (add term if not exist)
		# read positing list of that term (if exist) (don't read the whole posing)
		# add docID(fliename) to positing list
		# sort positing list of that term
	# // until all terms of DOC are read
# // until all file are indexed. 

# problems
	# storing Dictionary
		# term1 freq1
		# term2 freq2

		# add new term into dictionary 
			# how to add line in the middle of the file?
		# use line number to identify each terms
	
	# how to store the posting 
		# 1 line of DocID for each term? 
		# how about adding a new terms in the middle of the posting file? 
			# add a line on the middle of the file?
				# create another file 
				# read one line from A , write to B
				# until reacht the target line 
				# write the line ,
				# then continuos read&write till eof
			# read the nth line of a file? how?
				# read line by line using a loop (save the only line we need)

import sys
import nltk
import getopt
import os 

"""
This program is to generate a index files(dictionary and posting list) 
from some documents. 
Dictionary will contain all terms from documents
Posting list will contain the list of DocID for a particular term
"""

path = "/Users/dennisli/Desktop/CS3245/reuters/testing/" 


def read_dict(dictionary_name):
	dictionary = []
	line_num = 0
	dict_file = open(dictionary_name)
	for line in dict_file:
		dictionary.append(line)
		line_num = line_num + 1
	dict_file.close()
	return dictionary

def get_doc_list():
	dirs = os.listdir( path )
	return dirs


def index(directory_of_documents, dictionary_name, posting):
	dictionary = read_dict(dictionary_name)
	doc_list = get_doc_list()

	for doc_file in doc_list:
		current_doc = open(path + doc_file)
		doc_tokens = []
		for line in current_doc:
			line_tokens = nltk.word_tokenize(line)
			doc_tokens.extend(line_tokens)
		doc_tokens.sort()

		# find replicate and count the freq, store into 2D list 
		freq = []
		count = 1
		prv_token = ""
		for one_token in doc_tokens:
			if (one_token == prv_token):
				count = count + 1
				prv_token = one_token
			else:
				freq.append([one_token,count])
				count = 1 
				prv_token = one_token

		# insert into dictionary and posting
		for term in freq:
			# not fininsheds


		current_doc.close()


def find_index(string, list):
	count = 0
	for item in list:
		if string = item:
			return count
		else:
			count = count + 1



def usage():
    print "usage: " + sys.argv[0] + " -i directory-of-documents -d dictionary-file -p posting-file"

# main : get the input filenames and directory
directory_of_documents = dictionary_name = posting= None
try:
    opts, args = getopt.getopt(sys.argv[1:], 'i:d:p:')
except getopt.GetoptError, err:
    usage()
    sys.exit(2)
for o, a in opts:
    if o == '-i':
        directory_of_documents = a
    elif o == '-d':
        dictionary_name = a
    elif o == '-p':
        posting = a
    else:
        assert False, "unhandled option"
if directory_of_documents == None or dictionary_name == None or posting == None:
    usage()
    sys.exit(2)

index(directory_of_documents, dictionary_name, posting)