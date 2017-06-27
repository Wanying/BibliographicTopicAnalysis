"""
@author Wanying Ding
@email wd78@drexel.edu
@description:
    This module generates documents from CSV files
"""
import csv
import json
import gensim.models.phrases as phrase
import re
import string


def loadCSVFile(inputfile,outputfile):
    firstline = True
    writer = file(outputfile,'w')
    with open(inputfile,'r') as csvfile:
        reader = csv.reader(csvfile,delimiter=',',quotechar='"')
        for row in reader:
            if firstline==True:
                firstline=False
                continue
            UI = row[48]
            TI = row[6].lower()
            DE = row[16].lower()
            ID = row[17].lower()
            AB = row[18].lower()
            PY=  int(row[36])
            info = dict()
            info["UI"] = UI#Unique Artical Identifier
            info["TI"] =TI #Document Title
            info["DE"] =DE #Author Keywords
            info["ID"] =ID #Keywords Plus
            info["AB"] =AB #Abstract
            info["PY"] = PY #Publish Year
            writer.write(json.dumps(info)+"\n")
            writer.flush()
    writer.flush()
    writer.close()


documentList = list()
jsonList = list()
exclude = set(string.punctuation)

def load_documents(file_addr):
    global documentList
    global jsonList

    with open(file_addr,'r') as jsonFile:
        jsonList = jsonFile.readlines()
        for line in jsonList:
            document = json.loads(line)
            abstract = document["AB"]
            title = document["TI"]
            text = abstract+" "+title
            refine = ''.join(ch for ch in text if ch not in exclude)
            documentList.append(refine)

def train_phrase():
    sentence_stream = list()
    for doc in documentList:
        wordlist = doc.split(" ")
        sentence_stream.append(wordlist)

    ps = phrase.Phrases(sentence_stream)
    bigram = phrase.Phraser(ps)
    return bigram

def refineText(documentFile,refinedTextFile):

    writer = file(refinedTextFile,'w')

    load_documents(documentFile)
    bigram = train_phrase()

    for i in range(len(jsonList)):
        jsonObj = json.loads(jsonList[i])
        phrases = bigram[documentList[i].split(" ")]
        id = jsonObj["UI"]
        author_keyword = jsonObj["DE"]
        keyword_plus = jsonObj["ID"]
        year = jsonObj["PY"]
        keywords = author_keyword+" "+keyword_plus
        keywords =re.sub("[;:]"," ",keywords)
        keywords = re.sub("-","_",keywords)
        keys =keywords.split(" ")
        n_keys=list()
        for key in keys:
            if key.strip()=="":
                continue
            n_keys.append(key.strip())
        phrases.extend(n_keys)
        doc = ""
        for word in phrases:
            word = word.strip()
            if word=="" or word==None:
                continue
            doc+=word+" "
        doc = doc.strip()
        if doc=="" or doc==None:
            continue
        document = dict()
        document["id"]=id
        document["time"]=year
        document["document"] = doc
        writer.write(json.dumps(document)+"\n")
        writer.flush()
    writer.flush()
    writer.close()

input = "../data/astro-ALP-2003-2010.csv"
output ="../data/data.txt"
loadCSVFile(inputfile=input,outputfile=output)

documentFile="../data/data.txt"
phrase_document = "../data/refine_document.txt"
refineText(documentFile=documentFile,refinedTextFile=phrase_document)

