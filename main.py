from typing import List
import argparse
import re
import math
from collections import Counter


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--database_file', type=str, default="database.txt")
    args = parser.parse_args()

    database_file = args.database_file

    def read_database():
        with open(database_file) as f:
            return f.readlines()

    mydatabase = read_database()

    # task 1 in regex
    def split_sents(unsplited):
        splited = list(map(lambda x:list(filter(None,re.split("([A-Z]+[^?.!]+[.?!] )",x))),unsplited))
        return splited

    database_splited = split_sents(mydatabase)

    # task 2 in regex
    def normalize_words(dsp):
        splited2 = list(map(lambda y:list(map(lambda x:list(filter(None,re.split(" |([.!?,]) ",x))),y)),dsp))
        return splited2

    database_splited2 = normalize_words(database_splited)

    # task 3 in regex
    def desensitization(unrep):
        phone_rep = list(map(lambda z: list(map(lambda y: list(map(lambda x: re.sub("\+86-\d{9,12}|1\d{9,12}","(phone)",x),y)),z)),unrep))
        email_rep = list(map(lambda z: list(map(lambda y: list(map(lambda x: re.sub("(\w+@\w+\.com)|(\w+@\w+\.+\w+\.cn)","(email)",x),y)),z)),phone_rep))
        return email_rep

    processeddata = desensitization(database_splited2)

    def lowercase_all_docs(a):
        return eval(re.sub("[A-Z]",lambda x:chr(ord(x.group(0))^32),str(a)))


    flattern = list(map(lambda x:[j for i in x for j in i],processeddata))
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

    def take5(a):
        return a[0:math.ceil(len(a)*0.05)]

    top5 = list(map(take5,TFIDFsorted))
    def extractword(a):
        return [i[0] for i in a]
    onlyword = list(map(extractword,top5))

    def keywords_extraction() -> List[List]:
        return onlyword




    def makeset(x):
        return [set(i) for i in x]
    sentenceset = list(map(makeset,processeddata))

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
    sentense_rep = list(map(wordjoin,processeddata))

    def TOPSEN(num,sen):
        coll = []
        for i in num:
            coll.append(sen[i])
        return coll
    REALTOPSEN = list(map(TOPSEN,topsennum,sentense_rep))

    def key_sentences_extraction() -> List[List]:
        return REALTOPSEN


    def key_phrase_extraction() -> List[List]:
        """
        :return: example return format if the database has 3 documents give None if no key phrase
        """

        return []



    database = read_database()
    keywords_list = keywords_extraction()
    key_phrases_list = key_phrase_extraction()
    key_sentences_list = key_sentences_extraction()

    with open("words.txt", "w") as f:
        for keywords in keywords_list:
            print(", ".join(keywords), file=f)
    with open("phrases.txt", "w") as f:
        for key_phrases in key_phrases_list:
            print(", ".join(key_phrases), file=f)
    with open("sents.txt", "w") as f:
        for key_sentences in key_sentences_list:
            print(", ".join(key_sentences), file=f)
