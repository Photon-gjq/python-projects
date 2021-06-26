import re

with open("database splited.txt","r") as fp:
    database_splited = eval(fp.readline())



def normalize_words(dsp):
    splited2 = list(map(lambda y:list(map(lambda x:list(filter(None,re.split(" |([.!?,]) ",x))),y)),dsp))
    return splited2

with open("database splited2.txt","w") as fp:
    fp.write(str(normalize_words(database_splited)))