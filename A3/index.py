
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

# for testing only
# path = "/Users/dennisli/Desktop/CS3245A2/A3/" 



def read_dict(dictionary_name):
	dictionary = []
	line_num = 0
	dict_file = open(dictionary_name)
	for line in dict_file:
		word = nltk.word_tokenize(line)
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
		


def get_doc_list():
	if(os.path.isfile(directory_of_documents) == False) :
		print "directory_of_documents not exist, indexing fail"
		exit()
	dirs = os.listdir( directory_of_documents )
	return dirs


def index(directory_of_documents, dictionary_name, posting):
	
	dictionary = []

	doc_list = get_doc_list()

	for doc_file in doc_list:
		current_doc = open(path + doc_file)
		doc_tokens = []
		for line in current_doc:
			line_tokens = nltk.word_tokenize(line)
			# lowercase all tokens
			for token in line_tokens:
				token = token.lower()
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
				prv_token = one_token
		freq.append([prv_token,count]) # for the last token 
		
		# insert into dictionary and posting
		for term in freq:
			position = find_index(term, dictionary)
			# case term not in dictionary (new term)
			if (position == -1):
				# add item to list dictionary, sort and get new line number
				doc_count = 1
				dict_term = (term[0],doc_count)
				dictionary.append(dict_term)
				dictionary.sort()
				dict_posit = find_index(term, dictionary)

				# write to dictionary file
				write_dict(dictionary_name,dictionary)

				# add the line on the posting list 
				post_file = open(posting, "r+")

				# read posting and get line_offset for jumping
				line_offset =[]
				offset =0
				for line in post_file:    
					line_offset.append(offset)    
					offset += len(line)
				post_file.seek(0)

				# Now, to skip to line n (with the first line being line 0, just dofile.seek(line_offset[n])
				"""
				if (dict_posit < len(line_offset) ):
					# case add line to line n of the file
					post_file.seek(line_offset[dict_posit])
					data = doc_file + " \n"
					post_file.write(data)
					post_file.close()
				else: 
					# case add to the end of file
					post_file.seek(0,2)
					data = doc_file + " \n"
					post_file.write(data)
					post_file.close()
				"""
				data = doc_file + " \n"

				post_file.seek(0,0)
				tmp_file = open("tmp","w")
				line_count = 0
				for post_line in post_file:
					if line_count == dict_posit:
						tmp_file.write(data)
						tmp_file.write(post_line)
					else:
						tmp_file.write(post_line)
					line_count = line_count + 1

				if line_count < dict_posit:
					tmp_file.write(data)

				post_file.close()
				tmp_file.close()

				# replace tmp file to posting file
				os.remove(posting)
				os.rename("tmp",posting)

			else:
				# case term's positing already exist in dict 

				# edit the freq of dictionary list
				for dictionary_entry in dictionary:
					if(dictionary_entry[0] == term[0]):
						dictionary_entry[1] = dictionary_entry[1] + term[1]
				# write the change to dict file
				write_dict(dictionary_name,dictionary)

				# edit the posting file
				post_file = open(posting, "r+")
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
				# add the new DocID and sort
				if not(doc_file in target_line_postings):
					target_line_postings.append(doc_file)
				target_line_postings.sort()
				data  = ""
				for doc_id in target_line_postings:
					if doc_id != '\n':					
					 	data = data + doc_id + " "
				data = data + "\n"

				# write each line to another file  )
				post_file.seek(0,0)
				tmp_file = open("tmp","w")
				line_count = 0
				for post_line in post_file:
					if line_count == dict_posit:
						tmp_file.write(data)
					else:
						tmp_file.write(post_line)
					line_count = line_count + 1

				post_file.close()
				tmp_file.close()

				# replace tmp file to posting file
				os.remove(posting)
				os.rename("tmp",posting)

		current_doc.close()
	# print dictionary


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