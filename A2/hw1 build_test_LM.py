#!/usr/bin/python
import re
import nltk
import sys
import getopt

#global constant
gram_size = 1   # used for Essay Question 4
start_symbol = '$'
end_symbol = '%'
not_exist = -1
overflow = 0

def build_LM(in_file):
    """
    build language models for each label
    each line in in_file contains a label and an URL separated by a tab(\t)
    """
    print 'building language models...'
    # This is an empty method
    # Pls implement your code in below
    
    # a dictionary stored the freq for each 4-gram
    freq = {'indonesian':{}, 'malaysian':{}, 'tamil':{}, 'other':{}, 'english':{}, 'dutch':{}, 'german':{}, 'portuguese':{}, 'spanish':{} }
    
    
    # read from file, create ngram of freq for each line
    file = open(in_file)
    for line in file:
        language = get_lang(line)
        res = get_content(line)
        res_len = len(res)
        freq[language] = combin(freq[language], gram_freq(res))
    
    # calculate probability of ngram for each languages with add one
    probi = {}
    for lang, freq_list in freq.items():
        probi[lang] = cal_probi(freq_list)

    file.close()
    return probi

# get the language from a line
def get_lang(line):
    return line.split()[0]

# remove the language name and newline charactorfrom the line
def get_content(line):
    #remove newline char
    line = line[0:-1]
    
    target = get_lang(line) + " "
    return line.replace(target, '')

# return a dictionary of {"****": frequency}
def gram_freq(res):
    frequency = {}
    """#handle start
    j = 1
    while j < gram_size:
        ngram = start_symbol * (gram_size - j) + res[0:j]
        if ngram in frequency:
            frequency[ngram] += 1
        else:
            frequency.update({ngram: 1})
        j += 1 
    """ #test
    # handle remains
    i = 0
    while i < len(res):
        ngram = res[i: (i + gram_size)]
        # handle end_symbol
        """
        if len(ngram) < gram_size:
            ngram = ngram + end_symbol * (gram_size - len(ngram))
        """# test
        if ngram in frequency:
            frequency[ngram] += 1
        else:
            frequency.update({ngram: 1})
        i += 1
    return frequency

#combin  dictionary a and 1D dictioanry b
def combin(a, b):
    for key,item in b.items():
        if key in a:
            a[key] += b[key]
        else:
            a.update({key:b[key]})
    return a


# return a dict of ngram's probability of one language
# from a dict of ngram frequency of ONE language
def cal_probi(freq_list):
    #find the total number of items
    num_item = 0
    for ngram, freq in freq_list.items():
        #freq += 1
        num_item += freq

    # calculate the probi
    probability = {}
    for ngram, freq in freq_list.items():
        probability[ngram] = float(freq) / num_item + 1

    return probability


def test_LM(in_file, out_file, LM):
    """
    test the language models on new URLs
    each line of in_file contains an URL
    you should print the most probable label for each URL into out_file
    """
    print "testing language models..."
    # This is an empty method
    # Pls implement your code in below
    inf = open(in_file)
    outf = open(out_file , 'w')
    for line in inf:
        language = determine_line_lang(line, LM)
        outf.write(language + " " + line)
    inf.close()
    outf.close()

# find the language with highest probability
def determine_line_lang(line, LM):
    max_probability = 0
    lang_result = ""
    for lang, ngram_and_prob in LM.items():
        if probability_lang_line(line, lang, LM) > max_probability:
            max_probability = probability_lang_line(line, lang, LM)
            lang_result = lang
        # print (lang, "BECOME TMPMAX ") #test
        if probability_lang_line(line, lang, LM) == overflow:
            print('overflow')
            return lang
    #print (line,"FINALMAX " +lang_result, probability_lang_line(line,lang,LM)) # testing
    return lang_result

# find the probability of a line of a specify language
def probability_lang_line(line, lang, LM):
    probability = 1;
    # handle Start
    """
    j = 1
    while j < gram_size:
        ngram = start_symbol * (gram_size - j) + line[0:j]
        probi_one_token = find_probi(ngram ,LM, lang)
        if probi_one_token != not_exist:
            probability = probability * probi_one_token
        j += 1 
    """ #test
    # handle remains
    i = 0
    while i < len(line):
        ngram = line[i: (i + gram_size) ]
        # handle end_symbol
        """    
        if len(ngram) < gram_size:
        ngram = ngram + end_symbol * (gram_size - len(ngram)) 
        """ #test
        probi_one_token = find_probi(ngram ,LM, lang)
        if probi_one_token != not_exist:
            probability = probability * probi_one_token
            # print (ngram,  probability, probi_one_token) #testing
        i += 1
        if (probability ==0):
            return overflow
    if probability != 1:
        return probability
    else:
        return not_exist;

def find_probi(token, LM , lang):
    if token in LM[lang]:
        return LM[lang][token]
    else:
        return not_exist;


def usage():
    print "usage: " + sys.argv[0] + " -b input-file-for-building-LM -t input-file-for-testing-LM -o output-file"

input_file_b = input_file_t = output_file = None
try:
    opts, args = getopt.getopt(sys.argv[1:], 'b:t:o:')
except getopt.GetoptError, err:
    usage()
    sys.exit(2)
for o, a in opts:
    if o == '-b':
        input_file_b = a
    elif o == '-t':
        input_file_t = a
    elif o == '-o':
        output_file = a
    else:
        assert False, "unhandled option"
if input_file_b == None or input_file_t == None or output_file == None:
    usage()
    sys.exit(2)

LM = build_LM(input_file_b)
# print LM #for testing
test_LM(input_file_t, output_file, LM)
