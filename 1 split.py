import re

with open("database.txt","r") as fp:
    database = fp.readlines()


def split_sents(unsplited):
    splited = list(map(lambda x:list(filter(None,re.split("([A-Z]+[^?.!]+[.?!] )",x))),unsplited))
    return splited

with open("database splited.txt","w") as fp:
    fp.write(str(split_sents(database)))