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

		print stack
		print result




	




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
