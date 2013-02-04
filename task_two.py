import task_one
import re,random, sys

N = 2
nGramList = []

# generates the word based on the probability
def getNextWord(wordList,prefix,N):
  candidateList = list()
  count = 0
  
  #print prefix+":"
  
  if N == 1:
    candidateList = wordList
    for wordTuple in wordList:
      count = count + wordTuple[1]
  else:
    for wordTuple in wordList:
      token = wordTuple[0]
      if(re.match(prefix,token)):
  	    candidateList.append(wordTuple)
  	    count = count + wordTuple[1]
    #print candidateList
  
  randIndex=random.randint(1,count);
  #print randIndex, count
  for candidate in candidateList:
    randIndex = randIndex - candidate[1]
    if randIndex <= 0:
     #print candidate[0]
     return candidate[0].split()


def sentenceGenerator(N):
  sentence = list()
  prefix = "<s>"
  suffix = [""]
  global nGramList
  count = 0
  if N == 0:
    wordList = sorted(nGramList[N-1].iteritems(), key=lambda (k,v):(v,k),reverse=False)
    #print wordList
  else:
    wordList = list()
    for key in nGramList[N-1]:
  	  wordList.append((key,nGramList[N-1][key]))
  
  while not re.search("<s>",suffix[-1]):
    lastSuffix = suffix
    suffix = getNextWord(wordList,prefix,N)
    temp = ""
    
    #print prefix, suffix
    
    if N > 1:
      temp = " ".join(suffix[1:])
    else:
      #print suffix[0]
      #print lastSuffix[0]
      if suffix[-1] == "<s>" and count < 5:
      	suffix[-1] = ""
      	continue
      #if suffix[0] == lastSuffix[0]:
      #	print "******* suffix matches prefix"
      #	suffix[-1] = ""
      #	continue
    
    #if N > 1:
    #  prefix = " ".join(suffix[1:])
    #else:
    #  prefix = temp
    
    prefix = temp
    
    prefix = prefix + " "
    #print "prefix",prefix+":"
    #print "suffix", suffix
    #print
    
    if N > 1:
      if (suffix[0] == suffix[1]):
    	suffix[-1] == suffix[-2]
    	continue
    	
    sentence.append(suffix[N-2])
    count = count + 1
    #print sentence
  
  return sentence;

def extendedmain():
  maxNumSentences = 10
  sentences = list()
  for n in range(1,N+1):
    w = "Sentences for N = " + str(n)
    print w
    print "No of sentences generated : "
    sentences.append(w)
    i = 0
    while i < maxNumSentences:
      sentence = sentenceGenerator(n) 
      if(len(sentence)<6): 
        continue
      text = " ".join(sentence).replace('<s> ','')
      text = text.replace(' <s>','')
      text = re.sub(' +',' ',text)
      #print text
      sentences.append(text)
      print str(i+1)+"..."
      i = i + 1
    print
      
  count = 0
  for s in sentences:
  	if count%(maxNumSentences+1) != 0:
  	  print count%(maxNumSentences+1),
  	print s
  	count = count + 1

def main():
  #print nGramList
  global N
  if len(sys.argv) > 1:
    N = int(sys.argv[1])
  else:
    N = 2
    
  #print N
  global nGramList
  nGramList = task_one.generateNgram(N,task_one.corpus3) # Generate Ngram for N=1, N=2, N=3
  print "Dataset3"
  extendedmain()
  nGramList = []
  nGramList = task_one.generateNgram(N,task_one.corpus4) # Generate Ngram for N=1, N=2, N=3
  print "Dataset4"
  extendedmain()

if __name__ == "__main__":
	main()