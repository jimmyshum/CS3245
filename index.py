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