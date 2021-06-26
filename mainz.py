from typing import List
import argparse
import re
import math
import operator
import copy


def read_database(database_file):
    database=''
    with open(database_file) as f:
        for line in f.readlines():
            database = database + line
        return database


# task 1 in regex
def split_sents(articles):
    pattern = re.compile(r'[.?!]\s[A-Z]')
    index = 0
    list1 = []
    while True:
        matchresult = pattern.search(articles, index)
        if not matchresult:
            break
        list1.append(articles[index:matchresult.start() + 1])
        index = matchresult.end() - 1
    list1.append(articles[index:])
    return (list1)


# task 2 in regex
def normalize_words(sentences):
    lenth = len(sentences)
    for i in range(lenth):
        content = sentences[i]
        sentences1 = ''
        pattern = re.compile(r'[.,?!](?!\w)')
        index = 0
        while True:
            matchresult = pattern.search(sentences[i], index)
            if not matchresult:
                break
            sentences1 = sentences1 + sentences[i][index:matchresult.end() - 1] + " " + matchresult.group()
            index = matchresult.end()
        pattern1 = re.compile(r'\s')
        sentences[i] = pattern1.split(sentences1)
    return (sentences)


# task 3 in regex
def desensitization(informations):
    for i in informations:
        for j in i :
            j = re.sub(r'(\+86-(\d{9,12}))', 'phone', j)
            j = re.sub(r'(1(\d{8,11}))', 'phone', j)
            j = re.sub(r'(\w+@\w+\.\w+\.cn)', 'email', j)
            j = re.sub(r'(\w+@\w+\.com)', 'email', j)
    return (informations)


def lowercase_all_docs(alls):
    for i in range(len(alls)):
        for j in range(len(alls[i])):
            pattern = re.compile(r'(\w+)')
            alls[i][j]=pattern.sub(lambda x:x.group(0).lower(),alls[i][j])
    return(alls)


#求某词在文章中出现的频率
def freqword(wordlis):
    freword = {}
    for i in wordlis:
        if str(i) in freword:
            freword[str(i)]=freword[str(i)]+1
        else:
            freword[str(i)]=1
    return freword


#将一个文档划分为所有文章
def ful(allfile):
    return re.split('\n', allfile)


#为了计算在所有文章的出现频率
def wordinfilecount(word, corpuslist):
    count = 0
    for i in corpuslist:
        if word in i:
            count = count + 1
            continue
    return count


#把所有的标点符号都除去
def rearrange(wordlis):
    wordlis0 = []
    for i in range(len(wordlis)):
        wordlis0 = wordlis0 + wordlis[i]
    for i in wordlis0:
        if i == '?' or i == '.' or i == ',' or i == '!':
            wordlis0.remove(i)
    return wordlis0


#计算tfidf
def tfidf(wordlis1, filelis, corpuslis):
    global orderdic1
    tf = 0
    idf = 0
    tf_idf = 0
    outlis = {}
    outdic = {}
    dic = freqword(wordlis1)
    for i in wordlis1:
        if wordinfilecount(str(i), corpuslis) == filelis:
            continue
        tf = dic[str(i)] / len(wordlis1)
        idf = math.log(filelis / (wordinfilecount(str(i), corpuslis) + 1))
        tf_idf = tf * idf
        outdic[str(i)] = tf_idf
        orderdic1 = sorted(outdic.items(), key=operator.itemgetter(1), reverse=True)
    return (orderdic1,outdic)


#得到第N篇文章的wordlis, filelis, corpuslis
def get_article(mud,database):
    win = database
    corpuslis = ful(win)
    articles = corpuslis[mud]
    sentences1 = split_sents(articles)
    sentences = copy.deepcopy(sentences1)
    wordlis1 = lowercase_all_docs(normalize_words(sentences1))
    wordlis=desensitization(wordlis1)
    filelis = len(corpuslis)
    return (wordlis, filelis, corpuslis,sentences)


#得到关键词的提取
def keywords_extraction_pre(wordlis, filelis, corpuslis):
    allof,allofdic=tfidf(rearrange(wordlis),filelis,corpuslis)
    keyword = []
    for i in range(len(allof)):
        keyword.append(allof[i][0])
    if len(rearrange(wordlis))<=20:
        num=1
    else:
        num=len(rearrange(wordlis))//20
    keywordall=keyword[0:num]
    return (keywordall,keyword,allofdic)


