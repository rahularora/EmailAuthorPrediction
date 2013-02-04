# Task 1 : Write a program that computes unsmoothed unigrams and
# bigrams for an arbitrary text corpus. We are using Dataset4.

import re, sys

corpus1 = "Dataset1_fbis/fbis.train"
corpus1test = "Dataset1_fbis/fbis.test"
corpus2 = "Dataset2_wsj/wsj.train"
corpus2test = "Dataset2_wsj/wsj.test"
corpus3 = "Dataset3/Train.txt"
corpus3test = "Dataset3/Test.txt"
corpus4 = "Dataset4/Train.txt"
corpus4test = "Dataset4/Test.txt"

nGramList = []
N = 2

# Reads a file
def readFile(filePath):
  fileHandler = open(filePath, 'r')
  #print fileHandler.read()
  if filePath == corpus1 or filePath == corpus2:
    pattern = re.compile('<TEXT>(.*?)<\/TEXT>', re.S)
    textList = pattern.findall(fileHandler.read().replace('\n', ''))
    fileText = " ".join(textList)
  else:
    fileText = fileHandler.read()
  
  #print fileText
  return fileText
  
# Modifies file and add <s>  
def modifyFile(fileText):
  #fileText = fileText.replace('\n', '').lower();
  fileText = re.sub('[^A-Za-z0-9\.\?\!\'\,]+', ' ', fileText)
  fileText = re.sub('[\.\!\?\;]+', ' <s> ', fileText)
  fileText = re.sub(' +',' ',fileText)
  
  textList = fileText.split()
  #print textList
  
  #Add starting <s> tags
  temp = ["<s>"]
  temp.extend(textList)

  temp = " ".join(temp).split(" ")
  
  return temp
  
def addTokenToDict(aDict,token):
  if token in aDict:
    aDict[token] = aDict[token] + 1
  else:
    aDict[token] = 1
    
  return aDict

def buildNGram(n, tList):
  for token in tList:
  	tempDict = nGramList[n-1]
  	tempDict = addTokenToDict(tempDict,token)
	nGramList[n-1] = tempDict

  #print tempDict

# Works completely fine
def genNgramTokens(N, tokenList):
  lenTokenList = len(tokenList)
  tList = list()
  for i in range(0, lenTokenList - N + 1):
    token = ""
    for j in range(i,i+N):
      token = token + tokenList[j] + " "

    #print "T:",token
    tList.append(token.rstrip(" "))
    #buildNGram(N, token.rstrip(" ")) 
  
  return tList
	
def generateNgram(N,corpus):
  fileText = readFile(corpus)
  tokenList = modifyFile(fileText)
  
  for n in range(1,N+1):
  	nGramList.append({})
  
  for n in range(1,N+1):
  	tList = genNgramTokens(n, tokenList)
  	buildNGram(n,tList)
  	
  return nGramList
  	
def printNgramList():
  #print len(nGramList)
  count = 1
  for ngram in nGramList:
    print "*******"
    print "For N =", count
    print "Total tokens = ", len(ngram)
    for key in ngram:
      print key, ngram[key]
    
    count = count + 1
    print

def main():
  global N
  if len(sys.argv) > 1:
    N = int(sys.argv[1])
  else:
    N = 2
  nGramList = generateNgram(N,corpus4)
  printNgramList()
  print N

if __name__ == "__main__":
	main()