import wikipedia
from bs4 import BeautifulSoup

def get_intro(n):
    # return a list of strings, each string is a paragraph
    para = wikipedia.summary(n)
    para = para.split('\n')
    return para


def wash(sec,topic):
    for line in sec[:]:
        if line==" "*len(line):
            sec.remove(line)
        elif line[:-1]==" "*(len(line)-1):
            sec.remove(line)
        else:
            continue
    sec = [line.strip() for line in sec]
    equations = BeautifulSoup(topic.html()).find_all('annotation')
    limit = len(equations)
    i=1
    for index, line in enumerate(sec):
        if i>=limit:
                break
        if line==equations[i-1].text:
            sec[index]="formula "+str(i)
            i+=1
    return sec


def dictcreator(sec,stage=1):
    # store each section in a dictionary
    part_list=[]
    if stage==1:
        for i, part in enumerate(sec):
            try:
                if part[:3]=="== ":
                    part_list.append(i)
            except:
                continue
    if stage==2:
        for i, part in enumerate(sec):
            try:
                if part[:4]=="=== ":
                    part_list.append(i)
            except:
                continue
        if len(part_list)==0:
            return sec
    text={}
    if len(part_list)==1:
        text[sec[0]]=sec[1:]
    else:
        for i, index in enumerate(part_list):
            if i==0:
                text[sec[index]]=sec[1:part_list[i+1]]
                continue
            if i==len(part_list)-1:
                text[sec[index]]=sec[index+1:]
                continue
            else:
                text[sec[index]]=sec[index+1:part_list[i+1]]
    return text


def get_full(n):
    topic = wikipedia.page(n)
    sec = topic.content.split('\n')
    sec = wash(sec,topic)
    print("Text washed")
    # remove introduction and endings
    for i, part in enumerate(sec):
        if part[:2]=="==":
            sec = sec[i:]
            break
    for i, part in enumerate(sec):
        if part=="== See also ==":
            sec = sec[:i]
            break
    text = dictcreator(sec)
    for key in text:
        text[key] = dictcreator(text[key],stage=2)
    return text