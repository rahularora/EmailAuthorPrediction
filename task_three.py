#Task 3 : Handle unknown words and implement smoothing

from __future__ import division
import math

import task_one

N = 2
print "Perplexity for Dataset 3 using Laplace Smoothing"
nGramList = task_one.generateNgram(N,task_one.corpus3) 
laplaceList = []
fileText = task_one.readFile(task_one.corpus3test)
tokenList = task_one.modifyFile(fileText)
nGramTestList = []

def findVocabCount():
  vocabCount = 0
  unigram = nGramList[0]
  for t in unigram:
    vocabCount = vocabCount + unigram[t]
  
  return vocabCount

def combineTokens(listWithUnknown):
  dictTokensWithUnknown = dict()
  #print listWithUnknown
  for n in listWithUnknown:
    dictTokensWithUnknown = dict(dictTokensWithUnknown.items() + n.items())
    
  #print dictTokensWithUnknown
  return dictTokensWithUnknown

def unknownWordHandling():
  listWithUnknown = []
  for n in range(1,N+1):
    oov = set()
    temp = dict()
    ngram = nGramList[n-1]
    tokenCount = 0
    wordCount = len(ngram)
    #print ngram
    OOV = "OOV" + str(n)
    for key in ngram:
      tokenCount = ngram[key] + tokenCount
      if ngram[key] == 1:
        oov.add(key)
        if OOV in temp:
          temp[OOV] = temp[OOV] + 1      
        else:
          temp[OOV] = 1
      else:
        temp[key] = ngram[key]
        
    listWithUnknown.append(temp)

  return listWithUnknown

def calcPerplexity(n):
  smoothNgram = laplaceList[n-1]    #test laplace smoothed ngram
  
  result = 0.0
  
  if n > 1:
  	lastSmoothNgram = laplaceList[n-2]
  	lastOOV = "OOV" + str(n-1)
  
  OOV = "OOV" + str(n)
  #print "##"
  for token in nGramTestList[n-1]:
    if token in smoothNgram:
      result = result + math.log(smoothNgram[token])
    else:
      result = result + math.log(smoothNgram[OOV])
    
  return result
  

def laplaceSmoothing(n,tokensDict,listWithUnknown):
  ngram = listWithUnknown[n-1]
  laplaceDict = {}
  vocabCount = findVocabCount()
      
  for key in ngram: 
    if n == 1:
      tokenCount = len(listWithUnknown[n-1])
    else:
      if len(key.split()) != 1:
        tokens = key.split()
        del tokens[-1]
        token = " ".join(tokens)
      else:
        token = key
      
      tokenCount = tokensDict[token]
      #print token
      #print tokenCount
      
    #print key
    laplaceDict[key] = (ngram[key] + 1)/(vocabCount+tokenCount)
  
  #print laplaceDict
  laplaceList.append(laplaceDict)
  return  

# Works completely fine
def genNgramTokens(N):
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

def genTokensFromTest(N):
  for n in range(1,N+1):
    tList = genNgramTokens(n)
    nGramTestList.append(genNgramTokens(n)) #List of tokens

def main():
  genTokensFromTest(N)
  listWithUnknown = unknownWordHandling()
  dictTokensWithUnknown = combineTokens(listWithUnknown)
  for n in range(1,N+1):
    laplaceSmoothing(n,dictTokensWithUnknown,listWithUnknown)
    tokenCount = len(nGramTestList[n-1])
    #print tokenCount
    Perplexity = calcPerplexity(n)
    print "N =",str(n),":",
    print int(math.exp(-1*Perplexity/tokenCount))
    
  #for d in listWithUnknown:
  #	print len(d)
  #print listWithUnknown
  #print laplaceList

if __name__ == "__main__":
	main()