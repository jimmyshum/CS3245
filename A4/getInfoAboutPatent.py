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
from lxml import etree

def get_doc_list(directory_of_documents):
	if(os.path.isdir(directory_of_documents) == False) :
		print "directory_of_documents not exist, indexing fail"
		exit()
	dirs = os.listdir( directory_of_documents )
	return dirs

def analysisPatent(dirs):
	titleNum = 0
	descNum = 0
	titleAndDescNum = 0
	titleOrDescNum = -1
	for patent in dirs:
		#print patent
		patent = "patsnap-corpus/"+patent
		titleNum += getPatentTitleNum(patent)
		descNum += getPatentDescNum(patent)
		titleAndDescNum += getPatentTitleAndDescNum(patent)
		titleOrDescNum += (getPatentTitleNum(patent) + getPatentDescNum(patent))

	print "Statiic of Patent"
	print "Total patent = " , len(dirs)
	print "patent that have Title = " ,titleNum
	print "patent that have Desc = " ,descNum
	print "patent that have Title and Desc = " ,titleAndDescNum
	print "patent that have Title or Desc = " ,titleOrDescNum





def getPatentTitleNum(patent):
	fopen = urllib.urlopen(patent)
	xml = fopen.read()
	parser = etree.XMLParser()
	tree = etree.parse(StringIO.StringIO(xml),parser)
	title = tree.xpath('//str[@name="Title"]/text()')
	if len(title) != 0:
		return 1
	else:
		return 0
	
def getPatentDescNum(patent):
	fopen = urllib.urlopen(patent)
	xml = fopen.read()
	parser = etree.XMLParser()
	tree = etree.parse(StringIO.StringIO(xml),parser)
	desc = tree.xpath('//str[@name="Abstract"]/text()')
	if len(desc) != 0:
		return 1
	else:
		return 0
	
def getPatentTitleAndDescNum(patent):
	fopen = urllib.urlopen(patent)
	xml = fopen.read()
	parser = etree.XMLParser()
	tree = etree.parse(StringIO.StringIO(xml),parser)
	title = tree.xpath('//str[@name="Title"]/text()')
	desc = tree.xpath('//str[@name="Abstract"]/text()')
	if (len(title)) != 0 and (len(desc) != 0):
		return 1
	else:
		return 0

dirs = get_doc_list("patsnap-corpus");
dirs.remove(".DS_Store")
analysisPatent(dirs)
#totalPatent = len(dirs)
#print totalPatent


