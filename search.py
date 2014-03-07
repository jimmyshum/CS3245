import re
import nltk
import sys
import getopt
def search(dictionary_file,postings_file,input_file,output_file):
	inFile = open(input_file,'r')
	outFile = open(output_file,'w')
	stack = []
	result = []
	for line in inFile:
		tokens = nltk.word_tokenize(line)
		print tokens

		for i in range(0,len(tokens)):
			s = tokens[i]
			if s == "AND":
				if stack:
					if stack[len(stack)-1] == "AND":
						result.append(stack.pop())

				stack.append(s)


			elif s == "OR":

				if stack:
					if stack[len(stack)-1] == "AND":
						result.append(stack.pop())
					if stack[len(stack)-1] == "OR":
						result.append(stack.pop())

				stack.append(s)
				

			elif s == "NOT":
				stack.append(s)

			elif s == "(":
				stack.append(s)

			elif s == ")":
				s = stack.pop()
				while s != "(":
					result.append(s)
					s = stack.pop()
				

			else:
				result.append(s)
				if stack:
					if stack[len(stack)-1] == "NOT":
						result.append(stack.pop())

				

		while len(stack) != 0:
			result.append(stack.pop())

	
		print result

def evaluateQuery(list):
	result = []
	for i in range(0,len(list)):
		if list[i] == "AND":
			list1 = result.pop()
			list2 = result.pop()
			result.append(opAND(list1,list2))

		elif list[i] == "OR":
			list1 = result.pop()
			list2 = result.pop()
			result.append(opOR(list1,list2))


		elif list[i] == "NOT":
			list1 = result.pop()
			result.append(opNOT(list1))

		else:
			result.append(list[i])
	return result


###test only
def test():
	list1 = [1,2,3,5,6,9]
	list2 = [2,3,4,6,7,8]
	print opAND(list1,list2)

	print opOR(list1,list2)
	print opNOT(list1,list2)
###test only

def opAND(list1,list2):
	return sorted(list(set(list1) & set(list2)))

def opOR(list1,list2):
	return sorted(list(set(list1) | set(list2)))

def opNOT(list1,list2):
	return sorted(list((set(list1) | set(list2)) - set(list1)))


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

#search(dictionary_file,postings_file,input_file,output_file)
print "resutl" , get_posting(postings_file, "February", read_dictionary(dictionary_file))
# test()