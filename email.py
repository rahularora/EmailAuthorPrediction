# Task 5 : Email-Authorship Prediction

import re
import pdb
import math
import nltk

trainingFile = "EnronDataset/train.txt"
testFile = "EnronDataset/validation.txt"
testFile2 = "EnronDataset/test.txt"

nGramList = []
#dict for storing ngrams and other info for different authors
AuthorDict = {}
# dictionary for storing vocab words
Vocab = {}
# the distinct words in all emails
global VocabSize
global TotalEmails

class Bunch:
    def __init__(self, **kwds):
        self.__dict__.update(kwds)


def addTokenToDict(aDict,token):
  if token in aDict:
    aDict[token] = aDict[token] + 1
  else:
    aDict[token] = 1
    
  return aDict

def buildNGram(n, gList, tList):
  for token in tList:
    tempDict = gList[n-1]
    tempDict = addTokenToDict(tempDict,token)
  gList[n-1] = tempDict

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
  
def generateNgram(N, gList, tokenList):
  
  for n in range(1,N+1):
    gList.append({})
  
  for n in range(1,N+1):
    tList = genNgramTokens(n, tokenList)
    buildNGram(n, gList, tList)
    
def printNgramList(gList):
  #print len(nGramList)
  count = 1
  for ngram in gList:
    print "*******"
    print "For N =", count
##    for key in ngram:
##      print key, ngram[key]
    
    count = count + 1
#    print

def calculateNumTokens(N, gList):
    if not gList:
        return 0;
    if not gList[N - 1]:
        return 0;
    return len(gList[N - 1]);
    
def naiveBayes(wordList):
    N = 1;
    maxPr = -10000000;
    maxAuthor = '';
    
    for author in AuthorDict:
        logPriorC = 0;
        logPr = 0;
        logPriorC = (math.log(AuthorDict[author].numDocs) - math.log(TotalEmails));
        numWords = AuthorDict[author].numWords; #calculateNumTokens(N, AuthorDict[author].ngramList);
        if numWords <= 0:
            print 'something wrong'
        logPr = 1;#logPriorC;
        for word in wordList:
          # calc freq of word in author wordlist
          wfreq = 0;
          word = word.strip(" ");
          if word in AuthorDict[author].ngramList[N - 1]:
            wfreq = AuthorDict[author].ngramList[N - 1][word];
          logPr = logPr + (math.log((wfreq + 1)) - math.log(VocabSize + numWords));
        print author, logPr
        if logPr > maxPr:
          maxPr = logPr;
          maxAuthor = author;
          
    print maxAuthor, maxPr;
    return maxAuthor

# func to run test
def readTestData():
  numCorrect = 0;
  TotalSample = 0;

  files = [testFile];

  of = open('out.txt', 'w')

  for file in files:
      f = open(file, 'r')
      
      for line in f:
        line = line.lower();
        line = re.sub(' +',' ',line)      
        author, mline = line.split(" ", 1);
        mline = re.sub('[^A-Za-z0-9.?!\']+', ' ', mline)
        mline.strip(' ');
        
        tokenList = mline.split(" ");
        tokenList = [w for w in tokenList if not w in nltk.corpus.stopwords.words('english')]

##        for i in range(0, len(tokenList)):
##            tokenList[i].strip(' ');
##            if tokenList[i].isdigit() == True:
##                tokenList[i] = tokenList[i].replace(tokenList[i], '<NUM>')        
        
        TotalSample = TotalSample + 1;

        predictedAuth = naiveBayes(tokenList);
        print 'Predicted Author:', predictedAuth, ' Actual Author: ', author

        of.write('{0}\n'.format(predictedAuth));

        if predictedAuth == author:
          numCorrect = numCorrect + 1;
      print 'Correct#:', numCorrect, ", Total#: ", TotalSample;
  

def readTrainingData():
  global TotalEmails;
  global VocabSize;

  TotalEmails = 0;
  VocabSize = 0;
  
  f = open(trainingFile, 'r')
  
  for line in f:
    line = line.lower();
    line = re.sub(' +',' ',line)
    author, mline = line.split(" ", 1);
    mline = re.sub('[^A-Za-z0-9.?!\']+', ' ', mline)
    mline.strip(' ');

    tokenList = mline.split(" ");
    tokenList = [w for w in tokenList if not w in nltk.corpus.stopwords.words('english')]
    
##    for i in range(0, len(tokenList)):
##        tokenList[i].strip(' ');
##        if tokenList[i].isdigit() == True:
##            tokenList[i] = tokenList[i].replace(tokenList[i], '<NUM>')        

##    pdb.set_trace();    

    TotalEmails = TotalEmails + 1;

    #save information
    if author in AuthorDict:
      AuthorDict[author].numDocs = AuthorDict[author].numDocs + 1;      # num of docs of author
      AuthorDict[author].numWords = AuthorDict[author].numWords + len(tokenList);
      AuthorDict[author].text.extend(tokenList);                        # combined text of all emails of author
    else:
      AuthorDict[author] = Bunch(numDocs=0,numWords=0,text=[],ngramList=[]);       
      AuthorDict[author].numDocs = 1;#AuthorDict[author].numDocs + 1;
      AuthorDict[author].numWords = len(tokenList);
      AuthorDict[author].text.extend(tokenList);

  for author in AuthorDict:
    generateNgram(1, AuthorDict[author].ngramList, AuthorDict[author].text);
    for word in AuthorDict[author].text:
      if word in Vocab:
        continue;
      Vocab[word] = 1;
      VocabSize = VocabSize + 1;
  
def main():
  readTrainingData();
  readTestData();

if __name__ == "__main__":
  main()
