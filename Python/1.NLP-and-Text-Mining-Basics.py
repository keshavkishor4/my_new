#########################
#Use below code if you see any package or module missing

#Step-1 : Write this code and stop it after 2 mins
import nltk
nltk.download('all')

#Step-2 : 
#Run below code and get the temp folder. 
nltk.data.path

#The temp folder looks path like this C:\\Users\\r14\\AppData\\Roaming\\nltk_data

#Setp-3
#Copy all 10 folders from this folder nltk_data_venkat
#Run below code after copying
nltk.download('all')

#########################Corpus Reader
from nltk.corpus import PlaintextCorpusReader
#defining our corpus directory:
dirname_politics = r"C:\Users\kkisho15\Documents\Python\NLP-Data-sets\Dats sets\mini_newsgroups\mini_newsgroups\talk.politics.misc"
#Reading the data with corpus:
politics_corpus = PlaintextCorpusReader(dirname_politics, '.*')

#All file names in the directory
politics_corpus.fileids()

#Few news examples
politics_corpus.raw('176869')
politics_corpus.raw('176878')
politics_corpus.raw('179097')

politics_corpus.words('179097')[1:100]

########################################Preparing Data for text mining
#importing data
import pandas as pd
User_restaurants_reviews = pd.read_csv(r"C:\Users\kkisho15\Documents\Python\NLP-Data-sets\Dats sets\User_Reviews\User_Reviews\User_restaurants_reviews.csv")
User_restaurants_reviews.shape
User_restaurants_reviews.head(20)

##############
#Lets take a small data, we will work on complete dataset later
user_data_tiny = User_restaurants_reviews[0:3]
user_data_tiny
user_data_tiny.columns.values
#########################################################
from nltk.tokenize import sent_tokenize, word_tokenize 

example_text = user_data_tiny["Review"][0]
print(example_text)

##################Tokenising

sent_tokens = sent_tokenize(example_text)
print(sent_tokens)

word_tokens = word_tokenize(example_text)
print(word_tokens)

####################Stop Words
from nltk.corpus import stopwords 
stop_words = set(stopwords.words('english')) ##Selecting the stop words we want
print(len(stop_words))
print(stop_words)

#Removing the stopwords
filtered_sentence = [word for word in word_tokens if not word in stop_words] 
print(filtered_sentence)

#The above code is simpler form of below code
#filtered_sentence1=[]
#for w in word_tokens:
#    if w not in stop_words:
#        filtered_sentence1.append(w)
#print(filtered_sentence1)

##########################Update with your own stop words
stop_words.update(['.', ',', '"', "'", '?', '!', ':', ';', '(', ')', '[', ']', '{', '}']) 
print(len(stop_words))
print(stop_words)

filtered_sentence1 = [word for word in word_tokens if not word in stop_words] 
print(filtered_sentence1)

#####################Stemming
from nltk.stem import PorterStemmer 
stemmer = PorterStemmer()	#Defining the Stemmer

#Stemming works better if we tokenize the sentences first.
example_text1 = user_data_tiny["Review"][1]
print(example_text1)

word_tokens1 = word_tokenize(example_text1)
print(word_tokens1)

stem_tokens=[stemmer.stem(word) for word in word_tokens1]
print(stem_tokens)

#########################Lemmatizing
from nltk.stem import WordNetLemmatizer 
lemmatizer = WordNetLemmatizer() 			#Choosing the Lemmatizer
Lemmatized_tokens = [lemmatizer.lemmatize(word) for word in word_tokens1] 
print(Lemmatized_tokens)

#lemmatised vs Stemmed Tokens
print(Lemmatized_tokens)
print(stem_tokens)


#Lemmatization is done based on part of speech we want in output word,
#Default is Verb = ‘v’
#Values for pos argument
# adverb= 'r'; noun = 'n'; adjective = 'a' ; verb = 'v'


#########################RegEx

review22_text = User_restaurants_reviews["Review"][22]

import re
#re.sub(regexpattern, replacement, string)
#Replacing numbers and currency with space
review22_text_cleaned=re.sub(r'\W+|\d+|_',  ' ',  review22_text)
print("Text after removing currency - \n " + review22_text_cleaned)

print("Actual Text - \n " + review22_text)

