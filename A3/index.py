
import sys
import nltk
import getopt
import os 
from nltk.stem import *


"""
This program is to generate a index files(dictionary and posting list) 
from some documents. 
Dictionary will contain all terms from documents
Posting list will contain the list of DocID for a particular term
"""

# for testing only
# path = "/Users/dennisli/Desktop/CS3245A2/A3/" 



def read_dict(dictionary_name):
	dictionary = []
	line_num = 0
	dict_file = open(dictionary_name)
	for line in dict_file:
		word = line.split(" ")
		word[1] = int(word[1])
		dictionary.append(word)
		line_num = line_num + 1
	dict_file.close()
	return dictionary

def write_dict(dictionary_name, dictionary):
	dict_file = open(dictionary_name, "w")
	for term in dictionary:
		line = term[0] + " " + str(term[1]) + "\n"
		dict_file.write(line)
	dict_file.close()
		
def write_post(posting_name, posting):
	post_file = open(posting_name, "w")
	for term in posting:
		line = ""
		for item in term:
			line = line + item[0] + ":" + str(item[1]) + " "
		line = line + "\n"
		post_file.write(line)

	post_file.close()


def get_doc_list():
	if(os.path.isdir(directory_of_documents) == False) :
		print "directory_of_documents not exist, indexing fail"
		exit()
	dirs = os.listdir( directory_of_documents )
	return dirs


def index(directory_of_documents, dictionary_name, posting_name):
	
	dictionary = []
	posting = [] # 3d list of [term][doc][id/freq]
	doc_list = get_doc_list()

	stemmer =  PorterStemmer()
	for doc_file in doc_list:
		print "indexing: ",doc_file
		if (directory_of_documents[-1] != "/" ):
			full_path = directory_of_documents + "/"+ doc_file
		else:
			full_path = directory_of_documents + doc_file
		current_doc = open(full_path)
		doc_tokens = []
		for line in current_doc:
			line_tokens = nltk.word_tokenize(line)
			# lowercase all tokens
			num_tokens = len(line_tokens)
			i = 0
			while i < num_tokens:
				# print "before-",token
				line_tokens[i] = stemmer.stem(line_tokens[i])
				line_tokens[i] = line_tokens[i].lower()
				i+=1
				# print "after -",token
			doc_tokens.extend(line_tokens)
		doc_tokens.sort()

		# find replicate and count the freq, store into 2D list 
		freq = []
		count = 1
		prv_token = ""
		one_token = ""
		for one_token in doc_tokens:
			if (prv_token == ""): # case first token, comparing with ""
				prv_token = one_token
				continue
			if (one_token == prv_token):
				count = count + 1
				prv_token = one_token
			else:
				freq.append([prv_token,count])
				count = 1
				prv_token = one_token
		freq.append([prv_token,count]) # for the last token 
		
		# insert into dictionary and posting
		for term in freq:
			position = find_index(term, dictionary)
			# case term not in dictionary (new term)
			if (position == -1):
				# add item to list dictionary, sort and get new line number
				doc_count = 1
				dict_term = [term[0],doc_count]
				dictionary.append(dict_term)
				dictionary.sort()
				dict_posit = find_index(term, dictionary)

				if (dict_posit > len(posting)):
					dict_posit = len(posting) -1
				# write to dictionary file
				# write_dict(dictionary_name,dictionary)

				# add the term on the posting list
				posting_item = [doc_file ,term[1]]	
				posting.insert(dict_posit, [posting_item])

			else:
				# case term's positing already exist in dict 

				# edit the freq of dictionary list
				for dictionary_entry in dictionary:
					if(dictionary_entry[0] == term[0]):
						dictionary_entry[1] = dictionary_entry[1] + 1
				
				dict_posit = find_index(term,dictionary)
				posting_item = [doc_file ,term[1]]
				posting[dict_posit].append(posting_item)
				posting[dict_posit].sort()
				
		current_doc.close()
	write_dict(dictionary_name, dictionary)
	write_post(posting_name, posting)


def find_index(term, list):
	count = 0
	for item in list:
		if (term[0] == item[0]):
			return count
		else:
			count = count + 1
	return -1



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

# clear content of dict and posting files
f = open(dictionary_name, 'w')
f.close()

f = open(posting, 'w')
f.close()

index(directory_of_documents, dictionary_name, posting)