# This file "text_processing.py" contains methods for text stemming

# author: tai.truong@software-developer.org.

# All needed imports for this script file
import nltk   # Natural Language Tool Kit
import re     # regular expression

# This method downloads needed NLTK parts
def prepare():
  nltk.download('stopwords')
  nltk.download('porter_test')
  # get all english stop words like 'the', 'is', 'are', 'over'
  stopWords = nltk.corpus.stopwords.words('english')
  return stopWords
  
# Example call
def example():
  stopWords = prepare()
  input = 'the quick brown foxes 123 jumped ❤☀ over äääßßß the lAzy Dog!'
  print('input:', input)
  normalized = normalizeWords(input, stopWords)
  print('normalized: ', normalized)
  stemmed = stem(normalized)
  print('stemmed: ', stemmed)
  searchTermList = ['fox', 'dogs', 'cat']
  print('search terms: ', searchTermList)
  stemmedSearchTermList = stem(searchTermList)
  print('stemmed search terms: ', stemmedSearchTermList)
  matchTextWithSearchTerms(input, searchTermList)
  print('match: ', matchTextWithSearchTerms(input, searchTermList))
  
# returns a list of normalized words
def normalizeWords(input, stopWords):
  # source: https://www.kdnuggets.com/2018/03/simple-text-classifier-google-colaboratory.html
  # replace all non-letters to whitespace. Example: hello#!world => hello  world
  input = re.sub('[^a-zA-Z]', ' ',  str(input))
  # replace non unicode words (\w), unicode digits (\d), or unicode whitespaces with whitespace
  input = re.sub(r'[^\w\d\s]', ' ', input)
  # replace trailing whitespaces into one whitespace
  input = re.sub(r'\s+', ' ', input)
  # make lowercase
  input = re.sub(r'^\s+|\s+?$', '', input.lower())
  filteredWords = []
  for word in input.split():
    if word not in stopWords:
      filteredWords.append(word)
  return filteredWords
  
# returns a stemmed list
def stem(list):
  ps = nltk.PorterStemmer()
  stemmedList = []
  for word in list:
    stemmedList.append(ps.stem(word))
  return stemmedList
  
# match does these steps:
# 1. normalize input (remove trailing whitespaces, digits, non-alphabetic characters)
# 2. remove stop words like 'is', 'a' from input
# 3. stems input
# 4. stems search terms (classified words found from images)
# 5. validates whether stemmed input contains stemmed search terms
# 6. returns the non-stemmed/normal words as result
def matchTextWithSearchTerms(inputText, searchTermList):
  normalized = normalizeWords(input)
  stemmed = stem(normalized)
  stemmedSearchTermList = stem(searchTermList)
  match = []
  for word in stemmed:
    if word in stemmedSearchTermList:
      index = stemmed.index(word)
      match.append(normalized[index])
  return match
