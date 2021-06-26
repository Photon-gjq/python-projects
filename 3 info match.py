import re

with open("database splited2.txt","r") as fp:
    database_splited2 = eval(fp.readline())



def desensitization(unrep):
    phone_rep = list(map(lambda z: list(map(lambda y: list(map(lambda x: re.sub("\+86-\d{9,12}|1\d{9,12}","(phone)",x),y)),z)),unrep))
    email_rep = list(map(lambda z: list(map(lambda y: list(map(lambda x: re.sub("(\w+@\w+\.com)|(\w+@\w+\.+\w+\.cn)","(email)",x),y)),z)),phone_rep))
    return email_rep

with open("info_matched.txt","w") as fp:
    fp.write(str(desensitization(database_splited2)))