import re
import nltk
import sys
import getopt
def search(dictionary_file,postings_file,input_file,output_file):


def usage():
    print "usage: " + sys.argv[0] + " -b input-file-for-building-LM -t input-file-for-testing-LM -o output-file"

dictionary_file = postings_file = input_file = output_file = None

try:
    opts, args = getopt.getopt(sys.argv[1:], 'p:t:q:o:')
except getopt.GetoptError, err:
    usage()
    sys.exit(2)
for o, a in opts:
    if o == '-p':
        dictionary_file = a
    elif o == '-t':
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