#pattern = r'''(?x)          # set flag to allow verbose regexps
#        (?:[A-Z]\.)+        # abbreviations, e.g. U.S.A.
#      | \w+(?:-\w+)*        # words with optional internal hyphens
#      | \$?\d+(?:\.\d+)?%?  # currency and percentages, e.g. $12.40, 82%
#      | \.\.\.              # ellipsis
#      | [][.,;"'?():_`-]    # these are separate tokens; includes ], [

########################################
#Case Study : The news articles text mining
###########################################

import os
path = r"C:\Users\kkisho15\Documents\Python\NLP-Data-sets\Dats sets\mini_newsgroups\mini_newsgroups\sci.space"
doc_dict = {}

for subdir, dirs, files in os.walk(path):
    for file in files:
        file_path = subdir + os.path.sep + file
        f = open(file_path, 'r')
        text = f.read()
        doc_dict[file] = text
        
#print(doc_dict)
print(doc_dict.keys())
doc_dict['60804']

#########lowering all the cases
for my_var in doc_dict:
    doc_dict[my_var] = doc_dict[my_var].lower()
doc_dict['60804']


############Removing Numbers
import re
# Use regular expressions to do a find-and-replace

for my_var in doc_dict:
    doc_dict[my_var] = re.sub(r'\d+',           # The pattern to search for
                      " ",                   # The pattern to replace it with
                      doc_dict[my_var])  # The text to search
doc_dict['60804']

##################################Removing Punctuations
import re
# Use regular expressions to do a find-and-replace
for my_var in doc_dict:
    doc_dict[my_var] = re.sub(r'\W+|\_',           # The pattern to search for
                      " ",                   # The pattern to replace it with
                      doc_dict[my_var])  # The text to search
doc_dict['60804']


###################Removing General English Stop words
from nltk.corpus import stopwords
from nltk import word_tokenize
stop = stopwords.words('english')
for my_var in doc_dict:
    doc_dict[my_var] = ' '.join([i for i in word_tokenize(doc_dict[my_var]) if i not in stop])
doc_dict['60804']

################Removing custom stop words
custom_stop = stopwords.words('english') + ['news', 'writes', 'told']
for my_var in doc_dict:
    doc_dict[my_var] = ' '.join([i for i in word_tokenize(doc_dict[my_var]) if i not in custom_stop])
doc_dict['60804']

############## Lemmatising

from nltk.stem import WordNetLemmatizer 
lemmatizer = WordNetLemmatizer() 			#Choosing the Lemmatizer
for my_var in doc_dict:
    doc_dict[my_var] = ' '.join([lemmatizer.lemmatize(i) for i in word_tokenize(doc_dict[my_var])])
doc_dict['60804']


############## Stemming ; This step can be ignored
doc_dict_1=doc_dict
from nltk.stem import PorterStemmer
stemmer = PorterStemmer()
for my_var in doc_dict_1:
    doc_dict_1[my_var] = ' '.join([stemmer.stem(i) for i in word_tokenize(doc_dict_1[my_var])])
doc_dict_1['60804']

#####################################################################
###Document Trem Matrix

#Data Import
import pandas as pd
User_restaurants_reviews = pd.read_csv(r"C:\Users\kkisho15\Documents\Python\NLP-Data-sets\Dats sets\User_Reviews\User_Reviews\User_restaurants_reviews.csv")
User_restaurants_reviews.shape
User_restaurants_reviews.head(20)

##############
#Lets take a small data, we will work on complete dataset later
input_data = User_restaurants_reviews[0:3]
print(input_data)
##########
#Creating Document Term Matrix

from sklearn.feature_extraction.text import CountVectorizer

countvec1 = CountVectorizer()
dtm_v1 = pd.DataFrame(countvec1.fit_transform(input_data['Review']).toarray(), columns=countvec1.get_feature_names(), index=None)
dtm_v1.head()


#####################################################
###Larger DTM

user_data_r100 =User_restaurants_reviews[0:100]

countvec1 = CountVectorizer()
Test_DTM_r100 = pd.DataFrame(countvec1.fit_transform(user_data_r100['Review']).toarray(), columns=countvec1.get_feature_names(), index=None)
Test_DTM_r100.head()

#Lets look at the TDM
Test_DTM_r100
Test_DTM_r100[0:10]
Test_DTM_r100[0:20]
Test_DTM_r100[0:50]
Test_DTM_r100[1:80]
Test_DTM_r100
 

