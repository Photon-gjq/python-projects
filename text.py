from typing import List
import argparse
import re


def read_database():
    with open('database.txt') as f:
        return f.readlines()
datas=read_database()



def split_cents(j):  # j表示文章编号
    sentences = re.split(r"([.?!\s+] [A-Z])", read_database()[j])
    sentences.append("")
    sentences = ["".join(i) for i in zip(sentences[0::2], sentences[1::2])]  # 以？！。 A-Z的组合为模式分割，并保留分割符
    a = []
    for i in range(0, len(sentences) - 2):
        a.append(''.join([(sentences[i])[-1:], sentences[i + 1]]))#现在得到的后面一个句子没有第一个字母，把前一个句子的最后一个大写字母移给后一个句子
    a = [a[i].rstrip('QWERTYUIOPASDFGHJKLZXCVBNM') for i in range(0, len(a))]#把两端的大写字母删除
    return a
    pass


def normalize_words(j):
    b = [split_cents(j)[i].rstrip('.?! ') for i in range(0, len(split_cents(j)))]
    for k in range(0, len(b)):
        b[k] = re.sub(',', '', b[k])
        b[k] = b[k].split(' ')
    return b
    pass


def desensitization(j):
    phonepattern = re.compile(r'(\\+86|1)\d{8,10}')#符合电话号码格式的句子
    emailpattern = re.compile(r'\w+?@\w+(.cn|.com)')#符合邮箱格式
    datas[j] = phonepattern.sub('Phone', read_database()[j])#替换
    datas[j] = emailpattern.sub('Email', read_database()[j])
    return datas[j]
    pass


def lowercase_all_docs(j):
    c = []
    for s in normalize_words(j):
        temp = []
        for i in range(0, len(s)):
            temp.append(s[i].lower())
        c.append(temp)
    return c


allwordlist = []#为方便制造所有单词的词表
stopwordlist = []
for j in range(0, len(read_database())):
    desensitization(j)
    b = lowercase_all_docs(j)
    d = []
    for i in range(0, len(b)):
        for k in range(0, len(b[i])):
            d.append((b[i])[k])
    allwordlist.append(d)
for word in allwordlist[0]:
    for i in range(1, len(allwordlist)):
        if word not in allwordlist[i]:
            break
        stopwordlist.append(word)

#思路是先提取每一篇的关键词，再append成所有关键词的列表
def tf_calculator(word, j):
    tf = (allwordlist[j].count(word) / len(allwordlist[j]))
    return tf


def idf_calculator(word):
    docscontaintheword = 0
    for i in range(0, len(allwordlist)):
        if word in allwordlist[i]:
            docscontaintheword += 1
    from math import log
    idf = log(len(allwordlist) / (docscontaintheword + 1))
    return idf


def tfidf_calculator(word, j):
    return tf_calculator(word, j) * idf_calculator(word)


def dictcreator(j):
    keys = allwordlist[j]
    values = [tfidf_calculator(word, j) for word in allwordlist[j]]
    d = dict(zip(keys, values))
    return sorted(d.items(), key=lambda x: x[1], reverse=True)


def keywordsselector(j):#提取某篇关键词的函数
    keywordsset = []
    for tuples in (dictcreator(j)[0:len(dictcreator(j)) // 20 + 1]):
        keywordsset.append(tuples[0])
    return keywordsset
def keywords_extraction():#上述函数的值append就可以得到所有关键词的列表
    allkeywords=[]
    for i in range(0,len(read_database())):
        allkeywords.append(keywordsselector(i))
    return allkeywords


def keyphraseselector(j):#思路同上，也是先试着提取一篇的关键词
    keyphrase=[]
    c=0
    a=keywordsselector(j)
    wordss=[tuples[0]for tuples in dictcreator(j)]#为方便把刚刚字典中的所有词提取出来，这是降序排列后的词表
    while True:
        d='noexist'#d是作为判断循环是否可以结束的变量
        for keyword in a:#此层循环寻找每句中关键词的下标
            for i in range(0, len(lowercase_all_docs(j))):#对每一句循环
                numbers = [n for n, x in enumerate(lowercase_all_docs(j)[i]) if x == keyword]#输出每句中关键词的所有下标
                for other in a:
                    if other==keyword:
                        continue
                    else:
                        numberz = [n for n, x in enumerate(lowercase_all_docs(j)[i]) if x == other]
                        for m in numbers:
                            if m-1 in numberz:#说明两个关键词再某句中是相连的
                                d = 'exist'#如果找到了关键词
                                try:
                                    a.remove(other)
                                    a.remove(keyword)#将关键词组中的两个单词删除
                                    a.append(wordss[len(wordss)//20+1+2*c])
                                    a.append(wordss[len(wordss)//20+2+2*c])#递补两个关键词
                                    keyphrase.append(' '.join([other,keyword]))
                                    c+=1

                                except:
                                    continue
                            elif m+1 in numberz:#同上
                                d='exist'
                                try:#发现有可能出现keyword不在a里的情况，但是这种情况下得不到关键短语，因此用一个try结构
                                    a.remove(other)
                                    a.remove(keyword)
                                    a.append(wordss[len(wordss)//20+1+2*c])
                                    a.append(wordss[len(wordss)//20+2+2*c])
                                    keyphrase.append(' '.join([keyword,other]))
                                    c+=1
                                except:
                                   continue
                            else:
                                continue
        if d=='noexist':#经过循环后如果d的值没有改变就说明循环中已经不能再产生新的关键短语了
            break
        return keyphrase
def key_phrase_extraction():
    allkeyphrase=[]#思路同提取关键词
    for i in range(0,len(read_database())):
        allkeyphrase.append(keyphraseselector(i))
    return allkeyphrase

def keysentselector(j):
    scores = []#这里对每个句子记分
    for i in range(0, len(lowercase_all_docs(j))):
        score = 0
        for words in keywordsselector(j):
            score += lowercase_all_docs(j)[i].count(words)
        scores.append(score)#句子中出现一个关键词，句子得分+1，这里得到一个和句子相对应的分数表
    order = [i for i in range(0, len(lowercase_all_docs(j)))]#把句子序号和得分合成一个字典，降序排列，取top25%
    sdict = dict(zip(order, scores))
    sdict = sorted(sdict.items(), key=lambda x: x[1], reverse=True)
    keynumbers = [tuples[0] for tuples in sdict[0:len(sdict) // 4]]
    keysents = [split_cents(j)[i] for i in keynumbers]#刚刚得到的是句子序号，这里读取序号对应的句子
    return keysents
def key_sentences_extraction():
    allkeysents=[]
    for i in range(0,len(read_database())):
        allkeysents.append(keysentselector(i))
    return allkeysents




if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--database_file', type=str, default="database.txt")
    args = parser.parse_args()

    database_file = args.database_file
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