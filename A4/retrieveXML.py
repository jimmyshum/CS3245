import re
import nltk
import sys
import getopt
import os
import math
from nltk.stem import *

def retrieveXML():



def usage():
    print "usage: " + sys.argv[0]

"""dictionary_file = postings_file = input_file = output_file = None

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

"""
retrieveXML();
#search(dictionary_file,postings_file,input_file,output_file)
