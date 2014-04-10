import re
import nltk
import sys
import getopt
import os
#import xml.dom
import math
import urllib
import StringIO
import lxml
#from xml.dom.minidom import parse,parseString
from lxml import etree
def retrieveXML():
	fopen = urllib.urlopen('cs3245-hw4/q1.xml')
	xml = fopen.read()
	parser = etree.XMLParser()
	tree = etree.parse(StringIO.StringIO(xml),parser)
	title = tree.xpath('//title/text()')
	desc = tree.xpath('//description/text()')
	
	#for i in range (0,len(elements)):
	#	print etree.tostring(elements[i])
	titleTokens = nltk.word_tokenize(title[0])
	descTokens = nltk.word_tokenize(desc[0])

	print titleTokens
	print descTokens
	#print title[0]
	#print desc[0]
	#print etree.tostring(title[0])
	#print etree.tostring(desc[0])

def retrievePatentXML():
	fopen = urllib.urlopen('patsnap-corpus/EP0115517A1.xml')
	xml = fopen.read()
	parser = etree.XMLParser()
	tree = etree.parse(StringIO.StringIO(xml),parser)
	title = tree.xpath('//str[@name="Title"]/text()')
	desc = tree.xpath('//str[@name="Abstract"]/text()')
	
	#for i in range (0,len(elements)):
	#	print etree.tostring(elements[i])
	titleTokens = nltk.word_tokenize(title[0])
	descTokens = nltk.word_tokenize(desc[0])

	print titleTokens
	print descTokens

def usage():
    print "usage: " + sys.argv[0]

#retrieveXML();
retrievePatentXML();
#search(dictionary_file,postings_file,input_file,output_file)
