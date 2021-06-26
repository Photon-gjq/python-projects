import re
from collections import Counter
import math

with open("info_matched.txt","r") as fp:
    email_rep = eval(fp.readline())

with open("top5.txt","r") as fp:
    onlyword = eval(fp.readline())

def makeset(x):
    return [set(i) for i in x]
sentenceset = list(map(makeset,email_rep))

def ct(wordset,sentence): #这个函数吃一个词语集和一个句子，吐出这个句子中出现这些词语的次数。
    t = 0
    for i in wordset:
        if i in sentence:
            t = t+1
    return t

def senct(wordset,sentence): #这个函数统计文中的每一个句子的关键词数
    return [[i,ct(wordset,sentence[i])] for i in range(len(sentence))]

def takesecond(elem): #这俩函数用来排序
    return elem[1]

def sortsecond(sen):
    sen.sort(key=takesecond,reverse = True)
    return sen

wordappearance = list(map(senct,onlyword,sentenceset)) #这玩意就是所有文章的所有句子中关键词出现的次数啦

wasorted = list(map(sortsecond,wordappearance)) #对次数排序，从而得到关键句

def take25(a):
    return a[0:math.ceil(len(a)*0.25)]
topsen = list(map(take25,wasorted))

def takef(a):
    return [i[0] for i in a]
topsennum = list(map(takef,topsen))

def wordjoin(a): #先要把替换了电话和邮件的词语集合变成句子再说
    return [" ".join(a[i]) for i in range(len(a))]
sentense_rep = list(map(wordjoin,email_rep))

def TOPSEN(num,sen):
    coll = []
    for i in num:
        coll.append(sen[i])
    return coll
REALTOPSEN = list(map(TOPSEN,topsennum,sentense_rep))

with open("topsentence.txt","w") as fp:
    fp.write(str(REALTOPSEN))