#对所有文件的关键词都提取
def keywords_extraction (database):
    filelis = len(ful(database))
    keyword=[]
    for i in range(filelis):
        wordlis, filelis, corpuslis,sentences=get_article(i,database)
        keyword.append(keywords_extraction_pre(wordlis, filelis, corpuslis)[0])
    return(keyword)


#得到一篇文章的关键句
def key_sentences_extraction_pre(mud,database):
    wordlis, filelis, corpuslis, sentences = get_article(mud,database)
    sentenceorder = {}
    sentenreorder = {}
    for i in range(len(wordlis)):
        numb = 0
        for j in range(len(sentences)):
            if sentences[j] in wordlis[i]:
                numb = numb + 1
        sentenceorder[i] = numb
        sentenreorder = sorted(sentenceorder.items(), key=operator.itemgetter(1), reverse=True)
    keysentences = []
    if len(sentences) <= 4:
        keysentences = sentences[int(sentenreorder[0][0])]
    else:
        numbee = len(sentences) // 4
        for i in range(numbee):
            keysentences.append(sentences[int(sentenreorder[i][0])])
    return (keysentences)


#得到所有文章的关键句
def key_sentences_extraction(database):
    filelis = len(ful(database))
    keysentence=[]
    for i in range(filelis):
        keysentence.append(key_sentences_extraction_pre(i,database))
    return(keysentence)


def key_phrase_extraction_pre(mud,database):
    wordlis, filelis, corpuslis, sentences = get_article(mud,database)
    keywordall,keyword,allofdic=keywords_extraction_pre(wordlis, filelis, corpuslis)
    keyphrase = []
    stoped=len(keywordall)
    guess=0
    while(guess!=stoped):
        dictkeyphrase = {}
        redictkeyphrase = {}
        for j in keywordall:
            for k in keywordall:
                if j==k:
                    continue
                varrr=0
                for i in wordlis:
                    if varrr==1:
                        break
                    else:
                        for h in range(len(i) - 1):
                            if j==i[h] and k==i[h+1]:
                                varrr=1
                                keyphrase_pre = str(j + ' ' + k)
                                dictkeyphrase[keyphrase_pre]=allofdic[j]+allofdic[k]
                                break
        redictkeyphrase= sorted(dictkeyphrase.items(), key=operator.itemgetter(1), reverse=True)
        redictkeyphrase_copy = copy.deepcopy(redictkeyphrase)
        word_in_phrase=[]
        for i in range(len(redictkeyphrase)):
            keyphrase_split = re.split(' ', redictkeyphrase[i][0])
            if keyphrase_split[0] in word_in_phrase or  keyphrase_split[1] in word_in_phrase:
                continue
            else:
                keyphrase.append(redictkeyphrase_copy[i][0])
                word_in_phrase.append(keyphrase_split[0])
                word_in_phrase.append(keyphrase_split[1])
                keywordall.remove(keyphrase_split[0])
                keywordall.remove(keyphrase_split[1])
                keyword.remove(keyphrase_split[0])
                keyword.remove(keyphrase_split[1])
        guess = len(keywordall)
        keywordall=keyword[0:stoped]
    return (keyphrase,keywordall)


#对所有关键短语提取
def key_phrase_extraction(database):
    filelis = len(ful(database))
    keyphrase = []
    keywordall = []
    for i in range(filelis):
        keyphrase_pre,keywordall_pre=key_phrase_extraction_pre(i,database)
        keyphrase.append(keyphrase_pre)
        keywordall.append(keywordall_pre)
    return(keyphrase,keywordall)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--database_file', type=str, default="test_database.txt")
    args = parser.parse_args()
    database_file = args.database_file
    database = read_database(database_file)

    keywords_list =keywords_extraction (database)
    key_phrases_list,new_keywords_list = key_phrase_extraction(database)
    key_sentences_list = key_sentences_extraction(database)

    with open("words.txt", "w") as f:
        for keywords in keywords_list:
            print(", ".join(keywords), file=f)
    with open("phrases.txt", "w") as f:
        for key_phrases in key_phrases_list:
            print(", ".join(key_phrases), file=f)
    with open("sents.txt", "w") as f:
        for key_sentences in key_sentences_list:
            print(", ".join(key_sentences), file=f)
    with open("new_keywords.txt", "w") as f:
        for keywords in new_keywords_list:
            print(", ".join(keywords), file=f)