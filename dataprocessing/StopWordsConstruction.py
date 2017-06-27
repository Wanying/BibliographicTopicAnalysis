"""
@author Wanying Ding
@email wd78@drexel.edu
@description
    This module is used to generate the stopwords for topic modeling
"""
import json
stopword_file = file("../data/stopwords.txt",'w')
document_reader = file("../data/refine_document.txt",'r')
word_dict=dict()
lines = document_reader.readlines()
total_frequency=0
for line in lines:
    doc = json.loads(line)["document"]
    words = doc.split(" ")
    doc_set=set()
    #DF
    for word in words:
        if word in doc_set:
            #each word in one document just count once
            continue
        doc_set.add(word)
        if word in word_dict:
            word_dict[word]+=1
        else:
            word_dict[word]=1

word_frequency_list = sorted(word_dict.items(),key=lambda(k,v):v,reverse=True)
threshold = int(0.1*len(lines))
for word in word_frequency_list:
    if word[1]>threshold:
        stopword_file.write(word[0]+"\n")
        stopword_file.flush()
stopword_file.flush()
stopword_file.close()
