import re
from collections import Counter
import math

with open("info_matched.txt","r") as fp:
    email_rep = eval(fp.readline())

flattern = list(map(lambda x:[j for i in x for j in i],email_rep))
flattern_withoutcap = eval(re.sub("[A-Z]",lambda x:chr(ord(x.group(0))^32),str(flattern)))
base_set = [set(i) for i in flattern_withoutcap]
stop = set.intersection(*base_set)

def counter(sentence):
    return Counter(sentence).most_common(math.ceil(len(sentence)*0.9)) 

def tf(sen):
    top25 = counter(sen)
    tf = [[j[0],j[1]/len(sen)] for j in top25]
    return tf

possibletf = list(map(tf,flattern_withoutcap))

allword = [j for i in base_set for j in i]
allwordcount = Counter(allword).most_common(len(allword))
transpose = [[row[i] for row in allwordcount] for i in range(2)]
IDFdict = dict(zip(*transpose))

def idffind(sen):
    return([[i,IDFdict[i]] for i in sen])
possibleIDF = list(map(idffind,base_set))

possibleTFtran = [[row[i] for row in possibletf[2]] for i in range(2)]
TFdict = dict(zip(*possibleTFtran))

def takefirst(elem):
    return elem[0]
def sortfirst(sen):
    sen.sort(key=takefirst)
    return sen
IDFsorted = list(map(sortfirst,possibleIDF))
TFsorted = list(map(sortfirst,possibletf))

def IDF(sen):
    return [[i[0],math.log(len(base_set)/(1+i[1]))] for i in sen]

TRUEIDF = list(map(IDF,possibleIDF))

def tfidf(a,b):
    res = []
    for i in range(len(a)):
        res.append([a[i][0],a[i][1]*b[i][1]])
    return res

TFIDF = list(map(tfidf,TRUEIDF,TFsorted))

def takesecond(elem):
    return elem[1]
def sortsecond(sen):
    sen.sort(key=takesecond,reverse = True)
    return sen

TFIDFsorted = list(map(sortsecond,TFIDF))

with open("TFIDF.txt","w") as fp:
    fp.write(str(TFIDFsorted))

def take5(a):
    return a[0:math.ceil(len(a)*0.05)]

top5 = list(map(take5,TFIDFsorted))
def extractword(a):
    return [i[0] for i in a]
onlyword = list(map(extractword,top5))

with open("top5.txt","w") as fp:
    fp.write(str(onlyword))
